import cloudscraper
import time
import random
import logging
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
from datetime import datetime
import json
from pathlib import Path
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
)

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
]

# Thread-safe queue for results
results_queue = Queue()

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def load_cleaned_urls():
    """Load URLs from cleaned JSON files"""
    urls_by_state = {}
    clean_urls_dir = Path(r'C:\Users\berna\etl_project\realstate\clean_urls')  # Fixed absolute path
    
    if not clean_urls_dir.exists():
        logging.error(f"Directory not found: {clean_urls_dir}")
        return {}
    
    for json_file in clean_urls_dir.glob('*_clean.json'):
        try:
            state = json_file.stem.split('_')[0]
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                urls_by_state[state] = data.get('urls', [])
                logging.info(f"Loaded {len(urls_by_state[state])} URLs for state {state}")
        except Exception as e:
            logging.error(f"Error loading {json_file}: {str(e)}")
    
    return urls_by_state

def scrape_olx_property_listing(url, state, max_retries=3):
    for attempt in range(max_retries):
        try:
            time.sleep(random.uniform(1, 2))
            
            scraper = cloudscraper.create_scraper(
                browser={
                    'browser': 'chrome',
                    'platform': 'windows',
                    'mobile': False,
                    'custom': get_random_user_agent(),
                }
            )
            
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0',
                'Referer': 'https://www.google.com/',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'cross-site',
                'Sec-Fetch-User': '?1'
            }
            
            scraper.headers.update(headers)
            response = scraper.get(url)
            response.raise_for_status()
            
            logging.info(f"Response status code: {response.status_code}")
            
            soup = BeautifulSoup(response.text, 'lxml')
            tree = html.fromstring(response.content)
            
            # Extract all details
            details = {'state': state}
            
            # Location
            try:
                location_details = tree.xpath("//div[@class='olx-d-flex olx-fd-column']/span[2]/text()")
                if location_details:
                    details['location'] = location_details[0].strip()
            except Exception as e:
                details['location'] = 'N/A'
                
            try:
                # Check for área útil
                area_text = soup.find('span', string='Área útil')
                if area_text:
                    area_value = area_text.find_next('span', {'class': 'ad__sc-hj0yqs-0 ekhFnR'})
                    if area_value:
                        details['area_util'] = area_value.text.strip()
                else:
                    # Check for área construída if área útil is not found
                    area_text = soup.find('span', string='Área construída')
                    if area_text:
                        area_value = area_text.find_next('span', {'class': 'ad__sc-hj0yqs-0 ekhFnR'})
                        if area_value:
                            details['area_util'] = area_value.text.strip()  # Still using area_util as column name for consistency
                    else:
                        details['area_util'] = 'N/A'
            except Exception as e:
                logging.warning(f"Error extracting area: {str(e)}")
                details['area_util'] = 'N/A'
            
            # Quartos
            quartos_link = soup.find('a', {'href': lambda x: x and 'quartos' in x})
            if quartos_link:
                details['quartos'] = quartos_link.text.strip()
            else:
                details['quartos'] = 'N/A'
            
            # Banheiros
            banheiros_span = soup.find('span', string='Banheiros')
            if banheiros_span:
                banheiros_value = banheiros_span.find_next('span', {'class': 'ad__sc-hj0yqs-0 ekhFnR'})
                if banheiros_value:
                    details['banheiros'] = banheiros_value.text.strip()
            else:
                details['banheiros'] = 'N/A'
            
            # Vagas na garagem
            vagas_container = soup.find('span', text='Vagas na garagem')
            if vagas_container:
                vagas_span = vagas_container.find_next('span', {'class': 'ad__sc-hj0yqs-0 ekhFnR'})
                if vagas_span:
                    details['vagas'] = vagas_span.text.strip()
            else:
                details['vagas'] = 'N/A'
            
            # Get price
            price_span = soup.find('span', {
                'data-ds-component': 'DS-Text',
                'class': 'olx-text olx-text--title-large olx-text--block'
            })
            
            details['price'] = price_span.text.strip() if price_span else 'N/A'
            details['url'] = url
            details['scraped_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return details
            
        except Exception as e:
            logging.warning(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
            if attempt == max_retries - 1:
                logging.error(f"Failed to parse {url} after {max_retries} attempts")
                return None
            time.sleep(random.uniform(0.1, 0.2))

def save_state_results(results, state):
    """Save all results for a state to a single CSV"""
    filename = f'olx_properties_{state}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    df = pd.DataFrame(results)
    
    # Reorder columns
    columns_order = [
        'price',
        'location',
        'area_util',
        'quartos',
        'banheiros',
        'vagas',
        'url',
        'scraped_date',
        'state'
    ]
    
    # Only include columns that exist in the DataFrame
    existing_columns = [col for col in columns_order if col in df.columns]
    df = df[existing_columns]
    
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    logging.info(f"State {state} saved to {filename} with {len(results)} properties")

def process_state_urls(state, urls, max_workers=17):
    """Process URLs for a single state using threading"""
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(scrape_olx_property_listing, url, state): url 
            for url in urls
        }
        
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                if result:
                    results.append(result)
                    logging.info(f"Processed {len(results)}/{len(urls)} URLs for state {state}")
                    
            except Exception as e:
                logging.error(f"Error processing {url}: {str(e)}")
    
    # Save all results for the state in a single file
    if results:
        save_state_results(results, state)
    
    return len(results)

def main():
    # Create output directory
    output_dir = Path('scraped_properties')
    output_dir.mkdir(exist_ok=True)
    os.chdir(output_dir)
    
    # Load cleaned URLs
    urls_by_state = load_cleaned_urls()
    
    if not urls_by_state:
        logging.error("No URLs loaded!")
        return
    
    # Process each state with cooldown period
    total_states = len(urls_by_state)
    for idx, (state, urls) in enumerate(urls_by_state.items(), 1):
        logging.info(f"Processing state {state} ({idx}/{total_states})")
        logging.info(f"Found {len(urls)} URLs for state {state}")
        
        properties_scraped = process_state_urls(state, urls)
        logging.info(f"Completed state {state}. Scraped {properties_scraped} properties")
        
        # Add cooldown period between states
        if idx < total_states:  # Don't wait after the last state
            cooldown = random.uniform(30, 50)
            logging.info(f"Cooling down for {cooldown:.2f} seconds before next state...")
            time.sleep(cooldown)
    
    logging.info("Scraping completed!")

if __name__ == "__main__":
    main()
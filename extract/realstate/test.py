import cloudscraper
import time
import random
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import json
import requests


def get_random_proxy():
    # You can add more proxies to this list
    proxies = [
        None,  # No proxy option
        # Add your proxies here if you have them
    ]
    return random.choice(proxies)


def scrape_property_details(url):
    # Initialize UserAgent
    ua = UserAgent()

    # Enhanced headers
    headers = {
        'authority': 'rs.olx.com.br',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Opera GX";v="113", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': ua.random,
        'referer': 'https://www.google.com/',
        'accept-encoding': 'gzip, deflate, br',
        'connection': 'keep-alive',
        'dnt': '1'
    }

    # Cookie dict to store cookies
    cookies = {}

    print(f"Starting property scraping for URL: {url}")
    print(f"Using User-Agent: {headers['user-agent']}")

    # Max retries
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            # Create new scraper instance each time
            scraper = cloudscraper.create_scraper(
                browser={
                    'browser': 'chrome',
                    'platform': 'windows',
                    'mobile': False
                },
                delay=10
            )

            # First, try to get the home page to get cookies
            print("Getting initial cookies from home page...")
            init_response = scraper.get(
                'https://rs.olx.com.br',
                headers=headers,
                timeout=30
            )

            # Update cookies
            cookies.update(init_response.cookies)

            # Add delay
            delay = random.uniform(3, 7)
            print(f"Waiting {delay:.2f} seconds...")
            time.sleep(delay)

            # Now try to get the actual property page
            print("Making request to property page...")
            response = scraper.get(
                url,
                headers=headers,
                cookies=cookies,
                timeout=30,
                allow_redirects=True
            )

            print(f"Response Status: {response.status_code}")

            # Check if we got a successful response
            if response.status_code == 200:
                print("Successfully got the page! Parsing details...")
                soup = BeautifulSoup(response.text, 'html.parser')

                # Save the HTML for debugging
                with open('last_response.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)

                # Initialize property details
                property_details = {
                    'url': url,
                    'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }

                # Extract price (adjusting selectors based on saved HTML)
                price = soup.find('span', class_='ad__sc-1wimjbb-1')
                if price:
                    property_details['price'] = price.text.strip()

                # Extract specifications
                specs = soup.find_all('div', class_='ad__sc-1f2ug0x-1')
                for spec in specs:
                    label_elem = spec.find('span', class_='ad__sc-1f2ug0x-2')
                    value_elem = spec.find('span', class_='ad__sc-1f2ug0x-3')
                    if label_elem and value_elem:
                        label = label_elem.text.strip().lower()
                        value = value_elem.text.strip()
                        property_details[label] = value

                # Save results
                filename = f'property_details_{int(time.time())}.json'
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(property_details, f, ensure_ascii=False, indent=2)

                print("\nExtracted details saved to:", filename)
                return property_details

            elif response.status_code == 403:
                print(f"Attempt {retry_count + 1} failed with 403 error")
                retry_count += 1

                # Longer delay between retries
                delay = random.uniform(10, 15)
                print(f"Waiting {delay:.2f} seconds before retry...")
                time.sleep(delay)

            else:
                print(f"Failed with status code: {response.status_code}")
                break

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            retry_count += 1
            time.sleep(random.uniform(5, 10))

    print("All attempts failed")
    return None


if __name__ == "__main__":
    test_url = "https://rs.olx.com.br/regioes-de-porto-alegre-torres-e-santa-cruz-do-sul/imoveis/maravilhosa-cobertura-duplex-com-156-m-de-area-privativa-no-bairro-bela-vista-2-dormitor-1350852449"
    result = scrape_property_details(test_url)

    if result:
        print("\nExtracted Property Details:")
        print("-" * 50)
        for key, value in result.items():
            print(f"{key}: {value}")
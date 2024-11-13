import scrapy
import json
from pathlib import Path
from datetime import datetime
import random
from time import sleep


class RealstatespiderSpider(scrapy.Spider):
    name = "realstatespider"
    allowed_domains = ["www.olx.com.br"]

    # Complete list of Brazilian states
    states = [
        'ac', 'al', 'ap', 'am', 'ba', 'ce', 'df', 'es', 'go',
        'ma', 'mt', 'ms', 'mg', 'pa', 'pb', 'pr', 'pe', 'pi',
        'rj', 'rn', 'rs', 'ro', 'rr', 'sc', 'sp', 'se', 'to'
    ]

    def __init__(self, max_pages=50, *args, **kwargs):
        super(RealstatespiderSpider, self).__init__(*args, **kwargs)
        self.max_pages = int(max_pages)

        # Setup output directory
        self.output_dir = Path('property_urls')
        self.output_dir.mkdir(exist_ok=True)

        # Initialize URL storage
        self.urls_by_state = {}

        # Custom settings for better performance
        self.custom_settings = {
            'CONCURRENT_REQUESTS': 1,
            'DOWNLOAD_DELAY': 1.5,
            'COOKIES_ENABLED': False,
        }

    def start_requests(self):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Opera GX";v="113", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0 (Edition std-1)',
        }

        for state in self.states:
            url = f'https://www.olx.com.br/imoveis/venda/estado-{state}?o=1'
            yield scrapy.Request(
                url=url,
                headers=headers,
                callback=self.parse,
                meta={
                    'state': state,
                    'page': 1
                }
            )

    def parse(self, response):
        state = response.meta['state']
        current_page = response.meta['page']

        # Extract property URLs
        property_urls = response.xpath(
            "//section[contains(@class, 'olx-ad-card olx-ad-card--horizontal')]//a[contains(@data-ds-component, 'DS-NewAdCard-Link')]/@href").getall()

        # Initialize state storage if needed
        if state not in self.urls_by_state:
            self.urls_by_state[state] = []

        # Store URLs
        self.urls_by_state[state].extend(property_urls)

        self.logger.info(f"Collected {len(property_urls)} URLs from {state} page {current_page}")

        # Check for next page
        if current_page < self.max_pages:
            next_page = current_page + 1
            next_url = f'https://www.olx.com.br/imoveis/venda/estado-{state}?o={next_page}'

            # Add random delay
            sleep(random.uniform(0.2, 0.7))

            yield scrapy.Request(
                url=next_url,
                headers=response.request.headers,  # Reuse the same headers
                callback=self.parse,
                meta={
                    'state': state,
                    'page': next_page
                }
            )
        else:
            self.save_urls(state)
    def save_urls(self, state):
        """Save URLs to JSON file"""
        if state in self.urls_by_state:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_path = self.output_dir / f'{state}_property_urls_{timestamp}.json'

            data = {
                'state': state,
                'timestamp': timestamp,
                'total_urls': len(self.urls_by_state[state]),
                'urls': self.urls_by_state[state]
            }

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            self.logger.info(f"Saved {len(self.urls_by_state[state])} URLs for {state}")
            del self.urls_by_state[state]

    def closed(self, reason):
        """Save any remaining URLs when spider closes"""
        for state in list(self.urls_by_state.keys()):
            self.save_urls(state)
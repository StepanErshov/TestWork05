import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def scrape_quotes() -> List[Dict]:
    base_url = "https://quotes.toscrape.com"
    quotes = []
    page = 1
    
    while True:
        url = f"{base_url}/page/{page}/"
        logger.info(f"Scraping page {page}: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            quote_elements = soup.find_all('div', class_='quote')
            
            if not quote_elements:
                logger.info(f"No more quotes found on page {page}. Stopping.")
                break
                
            for quote_element in quote_elements:
                try:
                    text = quote_element.find('span', class_='text').get_text(strip=True)
                    author = quote_element.find('small', class_='author').get_text(strip=True)
                    tags = [tag.get_text(strip=True) for tag in quote_element.find_all('a', class_='tag')]
                    
                    quotes.append({
                        'author': author,
                        'quote': text,
                        'tags': tags
                    })
                    
                except Exception as e:
                    logger.error(f"Error parsing quote element: {e}")
                    continue
            
            next_button = soup.find('li', class_='next')
            if not next_button:
                logger.info("No next page found. Stopping.")
                break
                
            page += 1
            
        except requests.RequestException as e:
            logger.error(f"Error scraping page {page}: {e}")
            break
        except Exception as e:
            logger.error(f"Unexpected error on page {page}: {e}")
            break
    
    logger.info(f"Scraped {len(quotes)} quotes total")
    return quotes
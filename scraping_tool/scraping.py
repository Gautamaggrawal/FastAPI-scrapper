import aiohttp
import asyncio
from bs4 import BeautifulSoup
from .models import ScrapingSettings, Product
from .constants import BASE_URL, HEADERS, cache
from .utils import ensure_directory_exists
import json

class ScrapingTool:
    def __init__(self, settings: ScrapingSettings):
        self.settings = settings
        self.scraped_products = []

    async def scrape_page(self, page_number: int):
        if page_number == 1:
            url = f"{BASE_URL}?page={page_number}"
        else:
            url = f"{BASE_URL}page/{page_number}"
        retries = 3

        async with aiohttp.ClientSession() as session:
            for attempt in range(retries):
                try:
                    async with session.get(url, headers=HEADERS) as response:
                        response.raise_for_status()
                        text = await response.text()
                        return BeautifulSoup(text, 'html.parser')
                except aiohttp.ClientError:
                    if attempt < retries - 1:
                        await asyncio.sleep(2)
                    else:
                        raise HTTPException(status_code=500, detail=f"Failed to scrape page {page_number}")

    async def parse_products(self, soup, page_num):
        try:
            product_cards = soup.find('div', id='mf-shop-content').find('ul').find_all('li')
            if not product_cards:
                return  # If no products are found, exit the function

            for card in product_cards:
                try:
                    title_tag = card.select_one(".woo-loop-product__title")
                    if not title_tag:
                        continue
                    
                    title = title_tag.text.strip()
                    price_tag = card.find('span', class_='woocommerce-Price-amount')
                    if not price_tag:
                        continue
                    
                    price = float(price_tag.select_one('bdi').text.strip().replace('₹', ''))

                    thumbnail = card.select_one('.mf-product-thumbnail')
                    img_path = None
                    if thumbnail:
                        img_tag = thumbnail.find('img')
                        if img_tag:
                            if page_num >= 2:
                                img_url = img_tag.get('data-lazy-src', '')
                            else:
                                img_url = img_tag.get('src', '')
                            if img_url:
                                img_path = await self.download_image(img_url, title)

                    if cache.get(title) == price:
                        continue

                    cache[title] = price
                    self.scraped_products.append(Product(product_title=title, product_price=price, path_to_image=img_path))

                except Exception as e:
                    continue

        except Exception as e:
            pass

    async def download_image(self, img_url, title):
        if img_url.startswith("data:image/"):
            return None

        async with aiohttp.ClientSession() as session:
            async with session.get(img_url) as img_response:
                img_response.raise_for_status()
                img_path = f"images/{title.replace(' ', '_')}.jpg"
                ensure_directory_exists("images")
                with open(img_path, "wb") as img_file:
                    while True:
                        chunk = await img_response.content.read(1024)
                        if not chunk:
                            break
                        img_file.write(chunk)
                return img_path

    async def scrape(self):
        page = 1
        tasks = []
        while not self.settings.max_pages or page <= self.settings.max_pages:
            tasks.append(self.scrape_page(page)) 
            page += 1

        pages = await asyncio.gather(*tasks)

        parse_tasks = []
        for i, soup in enumerate(pages, start=1):
            parse_tasks.append(self.parse_products(soup, i))

        await asyncio.gather(*parse_tasks)

    def save_to_db(self):
        with open("product.json", "w") as db_file:
            json.dump([product.dict() for product in self.scraped_products], db_file, indent=4)

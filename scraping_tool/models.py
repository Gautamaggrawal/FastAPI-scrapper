from pydantic import BaseModel, Field
from typing import Optional

class ScrapingSettings(BaseModel):
    max_pages: Optional[int] = Field(None, description="Maximum pages to scrape")
    proxy: Optional[str] = Field(None, description="Proxy string for scraping")

class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str
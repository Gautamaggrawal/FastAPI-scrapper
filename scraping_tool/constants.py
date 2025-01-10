import os

# Constants
BASE_URL = os.getenv("BASE_URL", "https://dentalstall.com/shop/")
STATIC_TOKEN = os.getenv("STATIC_TOKEN", "default-token")
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; scraping-tool/1.0)"}
# In-memory cache to store scraped results
cache = {}
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .models import ScrapingSettings, Product
from .scraping import ScrapingTool
from .constants import STATIC_TOKEN
import os
import json

# FastAPI app
app = FastAPI()
security = HTTPBearer()

# Authentication dependency
def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != STATIC_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized")

# API endpoints
@app.post("/scrape", dependencies=[Depends(authenticate)])
async def scrape(settings: ScrapingSettings):
    scraper = ScrapingTool(settings)
    await scraper.scrape()  # Use await for async scraping
    scraper.save_to_db()
    total_products = len(scraper.scraped_products)
    print(f"Scraped {total_products} products.")
    return {"message": f"Scraped {total_products} products."}

@app.get("/products", dependencies=[Depends(authenticate)], response_model=list[Product])
async def get_products():
    if not os.path.exists("products.json"):
        raise HTTPException(status_code=404, detail="No products found.")

    with open("products.json", "r") as db_file:
        products = json.load(db_file)
    return products

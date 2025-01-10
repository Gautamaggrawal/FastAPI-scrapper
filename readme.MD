# Scraping Tool using FastAPI

## Overview

This project implements a web scraping tool using the FastAPI framework to automate information scraping from websites. The tool is designed to scrape product details like name, price, and images and store them locally. It supports additional features like pagination, caching, retry mechanisms, and optional proxy usage.

## Features

### Scraping Capabilities

- Scrapes product details including name, price, and images from the target website.
- Handles pagination effectively using `<nav class="woocommerce-pagination">` structure.

### Settings

- Limit the number of pages to scrape.
- Provide a proxy string for scraping.

### Data Storage

- Stores scraped data in a `products.json` file in the following format:

```json
[
    {
        "product_title": "",
        "product_price": 0,
        "path_to_image": ""
    }
]
```

- Images are saved locally in the `images/` directory.

### Notification

- Prints the number of products scraped at the end of the session.

### Caching

- Utilizes in-memory caching to avoid redundant database updates for unchanged product prices.

### Authentication

- Requires a static token for accessing API endpoints.

### Retry Mechanism

- Retries failed requests up to 3 times before raising an exception.

## Directory Structure

```
.
├── scraping_tool/
│   ├── __init__.py
│   ├── app.py          # FastAPI application entry point
│   ├── models.py       # Pydantic models for data validation
│   ├── scraping.py     # Scraping logic
│   ├── utils.py        # Constants and utility functions
├── images/             # Directory for storing downloaded images
├── products.json       # JSON file storing scraped product data
```

## Requirements

- Python 3.9+
- FastAPI
- Requests
- BeautifulSoup4
- Uvicorn (for running the server)
- python-dotenv (optional for managing environment variables)

## Setup

### Clone the Repository

```bash
git clone https://github.com/Gautamaggrawal/FastAPI-scrapper
cd FastAPI-scrapper
```

### Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Up Environment Variables (Optional)

Create a `.env` file (optional) and add the following:

```
STATIC_TOKEN=your-static-token
```

## Usage

### 1. Start the FastAPI Server

```bash
uvicorn scraping_tool.app:app --reload
```

### 2. API Endpoints

#### **POST /scrape**

- **Description**: Initiates the scraping process.
- **Authentication**: Requires the `Authorization` header with the static token.
- **Sample Curl**:

```bash
curl --location 'http://127.0.0.1:8000/scrape' \
--header 'Authorization: Bearer your-static-token' \
--header 'Content-Type: application/json' \
--data '{"max_pages": 2, "proxy": null}'
```

- **Body**:

```json
{
    "max_pages": 5,
    "proxy": "http://proxy-url"
}
```

- **Response**:

```json
{
    "message": "Scraped 100 products."
}
```

#### **GET /products**

- **Description**: Fetches the list of scraped products.
- **Authentication**: Requires the `Authorization` header with the static token.
- **Sample Curl**:

```bash
curl --location 'http://127.0.0.1:8000/products' \
--header 'Authorization: Bearer your-static-token'
```
- **Response**:

```json
[
    {
        "product_title": "Product 1",
        "product_price": 20.99,
        "path_to_image": "images/Product_1.jpg"
    }
]
```

## How It Works

- **Pagination Handling**: Extracts the next page URL from the pagination structure on the website.
- **Retry Mechanism**: Retries requests for pages up to 3 times in case of failure.
- **Image Download**: Downloads product images and saves them in the `images/` directory.
- **Caching**: Avoids redundant updates for products whose prices haven't changed.

## Future Enhancements

- Add support for database storage (e.g., SQLite, PostgreSQL).
- Implement advanced notification mechanisms (e.g., email, Slack).
- Introduce dynamic scraping rules for flexibility across multiple websites.
- Include advanced authentication strategies (e.g., JWT, OAuth).
- Add Docker support for containerization.

## Contributing

Feel free to fork this repository and submit pull requests. For significant changes, please open an issue first to discuss your ideas.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

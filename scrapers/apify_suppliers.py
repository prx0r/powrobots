"""Apify-based supplier scrapers for AliExpress, Alibaba, Amazon.

Requires: pip install apify-client
Set env var: APIFY_TOKEN=<your-token>

Usage:
    from scrapers.apify_suppliers import scrape_aliexpress
    results = scrape_aliexpress("STS3215 servo motor", max_results=50)
"""

import os
import json
from datetime import datetime, timezone
from typing import Optional

try:
    from apify_client import ApifyClient
    HAS_APIFY = True
except ImportError:
    HAS_APIFY = False


def _get_client():
    """Get Apify client from environment."""
    token = os.environ.get("APIFY_TOKEN", "")
    if not token:
        raise ValueError("APIFY_TOKEN not set")
    return ApifyClient(token)


def scrape_aliexpress(keyword: str, max_results: int = 50, country: str = "United Kingdom") -> list:
    """Scrape AliExpress product listings via Apify actor.

    Returns list of dicts with: title, price, currency, rating, orders, url, store
    """
    if not HAS_APIFY:
        raise ImportError("apify-client not installed: pip install apify-client")

    client = _get_client()
    run = client.actor("agentx/aliexpress-product-scraper").call(input={
        "keyword": keyword,
        "country": country,
        "max_results": max_results,
    })

    results = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        results.append({
            "source": "aliexpress",
            "title": item.get("title", ""),
            "price": item.get("currentPrice"),
            "original_price": item.get("originalPrice"),
            "currency": item.get("currency", "USD"),
            "rating": item.get("rating"),
            "orders": item.get("ordersCount"),
            "url": item.get("url", ""),
            "store": item.get("storeName", ""),
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        })

    return results


def scrape_amazon(keyword: str, max_results: int = 20, domain: str = "co.uk") -> list:
    """Scrape Amazon product listings via Apify actor.

    Returns list of dicts with: title, price, currency, rating, asin, url
    """
    if not HAS_APIFY:
        raise ImportError("apify-client not installed: pip install apify-client")

    client = _get_client()
    run = client.actor("apify/e-commerce-scraping-tool").call(input={
        "startUrls": [f"https://www.{domain}/s?k={keyword.replace(' ', '+')}"],
        "maxItems": max_results,
    })

    results = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        results.append({
            "source": "amazon",
            "domain": domain,
            "title": item.get("name", ""),
            "price": item.get("price"),
            "currency": item.get("currency", "GBP"),
            "rating": item.get("rating"),
            "reviews": item.get("reviewsCount"),
            "asin": item.get("asin", ""),
            "url": item.get("url", ""),
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        })

    return results


def scrape_ebay(keyword: str, max_results: int = 20) -> list:
    """Scrape eBay UK listings via Apify actor.

    Returns list of dicts with: title, price, currency, condition, seller, url
    """
    if not HAS_APIFY:
        raise ImportError("apify-client not installed: pip install apify-client")

    client = _get_client()
    run = client.actor("apify/e-commerce-scraping-tool").call(input={
        "startUrls": [f"https://www.ebay.co.uk/sch/i.html?_nkw={keyword.replace(' ', '+')}"],
        "maxItems": max_results,
    })

    results = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        results.append({
            "source": "ebay",
            "title": item.get("name", ""),
            "price": item.get("price"),
            "currency": item.get("currency", "GBP"),
            "condition": item.get("condition", ""),
            "seller": item.get("seller", ""),
            "url": item.get("url", ""),
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        })

    return results


def search_component(component_name: str, mpn: str = "") -> dict:
    """Search multiple suppliers for a component.

    Returns aggregated results from AliExpress, Amazon UK, eBay UK.
    """
    query = f"{mpn} {component_name}".strip() if mpn else component_name

    results = {"aliexpress": [], "amazon": [], "ebay": []}

    try:
        results["aliexpress"] = scrape_aliexpress(query, max_results=10)
    except Exception as e:
        results["aliexpress_error"] = str(e)

    try:
        results["amazon"] = scrape_amazon(query, max_results=10)
    except Exception as e:
        results["amazon_error"] = str(e)

    try:
        results["ebay"] = scrape_ebay(query, max_results=10)
    except Exception as e:
        results["ebay_error"] = str(e)

    return results

"""Scrape all configured suppliers and store results.

Usage:
    python scrapers/run_all.py
    python scrapers/run_all.py --component sts3215-c001
    python scrapers/run_all.py --supplier aliexpress
"""

import argparse
import json
import sys
import os
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.apify_suppliers import (
    scrape_aliexpress, scrape_amazon, scrape_ebay, search_component, HAS_APIFY
)
from powrobots.shared.persist import get_db


# Components to search (from component basket)
SEARCH_QUERIES = [
    ("sts3215-c001", "STS3215 servo motor C001"),
    ("sts3215-c044", "STS3215 servo motor C044"),
    ("sts3215-c046", "STS3215 servo motor C046"),
    ("roborock-lds01rr", "Roborock LDS01RR LiDAR"),
    ("esp32-s3", "ESP32-S3 devkit"),
    ("soil-moisture-sensor", "capacitive soil moisture sensor"),
    ("dht22", "DHT22 temperature humidity sensor"),
    ("ws2812b", "WS2812B RGB LED"),
    ("sg90-servo", "SG90 micro servo"),
    ("ssd1306", "SSD1306 OLED display 0.96"),
]


def store_scraped_results(component_id: str, results: list, supplier: str):
    """Store scraped results as component_market_observation."""
    conn = get_db()
    now = datetime.now(timezone.utc).isoformat()
    stored = 0

    for item in results:
        price = item.get("price")
        if price is None:
            continue

        try:
            conn.execute(
                """INSERT INTO component_market_observation
                (component_id, distributor_id, currency, unit_price_1,
                 observed_at, stock_qty, lead_time_days)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (component_id, supplier, item.get("currency", "USD"),
                 float(price), now, item.get("orders"), None)
            )
            stored += 1
        except Exception:
            pass

    conn.commit()
    conn.close()
    return stored


def run_supplier(supplier: str, queries: list = None):
    """Run scraping for a specific supplier."""
    if queries is None:
        queries = SEARCH_QUERIES

    print(f"=== Scraping {supplier} ===")
    total_stored = 0

    for component_id, query in queries:
        try:
            if supplier == "aliexpress":
                results = scrape_aliexpress(query, max_results=5)
            elif supplier == "amazon":
                results = scrape_amazon(query, max_results=5)
            elif supplier == "ebay":
                results = scrape_ebay(query, max_results=5)
            else:
                print(f"  Unknown supplier: {supplier}")
                continue

            stored = store_scraped_results(component_id, results, supplier)
            total_stored += stored
            print(f"  {component_id:30s} {len(results):>3} found  {stored:>3} stored")

        except Exception as e:
            print(f"  {component_id:30s} ERROR: {e}")

    print(f"\nTotal: {total_stored} observations stored")
    return total_stored


def run_all():
    """Run scraping for all configured suppliers."""
    if not HAS_APIFY:
        print("ERROR: apify-client not installed")
        print("Run: pip install apify-client")
        print("Set: APIFY_TOKEN=<your-token>")
        return

    total = 0
    for supplier in ["aliexpress", "amazon", "ebay"]:
        try:
            total += run_supplier(supplier)
        except Exception as e:
            print(f"ERROR scraping {supplier}: {e}")

    print(f"\n=== Complete: {total} total observations ===")


def main():
    parser = argparse.ArgumentParser(description="Scrape supplier data")
    parser.add_argument("--supplier", help="Specific supplier to scrape")
    parser.add_argument("--component", help="Specific component to search")
    parser.add_argument("--query", help="Custom search query")
    args = parser.parse_args()

    if args.component:
        query = args.query or args.component
        results = search_component(query)
        for supplier, items in results.items():
            if isinstance(items, list) and items:
                stored = store_scraped_results(args.component, items, supplier)
                print(f"{supplier}: {len(items)} found, {stored} stored")
    elif args.supplier:
        run_supplier(args.supplier)
    else:
        run_all()


if __name__ == "__main__":
    main()

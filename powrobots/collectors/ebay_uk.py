"""eBay UK Browse Collector — used robot market data.

Uses the official eBay Browse API.
Requires OAuth application token.
"""

import json
import os
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record


class EbayUkCollector(BaseCollector):
    SOURCE_ID = 'ebay_uk'
    DATASET = 'robot_listings'
    PARSER_ID = 'ebay_browse_v1'

    SEARCH_QUERIES = [
        'ABB robot', 'FANUC robot', 'KUKA robot', 'Yaskawa robot',
        'Universal Robots', 'teach pendant', 'servo amplifier',
        'servo motor', 'robot controller', 'PLC',
    ]

    def __init__(self, app_id: str = None):
        self.app_id = app_id or os.environ.get('EBAY_APP_ID', '')

    def fetch(self):
        if not self.app_id:
            return None
        return None  # Would search each query

    def parse(self, raw_content, raw_hash, result):
        if not raw_content:
            return
        data = json.loads(raw_content)
        for item in data.get('itemSummaries', []):
            item_id = item.get('itemId', '')
            title = item.get('title', '')
            if not item_id:
                result.records_invalid += 1
                continue
            price_data = item.get('price', {})
            normalized = {
                'source_native_id': item_id,
                'title': title,
                'price': price_data.get('value'),
                'currency': price_data.get('currency'),
                'condition': item.get('condition', ''),
                'seller': item.get('seller', {}).get('username', ''),
                'location': item.get('itemEndDate', ''),
                'listing_url': item.get('itemWebUrl', ''),
            }
            ir = insert_source_record(
                self.SOURCE_ID, self.DATASET, item_id,
                normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
            )
            if ir['inserted']:
                result.records_new += 1
            else:
                result.records_unchanged += 1


if __name__ == '__main__':
    EbayUkCollector().run()

"""Mouser Component Collector — electronics distributor data.

Uses the official Mouser Search API.
Requires API key (free, register at mouser.com/api).
"""

import json
import os
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record, upsert_component


class MouserCollector(BaseCollector):
    SOURCE_ID = 'mouser'
    DATASET = 'components'
    PARSER_ID = 'mouser_api_v1'

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get('MOUSER_API_KEY', '')

    def fetch(self):
        if not self.api_key:
            return None
        # Would search for tracked component MPNs
        return None

    def parse(self, raw_content, raw_hash, result):
        if not raw_content:
            return
        data = json.loads(raw_content)
        parts = data.get('SearchResults', {}).get('Parts', [])
        for part in parts:
            mpn = part.get('ManufacturerPartNumber', '')
            if not mpn:
                result.records_invalid += 1
                continue
            normalized = {
                'source_native_id': mpn,
                'mpn': mpn,
                'manufacturer': part.get('Manufacturer', ''),
                'description': part.get('Description', ''),
                'category': part.get('Category', ''),
                'stock': part.get('AvailabilityInStock', ''),
                'price': part.get('PriceBreaks', [{}])[0].get('Price', '') if part.get('PriceBreaks') else '',
                'lifecycle': part.get('ProductStatus', ''),
            }
            ir = insert_source_record(
                self.SOURCE_ID, self.DATASET, mpn,
                normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
            )
            if ir['inserted']:
                result.records_new += 1
            else:
                result.records_unchanged += 1

            upsert_component(mpn, part.get('Description', ''),
                              mpn=mpn, category=part.get('Category', ''))


if __name__ == '__main__':
    MouserCollector().run()

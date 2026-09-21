"""Farnell/element14 Collector — UK component pricing in GBP.

Uses the element14 Product Search API.
Source: https://uk.farnell.com/
API: https://partner.element14.com/
"""

import json
import os
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record, upsert_component, get_db


class FarnellCollector(BaseCollector):
    SOURCE_ID = 'farnell'
    DATASET = 'components'
    PARSER_ID = 'element14_api_v1'

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get('FARNELL_API_KEY', '')

    def fetch(self):
        if not self.api_key:
            return None
        return None  # Would search tracked MPNs

    def parse(self, raw_content, raw_hash, result):
        if not raw_content:
            return
        data = json.loads(raw_content)
        products = data.get('manufacturerPartNumberSearchResults', {}).get('manufacturerPartNumberSearchReturn', [])
        if not products:
            products = data.get('keywordSearchResults', {}).get('keywordSearchReturn', [])
        for part in products:
            mpn = part.get('manufacturerPartNumber', '')
            if not mpn:
                result.records_invalid += 1
                continue
            normalized = {
                'source_native_id': mpn,
                'mpn': mpn,
                'manufacturer': part.get('brandName', ''),
                'description': part.get('displayName', ''),
                'price_gbp': part.get('prices', [{}])[0].get('cost', '') if part.get('prices') else '',
                'stock': part.get('stockLevel', ''),
                'lead_time': part.get('minLeadTime', ''),
                'lifecycle': part.get('productStatus', ''),
            }
            ir = insert_source_record(
                self.SOURCE_ID, self.DATASET, mpn,
                normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
            )
            if ir['inserted']:
                result.records_new += 1
            else:
                result.records_unchanged += 1

            upsert_component(mpn, part.get('displayName', ''),
                              mpn=mpn, category=part.get('category', ''))


if __name__ == '__main__':
    FarnellCollector().run()

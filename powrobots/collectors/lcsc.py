"""LCSC Electronics Collector — China component pricing in CNY.

Uses the LCSC Open API.
Source: https://www.lcsc.com/
API: https://www.lcsc.com/docs/openapi/index.html
"""

import json
import os
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record, upsert_component, get_db


class LcscCollector(BaseCollector):
    SOURCE_ID = 'lcsc'
    DATASET = 'components'
    PARSER_ID = 'lcsc_api_v1'

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get('LCSC_API_KEY', '')

    def fetch(self):
        if not self.api_key:
            return None
        return None  # Would search tracked MPNs

    def parse(self, raw_content, raw_hash, result):
        if not raw_content:
            return
        data = json.loads(raw_content)
        for part in data.get('result', {}).get('detail', []):
            mpn = part.get('productModel', '')
            if not mpn:
                result.records_invalid += 1
                continue
            normalized = {
                'source_native_id': mpn,
                'mpn': mpn,
                'manufacturer': part.get('brandNameEn', ''),
                'description': part.get('productDescEn', ''),
                'price_cny': part.get('productPriceList', [{}])[0].get('productPrice', '') if part.get('productPriceList') else '',
                'stock': part.get('stockNumber', ''),
                'moq': part.get('minPacketNumber', ''),
                'lifecycle': part.get('productGrade', ''),
            }
            ir = insert_source_record(
                self.SOURCE_ID, self.DATASET, mpn,
                normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
            )
            if ir['inserted']:
                result.records_new += 1
            else:
                result.records_unchanged += 1

            upsert_component(mpn, part.get('productDescEn', ''),
                              mpn=mpn, category=part.get('productCategory', ''))


if __name__ == '__main__':
    LcscCollector().run()

"""HMRC UK Trade Info Trader Collector — open, no auth.

Searches for specific traders by commodity code.
Source: https://www.uktradeinfo.com/
API: completely open, no authentication required.
"""

import json
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record, upsert_organisation, get_db

# HS codes for robotics components
ROBOTICS_HS_CODES = [
    '847950',  # Industrial robots
    '847910',  # Plants for assembling
    '8501',    # Electric motors
    '8503',    # Parts for motors
    '8483',    # Transmission shafts, gearboxes
    '8482',    # Bearings
    '8542',    # Electronic ICs
    '9031',    # Measuring instruments (encoders)
    '8536',    # Switching apparatus
    '8504',    # Power supplies
]


class HmrcTraderCollector(BaseCollector):
    SOURCE_ID = 'hmrc_traders'
    DATASET = 'trader_data'
    PARSER_ID = 'hmrc_tradeinfo_v1'

    def fetch(self):
        """Fetch HMRC trader data for robotics commodity codes."""
        all_traders = []
        for code in ROBOTICS_HS_CODES[:3]:  # Start with top 3
            url = f'https://www.uktradeinfo.com/odata/Traders?$filter=CommodityCode eq \'{code}\'&$top=100'
            acq = self._fetch_url(url, timeout=15)
            if acq and acq.get('status') == 200:
                try:
                    data = json.loads(acq['content'])
                    traders = data.get('value', [])
                    for t in traders:
                        t['_commodity_code'] = code
                    all_traders.extend(traders)
                except (json.JSONDecodeError, KeyError):
                    pass
        if not all_traders:
            return None
        return json.dumps(all_traders).encode()

    def parse(self, raw_content, raw_hash, result):
        """Parse HMRC trader records."""
        if not raw_content:
            return
        traders = json.loads(raw_content)
        for trader in traders:
            trader_id = str(trader.get('TraderId', trader.get('Id', '')))
            name = trader.get('TraderName', '')
            if not trader_id:
                result.records_invalid += 1
                continue
            normalized = {
                'source_native_id': trader_id,
                'trader_name': name,
                'commodity_code': trader.get('_commodity_code', ''),
                'postcode': trader.get('Postcode', ''),
                'import_export': trader.get('ImportExport', ''),
                'country': trader.get('Country', ''),
            }
            ir = insert_source_record(
                self.SOURCE_ID, self.DATASET, trader_id,
                normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
            )
            if ir['inserted']:
                result.records_new += 1
            else:
                result.records_unchanged += 1

            if name:
                upsert_organisation(trader_id, name, org_type='hmrc_trader')


if __name__ == '__main__':
    HmrcTraderCollector().run()

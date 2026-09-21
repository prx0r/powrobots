"""HMRC UK Trade Statistics Collector — robotics trade flows.

Downloads monthly UK Overseas Trade Statistics bulk data.
Source: https://www.gov.uk/government/statistics/uk-overseas-trade-in-goods-statistics
"""

import csv
import io
import json
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record, get_db

# Robotics-relevant HS codes
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


class HmrcTradeCollector(BaseCollector):
    SOURCE_ID = 'hmrc_trade'
    DATASET = 'uk_overseas_trade'
    PARSER_ID = 'hmrc_otsg_v1'

    def fetch(self):
        """Fetch HMRC OTS bulk data."""
        # HMRC publishes monthly ZIP files
        # For checkpoint 1, fetch the latest monthly summary
        url = 'https://www.gov.uk/government/statistical-data-sets/uk-overseas-trade-in-goods-statistics-monthly'
        acq = self._fetch_url(url, timeout=30)
        if acq and acq.get('status') == 200:
            return acq['content']
        return None

    def parse(self, raw_content, raw_hash, result):
        """Parse HMRC trade data. Store raw for later extraction."""
        if not raw_content:
            return
        text = raw_content.decode('utf-8', errors='replace')
        # The page is HTML - store as evidence, actual CSV extraction
        # happens from linked download files
        normalized = {
            'source_native_id': 'hmrc_monthly_index',
            'content_type': 'html_index',
            'content_length': len(raw_content),
            'note': 'HMRC trade statistics index. CSV download links embedded.',
            'hs_codes_tracked': ROBOTICS_HS_CODES,
        }
        ir = insert_source_record(
            self.SOURCE_ID, self.DATASET, 'monthly_index',
            normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
        )
        if ir['inserted']:
            result.records_new += 1
        else:
            result.records_unchanged += 1

    def store_trade_record(self, month: str, flow: str, commodity_code: str,
                            partner_country: str, value_gbp: float,
                            net_mass_kg: float = None, supplementary_qty: float = None):
        """Store a single trade record."""
        conn = get_db()
        conn.execute(
            "INSERT INTO uk_trade_record "
            "(month, flow, commodity_code, partner_country, value_gbp, net_mass_kg, "
            "supplementary_qty, source_id, observed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (month, flow, commodity_code, partner_country, value_gbp,
             net_mass_kg, supplementary_qty, self.SOURCE_ID,
             datetime.now(timezone.utc).isoformat())
        )
        conn.commit()
        conn.close()


if __name__ == '__main__':
    HmrcTradeCollector().run()

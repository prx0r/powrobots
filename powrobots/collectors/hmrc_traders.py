"""HMRC UK Trade Info Trader Collector — open, no auth.

Fetches CSV of traders by commodity code 847950 (industrial robots).
Source: https://www.uktradeinfo.com/search/traders/
CSV endpoint: /umbraco/api/searchdownload/traders
"""

import csv
import io
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record, upsert_organisation


class HmrcTraderCollector(BaseCollector):
    SOURCE_ID = 'hmrc_traders'
    DATASET = 'trader_data'
    PARSER_ID = 'hmrc_tradeinfo_csv_v1'

    def fetch(self):
        """Fetch HMRC trader search results as CSV for commodity 847950."""
        acq = self._fetch_url(
            'https://www.uktradeinfo.com/umbraco/api/searchdownload/traders'
            '?commodities=847950&filename=Trader%20search%20results.csv',
            timeout=30,
            headers={'Accept': 'text/csv, application/csv, */*'},
        )
        if acq and acq.get('status') == 200:
            return acq['content']
        return None

    def parse(self, raw_content, raw_hash, result):
        if not raw_content:
            return

        text = raw_content.decode('utf-8', errors='replace')
        reader = csv.DictReader(io.StringIO(text))

        seen_companies = set()
        traders_found = 0

        for row in reader:
            name = (row.get('CompanyName') or row.get('Company name') or
                    row.get('Trader name') or '').strip()
            if not name:
                continue

            address_parts = []
            for i in range(1, 6):
                addr = row.get(f'Address{i}', '').strip()
                if addr:
                    address_parts.append(addr)
            address = ', '.join(address_parts)

            postcode = (row.get('PostCode') or row.get('Postcode') or '').strip()
            commodity = (row.get('CommodityCode') or
                        row.get('Commodity code') or '').strip()
            description = (row.get('CN8Description') or
                          row.get('Commodity description') or
                          row.get('HS2Description') or '').strip()
            trade_type = (row.get('TradeTypeDescription') or
                         row.get('Trader type') or '').strip()
            month = (row.get('Month') or '').strip()
            year = (row.get('Year') or '').strip()

            # Create one record per company (not per month)
            company_key = name.upper()
            if company_key in seen_companies:
                continue
            seen_companies.add(company_key)

            native_id = f"trader:{company_key}"

            normalized = {
                'company_name': name,
                'address': address,
                'postcode': postcode,
                'commodity_code': commodity or '847950',
                'commodity_description': description,
                'trade_type': trade_type,
                'country_code': 'GB',
            }

            ir = insert_source_record(
                self.SOURCE_ID, self.DATASET, native_id,
                normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
            )
            if ir['inserted']:
                result.records_new += 1
            else:
                result.records_unchanged += 1

            # Upsert as organisation
            org_id = f"uk_trader:{company_key}"
            upsert_organisation(
                org_id=org_id,
                canonical_name=name,
                country_code='GB',
                org_type='trader',
                aliases=[name],
            )

            traders_found += 1

        print(f'  Parsed {traders_found} unique traders from CSV')


if __name__ == '__main__':
    HmrcTraderCollector().run()

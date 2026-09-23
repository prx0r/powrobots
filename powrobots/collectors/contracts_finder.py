"""Contracts Finder Collector — UK government procurement.

Parses HTML search results from Contracts Finder for robotics-related notices.
Source: https://www.contractsfinder.service.gov.uk/
"""

from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record, upsert_organisation

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

SEARCH_TERMS = [
    'robot', 'robotics', 'automation', 'automated', 'autonomous',
    'AMR', 'AGV', 'cobot', 'manipulator', 'machine vision',
    'industrial automation', 'warehouse automation',
]


class ContractsFinderCollector(BaseCollector):
    SOURCE_ID = 'contracts_finder'
    DATASET = 'procurement_notices'
    PARSER_ID = 'cf_html_v1'

    def _write_procurement_notice(self, normalized, source_record_id=''):
        """Write to procurement_notice table."""
        from powrobots.shared.db import get_db
        conn = get_db()
        try:
            conn.execute(
                'INSERT OR IGNORE INTO procurement_notice '
                '(notice_id, source_id, stage, published_at, buyer_name, title, '
                'value_min, currency, region, raw_observation_id) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (normalized.get('notice_id', ''), 'contracts_finder',
                 normalized.get('procurement_stage', ''),
                 normalized.get('publication_date', ''),
                 normalized.get('buyer', ''),
                 normalized.get('title', ''),
                 None, 'GBP',
                 normalized.get('contract_location', ''),
                 source_record_id)
            )
            conn.commit()
        except Exception:
            pass
        finally:
            conn.close()

    def fetch(self):
        """Search Contracts Finder for robotics-related notices."""
        term = 'robot'
        url = (f'https://www.contractsfinder.service.gov.uk/Search/Results'
               f'?searchTerm={term}&isMainSearch=true')
        acq = self._fetch_url(url, timeout=15)
        if acq and acq.get('status') == 200:
            return acq['content']
        return None

    def parse(self, raw_content, raw_hash, result):
        """Parse Contracts Finder HTML search results."""
        if not raw_content:
            return
        if BeautifulSoup is None:
            print('  WARNING: beautifulsoup4 not installed, skipping parse')
            return

        html = raw_content.decode('utf-8', errors='replace')
        soup = BeautifulSoup(html, 'html.parser')

        results_div = soup.find('div', class_='notice-search-results')
        if not results_div:
            print('  No results container found')
            return

        items = results_div.find_all('div', class_='search-result')
        notices_found = 0

        for item in items:
            # Title and URL
            header = item.find('div', class_='search-result-header')
            if not header:
                continue
            link = header.find('a')
            if not link:
                continue
            title = link.get_text(strip=True)
            href = link.get('href', '')
            notice_id = href.split('/')[-1].split('?')[0] if href else ''

            # Buyer
            sub = item.find('div', class_='search-result-sub-header')
            buyer = sub.get_text(strip=True) if sub else ''

            # Fields
            fields = {}
            for entry in item.find_all('div', class_='search-result-entry'):
                strong = entry.find('strong')
                if strong:
                    label = strong.get_text(strip=True)
                    value = entry.get_text(strip=True).replace(label, '', 1).strip()
                    fields[label] = value

            normalized = {
                'notice_id': notice_id,
                'title': title,
                'buyer': buyer,
                'url': f'https://www.contractsfinder.service.gov.uk{href}' if href else '',
                'procurement_stage': fields.get('Procurement stage', ''),
                'notice_status': fields.get('Notice status', ''),
                'closing_date': fields.get('Closing', ''),
                'contract_location': fields.get('Contract location', ''),
                'contract_value': fields.get('Contract value', ''),
                'publication_date': fields.get('Publication date', ''),
            }

            ir = insert_source_record(
                self.SOURCE_ID, self.DATASET, notice_id or title,
                normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
            )
            if ir['inserted']:
                result.records_new += 1
            else:
                result.records_unchanged += 1

            # Upsert buyer as organisation
            if buyer:
                org_id = f"uk_buyer:{buyer.upper()}"
                upsert_organisation(
                    org_id=org_id,
                    canonical_name=buyer,
                    country_code='GB',
                    org_type='buyer',
                )

            # Write to procurement_notice table
            self._write_procurement_notice(normalized, notice_id or title)

            notices_found += 1

        print(f'  Parsed {notices_found} contract notices from HTML')


if __name__ == '__main__':
    ContractsFinderCollector().run()

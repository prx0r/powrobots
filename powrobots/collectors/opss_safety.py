"""OPSS Product Safety Collector — UK safety alerts/recalls.

Parses individual safety alerts from GOV.UK product safety pages.
Source: https://www.gov.uk/product-safety-alerts-reports-recalls
"""

from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


class OpsSafetyCollector(BaseCollector):
    SOURCE_ID = 'opss_safety'
    DATASET = 'safety_alerts'
    PARSER_ID = 'opss_html_v1'

    def _write_safety_notice(self, normalized):
        """Write to safety_notice table."""
        from powrobots.shared.db import get_db
        conn = get_db()
        try:
            conn.execute(
                'INSERT OR IGNORE INTO safety_notice '
                '(notice_id, source_id, product, category, risk_level, '
                'failure_description, recall_date, observed_at) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, datetime(\'now\'))',
                (normalized.get('alert_id', ''), 'opss_safety',
                 normalized.get('title', ''),
                 normalized.get('product_category', ''),
                 normalized.get('risk_level', ''),
                 normalized.get('alert_type', ''),
                 normalized.get('date_published', ''))
            )
            conn.commit()
        except Exception:
            pass
        finally:
            conn.close()

    def fetch(self):
        """Fetch OPSS product safety alerts (machinery category)."""
        url = 'https://www.gov.uk/product-safety-alerts-reports-recalls?categories%5B0%5D=machinery'
        acq = self._fetch_url(url, timeout=15)
        if acq and acq.get('status') == 200:
            return acq['content']
        return None

    def parse(self, raw_content, raw_hash, result):
        """Parse OPSS alerts HTML into individual alert records."""
        if not raw_content:
            return
        if BeautifulSoup is None:
            print('  WARNING: beautifulsoup4 not installed, skipping parse')
            return

        html = raw_content.decode('utf-8', errors='replace')
        soup = BeautifulSoup(html, 'html.parser')

        items = soup.find_all('li', class_='gem-c-document-list__item')
        alerts_found = 0

        for item in items:
            # Title and URL
            title_div = item.find('div', class_='gem-c-document-list__item-title')
            if not title_div:
                continue
            link = title_div.find('a')
            if not link:
                continue
            title = link.get_text(strip=True)
            href = link.get('href', '')
            alert_id = href.rstrip('/').split('/')[-1] if href else ''

            # Metadata
            metadata = {}
            for li in item.find_all('li', class_='gem-c-document-list__attribute'):
                text = li.get_text(strip=True)
                if ':' in text:
                    label, value = text.split(':', 1)
                    metadata[label.strip()] = value.strip()

            normalized = {
                'alert_id': alert_id,
                'title': title,
                'alert_type': metadata.get('Alert type', ''),
                'risk_level': metadata.get('Risk level', ''),
                'product_category': metadata.get('Product category', ''),
                'date_published': metadata.get('Date published', ''),
                'url': f'https://www.gov.uk{href}' if href and not href.startswith('http') else href,
            }

            ir = insert_source_record(
                self.SOURCE_ID, self.DATASET, alert_id or title,
                normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
            )
            if ir['inserted']:
                result.records_new += 1
            else:
                result.records_unchanged += 1

            # Write to safety_notice table
            self._write_safety_notice(normalized)

            alerts_found += 1

        print(f'  Parsed {alerts_found} safety alerts from HTML')


if __name__ == '__main__':
    OpsSafetyCollector().run()

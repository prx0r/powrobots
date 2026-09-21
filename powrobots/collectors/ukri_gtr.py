"""UKRI Gateway to Research Collector — grants and research projects.

Uses the GtR REST API (no auth required for basic access).
Returns XML, not JSON.
"""

import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record, upsert_organisation


class UkriGtrCollector(BaseCollector):
    SOURCE_ID = 'ukri_gtr'
    DATASET = 'research_projects'
    PARSER_ID = 'gtr_xml_v1'

    def fetch(self):
        """Fetch UKRI Gateway to Research projects related to robotics."""
        acq = self._fetch_url(
            'https://gtr.ukri.org/gtr/api/projects?q=robot&s=10&p=1',
            timeout=15
        )
        if acq and acq.get('status') == 200:
            return acq['content']
        return None

    def parse(self, raw_content, raw_hash, result):
        if not raw_content:
            return
        # GtR returns XML
        try:
            text = raw_content.decode('utf-8', errors='replace')
            # Strip namespace for easier parsing
            text = re.sub(r'ns\d+:', '', text)
            root = ET.fromstring(text)
            projects = root.findall('.//project')
            for proj in projects:
                project_id = proj.get('{http://gtr.ukri.org/gtr/api}id', '')
                if not project_id:
                    # Try href
                    href = proj.get('{http://gtr.ukri.org/gtr/api}href', '')
                    if '/projects/' in href:
                        project_id = href.split('/projects/')[-1]
                title_el = proj.find('title')
                title = title_el.text if title_el is not None else ''
                status_el = proj.find('status')
                status = status_el.text if status_el is not None else ''
                funder_el = proj.find('leadFunder')
                funder = funder_el.text if funder_el is not None else ''

                if not project_id:
                    result.records_invalid += 1
                    continue

                normalized = {
                    'source_native_id': project_id,
                    'title': title,
                    'status': status,
                    'lead_funder': funder,
                }

                ir = insert_source_record(
                    self.SOURCE_ID, self.DATASET, project_id,
                    normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
                )
                if ir['inserted']:
                    if ir.get('duplicate_of'):
                        result.records_changed += 1
                    else:
                        result.records_new += 1
                else:
                    result.records_unchanged += 1

                # Extract organisations from links
                for link in proj.findall('.//link'):
                    rel = link.get('rel', '')
                    href = link.get('href', '')
                    if 'organisations/' in href and rel == 'LEAD_ORG':
                        org_id = href.split('/organisations/')[-1]
                        upsert_organisation(org_id, f'UKRI Org {org_id[:8]}')

        except ET.ParseError:
            result.records_invalid += 1


if __name__ == '__main__':
    UkriGtrCollector().run()

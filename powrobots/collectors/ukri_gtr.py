"""UKRI Gateway to Research Collector — grants and research projects.

Uses the GtR REST API (no auth required for basic access).
"""

import json
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record, upsert_organisation


class UkriGtrCollector(BaseCollector):
    SOURCE_ID = 'ukri_gtr'
    DATASET = 'research_projects'
    PARSER_ID = 'gtr_api_v1'

    def fetch(self):
        """Fetch UKRI Gateway to Research projects related to robotics."""
        all_projects = []
        for term in ['robotics', 'robot', 'automation', 'autonomous', 'mechatronics']:
            url = f'https://gtr.ukri.org/gtr/api/projects?q={term}&p=0&s=10&fetch=concept,org'
            acq = self._fetch_url(url, timeout=15)
            if acq and acq.get('status') == 200:
                try:
                    data = json.loads(acq['content'])
                    projects = data.get('grants', {}).get('grant', [])
                    all_projects.extend(projects)
                except (json.JSONDecodeError, KeyError):
                    pass
        if not all_projects:
            return None
        return json.dumps(all_projects).encode()

    def parse(self, raw_content, raw_hash, result):
        projects = json.loads(raw_content)
        for project in projects:
            project_id = project.get('id', '')
            title = project.get('title', '')
            if not project_id:
                result.records_invalid += 1
                continue

            normalized = {
                'source_native_id': project_id,
                'title': title,
                'programme': project.get(' programme', {}).get('name', ''),
                'lead_funder': project.get('leadFunder', {}).get('name', ''),
                'start_date': project.get('startDate', ''),
                'end_date': project.get('endDate', ''),
                'award_amount': project.get('awardAmountPence', 0) / 100,
                'status': project.get('status', ''),
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

            # Create organisation from lead research organisation
            orgs = project.get('researchOrganisations', {}).get('researchOrganisation', [])
            for org in orgs:
                org_id = org.get('id', '')
                org_name = org.get('name', '')
                if org_id and org_name:
                    upsert_organisation(org_id, org_name)


if __name__ == '__main__':
    UkriGtrCollector().run()

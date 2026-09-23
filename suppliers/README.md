# Supplier Inventory

Every supplier POW tracks, with API access, scraping method, and data coverage.

---

## Tier 1: API access (structured data)

| Supplier | Country | API | Auth | Data | Scraper |
|----------|---------|-----|------|------|---------|
| **Mouser** | UK/Global | REST API | API key (free) | Components, prices, stock, datasheets | `mouser_collector.py` |
| **Farnell/element14** | UK | REST API | API key (free) | UK GBP pricing, stock, lead times | `farnell_collector.py` |
| **LCSC** | China | REST API | API key | China CNY pricing, stock, grades | `lcsc_collector.py` |
| **eBay** | UK/Global | Browse API | OAuth 2.0 | Used parts, listings, sold prices | `ebay_collector.py` |
| **Companies House** | UK | REST API | Basic auth | Company data, directors, filings | `companies_house_collector.py` |
| **RS Components** | UK | API | API key | Industrial components, UK stock | `rs_collector.py` |

## Tier 2: Scraping (Apify actors)

| Supplier | Country | Method | Actor | Data | Frequency |
|----------|---------|--------|-------|------|-----------|
| **AliExpress** | China | Apify | `agentx/aliexpress-product-scraper` | Product listings, prices, ratings, orders | Daily |
| **Alibaba** | China | Apify | `apify/web-scraper` | Wholesale pricing, MOQ, supplier info | Daily |
| **Amazon UK** | UK | Apify | `apify/e-commerce-scraping-tool` | Product prices, availability, reviews | Daily |
| **Taobao** | China | Apify | Custom scraper | Consumer pricing, availability | Weekly |

## Tier 3: Manual / web research

| Supplier | Country | Method | Data | Frequency |
|----------|---------|--------|------|-----------|
| **RobotShop** | UK | Web scrape | Robotics components, kits | Weekly |
| **PartaBot** | US | Web scrape | SO-101 kits, robot parts | Weekly |
| **Seeed Studio** | China | API (limited) | SO-101 kits, components | Weekly |
| **Feetech** | China | Direct | Servo manufacturer pricing | Monthly |
| **Husqvarna UK** | UK | Web scrape | Automower spare parts | Weekly |
| **iFixit** | Global | Web scrape | Repair guides, part compatibility | Weekly |

## Tier 4: Future (when needed)

| Supplier | Country | Method | Data | Priority |
|----------|---------|--------|------|----------|
| **DigiKey** | US/Global | API | Components, pricing | P2 |
| **JLCPCB** | China | API (approval needed) | PCB fabrication, assembly | P2 |
| **Seeed Fusion** | China | API | BOM sourcing, PCB assembly | P2 |
| **TME** | EU | API | European component pricing | P3 |
| **RS Americas** | US | API | US industrial components | P3 |

---

## How scraping works

### Apify integration

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")

# Scrape AliExpress for STS3215 servos
run = client.actor("agentx/aliexpress-product-scraper").call(input={
    "keyword": "STS3215 servo motor",
    "country": "United Kingdom",
    "max_results": 50,
})

# Get results
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item["title"], item["currentPrice"], item["currency"])
```

### GitHub Actions scheduling

```yaml
# .github/workflows/scrape-suppliers.yml
name: Scrape Supplier Data
on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6am UTC
  workflow_dispatch:

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install apify-client
      - run: python scrapers/run_all.py
        env:
          APIFY_TOKEN: ${{ secrets.APIFY_TOKEN }}
      - run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add data/
          git commit -m "Update supplier data [skip ci]" || exit 0
          git push
```

### Data flow

```
Apify actors / API calls / web scraping
        ↓
scrapers/run_all.py (orchestrator)
        ↓
powrobots/shared/persist.py (store_raw, insert_source_record)
        ↓
SQLite database (component_market_observation, source_record)
        ↓
powops reads via collector_db
        ↓
Dashboard + MCP
```

---

## API key inventory

| Service | Key env var | Status | Notes |
|---------|------------|--------|-------|
| Companies House | `COMPANIES_HOUSE_API_KEY` | Available | Free, 500 req/day |
| Mouser | `MOUSER_API_KEY` | Needed | Free, 1000 req/day |
| Farnell | `FARNELL_API_KEY` | Needed | Free |
| LCSC | `LCSC_API_KEY` | Needed | Free |
| eBay | `EBAY_APP_ID` | Needed | OAuth setup required |
| Apify | `APIFY_TOKEN` | Needed | Free tier: $5/mo credit |
| RS Components | `RS_API_KEY` | Needed | Free |

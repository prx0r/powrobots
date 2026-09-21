# API Keys Required

Human action needed to obtain free API keys for data collection.

## Priority 1 — Immediate (free, instant registration)

### Companies House
- URL: https://developer.company-information.service.gov.uk/get-started
- Cost: Free
- What it gives: UK company data (name, status, officers, filings, SIC codes)
- Used for: Mapping integrators, suppliers, grant recipients to legal entities
- Registration: Create account → get API key

### Mouser Electronics
- URL: https://www.mouser.com/api-search/
- Cost: Free (30 calls/min, 1,000 calls/day)
- What it gives: Component stock, pricing, lead time, lifecycle, replacements
- Used for: Component BOM tracking, price/availability monitoring
- Registration: Create account → API Settings → get API key

### Farnell / element14
- URL: https://partner.element14.com/
- Cost: Free
- What it gives: UK component pricing, stock, availability, lead time
- Used for: UK landed component prices
- Registration: Create account → API key

### DigiKey
- URL: https://developer.digikey.com/
- Cost: Free
- What it gives: Component specs, pricing, stock, substitutions
- Used for: Component identity and lifecycle
- Registration: Create account → API key

### eBay Browse API
- URL: https://developer.ebay.com/api/buy
- Cost: Free (5,000 calls/day)
- What it gives: UK marketplace listings for used robots, parts, components
- Used for: Used robot market monitoring, spare parts pricing
- Registration: Create account → Application → get OAuth App ID

## Priority 2 — When ready

### LCSC Electronics (China)
- URL: https://www.lcsc.com/docs/openapi/index.html
- Cost: Unknown (contact support)
- What it gives: China component pricing in CNY
- Used for: China→UK spread calculation
- Registration: Contact LCSC for API access

### Adzuna Job Search
- URL: https://developer.adzuna.com/
- Cost: Free tier available
- What it gives: UK job listings with salary data
- Used for: Robotics labour demand signals
- Registration: Create account → API key

## Priority 3 — Later

### UN Comtrade
- URL: https://comtradeapi.un.org/
- Cost: Free (limited calls)
- What it gives: Global trade flows by HS code
- Used for: China→UK robot/component trade analysis
- Registration: Create account

### Nexar / Octopart
- URL: https://nexar.com/api
- Cost: Free tier limited
- What it gives: 70M+ electronic parts, distributor stock, pricing
- Used for: Component enrichment (not primary source)
- Registration: Create account

## Currently Working (no keys needed)

| Source | Status |
|--------|--------|
| HMRC UK Trade Info | ✅ Open, no auth |
| UKRI Gateway to Research | ✅ Open, no auth |
| OPSS Product Safety | ✅ Open, no auth |
| BARA / Automate UK | ✅ Open, no auth |
| Contracts Finder | ✅ Open, no auth |
| BGS Minerals | ✅ Open, no auth |
| ONS PPI | ✅ Open, no auth |
| RBTX/igus | ✅ Open, no auth |
| Apprenticeships | ✅ Open, no auth |

## Already Obtained

### Dataspace — REST API
- Key name: `key1`
- Description: data collection
- Key type: Rest API key
- API key: `d284d51e-b98b-4517-861d-0f8b2273ceeb`
- Registered: 21 September 2026

### Dataspace — Streaming API
- Key name: `powstream`
- Description: Real-time UK trade capacity monitoring
- Key type: Streaming API Key
- Stream key: `0aa57ba1-9f9a-4e5b-a45f-0e69b56a71ad`
- Registered: 21 September 2026

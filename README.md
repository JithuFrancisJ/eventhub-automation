# eventhub-automation

Playwright + pytest automation framework for [EventHub](https://eventhub.rahulshettyacademy.com).

## Setup

```bash
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

## Run Tests

```bash
# All tests
pytest

# UI tests only
pytest tests/ui

# API tests only
pytest tests/api

# Hybrid tests only
pytest tests/hybrid

# By marker
pytest -m positive
pytest -m negative

# By environment
TEST_ENV=qa pytest
```

## Reports

HTML report is auto-generated at `reports/report.html` after every run.
Open it in a browser to view pass/fail results, test details, and durations.

## Project Structure

```
eventhub-automation/
├── api/
│   ├── clients/        # BaseClient, AuthClient, EventClient, BookingClient
│   ├── endpoints/      # AuthEndpoints, EventEndpoints, BookingEndpoints
│   └── models/         # BookingModel, EventModel, UserModel
├── components/         # NavBar
├── config/             # qa.yaml
├── fixtures/           # ui_fixtures, api_fixtures, hybrid_fixtures
├── pages/              # BasePage, LoginPage, HomePage, EventsPage, CheckoutPage, OrderConfirmationPage, MyBookingsPage
├── reports/            # auto-generated HTML reports (gitignored)
├── tests/
│   ├── ui/
│   │   ├── login/      # positive (1), negative (5)
│   │   ├── events/     # positive (11), negative (4)
│   │   └── bookings/   # positive (5), negative (2)
│   ├── api/
│   │   ├── auth/       # positive (3), negative (7)
│   │   ├── events/     # positive (6), negative (5)
│   │   └── bookings/   # positive (6), negative (6)
│   └── hybrid/
│       ├── booking/    # create (1), verify (1), cancel (1)
│       └── user/       # full flow (1)
└── utils/              # config_reader, logger, assertions, helpers, test_data
```

## Pages

| Page | URL |
|------|-----|
| Login | `/login` |
| Home | `/` |
| Events | `/events` |
| My Bookings | `/bookings` |
| Checkout | `/events/{id}` |
| Order Confirmation | after booking |

## Markers

| Marker | Description |
|--------|-------------|
| `ui` | UI tests |
| `api` | API tests |
| `hybrid` | Hybrid tests |
| `positive` | Positive test cases |
| `negative` | Negative test cases |

## Important Notes

- **Login**: After `Sign In` click, use `wait_for_url(base_url + "/")` — `wait_for_load_state("networkidle")` resolves before redirect completes
- **Ticket controls**: App uses Unicode minus `−` (U+2212) not hyphen `-`. Locators use XPath sibling of `#ticket-count`
- **`#book-now-btn`**: Present in DOM on events page but requires `wait_for_url` after click to confirm navigation to checkout
- **Auth**: App uses token-based auth stored in localStorage. Token key: `token`
- **Config**: Single environment (`qa`). `TEST_ENV` env variable selects config file

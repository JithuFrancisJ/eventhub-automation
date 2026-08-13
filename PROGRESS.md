# Framework Build Progress

## Completed

### Config
- `config/qa.yaml` — base_url, api_base_url, urls (home, events, my_bookings, login), email, password, browser, headless
- `config/dev.yaml` — deleted (single environment only)

### Utils
- `utils/config_reader.py` — reads qa.yaml via `get_config()`, supports `TEST_ENV` env variable
- `utils/logger.py` — basic logging setup
- `utils/assertions.py` — `assert_status_code`, `assert_key_in_response`, `get_detail_message(response, field)`
- `utils/helpers.py` — `wait()`, `format_date()`, `wait_for_url()`, `take_screenshot()`, `clear_local_storage()`
- `utils/test_data.py` — `BOOKING_DETAILS`, `INVALID_USER`, `load_json()`, `make_booking_payload(event_id, quantity)`

### Pages
- `pages/base_page.py` — base class with `navigate(url_key)` using config urls
- `pages/login_page.py` — email, password, signIn locators, error locators + `login()` method
  - `error_invalid_credentials` — `.fixed.top-4.right-4 p`
  - `error_invalid_email` — `get_by_text("Enter a valid email")`
  - `error_invalid_password` — `get_by_text("Password must be at least 6 characters")`
  - `login()` does NOT include `wait_for_url` — handled in positive test only
- `pages/home_page.py` — body button locators + click methods
- `pages/events_page.py` — search, categories, cities, book_now, event_links, event_titles (`article h3`), event_cards, no_results, clear_filters + action methods
- `pages/checkout_page.py` — form fields, ticket controls, confirm_booking + action methods
- `pages/order_confirmation_page.py` — confirmation elements + click methods
- `pages/my_bookings_page.py` — booking card elements + action methods with dialog handling

### Components
- `components/navbar.py` — home (`#nav-home`), events (`#nav-events`), my_bookings (`#nav-bookings`), logout (`#logout-btn`)

### Fixtures
- `fixtures/ui_fixtures.py` — config, browser (dynamic from qa.yaml), page (uses `new_context()` for full isolation)
- `fixtures/api_fixtures.py` — auth_client, auth_token, event_client, booking_client (all use shared `config` fixture)
- `fixtures/hybrid_fixtures.py` — `authenticated_page` — logs in via UI, yields page ready for hybrid tests

### Root
- `conftest.py` — imports all fixtures globally (config, browser, page, auth_client, auth_token, event_client, booking_client, authenticated_page)
- `pytest.ini` — markers (ui, api, hybrid, positive, negative), testpaths, addopts (auto HTML report to `reports/report.html`)
- `requirements.txt` — pytest, playwright, pytest-playwright, requests, pyyaml, openpyxl, python-dotenv, pytest-html

### API
- `api/clients/base_client.py` — BaseClient with get (supports custom headers), post, put, delete
- `api/clients/auth_client.py` — `register()`, `login()`, `get_me(token)`
- `api/clients/event_client.py` — `get_events(params)`, `get_event(id)`, `create_event()`, `update_event()`, `delete_event()`
- `api/clients/booking_client.py` — `get_bookings(params)`, `get_booking(id)`, `get_booking_by_ref(ref)`, `create_booking()`, `delete_booking()`
- `api/endpoints/auth_endpoints.py` — LOGIN `/auth/login`, REGISTER `/auth/register`, ME `/auth/me`
- `api/endpoints/event_endpoints.py` — EVENTS `/events`, EVENT_BY_ID `/events/{id}`
- `api/endpoints/booking_endpoints.py` — BOOKINGS `/bookings`, BOOKING_BY_ID `/bookings/{id}`, BOOKING_BY_REF `/bookings/ref/{ref}`
- `api/models/user_model.py` — `UserModel(email, password)` + `to_dict()`
- `api/models/event_model.py` — `EventModel(title, category, venue, city, event_date, price, total_seats, description, image_url)` + `to_dict()`
- `api/models/booking_model.py` — `BookingModel(event_id, customer_name, customer_email, customer_phone, quantity)` + `to_dict()`

### Tests Completed
- `tests/ui/login/positive/test_login_positive.py` — 1 test (valid login + wait_for_url + assert URL) ✅
- `tests/ui/login/negative/test_login_negative.py` — 5 tests (invalid email, invalid password, null email, null password, null both) ✅
- `tests/ui/events/positive/test_event_search.py` — 6 tests (all events default, search by title, search by venue, filter by category, filter by city, clear filters) ✅
- `tests/ui/events/negative/test_event_search_negative.py` — 4 tests (nonexistent term, whitespace search, category+city combo, search+category combo) ✅
- `tests/api/auth/positive/test_auth_positive.py` — 3 tests (valid login, register with random email saved to data/registered_users.txt, get_me) ✅
- `tests/api/auth/negative/test_auth_negative.py` — 7 tests (invalid credentials, invalid email, invalid password, null email, null password, null both, invalid token) ✅
- `tests/ui/events/positive/test_event_booking.py` — 5 tests (single ticket, multiple tickets, booking ref, view my bookings, browse more events) ✅
- `tests/ui/bookings/positive/test_my_bookings.py` — 5 tests (card displayed, booking ref on card, view details, cancel booking, clear all) ✅
- `tests/ui/bookings/negative/test_my_bookings_negative.py` — 2 tests (empty state, browse events from empty state) ✅
- `tests/api/events/positive/test_events_positive.py` — 6 tests (get all, get by id, response fields, search, filter by category, filter by city) ✅
- `tests/api/events/negative/test_events_negative.py` — 5 tests (nonexistent id, invalid id, no results, invalid category, invalid city) ✅
- `tests/api/bookings/positive/test_bookings_positive.py` — 6 tests (create, get all, get by id, get by ref, delete, response fields) ✅
- `tests/api/bookings/negative/test_bookings_negative.py` — 6 tests (missing fields, invalid event id, nonexistent id, invalid ref, delete nonexistent, no auth) ✅
- `tests/hybrid/booking/test_create_booking.py` — 1 test (book via UI, verify via API) ✅
- `tests/hybrid/booking/test_verify_booking.py` — 1 test (create via API, verify appears on UI) ✅
- `tests/hybrid/booking/test_cancel_booking.py` — 1 test (cancel via UI, verify deleted via API) ✅
- `tests/hybrid/user/test_user_booking_flow.py` — 1 test (full end-to-end booking flow) ✅

### Key Decisions
- `cleanup_booking` fixture in booking tests — collects booking refs during test, deletes via API in teardown to restore seats
- `booking_client` teardown uses `resp.json()["data"]["id"]` — id is nested under `data` key
- Event 2 (Hollywood Monsoon Night, `/events/2`) used for booking tests — has enough seats and resets via teardown
- Cancel Booking uses an inline modal — click `#cancel-booking-btn` then `"Yes, cancel it"` button (not a browser dialog)
- `authenticated_page` fixture uses UI login (not localStorage injection) — localStorage approach doesn't persist due to Next.js redirect to `/login`
- `make_booking_payload(event_id, quantity)` added to `test_data.py` — reusable across API and hybrid tests
- `event_client` and `booking_client` fixtures now include auth token in headers
- `page` fixture uses `new_context()` not `new_page()` — ensures full isolation (no shared cookies/localStorage)
- `login()` method does NOT include `wait_for_url` — positive test handles it, negative tests don't need it
- API base URL is `https://api.eventhub.rahulshettyacademy.com/api` — different from UI base URL
- `details` array in validation error responses — use `get_detail_message(response, field)` to find by field key, not index
- `get_me` invalid token returns `"Invalid or expired token"` not `"Unauthorized"`
- Random email for register test uses `uuid.uuid4().hex[:8]` — saved to `data/registered_users.txt`
- Event titles are in `article h3` not `h2`
- App does NOT trim whitespace in search — spaces return 0 results
- Concert event (Hollywood Monsoon Night) is in Los Angeles, not Mumbai or Delhi — use Mumbai for Concert+city no-results combo

## Pending

All planned tests completed. 65 tests passing across UI, API, and hybrid suites.

### Reporting
- `pytest-html` installed and configured — report auto-generated at `reports/report.html` on every run
- `reports/` added to `.gitignore`

import pytest
from pages.login_page import LoginPage
from pages.events_page import EventsPage
from playwright.sync_api import expect


@pytest.fixture(autouse=True)
def navigate_to_events(page, config):
    login_page = LoginPage(page, config)
    login_page.login(config["email"], config["password"])
    page.wait_for_url(config["base_url"] + "/")
    events_page = EventsPage(page, config)
    events_page.navigate("events")
    page.wait_for_timeout(2000)


@pytest.mark.ui
@pytest.mark.negative
def test_search_nonexistent_term_shows_no_results(page, config):
    events_page = EventsPage(page, config)
    events_page.search_event("xyznonexistent999")
    page.wait_for_timeout(1000)
    expect(events_page.event_cards).to_have_count(0)
    expect(events_page.no_results).to_be_visible()


@pytest.mark.ui
@pytest.mark.negative
def test_search_whitespace_shows_no_results(page, config):
    events_page = EventsPage(page, config)
    events_page.search_event("   ")
    page.wait_for_timeout(1000)
    expect(events_page.event_cards).to_have_count(0)
    expect(events_page.no_results).to_be_visible()


@pytest.mark.ui
@pytest.mark.negative
def test_category_and_city_combo_no_results(page, config):
    events_page = EventsPage(page, config)
    events_page.select_category("Concert")
    events_page.select_city("Mumbai")
    page.wait_for_timeout(1000)
    expect(events_page.event_cards).to_have_count(0)
    expect(events_page.no_results).to_be_visible()


@pytest.mark.ui
@pytest.mark.negative
def test_search_and_category_combo_no_results(page, config):
    events_page = EventsPage(page, config)
    events_page.search_event("Dilli")
    events_page.select_category("Concert")
    page.wait_for_timeout(1000)
    expect(events_page.event_cards).to_have_count(0)
    expect(events_page.no_results).to_be_visible()

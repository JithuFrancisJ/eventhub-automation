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
@pytest.mark.positive
def test_all_events_displayed_by_default(page, config):
    events_page = EventsPage(page, config)
    expect(events_page.event_cards).to_have_count(3)


@pytest.mark.ui
@pytest.mark.positive
def test_search_by_event_title(page, config):
    events_page = EventsPage(page, config)
    events_page.search_event("Dilli")
    page.wait_for_timeout(1000)
    expect(events_page.event_cards).to_have_count(1)
    expect(events_page.event_titles.first).to_contain_text("Dilli Diwali Mela")


@pytest.mark.ui
@pytest.mark.positive
def test_search_by_venue(page, config):
    events_page = EventsPage(page, config)
    events_page.search_event("Pragati")
    page.wait_for_timeout(1000)
    expect(events_page.event_cards).to_have_count(1)
    expect(events_page.event_titles.first).to_contain_text("Dilli Diwali Mela")


@pytest.mark.ui
@pytest.mark.positive
def test_filter_by_category(page, config):
    events_page = EventsPage(page, config)
    events_page.select_category("Concert")
    page.wait_for_timeout(1000)
    expect(events_page.event_cards).to_have_count(1)
    expect(events_page.event_titles.first).to_contain_text("Hollywood Monsoon Night")


@pytest.mark.ui
@pytest.mark.positive
def test_filter_by_city(page, config):
    events_page = EventsPage(page, config)
    events_page.select_city("Delhi")
    page.wait_for_timeout(1000)
    expect(events_page.event_cards).to_have_count(1)
    expect(events_page.event_titles.first).to_contain_text("Dilli Diwali Mela")


@pytest.mark.ui
@pytest.mark.positive
def test_clear_filters_restores_all_events(page, config):
    events_page = EventsPage(page, config)
    events_page.select_category("Concert")
    page.wait_for_timeout(1000)
    expect(events_page.event_cards).to_have_count(1)
    events_page.clear_filters.click()
    page.wait_for_timeout(1000)
    expect(events_page.event_cards).to_have_count(3)

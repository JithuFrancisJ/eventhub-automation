import pytest
from playwright.sync_api import sync_playwright
from utils.config_reader import get_config


@pytest.fixture(scope="session")
def config():
    return get_config()


@pytest.fixture(scope="session")
def browser(config):
    with sync_playwright() as p:
        browser_type = getattr(p, config["browser"])
        browser = browser_type.launch(headless=config["headless"])
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

class BasePage:

    def __init__(self, page, config):
        self.page = page
        self.base_url = config["base_url"]
        self.urls = config["urls"]

    def navigate(self, url_key):
        self.page.goto(self.base_url + self.urls[url_key])

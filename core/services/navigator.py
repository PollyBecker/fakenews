from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

try:
    from webdriver_manager.chrome import ChromeDriverManager
    WDM_AVAILABLE = True
except ImportError:
    WDM_AVAILABLE = False


class Navigator:
    def __init__(self, headless: bool = False):
        self._driver = None
        self._headless = headless

    def _get_driver(self):
        if self._driver is None:
            options = Options()
            if self._headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            if WDM_AVAILABLE:
                service = Service(ChromeDriverManager().install())
                self._driver = webdriver.Chrome(service=service, options=options)
            else:
                self._driver = webdriver.Chrome(options=options)

        return self._driver

    def open_url(self, url: str):
        self._get_driver().get(url)

    def scroll(self, amount: int = 300):
        self._get_driver().execute_script(f'window.scrollBy(0, {amount})')

    def get_screenshot(self) -> bytes:
        return self._get_driver().get_screenshot_as_png()

    def close(self):
        if self._driver:
            self._driver.quit()
            self._driver = None

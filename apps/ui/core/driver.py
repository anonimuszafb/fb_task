from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

instance = None


def initialize(browser='firefox'):
    global instance
    if browser.lower() == 'chrome':
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        service = ChromeService(ChromeDriverManager().install())
        instance = webdriver.Chrome(service=service, options=options)
    else:
        options = FirefoxOptions()
        options.add_argument('--headless')
        options.set_preference('intl.accept_languages', 'en-US, en')
        instance = webdriver.Firefox(options=options)
    instance.implicitly_wait(2)


def quit_driver():
    global instance
    instance.quit()

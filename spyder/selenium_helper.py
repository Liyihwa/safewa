import selenium.webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import selenium.webdriver.chrome.options
def get_chrome_driver(binary_path=r'C:\Program Files (x86)\Chromebrowser\Chrome.exe',
                      webdriver_path=r'D:\env\webdriver\chrome\chromedriver.exe',
                      headless=False,
                      implicitly_wait=10):

    options = selenium.webdriver.chrome.options.Options()
    options.binary_location=binary_path
    options.add_experimental_option("excludeSwitches",['enable-automation'])
    if headless:
        options.add_argument("--headless")
    browser = selenium.webdriver.Chrome(service=Service(webdriver_path),options=options)
    browser.implicitly_wait(implicitly_wait)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
    　　    Object.defineProperty(navigator, 'webdriver', {
    　　      get: () => undefined
    　　    })
    　　  """})
    return browser
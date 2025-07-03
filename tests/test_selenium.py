import time
import uuid
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os, sys

@pytest.fixture(scope="module")
def driver(request):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1280,800")

    path = ChromeDriverManager().install()
    if sys.platform.startswith("win") and not path.endswith("chromedriver.exe"):
        path = os.path.join(os.path.dirname(path), "chromedriver.exe")

    service = Service(path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    request.addfinalizer(driver.quit)
    return driver


def test_login_form_fields_fillable(driver):
    driver.get("http://localhost:3000/login")
    driver.execute_script("window.localStorage.clear();")

    email_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.ID, "password")

    email_input.send_keys("fake@example.com")
    password_input.send_keys("123456")

    assert email_input.get_attribute("value") == "fake@example.com"


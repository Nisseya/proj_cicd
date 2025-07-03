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

def test_register_login_dashboard(driver):
    email = f"test_{uuid.uuid4().hex[:6]}@e2e.com"
    password = "e2epassword"
    name = "E2E Test User"

    # Aller à la page d'inscription
    driver.get("http://localhost:3000/register")
    time.sleep(1)

    driver.find_element(By.NAME, "name").send_keys(name)
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.TAG_NAME, "form").submit()
    time.sleep(2)

    # Devrait rediriger vers /dashboard
    assert "/dashboard" in driver.current_url

    # Se déconnecter en supprimant localStorage (si implémenté)
    driver.execute_script("window.localStorage.clear();")
    driver.get("http://localhost:3000/login")
    time.sleep(1)

    # Page de login
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.TAG_NAME, "form").submit()
    time.sleep(2)

    # Redirection post-login
    assert "/dashboard" in driver.current_url

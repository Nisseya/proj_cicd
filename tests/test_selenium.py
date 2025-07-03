import os, sys, time
import pytest, uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


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


def test_login_success(driver):
    driver.get("http://localhost:3000/login")
    driver.execute_script("window.localStorage.clear();")

    driver.find_element(By.ID, "email").send_keys("admin@test.com")
    driver.find_element(By.ID, "password").send_keys("password")
    driver.find_element(By.TAG_NAME, "form").submit()

    WebDriverWait(driver, 5).until(lambda d: "/dashboard" in d.current_url)
    assert "/dashboard" in driver.current_url

def test_open_task_form(driver):
    test_login_success(driver)  

    create_button = WebDriverWait(driver, 5).until(
        lambda d: d.find_element(By.XPATH, "//button[contains(text(), 'Nouvelle Tâche')]")
    )
    create_button.click()

    title_input = WebDriverWait(driver, 5).until(
        lambda d: d.find_element(By.ID, "title")
    )
    assert title_input.is_displayed()


def test_create_task(driver):
    test_login_success(driver)
    create_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Nouvelle Tâche')]"))
    )
    create_btn.click()

    task_title = f"Tâche Selenium {uuid.uuid4().hex[:5]}"
    title_input = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "title"))
    )
    title_input.send_keys(task_title)

    driver.find_element(By.ID, "priority").send_keys("high")

    driver.find_element(By.CSS_SELECTOR, "form.task-form button[type='submit']").click()

    WebDriverWait(driver, 5).until(lambda d: task_title in d.page_source)
    assert task_title in driver.page_source


def test_edit_task(driver):
    test_create_task(driver)

    edit_btn = WebDriverWait(driver, 5).until(
        lambda d: d.find_element(By.XPATH, "//button[@title='Modifier']")
    )
    edit_btn.click()

    title_input = WebDriverWait(driver, 5).until(
        lambda d: d.find_element(By.ID, "title")
    )
    new_title = "Tâche modifiée"
    title_input.clear()
    title_input.send_keys(new_title)

    driver.find_element(By.CSS_SELECTOR, "form.task-form button[type='submit']").click()

    WebDriverWait(driver, 5).until(lambda d: new_title in d.page_source)
    assert new_title in driver.page_source

    
def test_login_failure(driver):
    driver.get("http://localhost:3000/login")
    driver.execute_script("window.localStorage.clear();")

    driver.find_element(By.ID, "email").send_keys("admin@test.com")
    driver.find_element(By.ID, "password").send_keys("wrongpass")
    driver.find_element(By.TAG_NAME, "form").submit()

    time.sleep(1)
    assert "/login" in driver.current_url
    assert "error" in driver.page_source.lower() 

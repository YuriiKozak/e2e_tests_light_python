import pytest
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.web.selenium.pages.login_page import LoginPage
from src.web.selenium.pages.login_page_v2 import LoginPageV2
from tests.fixtures.configs import Configs

FREE_PROJECTS = "Free Projects"
TARGET_PROJECT = "Popopo"


@pytest.mark.regression
def test_project_search(driver: WebDriver, configs: Configs):
    wait = WebDriverWait(
        driver,
        10,
        poll_frequency=0.1,
        ignored_exceptions=[NoSuchElementException, StaleElementReferenceException],
    )

    driver.get(configs.url)
    driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_email").send_keys(configs.email)
    driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_password").send_keys(configs.password)
    driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_remember_me").click()
    driver.find_element(By.CSS_SELECTOR, "#content-desktop [value='Sign In']").click()
    driver.find_element(By.CSS_SELECTOR, "#content-desktop .common-flash-success").click()

    driver.find_element(By.CSS_SELECTOR, "#content-desktop #search").send_keys(TARGET_PROJECT)
    driver.find_element(By.CSS_SELECTOR, f"#content-desktop [title='{TARGET_PROJECT}']").click()
    wait.until(EC.visibility_of_element_located((By.XPATH, f"//h2[contains(., '{TARGET_PROJECT}')]")))


@pytest.mark.regression
def test_login_with_page_object_v1(driver: WebDriver, configs: Configs):
    login_page = LoginPage(driver)
    login_page.open(configs.url)
    login_page.is_loaded()
    login_page.login(email=configs.email, password=configs.password)
    login_page.should_see_success_message()


@pytest.mark.regression
def test_login_with_page_object_v2(driver: WebDriver, configs: Configs):
    login_page = LoginPageV2(driver)
    login_page.open(configs.url)
    login_page.is_loaded()
    login_page.login(email=configs.email, password=configs.password)
    login_page.should_see_success_message()

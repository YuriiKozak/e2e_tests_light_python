import pytest
from selenium import webdriver


@pytest.fixture(scope="function")
def driver(request):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(0)
    yield driver
    driver.quit()

# tests/test_integration.py

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Update BASE_URL sesuai dengan alamat PHP built-in server
BASE_URL = "http://localhost:8000/"

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    # Inisialisasi ChromeDriver (pastikan chromedriver sudah tersedia)
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_valid_login(driver):
    # Test Case 1: Validasi login dengan kredensial valid
    driver.get(BASE_URL + "login.php")
    driver.find_element(By.ID, "inputUsername").send_keys("admin")
    driver.find_element(By.ID, "inputPassword").send_keys("admin")
    driver.find_element(By.XPATH, "//button[contains(text(),\"OK I'm sign in\")]").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "employee")))
    assert "employee" in driver.page_source

def test_invalid_login(driver):
    # Test Case 2: Validasi login dengan kredensial salah
    driver.get(BASE_URL + "login.php")
    driver.find_element(By.ID, "inputUsername").send_keys("admin")
    driver.find_element(By.ID, "inputPassword").send_keys("wrongpass")
    driver.find_element(By.XPATH, "//button[contains(text(),\"OK I'm sign in\")]").click()
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, "//label"), "Damn, wrong credentials!!")
    )
    assert "Damn, wrong credentials!!" in driver.page_source

def test_create_contact(driver):
    # Test Case 3: Integrasi create contact
    driver.get(BASE_URL + "login.php")
    driver.find_element(By.ID, "inputUsername").send_keys("admin")
    driver.find_element(By.ID, "inputPassword").send_keys("admin")
    driver.find_element(By.XPATH, "//button[contains(text(),\"OK I'm sign in\")]").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Add New Contact")))
    driver.find_element(By.LINK_TEXT, "Add New Contact").click()
    driver.find_element(By.NAME, "name").send_keys("Test User")
    driver.find_element(By.NAME, "email").send_keys("testuser@example.com")
    driver.find_element(By.NAME, "phone").send_keys("1234567890")
    driver.find_element(By.NAME, "title").send_keys("Tester")
    driver.find_element(By.XPATH, "//input[@type='submit' and @value='Save']").click()
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Test User")
    )
    assert "Test User" in driver.page_source

def test_update_contact(driver):
    # Test Case 4: Integrasi update contact
    driver.get(BASE_URL + "login.php")
    driver.find_element(By.ID, "inputUsername").send_keys("admin")
    driver.find_element(By.ID, "inputPassword").send_keys("admin")
    driver.find_element(By.XPATH, "//button[contains(text(),\"OK I'm sign in\")]").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "edit")))
    edit_links = driver.find_elements(By.LINK_TEXT, "edit")
    if edit_links:
        edit_links[0].click()
    else:
        pytest.skip("No contact available to update")
    name_field = driver.find_element(By.NAME, "name")
    name_field.clear()
    new_name = "Updated User"
    name_field.send_keys(new_name)
    driver.find_element(By.XPATH, "//input[@type='submit' and @value='Update']").click()
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), new_name)
    )
    assert new_name in driver.page_source

def test_delete_contact(driver):
    # Test Case 5: Integrasi delete contact
    driver.get(BASE_URL + "login.php")
    driver.find_element(By.ID, "inputUsername").send_keys("admin")
    driver.find_element(By.ID, "inputPassword").send_keys("admin")
    driver.find_element(By.XPATH, "//button[contains(text(),\"OK I'm sign in\")]").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "delete")))
    delete_links = driver.find_elements(By.LINK_TEXT, "delete")
    if delete_links:
        row = delete_links[-1].find_element(By.XPATH, "./ancestor::tr")
        contact_name = row.find_elements(By.TAG_NAME, "td")[1].text
        delete_links[-1].click()
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            driver.switch_to.alert.accept()
        except Exception:
            pass
        time.sleep(2)
        assert contact_name not in driver.page_source
    else:
        pytest.skip("No contact available to delete")

import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost/"  # Ubah URL sesuai dengan konfigurasi server aplikasi Anda

@pytest.fixture(scope="session")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
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
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "employee")))
    except Exception:
        pytest.fail("Login dengan kredensial valid gagal.")

def test_invalid_login(driver):
    # Test Case 2: Validasi login dengan kredensial salah
    driver.get(BASE_URL + "login.php")
    driver.find_element(By.ID, "inputUsername").send_keys("admin")
    driver.find_element(By.ID, "inputPassword").send_keys("wrongpass")
    driver.find_element(By.XPATH, "//button[contains(text(),\"OK I'm sign in\")]").click()
    try:
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, "//label"), "Damn, wrong credentials!!")
        )
    except Exception:
        pytest.fail("Pesan error tidak muncul untuk kredensial salah.")

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
    try:
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Test User")
        )
    except Exception:
        pytest.fail("Pembuatan kontak baru gagal.")

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
        pytest.skip("Tidak ada kontak untuk di-update.")
    name_field = driver.find_element(By.NAME, "name")
    name_field.clear()
    new_name = "Updated User"
    name_field.send_keys(new_name)
    driver.find_element(By.XPATH, "//input[@type='submit' and @value='Update']").click()
    try:
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), new_name)
        )
    except Exception:
        pytest.fail("Update kontak gagal.")

def test_delete_contact(driver):
    # Test Case 5: Integrasi delete contact
    driver.get(BASE_URL + "login.php")
    driver.find_element(By.ID, "inputUsername").send_keys("admin")
    driver.find_element(By.ID, "inputPassword").send_keys("admin")
    driver.find_element(By.XPATH, "//button[contains(text(),\"OK I'm sign in\")]").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "delete")))
    delete_links = driver.find_elements(By.LINK_TEXT, "delete")
    if delete_links:
        # Ambil nama kontak dari baris terkait (misal kolom kedua adalah nama)
        row = delete_links[-1].find_element(By.XPATH, "./ancestor::tr")
        contact_name = row.find_elements(By.TAG_NAME, "td")[1].text
        delete_links[-1].click()
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            driver.switch_to.alert.accept()
        except Exception:
            pass
        time.sleep(2)  # Memberikan waktu untuk proses penghapusan
        page_body = driver.find_element(By.TAG_NAME, "body").text
        if contact_name in page_body:
            pytest.fail("Kontak tidak terhapus.")
    else:
        pytest.skip("Tidak ada kontak untuk dihapus.")

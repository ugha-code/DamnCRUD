import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Pastikan aplikasi PHP dijalankan di port 8000
BASE_URL = "http://localhost:8000/"

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    # Inisialisasi ChromeDriver (pastikan chromedriver tersedia di PATH)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

def login(driver, username="admin", password="admin"):
    driver.get(BASE_URL + "login.php")
    driver.find_element(By.ID, "inputUsername").send_keys(username)
    driver.find_element(By.ID, "inputPassword").send_keys(password)
    driver.find_element(By.XPATH, "//button[contains(text(),\"OK I'm sign in\")]").click()
    # Tunggu sampai dashboard muncul
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "employee")))

@pytest.mark.parametrize("username,password,expected", [
    ("admin", "admin", True),          # Test case 1: valid login
    ("admin", "wrongpass", False)        # Test case 2: invalid login
])
def test_login(driver, username, password, expected):
    driver.get(BASE_URL + "login.php")
    driver.find_element(By.ID, "inputUsername").send_keys(username)
    driver.find_element(By.ID, "inputPassword").send_keys(password)
    driver.find_element(By.XPATH, "//button[contains(text(),\"OK I'm sign in\")]").click()
    if expected:
        # Jika login valid, harus ada elemen tabel dengan id "employee"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "employee")))
        assert True
    else:
        # Untuk login invalid, periksa pesan error
        error_present = WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, "//label"), "Damn, wrong credentials!!")
        )
        assert error_present

def test_create_contact(driver):
    # Test Case 3: Create contact
    login(driver)
    driver.find_element(By.LINK_TEXT, "Add New Contact").click()
    driver.find_element(By.NAME, "name").send_keys("Test User")
    driver.find_element(By.NAME, "email").send_keys("testuser@example.com")
    driver.find_element(By.NAME, "phone").send_keys("1234567890")
    driver.find_element(By.NAME, "title").send_keys("Tester")
    driver.find_element(By.XPATH, "//input[@type='submit' and @value='Save']").click()
    # Verifikasi kontak baru muncul
    assert WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Test User")
    )

def test_update_contact(driver):
    # Test Case 4: Update contact
    login(driver)
    # Klik link "edit" pada salah satu kontak (misal, yang pertama)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "edit")))
    edit_links = driver.find_elements(By.LINK_TEXT, "edit")
    if edit_links:
        edit_links[0].click()
    else:
        pytest.skip("Tidak ada kontak untuk di-update")
    # Ubah nama menjadi "Updated User"
    name_field = driver.find_element(By.NAME, "name")
    name_field.clear()
    new_name = "Updated User"
    name_field.send_keys(new_name)
    driver.find_element(By.XPATH, "//input[@type='submit' and @value='Update']").click()
    # Verifikasi perubahan di halaman index
    assert WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), new_name)
    )

def test_delete_contact(driver):
    # Test Case 5: Delete contact
    login(driver)
    # Ambil daftar link "delete"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "delete")))
    delete_links = driver.find_elements(By.LINK_TEXT, "delete")
    if delete_links:
        # Ambil nama kontak dari baris terakhir untuk dihapus
        row = delete_links[-1].find_element(By.XPATH, "./ancestor::tr")
        contact_name = row.find_elements(By.TAG_NAME, "td")[1].text
        delete_links[-1].click()
        # Terima alert konfirmasi (jika ada)
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            driver.switch_to.alert.accept()
        except Exception:
            pass
        time.sleep(2)
        page_body = driver.find_element(By.TAG_NAME, "body").text
        assert contact_name not in page_body
    else:
        pytest.skip("Tidak ada kontak untuk dihapus")

"""
Test Procedure ID : TP-08-001
Test Case ID      : TC-08-001
Feature           : F008 Manage Settings
Objective         : Verify that the admin can successfully update profile settings
                    with all valid information.
Preconditions     : Admin logged in. Docker containers running.
Note              : TCS specifies Name, Email, Organization fields. The current UI
                    has Name, Username, Phone fields. Email is permanently disabled
                    (cannot be edited). Organization field does not exist — Company
                    is shown as read-only. Test is adapted to use available editable
                    fields: Name, Username, Phone.
Tool              : Selenium
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import login, BASE_URL, WAIT
import time


class TestTC08001:
    def test_update_profile_valid_data(self, driver):
        """TC-08-001: Update profile with valid Name, Username, Phone."""

        # Step 1: Login and navigate to Settings
        login(driver)
        driver.get(f"{BASE_URL}/settings")

        # Step 2: Wait for profile form to load (name field populated)
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((By.ID, "name"))
        )
        time.sleep(3)  # pause — let page fully render

        # Store original values for cleanup
        original_name = driver.find_element(By.ID, "name").get_attribute("value")
        original_username = driver.find_element(By.ID, "username").get_attribute("value")
        original_phone = driver.find_element(By.ID, "phone").get_attribute("value")

        # Step 3: Click "Edit Profile"
        driver.find_element(
            By.XPATH, "//button[.//span[contains(text(),'Edit Profile')]]"
        ).click()
        WebDriverWait(driver, WAIT).until(
            EC.element_to_be_clickable((By.ID, "name"))
        )
        time.sleep(2)  # pause — see edit mode activated

        # Step 4: Enter valid profile data
        name_input = driver.find_element(By.ID, "name")
        name_input.clear()
        time.sleep(1)
        name_input.send_keys("Tan Jane")
        time.sleep(1)

        username_input = driver.find_element(By.ID, "username")
        username_input.clear()
        time.sleep(1)
        username_input.send_keys("tanjane")
        time.sleep(1)

        phone_input = driver.find_element(By.ID, "phone")
        phone_input.clear()
        time.sleep(1)
        phone_input.send_keys("60199999999")
        time.sleep(2)  # pause — see all fields filled

        # Step 5: Click "Save Changes"
        driver.find_element(By.XPATH, "//button[contains(., 'Save Changes')]").click()

        # Step 6: Verify success message
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Profile updated successfully')]")
            )
        )
        assert "Profile updated successfully" in driver.page_source, \
            "FAIL: Expected success message 'Profile updated successfully' not displayed."

        print("PASS: Profile updated successfully with valid data.")
        time.sleep(3)  # pause — see success message

        # Cleanup: revert to original values
        driver.find_element(
            By.XPATH, "//button[.//span[contains(text(),'Edit Profile')]]"
        ).click()
        WebDriverWait(driver, WAIT).until(EC.element_to_be_clickable((By.ID, "name")))
        time.sleep(1)

        driver.find_element(By.ID, "name").clear()
        driver.find_element(By.ID, "name").send_keys(original_name)
        driver.find_element(By.ID, "username").clear()
        driver.find_element(By.ID, "username").send_keys(original_username)
        driver.find_element(By.ID, "phone").clear()
        driver.find_element(By.ID, "phone").send_keys(original_phone)
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[contains(., 'Save Changes')]").click()
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Profile updated successfully')]")
            )
        )
        time.sleep(2)  # pause — see revert success

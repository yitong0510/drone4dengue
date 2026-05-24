"""
Test Procedure ID : TP-08-003
Test Case ID      : TC-08-003
Feature           : F008 Manage Settings
Objective         : Verify that the admin can successfully change password when all
                    password requirements are met.
Preconditions     : Admin logged in. Docker containers running.
Note              : TCS specifies Current Password = 'AdminPass123!'. In the current
                    UI, the Current Password field is permanently disabled — it cannot
                    be filled. The API also does not verify the current password before
                    updating. Test is adapted: only New Password and Confirm Password
                    are entered. Password is set to the same value as current
                    ('adminpass1') so login credentials remain unchanged.
Tool              : Selenium
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import login, BASE_URL, WAIT
import time


class TestTC08003:
    def test_valid_password_change(self, driver):
        """TC-08-003: Change password with valid matching passwords."""

        # Step 1: Login and navigate to Settings
        login(driver)
        driver.get(f"{BASE_URL}/settings")

        # Step 2: Wait for Password Settings section to load
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((By.ID, "new-password"))
        )

        # Step 3: Enter new password
        # Using current password value to keep credentials unchanged
        driver.find_element(By.ID, "new-password").send_keys("adminpass1")

        # Step 4: Confirm new password
        driver.find_element(By.ID, "confirm-password").send_keys("adminpass1")

        # Step 5: Click "Update Password"
        driver.find_element(
            By.XPATH, "//button[contains(., 'Update Password')]"
        ).click()

        # Step 6: Verify success message
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Password updated successfully')]")
            )
        )
        assert "Password updated successfully" in driver.page_source, \
            "FAIL: Expected success message 'Password updated successfully' not displayed."

        print("PASS: Password updated successfully. "
              "Note: Current password field is disabled in UI — adapted test.")

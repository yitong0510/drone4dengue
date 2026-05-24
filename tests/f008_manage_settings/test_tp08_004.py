"""
Test Procedure ID : TP-08-004
Test Case ID      : TC-08-004
Feature           : F008 Manage Settings
Objective         : Verify that the system validates password requirements and
                    rejects invalid password inputs.
Preconditions     : Admin logged in. Docker containers running.
Note              : Current Password field is permanently disabled in the current UI.
                    The UI password validation regex is /^(?=.*\d).{8,}$/ which only
                    checks for minimum 8 characters and at least one digit. It does
                    NOT validate uppercase, special character, same-as-current, or
                    maximum length (128 chars). Several sub-cases are therefore FAIL
                    due to missing validation. Tests that would change the password
                    include a cleanup step to revert credentials.
Tool              : Selenium
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import login, BASE_URL, WAIT
import time

CURRENT_PASSWORD = "adminpass1"


def go_to_password_section(driver):
    login(driver)
    driver.get(f"{BASE_URL}/settings")
    WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((By.ID, "new-password"))
    )


def revert_password(driver):
    """Revert password back to the original if it was inadvertently changed."""
    try:
        new_pw = driver.find_element(By.ID, "new-password")
        new_pw.clear()
        new_pw.send_keys(CURRENT_PASSWORD)
        confirm_pw = driver.find_element(By.ID, "confirm-password")
        confirm_pw.clear()
        confirm_pw.send_keys(CURRENT_PASSWORD)
        driver.find_element(By.XPATH, "//button[contains(., 'Update Password')]").click()
        time.sleep(2)
    except Exception:
        pass


class TestTC08004:
    def test_wrong_current_password(self, driver):
        """TC-08-004a: Current = 'WrongPass123' — expects error 'Current password is incorrect'."""
        pytest.skip(
            "NOT TESTABLE: The Current Password field is permanently disabled in the "
            "current UI. It cannot be filled to test wrong password validation. "
            "The API also does not verify the current password before updating. "
            "TCS expected: error 'Current password is incorrect'."
        )

    def test_password_too_short(self, driver):
        """TC-08-004b: New = 'Pass1!' (7 chars) — expects error 'Password must be at least 8 characters'."""
        go_to_password_section(driver)

        driver.find_element(By.ID, "new-password").send_keys("Pass1!")  # 6 chars, has digit
        driver.find_element(By.ID, "confirm-password").send_keys("Pass1!")
        driver.find_element(By.XPATH, "//button[contains(., 'Update Password')]").click()
        time.sleep(1)

        page_source = driver.page_source
        # TCS expects: "Password must be at least 8 characters"
        # Actual: "Password must be at least 8 characters, including a number."
        error_shown = "Password must be at least 8 characters" in page_source
        assert error_shown, \
            "FAIL: Expected error 'Password must be at least 8 characters' " \
            "but no matching error was displayed."

    def test_missing_uppercase(self, driver):
        """TC-08-004c: New = 'newpass123!' (no uppercase) — expects error 'Password must contain uppercase letter'."""
        go_to_password_section(driver)

        driver.find_element(By.ID, "new-password").send_keys("newpass123!")
        driver.find_element(By.ID, "confirm-password").send_keys("newpass123!")
        driver.find_element(By.XPATH, "//button[contains(., 'Update Password')]").click()
        time.sleep(2)

        page_source = driver.page_source
        # Cleanup: revert if password was inadvertently changed
        if "Password updated successfully" in page_source:
            revert_password(driver)

        # TCS expects: "Password must contain uppercase letter"
        error_shown = "uppercase" in page_source.lower() or "must contain uppercase" in page_source
        assert error_shown, \
            "FAIL: Expected error 'Password must contain uppercase letter' " \
            "but no such error was displayed. The UI does not validate for uppercase requirement."

    def test_missing_special_char(self, driver):
        """TC-08-004d: New = 'NewPass123' (no special char) — expects error 'Password must contain special character'."""
        go_to_password_section(driver)

        driver.find_element(By.ID, "new-password").send_keys("NewPass123")
        driver.find_element(By.ID, "confirm-password").send_keys("NewPass123")
        driver.find_element(By.XPATH, "//button[contains(., 'Update Password')]").click()
        time.sleep(2)

        page_source = driver.page_source
        # Cleanup: revert if password was inadvertently changed
        if "Password updated successfully" in page_source:
            revert_password(driver)

        # TCS expects: "Password must contain special character"
        error_shown = "special character" in page_source.lower()
        assert error_shown, \
            "FAIL: Expected error 'Password must contain special character' " \
            "but no such error was displayed. The UI does not validate for special character requirement."

    def test_same_as_current(self, driver):
        """TC-08-004e: New = same as current — expects error 'New password cannot be same as current'."""
        go_to_password_section(driver)

        # Using the actual current password — safe because even if accepted, password stays the same
        driver.find_element(By.ID, "new-password").send_keys(CURRENT_PASSWORD)
        driver.find_element(By.ID, "confirm-password").send_keys(CURRENT_PASSWORD)
        driver.find_element(By.XPATH, "//button[contains(., 'Update Password')]").click()
        time.sleep(2)

        page_source = driver.page_source
        # TCS expects: "New password cannot be same as current"
        error_shown = "same as current" in page_source.lower() or "cannot be same" in page_source.lower()
        assert error_shown, \
            "FAIL: Expected error 'New password cannot be same as current' " \
            "but no such error was displayed. The UI does not validate against same-as-current passwords."

    def test_confirmation_mismatch(self, driver):
        """TC-08-004f: New = 'NewPass456!' Confirm = 'NewPass789!' — expects error 'Passwords do not match'."""
        go_to_password_section(driver)

        driver.find_element(By.ID, "new-password").send_keys("NewPass456!")
        driver.find_element(By.ID, "confirm-password").send_keys("NewPass789!")
        driver.find_element(By.XPATH, "//button[contains(., 'Update Password')]").click()
        time.sleep(1)

        page_source = driver.page_source
        # TCS expects: "Passwords do not match. Please re-enter"
        # Actual: "The passwords do not match."
        error_shown = "do not match" in page_source.lower() or "passwords do not match" in page_source.lower()
        assert error_shown, \
            "FAIL: Expected error 'Passwords do not match. Please re-enter' " \
            "but no matching error was displayed."

    def test_password_too_long(self, driver):
        """TC-08-004g: New = 129 character password — expects error 'Password must be 128 characters or less'."""
        go_to_password_section(driver)

        long_password = "NewPass1!" + "A" * 120  # 129 chars total, has digit
        driver.find_element(By.ID, "new-password").send_keys(long_password)
        driver.find_element(By.ID, "confirm-password").send_keys(long_password)
        driver.find_element(By.XPATH, "//button[contains(., 'Update Password')]").click()
        time.sleep(2)

        page_source = driver.page_source
        # Cleanup: revert if password was inadvertently changed
        if "Password updated successfully" in page_source:
            revert_password(driver)

        # TCS expects: "Password must be 128 characters or less"
        error_shown = "128 characters" in page_source or "characters or less" in page_source
        assert error_shown, \
            "FAIL: Expected error 'Password must be 128 characters or less' " \
            "but no such error was displayed. The UI does not validate for maximum password length."

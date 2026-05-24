"""
Test Procedure ID : TP-08-002
Test Case ID      : TC-08-002
Feature           : F008 Manage Settings
Objective         : Verify that the system validates profile field inputs and
                    rejects invalid data.
Preconditions     : Admin logged in. Docker containers running.
Note              : Several sub-cases are not testable due to UI constraints:
                    - Invalid email format / Duplicate email: Email field is
                      permanently disabled (read-only) in the current UI.
                    - Organization exceeds 255 chars: No Organization field in UI.
                    Sub-cases that ARE testable use assert-based failures to
                    document missing validation in the current implementation.
Tool              : Selenium
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import login, BASE_URL, WAIT
import time


def enter_edit_mode(driver):
    driver.get(f"{BASE_URL}/settings")
    # Wait for name field to be populated (profile API call completed)
    WebDriverWait(driver, WAIT).until(
        lambda d: d.find_element(By.ID, "name").get_attribute("value") not in (None, "")
    )
    time.sleep(2)  # let framer-motion animations settle
    # Use JS click to bypass any animation overlay blocking the button
    btn = driver.find_element(
        By.XPATH, "//button[.//span[contains(text(),'Edit Profile')]]"
    )
    driver.execute_script("arguments[0].click();", btn)
    WebDriverWait(driver, WAIT).until(EC.element_to_be_clickable((By.ID, "name")))
    time.sleep(1)


def revert_name(driver, original_name):
    """Revert profile name back to original after a test accidentally saves."""
    try:
        btn = WebDriverWait(driver, WAIT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[contains(text(),'Edit Profile')]]")
            )
        )
        driver.execute_script("arguments[0].click();", btn)
        WebDriverWait(driver, WAIT).until(EC.element_to_be_clickable((By.ID, "name")))
        name_input = driver.find_element(By.ID, "name")
        name_input.clear()
        name_input.send_keys(original_name)
        driver.find_element(By.XPATH, "//button[contains(., 'Save Changes')]").click()
        time.sleep(2)
    except Exception:
        pass


class TestTC08002:
    def test_empty_name(self, driver):
        """TC-08-002a: Name = blank — expects error 'Name is required'."""
        login(driver)
        enter_edit_mode(driver)

        name_input = driver.find_element(By.ID, "name")
        name_input.clear()
        time.sleep(1)  # let Save Changes button fully render after clear

        save_btn = driver.find_element(By.XPATH, "//button[contains(., 'Save Changes')]")
        driver.execute_script("arguments[0].click();", save_btn)
        time.sleep(1)

        page_source = driver.page_source
        # TCS expects: "Name is required"
        # Actual UI shows: "Please fill out this field"
        error_shown = "Name is required" in page_source
        assert error_shown, \
            "FAIL: Expected error 'Name is required' but system displayed " \
            "'Please fill out this field' instead. Error message does not match TCS specification."

    def test_name_with_special_characters(self, driver):
        """TC-08-002b: Name = 'Jane@#123' — expects error 'Name cannot contain special characters'."""
        login(driver)
        enter_edit_mode(driver)

        original_name = driver.find_element(By.ID, "name").get_attribute("value")

        name_input = driver.find_element(By.ID, "name")
        name_input.clear()
        name_input.send_keys("Jane@#123")

        driver.find_element(By.XPATH, "//button[contains(., 'Save Changes')]").click()
        time.sleep(2)

        page_source = driver.page_source

        # Cleanup: revert if name was accidentally saved
        if "Profile updated successfully" in page_source:
            revert_name(driver, original_name)

        # TCS expects: "Name cannot contain special characters"
        error_shown = "special characters" in page_source or "cannot contain" in page_source
        assert error_shown, \
            "FAIL: Expected error 'Name cannot contain special characters' " \
            "but no such validation error was displayed. System accepted name with special characters."

    def test_invalid_email_format(self, driver):
        """TC-08-002c: Email = 'admin@gmail' (invalid format) — expects error 'Invalid email format'."""
        pytest.skip(
            "NOT TESTABLE: The Email field is permanently disabled (read-only) in the "
            "current UI. It is not editable even in Edit Profile mode. There is no way "
            "to enter an invalid email format. TCS expected: error 'Invalid email format'."
        )

    def test_duplicate_email(self, driver):
        """TC-08-002d: Email = existing admin email — expects error 'Email already registered'."""
        pytest.skip(
            "NOT TESTABLE: The Email field is permanently disabled (read-only) in the "
            "current UI. It cannot be changed to test duplicate email validation. "
            "TCS expected: error 'Email already registered'."
        )

    def test_name_exceeds_255_chars(self, driver):
        """TC-08-002e: Name = 'T' x 256 — expects error 'Name must be 255 characters or less'."""
        login(driver)
        enter_edit_mode(driver)

        original_name = driver.find_element(By.ID, "name").get_attribute("value")

        name_input = driver.find_element(By.ID, "name")
        name_input.clear()
        name_input.send_keys("T" * 256)

        driver.find_element(By.XPATH, "//button[contains(., 'Save Changes')]").click()
        time.sleep(2)

        page_source = driver.page_source

        # Cleanup: revert if name was accidentally saved
        if "Profile updated successfully" in page_source:
            revert_name(driver, original_name)

        # TCS expects: "Name must be 255 characters or less"
        error_shown = "255 characters" in page_source or "characters or less" in page_source
        assert error_shown, \
            "FAIL: Expected error 'Name must be 255 characters or less' " \
            "but no such validation error was displayed. System accepted name exceeding 255 characters."

    def test_organization_exceeds_255_chars(self, driver):
        """TC-08-002f: Organization = 'M' x 256 — expects error 'Organization must be 255 characters or less'."""
        pytest.skip(
            "NOT TESTABLE: The Organization field does not exist in the current UI. "
            "The Profile Settings section shows Name, Username, Email (disabled), Phone, "
            "and Company (read-only) fields. There is no Organization input field. "
            "TCS expected: error 'Organization must be 255 characters or less'."
        )

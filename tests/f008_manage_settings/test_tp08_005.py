"""
Test Procedure ID : TP-08-005
Test Case ID      : TC-08-005
Feature           : F008 Manage Settings
Objective         : Verify that the admin can successfully update notification preferences.
Preconditions     : Admin logged in. Docker containers running.
Tool              : Selenium
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from tests.conftest import login, BASE_URL, WAIT
import time


def go_to_notifications(driver):
    login(driver)
    driver.get(f"{BASE_URL}/settings")
    WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((By.ID, "alert-frequency"))
    )
    time.sleep(1)


def get_notification_checkboxes(driver):
    """Return (email_checkbox, sms_checkbox) from the notification section."""
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    return checkboxes[0], checkboxes[1]


def set_toggle(driver, checkbox, desired_state: bool):
    """Set a toggle checkbox to the desired on/off state."""
    current = checkbox.is_selected()
    if current != desired_state:
        driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(0.3)


def save_preferences(driver):
    driver.find_element(By.XPATH, "//button[contains(., 'Save Preferences')]").click()
    WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'preferences saved')]")
        )
    )


class TestTC08005:
    def test_email_only_notifications(self, driver):
        """TC-08-005a: Email ON, SMS OFF, Frequency = Daily → 'Notification preferences saved'."""
        go_to_notifications(driver)

        email_cb, sms_cb = get_notification_checkboxes(driver)
        set_toggle(driver, email_cb, True)
        set_toggle(driver, sms_cb, False)

        Select(driver.find_element(By.ID, "alert-frequency")).select_by_value("daily")

        save_preferences(driver)

        assert "preferences saved" in driver.page_source.lower(), \
            "FAIL: Expected success message 'Notification preferences saved' not displayed."

        print("PASS: Email-only notification preferences saved successfully.")

    def test_sms_only_notifications(self, driver):
        """TC-08-005b: Email OFF, SMS ON, Frequency = Immediate → 'Notification preferences saved'."""
        go_to_notifications(driver)

        email_cb, sms_cb = get_notification_checkboxes(driver)
        set_toggle(driver, email_cb, False)
        set_toggle(driver, sms_cb, True)

        Select(driver.find_element(By.ID, "alert-frequency")).select_by_value("immediate")

        save_preferences(driver)

        assert "preferences saved" in driver.page_source.lower(), \
            "FAIL: Expected success message 'Notification preferences saved' not displayed."

        print("PASS: SMS-only notification preferences saved successfully.")

    def test_both_notifications_enabled(self, driver):
        """TC-08-005c: Email ON, SMS ON, Frequency = Weekly → 'Notification preferences saved'."""
        go_to_notifications(driver)

        email_cb, sms_cb = get_notification_checkboxes(driver)
        set_toggle(driver, email_cb, True)
        set_toggle(driver, sms_cb, True)

        Select(driver.find_element(By.ID, "alert-frequency")).select_by_value("weekly")

        save_preferences(driver)

        assert "preferences saved" in driver.page_source.lower(), \
            "FAIL: Expected success message 'Notification preferences saved' not displayed."

        print("PASS: Both email and SMS notification preferences saved successfully.")

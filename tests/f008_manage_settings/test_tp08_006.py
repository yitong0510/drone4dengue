"""
Test Procedure ID : TP-08-006
Test Case ID      : TC-08-006
Feature           : F008 Manage Settings
Objective         : Verify that the system validates notification preferences and
                    prevents saving invalid configurations.
Preconditions     : Admin logged in. Docker containers running.
Note              : TC-08-006b (no frequency selected) is NOT TESTABLE: the Alert
                    Frequency field is a dropdown that always has a selected value
                    (Immediate/Daily/Weekly). A blank selection state is not possible
                    in the current UI implementation.
Tool              : Selenium
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import login, BASE_URL, WAIT
import time


def get_notification_checkboxes(driver):
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    return checkboxes[0], checkboxes[1]


def set_toggle(driver, checkbox, desired_state: bool):
    current = checkbox.is_selected()
    if current != desired_state:
        driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(0.3)


class TestTC08006:
    def test_both_notifications_disabled(self, driver):
        """TC-08-006a: Email OFF, SMS OFF → expects warning 'At least one notification method must be enabled'."""
        login(driver)
        driver.get(f"{BASE_URL}/settings")
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((By.ID, "alert-frequency"))
        )
        time.sleep(1)

        email_cb, sms_cb = get_notification_checkboxes(driver)
        set_toggle(driver, email_cb, False)
        set_toggle(driver, sms_cb, False)

        driver.find_element(By.XPATH, "//button[contains(., 'Save Preferences')]").click()
        time.sleep(2)

        page_source = driver.page_source
        # TCS expects: warning "At least one notification method must be enabled"
        warning_shown = (
            "at least one" in page_source.lower() or
            "notification method must be enabled" in page_source.lower()
        )
        assert warning_shown, \
            "FAIL: Expected warning 'At least one notification method must be enabled' " \
            "but no such warning was displayed. System saved preferences with both " \
            "notification methods disabled without any validation warning."

    def test_no_frequency_selected(self, driver):
        """TC-08-006b: Email ON, SMS OFF, Frequency = blank → expects error 'Please select'."""
        pytest.skip(
            "NOT TESTABLE: The Alert Frequency field is a dropdown (<select>) that always "
            "has a pre-selected value (Immediate/Daily/Weekly). A blank or empty selection "
            "state is not possible in the current UI — there is no empty option in the list. "
            "TCS expected: error 'Please select'."
        )

"""
Test Procedure ID : TP-08-007
Test Case ID      : TC-08-007
Feature           : F008 Manage Settings
Objective         : Verify that the admin can successfully update system configuration
                    with all valid parameters.
Preconditions     : Admin logged in. Docker containers running.
Note              : TCS specifies numeric inputs: Threshold (0-100), Model Params
                    {"accuracy": 0.95}, Sync Interval (1-1440 minutes). The current UI
                    does NOT use these numeric fields:
                    - Threshold is a radio group: Low / Medium / High
                    - Model Params are individual weight sliders (not a JSON accuracy field)
                    - Sync Mode is a radio: Automatic / Manual (no numeric interval)
                    All three TCS sub-cases (mid-range, minimum, maximum numeric boundaries)
                    are NOT TESTABLE as specified. Test is adapted to verify that the
                    available System Configuration controls can be saved successfully.
Tool              : Selenium
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import login, BASE_URL, WAIT
import time


class TestTC08007:
    def test_mid_range_values(self, driver):
        """TC-08-007a: Threshold=50, Model Params={'accuracy':0.95}, Sync=60 → 'Settings applied successfully'."""
        pytest.skip(
            "NOT TESTABLE: The current UI does not have a numeric Threshold input (0-100). "
            "Threshold is a radio group (Low/Medium/High). Model Params are not a JSON "
            "accuracy field but separate weight sliders. Sync Interval is not a numeric "
            "minutes input but a radio (Automatic/Manual). Numeric range validation cannot "
            "be tested with the current UI controls."
        )

    def test_min_boundaries(self, driver):
        """TC-08-007b: Threshold=0, Model Params={'accuracy':0.0}, Sync=1 → 'Settings applied successfully'."""
        pytest.skip(
            "NOT TESTABLE: Same reason as TC-08-007a. The UI does not have numeric input "
            "fields for Threshold, Model Accuracy, or Sync Interval."
        )

    def test_max_boundaries(self, driver):
        """TC-08-007c: Threshold=100, Model Params={'accuracy':1.0}, Sync=1440 → 'Settings applied successfully'."""
        pytest.skip(
            "NOT TESTABLE: Same reason as TC-08-007a. The UI does not have numeric input "
            "fields for Threshold, Model Accuracy, or Sync Interval."
        )

    def test_valid_system_config_save(self, driver):
        """TC-08-007 Adapted: Verify valid system configuration can be saved using available UI controls."""
        login(driver)
        driver.get(f"{BASE_URL}/settings")
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='threshold']"))
        )
        time.sleep(1)

        # Set Dengue Alert Threshold to Medium (mid-range equivalent)
        medium_radio = driver.find_element(
            By.CSS_SELECTOR, "input[name='threshold'][value='medium']"
        )
        driver.execute_script("arguments[0].click();", medium_radio)

        # Set Sync Mode to Automatic
        auto_radio = driver.find_element(
            By.CSS_SELECTOR, "input[name='sync'][value='automatic']"
        )
        driver.execute_script("arguments[0].click();", auto_radio)

        # Click Apply Settings
        driver.find_element(By.XPATH, "//button[contains(., 'Apply Settings')]").click()

        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'System configuration saved successfully')]")
            )
        )
        assert "System configuration saved successfully" in driver.page_source, \
            "FAIL: Expected success message 'System configuration saved successfully' not displayed."

        print("PASS: System configuration saved successfully using available UI controls. "
              "Note: Numeric threshold/sync interval inputs from TCS are not present in UI.")

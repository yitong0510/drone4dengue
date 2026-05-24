"""
Test Procedure ID : TP-07-003
Test Case ID      : TC-07-003
Feature           : F007 Generate Report
Objective         : Verify "Generate Report" button is disabled when required
                    filters (Start Date, End Date, Location, Data Type per UC-10)
                    are incomplete.
Preconditions     : Admin logged in. Docker containers running.
Note              : UC-10 specifies Location and Data Type as required filter
                    criteria. These fields are absent in the current UI.
                    Tests for missing Location and Data Type filters FAIL
                    as the UI does not implement these UC-10 requirements.
Tool              : Selenium
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import login, set_date, BASE_URL, WAIT


class TestTC07003:
    def test_button_disabled_missing_start_date(self, driver):
        """TC-07-003a: Button disabled when Start Date is empty."""

        # Step 1: Login and navigate to Reports page
        login(driver)
        driver.get(f"{BASE_URL}/reports")
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='date']"))
        )

        # Step 2: Enter only End Date, leave Start Date empty
        date_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='date']")
        set_date(driver, date_inputs[1], "2025-12-31")  # End Date only

        # Step 3: Verify Generate Report button is disabled
        btn = driver.find_element(By.XPATH, "//button[.//span[contains(text(),'Generate Report')]]")
        assert not btn.is_enabled(), \
            "FAIL: Button should be DISABLED when Start Date is missing"

        print("PASS: Button correctly disabled when Start Date is missing")

    def test_button_disabled_missing_end_date(self, driver):
        """TC-07-003b: Button disabled when End Date is empty."""

        # Step 1: Login and navigate to Reports page
        login(driver)
        driver.get(f"{BASE_URL}/reports")
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='date']"))
        )

        # Step 2: Enter only Start Date, leave End Date empty
        date_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='date']")
        set_date(driver, date_inputs[0], "2025-03-20")  # Start Date only

        # Step 3: Verify Generate Report button is disabled
        btn = driver.find_element(By.XPATH, "//button[.//span[contains(text(),'Generate Report')]]")
        assert not btn.is_enabled(), \
            "FAIL: Button should be DISABLED when End Date is missing"

        print("PASS: Button correctly disabled when End Date is missing")

    def test_button_disabled_both_dates_empty(self, driver):
        """TC-07-003c: Button disabled when both Start Date and End Date are empty."""

        # Step 1: Login and navigate to Reports page
        login(driver)
        driver.get(f"{BASE_URL}/reports")
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='date']"))
        )

        # Step 3: Verify Generate Report button is disabled
        btn = driver.find_element(By.XPATH, "//button[.//span[contains(text(),'Generate Report')]]")
        assert not btn.is_enabled(), \
            "FAIL: Button should be DISABLED when both dates are empty"

        print("PASS: Button correctly disabled when both dates are empty")

    def test_button_disabled_missing_location(self, driver):
        """TC-07-003d: Button disabled when Location filter is missing — UC-10 requirement b."""

        login(driver)
        driver.get(f"{BASE_URL}/reports")
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='date']"))
        )

        # UC-10 requires a Location filter. Verify it exists in the UI.
        location_filter = driver.find_elements(
            By.XPATH, "//*[contains(@placeholder,'Location') or contains(@aria-label,'Location') or contains(text(),'Location')]"
        )
        assert len(location_filter) > 0, \
            "FAIL: Location filter is not present in the UI. UC-10 requires Location as a mandatory filter criterion."

        print("PASS: Location filter present in UI")

    def test_button_disabled_missing_data_type(self, driver):
        """TC-07-003e: Button disabled when Data Type filter is missing — UC-10 requirement c."""

        login(driver)
        driver.get(f"{BASE_URL}/reports")
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='date']"))
        )

        # UC-10 requires a Data Type filter (active cases, drone images, predictions).
        datatype_filter = driver.find_elements(
            By.XPATH, "//*[contains(@placeholder,'Data Type') or contains(@aria-label,'Data Type') or contains(text(),'Data Type')]"
        )
        assert len(datatype_filter) > 0, \
            "FAIL: Data Type filter is not present in the UI. UC-10 requires Data Type (active cases, drone images, predictions) as a mandatory filter criterion."

        print("PASS: Data Type filter present in UI")

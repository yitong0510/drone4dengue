"""
Test Procedure ID : TP-07-001
Test Case ID      : TC-07-001
Feature           : F007 Generate Report
Objective         : Verify the system generates a report successfully when
                    all required filters (Start Date, End Date, Location,
                    Data Type) are provided with valid data per UC-10.
Preconditions     : Docker containers running. Admin logged in.
Note              : UC-10 specifies three filter criteria: (a) Start Date and
                    End Date, (b) Location, (c) Data Type. The current UI only
                    provides date inputs — Location and Data Type filters are
                    absent. Test FAILS due to missing UC-10 filter requirements.
Tool              : Selenium
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import login, set_date, BASE_URL, WAIT

START_DATE = "2025-03-20"
END_DATE   = "2025-12-31"


class TestTC07001:
    def test_generate_report_valid_dates(self, driver):
        """TC-07-001: Generate report with valid filters per UC-10 (Start Date, End Date, Location, Data Type)."""

        # Step 1: Login as admin
        login(driver)

        # Step 2: Navigate to Reports page
        driver.get(f"{BASE_URL}/reports")
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='date']"))
        )

        # Step 3: Enter Start Date
        date_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='date']")
        set_date(driver, date_inputs[0], START_DATE)

        # Step 4: Enter End Date
        set_date(driver, date_inputs[1], END_DATE)

        # Step 5: Check Location filter (UC-10 requirement b)
        location_filter = driver.find_elements(
            By.XPATH, "//*[contains(@placeholder,'Location') or contains(@aria-label,'Location') or contains(text(),'Location')]"
        )
        location_missing = len(location_filter) == 0

        # Step 6: Check Data Type filter (UC-10 requirement c)
        datatype_filter = driver.find_elements(
            By.XPATH, "//*[contains(@placeholder,'Data Type') or contains(@aria-label,'Data Type') or contains(text(),'Data Type')]"
        )
        datatype_missing = len(datatype_filter) == 0

        # Step 7: Assert both — collect all failures before stopping
        failures = []
        if location_missing:
            failures.append("Location filter is not present in the UI. UC-10 requires Location as a filter criterion.")
        if datatype_missing:
            failures.append("Data Type filter is not present in the UI. UC-10 requires Data Type (active cases, drone images, predictions) as a filter criterion.")
        assert not failures, "FAIL: " + " | ".join(failures)

        # Step 7: Click "Generate Report"
        btn = driver.find_element(By.XPATH, "//button[.//span[contains(text(),'Generate Report')]]")
        btn.click()

        # Step 8: Wait for report to load and verify report content appears
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'Total Cases') or contains(text(),'Weekly Overview') or contains(text(),'Report')]")
            )
        )

        print("PASS: Report generated successfully with all UC-10 required filters")

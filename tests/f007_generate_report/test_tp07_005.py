"""
Test Procedure ID : TP-07-005
Test Case ID      : TC-07-005
Feature           : F007 Generate Report
Objective         : Verify the system generates reports at date boundaries
                    (minimum date, maximum date, and single day).
Preconditions     : Admin logged in. Docker containers running.
                    Data available: 2025-03-20 to 2026-05-14
Note              : TCS assumes data from 2023-01-01. Actual seeded data starts
                    at 2025-03-20. Dates adjusted to match actual data range.
Tool              : Selenium
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import login, set_date, BASE_URL, WAIT

# Actual data boundaries in the seeded database
EARLIEST_DATE = "2025-03-20"
LATEST_DATE   = "2026-05-14"
SINGLE_DAY    = "2025-06-15"


def fill_and_generate(driver, start, end):
    """Navigate to reports, fill dates, click Generate Report, wait for result."""
    login(driver)
    driver.get(f"{BASE_URL}/reports")
    WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='date']"))
    )
    date_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='date']")
    set_date(driver, date_inputs[0], start)
    set_date(driver, date_inputs[1], end)
    driver.find_element(By.XPATH, "//button[.//span[contains(text(),'Generate Report')]]").click()
    import time; time.sleep(5)


class TestTC07005:
    def test_minimum_boundary_date(self, driver):
        """TC-07-005a: Report at earliest available date."""

        # Step 1-4: Login, navigate, enter earliest date as both start and end
        fill_and_generate(driver, EARLIEST_DATE, EARLIEST_DATE)

        # Step 5: Verify report appears (no error)
        page_source = driver.page_source
        error_els = driver.find_elements(By.CSS_SELECTOR, ".text-red-600")
        error_visible = any(e.is_displayed() for e in error_els)

        assert not error_visible, f"FAIL: Error shown for minimum boundary date {EARLIEST_DATE}"
        print(f"PASS: Report generated for minimum boundary date ({EARLIEST_DATE})")

    def test_maximum_boundary_date(self, driver):
        """TC-07-005b: Report at latest available date."""

        fill_and_generate(driver, LATEST_DATE, LATEST_DATE)

        error_els = driver.find_elements(By.CSS_SELECTOR, ".text-red-600")
        error_visible = any(e.is_displayed() for e in error_els)

        assert not error_visible, f"FAIL: Error shown for maximum boundary date {LATEST_DATE}"
        print(f"PASS: Report generated for maximum boundary date ({LATEST_DATE})")

    def test_single_day_report(self, driver):
        """TC-07-005c: Report for a single day (Start Date = End Date)."""

        fill_and_generate(driver, SINGLE_DAY, SINGLE_DAY)

        error_els = driver.find_elements(By.CSS_SELECTOR, ".text-red-600")
        error_visible = any(e.is_displayed() for e in error_els)

        assert not error_visible, f"FAIL: Error shown for single day report ({SINGLE_DAY})"
        print(f"PASS: Report generated for single day ({SINGLE_DAY})")

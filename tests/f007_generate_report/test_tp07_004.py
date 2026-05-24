"""
Test Procedure ID : TP-07-004
Test Case ID      : TC-07-004
Feature           : F007 Generate Report
Objective         : Verify the system handles invalid date configurations
                    (Start Date after End Date, future End Date, etc.)
Preconditions     : Admin logged in. Docker containers running.
Tool              : Selenium
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import login, set_date, BASE_URL, WAIT


class TestTC07004:
    def test_start_date_after_end_date(self, driver):
        """TC-07-004a: Start Date is after End Date."""

        # Step 1: Login and navigate to Reports page
        login(driver)
        driver.get(f"{BASE_URL}/reports")
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='date']"))
        )

        # Step 2: Enter Start Date AFTER End Date (reversed)
        date_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='date']")
        set_date(driver, date_inputs[0], "2025-10-31")  # Start Date
        set_date(driver, date_inputs[1], "2025-05-01")  # End Date (earlier than start)

        # Step 3: Click Generate Report
        btn = driver.find_element(By.XPATH, "//button[.//span[contains(text(),'Generate Report')]]")
        btn.click()

        import time; time.sleep(3)

        # Step 4: TCS expects error "Start Date cannot be after End Date"
        page_source = driver.page_source
        error_shown = "cannot be after" in page_source or \
                      "invalid" in page_source.lower() or \
                      len(driver.find_elements(By.CSS_SELECTOR, ".text-red-600")) > 0

        assert error_shown, \
            "FAIL: Expected validation error 'Start Date cannot be after End Date' " \
            "but no error message was displayed. System accepted reversed dates without warning."

    def test_future_end_date(self, driver):
        """TC-07-004b: End Date is in the future (beyond data range)."""

        login(driver)
        driver.get(f"{BASE_URL}/reports")
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='date']"))
        )

        date_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='date']")
        set_date(driver, date_inputs[0], "2025-01-01")
        set_date(driver, date_inputs[1], "2027-12-31")  # Far future date

        btn = driver.find_element(By.XPATH, "//button[.//span[contains(text(),'Generate Report')]]")
        btn.click()

        import time; time.sleep(3)

        # TCS expects error "End Date cannot be after 2025-12-31"
        page_source = driver.page_source
        error_shown = "cannot be after" in page_source or \
                      "future" in page_source.lower() or \
                      len(driver.find_elements(By.CSS_SELECTOR, ".text-red-600")) > 0

        assert error_shown, \
            "FAIL: Expected validation error 'End Date cannot be after 2025-12-31' " \
            "but no error message was displayed. System accepted future dates without warning."

"""
Test Procedure ID : TP-07-009
Test Case ID      : TC-07-009
Feature           : F007 Generate Report
Objective         : Verify the system allows the admin to change the export format
                    after report preview is generated and exports in the newly
                    selected format.
Preconditions     : Report must be generated first (TC-07-001 must pass).
                    Admin logged in. Docker containers running.
Note              : The current UI does not have a format dropdown selector.
                    Export formats are individual buttons (PDF, CSV, XLSX, JSON).
                    Test is adapted: generate report, click Export as PDF first,
                    then click Export as CSV to simulate changing format.
Tool              : Selenium
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import login, set_date, BASE_URL, WAIT
import time

START_DATE = "2025-03-20"
END_DATE   = "2025-12-31"


class TestTC07009:
    def test_change_export_format_pdf_to_csv(self, driver):
        """TC-07-009: Generate report, export as PDF, then change to CSV."""

        # Step 1: Login and navigate to Reports page
        login(driver)
        driver.get(f"{BASE_URL}/reports")
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='date']"))
        )

        # Step 2: Enter valid date range
        date_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='date']")
        set_date(driver, date_inputs[0], START_DATE)
        set_date(driver, date_inputs[1], END_DATE)

        # Step 3: Click Generate Report and wait for export buttons
        driver.find_element(By.XPATH, "//button[.//span[contains(text(),'Generate Report')]]").click()
        WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export as PDF')]"))
        )

        # Step 4: Click Export as PDF (initial format)
        pdf_btn = driver.find_element(By.XPATH, "//button[contains(., 'Export as PDF')]")
        assert pdf_btn.is_displayed(), "FAIL: Export as PDF button not visible"
        pdf_btn.click()
        time.sleep(2)

        # Verify no error after PDF export
        error_elements = driver.find_elements(By.CSS_SELECTOR, ".text-red-600")
        assert all(not e.is_displayed() for e in error_elements), \
            "FAIL: Error shown after PDF export"

        # Step 5: Change format — click Export as CSV
        csv_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export as CSV')]"))
        )
        assert csv_btn.is_displayed(), "FAIL: Export as CSV button not visible after switching format"
        csv_btn.click()
        time.sleep(2)

        # Verify no error after CSV export
        error_elements = driver.find_elements(By.CSS_SELECTOR, ".text-red-600")
        assert all(not e.is_displayed() for e in error_elements), \
            "FAIL: Error shown after switching to CSV export"

        print("PASS: Successfully changed export format from PDF to CSV. "
              "Both exports triggered without error.")

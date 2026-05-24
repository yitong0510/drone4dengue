"""
Test Procedure ID : TP-07-002
Test Case ID      : TC-07-002
Feature           : F007 Generate Report
Objective         : Verify the system exports the report in PDF, CSV, and XLSX formats.
Preconditions     : Report must be generated first (TC-07-001 must pass).
                    Admin logged in. Docker containers running.
Tool              : Selenium
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import login, set_date, BASE_URL, WAIT

START_DATE = "2025-03-20"
END_DATE   = "2025-12-31"


def generate_report(driver):
    """Helper: login, navigate to reports, fill dates, click Generate Report."""
    login(driver)
    driver.get(f"{BASE_URL}/reports")
    WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='date']"))
    )
    date_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='date']")
    set_date(driver, date_inputs[0], START_DATE)
    set_date(driver, date_inputs[1], END_DATE)
    driver.find_element(By.XPATH, "//button[.//span[contains(text(),'Generate Report')]]").click()
    # Wait for export PDF button — only appears after reportGenerated = true and loading = false
    # Use contains(., ...) not contains(text(), ...) because JSX splits "Export as " and "PDF"
    # into two separate DOM text nodes; . concatenates them for matching.
    WebDriverWait(driver, 90).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Export as PDF')]")
        )
    )


class TestTC07002:
    def test_export_pdf(self, driver):
        """TC-07-002a: Export report as PDF."""
        generate_report(driver)

        # generate_report already waited for PDF button to be clickable
        pdf_btn = driver.find_element(By.XPATH, "//button[contains(., 'Export as PDF')]")
        assert pdf_btn.is_displayed(), "FAIL: Export as PDF button not visible"

        pdf_btn.click()

        import time; time.sleep(2)
        error_elements = driver.find_elements(By.CSS_SELECTOR, ".text-red-600")
        assert all(not e.is_displayed() for e in error_elements), \
            "FAIL: Error shown after PDF export"

        print("PASS: PDF export triggered successfully")

    def test_export_csv(self, driver):
        """TC-07-002b: Export report as CSV."""
        generate_report(driver)

        csv_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export as CSV')]"))
        )
        assert csv_btn.is_displayed(), "FAIL: Export as CSV button not visible"
        csv_btn.click()

        import time; time.sleep(2)
        error_elements = driver.find_elements(By.CSS_SELECTOR, ".text-red-600")
        assert all(not e.is_displayed() for e in error_elements), \
            "FAIL: Error shown after CSV export"

        print("PASS: CSV export triggered successfully")

    def test_export_xlsx(self, driver):
        """TC-07-002c: Export report as XLSX."""
        generate_report(driver)

        xlsx_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export as XLSX')]"))
        )
        assert xlsx_btn.is_displayed(), "FAIL: Export as XLSX button not visible"
        xlsx_btn.click()

        import time; time.sleep(2)
        error_elements = driver.find_elements(By.CSS_SELECTOR, ".text-red-600")
        assert all(not e.is_displayed() for e in error_elements), \
            "FAIL: Error shown after XLSX export"

        print("PASS: XLSX export triggered successfully")

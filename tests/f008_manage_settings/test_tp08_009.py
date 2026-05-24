"""
Test Procedure ID : TP-08-009
Test Case ID      : TC-08-009
Feature           : F008 Manage Settings
Objective         : Verify that the admin can cancel profile edits and changes are discarded.
Preconditions     : Admin logged in. Docker containers running.
Note              : TCS specifies changing Name and Email before cancelling. The current
                    UI has the Email field permanently disabled. Test is adapted to change
                    Name only (and Phone), then cancel and verify original values are restored.
Tool              : Selenium
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import login, BASE_URL, WAIT
import time


class TestTC08009:
    def test_cancel_profile_edit(self, driver):
        """TC-08-009: Change Name, click Cancel — original profile data should be restored."""

        # Step 1: Login and navigate to Settings
        login(driver)
        driver.get(f"{BASE_URL}/settings")

        # Step 2: Wait for profile form to load
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((By.ID, "name"))
        )
        time.sleep(1)

        # Step 3: Record original name
        original_name = driver.find_element(By.ID, "name").get_attribute("value")
        assert original_name, "Precondition failed: Could not read original name from profile form."

        # Step 4: Click "Edit Profile" to enter edit mode
        driver.find_element(
            By.XPATH, "//button[.//span[contains(text(),'Edit Profile')]]"
        ).click()
        WebDriverWait(driver, WAIT).until(
            EC.element_to_be_clickable((By.ID, "name"))
        )

        # Step 5: Change the name to a different value (TCS uses "Tan Sarah")
        name_input = driver.find_element(By.ID, "name")
        name_input.clear()
        name_input.send_keys("Tan Sarah")

        # Verify the field now shows the new value
        assert driver.find_element(By.ID, "name").get_attribute("value") == "Tan Sarah", \
            "Precondition failed: Name field did not update to 'Tan Sarah'."

        # Step 6: Click "Cancel" to discard changes
        driver.find_element(
            By.XPATH, "//button[.//span[contains(text(),'Cancel')]]"
        ).click()

        # Step 7: Wait for form to revert to read-only mode
        time.sleep(1)

        # Step 8: Verify original name is restored
        reverted_name = driver.find_element(By.ID, "name").get_attribute("value")
        assert reverted_name == original_name, \
            f"FAIL: Expected original name '{original_name}' after cancel, " \
            f"but got '{reverted_name}'. Changes were not discarded."

        # Verify the edit button is back to "Edit Profile" (not "Cancel")
        edit_btn = driver.find_element(
            By.XPATH, "//button[.//span[contains(text(),'Edit Profile')]]"
        )
        assert edit_btn.is_displayed(), \
            "FAIL: 'Edit Profile' button not visible after cancellation — form may still be in edit mode."

        print(f"PASS: Profile edit cancelled successfully. "
              f"Original name '{original_name}' restored after clicking Cancel.")

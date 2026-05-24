"""
Test Procedure ID : TP-07-008
Test Case ID      : TC-07-008
Feature           : F007 Generate Report
Objective         : Verify the system validates export format and handles invalid
                    format selections.
Preconditions     : Admin logged in. Docker containers running.
Note              : The current UI does NOT have a free-form export format selector.
                    Export options are presented as 4 fixed buttons:
                    PDF, CSV, XLSX, JSON. There is no input field where an
                    unsupported format like "JPEG" can be entered, and no blank
                    selection is possible. TC-07-008 cannot be executed as specified.
                    Tests are marked as skipped with reason documented below.
Tool              : Selenium
"""
import pytest
from tests.conftest import login, BASE_URL, WAIT


class TestTC07008:
    def test_unsupported_export_format(self, driver):
        """TC-07-008a: Export Format = 'JPEG' (unsupported)."""
        pytest.skip(
            "NOT TESTABLE: The current UI does not have a free-form export format "
            "selector. Export options are fixed buttons (PDF, CSV, XLSX, JSON). "
            "There is no way to input an unsupported format such as 'JPEG'. "
            "TCS expected: error 'Unsupported export format'."
        )

    def test_no_format_selected(self, driver):
        """TC-07-008b: Export Format = blank (no format selected)."""
        pytest.skip(
            "NOT TESTABLE: The current UI does not have a format dropdown that can "
            "be left blank. Export options are fixed buttons (PDF, CSV, XLSX, JSON). "
            "A blank selection state is not possible in the current implementation. "
            "TCS expected: prompt 'Please select an export format'."
        )

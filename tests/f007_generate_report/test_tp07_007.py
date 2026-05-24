"""
Test Procedure ID : TP-07-007
Test Case ID      : TC-07-007
Feature           : F007 Generate Report
Objective         : Verify the system validates and rejects unsupported data types.
Preconditions     : Admin logged in. Docker containers running.
Note              : Data Type filter is NOT implemented in the current UI.
                    The Reports page only provides Start Date and End Date inputs.
                    TC-07-007 cannot be executed as specified in the TCS.
                    Test is marked as skipped with reason documented below.
Tool              : Selenium
"""
import pytest
from tests.conftest import login, BASE_URL, WAIT


class TestTC07007:
    def test_unsupported_data_type(self, driver):
        """TC-07-007: Data Type = 'Drone model' (unsupported)."""
        pytest.skip(
            "NOT TESTABLE: Data Type filter is not implemented in the current UI. "
            "The Reports page only provides Start Date and End Date inputs. "
            "No data type selector exists to enter 'Drone model'. "
            "TCS expected: error 'Unsupported data type selected'."
        )

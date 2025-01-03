from unittest.mock import Mock, patch

import pytest

from src.monitoring.alert_manager import AlertManager


class TestAlertManager:
    @pytest.fixture
    def manager(self):
        return AlertManager()

    @patch("github.Github")
    def test_check_repository(self, mock_github):
# mock_repo
        mock_repo.name = "test-repo"
        mock_repo.get_issues().totalCount = 15  # Above threshold
        mock_repo.get_pulls().totalCount = 3  # Below threshold

# manager
# alerts

        assert len(alerts) == 1
        assert alerts[0]["type"] == "high_issues"

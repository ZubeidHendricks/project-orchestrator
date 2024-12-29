from unittest.mock import Mock, patch

import pytest

from src.workflows.status_updater import StatusUpdater


class TestStatusUpdater:
    @pytest.fixture
    def updater(self):
        return StatusUpdater()

    @patch("github.Github")
    def test_analyze_repository(self, mock_github):
# mock_repo
        mock_repo.get_issues().totalCount = 5
        mock_repo.get_pulls().totalCount = 2
        mock_repo.get_commits().totalCount = 10

# updater
# result

        assert "open_issues" in result
        assert "open_prs" in result
        assert "last_commit" in result

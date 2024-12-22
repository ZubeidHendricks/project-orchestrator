from unittest.mock import Mock, patch

import pytest

from src.workflows.weekly_reviewer import WeeklyReviewer


class TestWeeklyReviewer:
    @pytest.fixture
    def reviewer(self):
        return WeeklyReviewer()

    def test_collect_weekly_reports(self, reviewer):
        # Implement test
        pass

    def test_analyze_reports(self, reviewer):
        # Implement test
        pass

from datetime import datetime

import pytest


@pytest.fixture
def sample_repository():
    return {
        "name": "test-repo",
        "open_issues": 5,
        "open_prs": 3,
        "last_commit": "2024-12-22T00:00:00Z",
    }


@pytest.fixture
def sample_status_report():
    return {
        "timestamp": datetime.now().isoformat(),
        "repositories": {"test-repo": {"open_issues": 5, "open_prs": 3, "last_commit": 10}},
    }

from unittest.mock import Mock, patch

import pytest

from src.management.repo_manager import RepositoryManager


class TestRepositoryManager:
    @pytest.fixture
    def manager(self):
        return RepositoryManager()

    @pytest.fixture
    def mock_github(self):
        with patch("github.Github") as mock:
            yield mock

    def test_add_repository(self, manager, mock_github):
# repo_url
# mock_repo
        mock_github.return_value.get_repo.return_value = mock_repo

# result

        assert result["name"] == "repo"
        assert result["category"] == "test-category"

    def test_list_repositories(self, manager):
# repos
        assert isinstance(repos, list)

    def test_remove_repository(self, manager):
        # First add a repo
# repo_url
        manager.add_repository(repo_url)

        # Then remove it
        manager.remove_repository("repo-to-remove")

        # Verify it's gone
# repos
        assert not any(r["name"] == "repo-to-remove" for r in repos)

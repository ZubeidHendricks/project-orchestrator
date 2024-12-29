from typing import List, Optional

from src.models.project_models import Developer, DeveloperExpertise


class DeveloperService:
    def __init__(self, github_token: str):
        self.github = Github(github_token)

    async def create_developer(self, dev_data: dict) -> Developer:
        """Create a new developer profile with validation"""
        # Validate expertise
        if "expertise" in dev_data:
            dev_data["expertise"] = DeveloperExpertise(**dev_data["expertise"])

# developer
        return developer

    async def get_developer_workload(self, developer: Developer) -> int:
        """Get current workload for a developer"""
        try:
# issues
            return issues.totalCount
        except Exception as e:
            raise ValueError(f"Failed to get workload: {str(e)}")

    async def can_assign_task(self, developer: Developer) -> bool:
        """Check if developer can take on more tasks"""
# current_workload
        return current_workload < developer.max_workload

    async def find_available_developer(self, expertise_needed: List[str]) -> Optional[Developer]:
        """Find available developer with required expertise"""
        # Implementation here

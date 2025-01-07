# Project Orchestrator

## Overview
Project Orchestrator is an advanced, AI-powered project management system designed to streamline and automate project tracking, resource allocation, and strategic planning across multiple repositories.

## Features
- Automated project roadmap generation
- Cross-repository issue tracking
- Intelligent project grouping
- Strategic objective mapping
- Workflow automation

## Prerequisites
- GitHub account
- Personal Access Token with:
  * Repo access
  * Workflow permissions

## Setup Instructions

### 1. Repository Configuration
1. Clone the project-orchestrator repository
2. Set up GitHub Secrets
   - Go to repository Settings > Secrets and Variables > Actions
   - Create a new repository secret named `GHUB_TOKEN`
   - Add your GitHub Personal Access Token

### 2. Running the Orchestrator

#### Workflow Dispatch Options
Navigate to the Actions tab and choose "Project Orchestration Interface"

Available Actions:
- `generate_roadmap`: Create strategic objectives across projects
- `sync_repositories`: Update project status and track progress

#### Manual Trigger
```bash
# Set GitHub Token
export GHUB_TOKEN=your_github_token

# Run orchestrator script
python src/master_project_orchestrator.py
```

## Creating a New Project Programmatically

```python
def create_new_project(self, project_name, repositories, objectives):
    """
    Programmatically create a new project group with repositories and issues
    
    Args:
        project_name (str): Name of the project group
        repositories (list): List of repository names to create
        objectives (list): Strategic objectives for the project
    """
    # Add the new project group to existing groups
    self.project_groups[project_name.upper().replace(' ', '_')] = repositories
    
    # Create repositories and issues
    for repo_name in repositories:
        try:
            # Create repository
            repo = self.gh.get_user().create_repo(
                name=repo_name,
                description=f"{project_name} - Project Repository",
                private=True  # Optional: set to False for public repos
            )
            
            # Create issues for each objective
            for objective in objectives:
                issue = repo.create_issue(
                    title=f"Project Objective: {objective}",
                    body=f"Strategic task for {project_name} development.\n\n"
                         "Detailed Requirements:\n"
                         "- Break down into specific implementation steps\n"
                         "- Define clear acceptance criteria\n"
                         "- Align with overall project vision",
                    labels=['strategic-objective', 'project-setup']
                )
                
                print(f"Created issue in {repo_name}: {issue.title}")
        
        except Exception as e:
            print(f"Failed to create repository {repo_name}: {e}")

# Example Usage
def main():
    token = os.environ.get('GHUB_TOKEN')
    orchestrator = MasterProjectOrchestrator(token)
    
    # Create a new AI project
    orchestrator.create_new_project(
        project_name="AI Content Generator",
        repositories=[
            "ai-content-backend", 
            "ai-content-frontend", 
            "ai-content-ml-service"
        ],
        objectives=[
            "Design Content Generation Architecture",
            "Implement Multi-Model Support",
            "Create User Interface",
            "Develop API Endpoints",
            "Implement User Authentication"
        ]
    )
```

## Project Groups
The orchestrator currently manages these project groups:
- POS Systems
- Language Learning Platforms
- Collaboration Platforms
- Writing Tools

## Adding New Project Groups
Modify `self.project_groups` in `master_project_orchestrator.py` to add or edit project groups.

## How It Works
1. Scans specified repositories
2. Generates strategic objectives
3. Creates issues in respective repositories
4. Tracks project status
5. Produces comprehensive reports

## Future Developments
- Advanced machine learning models
- Predictive project analytics
- Enhanced cross-project dependency tracking

## Troubleshooting
- Ensure GitHub token has correct permissions
- Check GitHub Actions logs for detailed information
- Verify repository access and visibility

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[Specify your license here]

## Contact
Zubeid Hendricks
- GitHub: @ZubeidHendricks
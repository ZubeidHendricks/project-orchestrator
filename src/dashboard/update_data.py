#!/usr/bin/env python3
import os
import json
from datetime import datetime
from github import Github
import networkx as nx

class CrossRepositoryOrchestrator:
    def __init__(self, token):
        self.gh = Github(token)
        self.repositories = [
            'project-orchestrator',
            'ai-dev-orchestrator'
        ]
    
    def build_dependency_graph(self):
        """Create a dependency network between repositories"""
        G = nx.DiGraph()
        
        for repo_name in self.repositories:
            try:
                repo = self.gh.get_repo(f'ZubeidHendricks/{repo_name}')
                
                # Add repository as a node
                G.add_node(repo_name, 
                           total_issues=repo.get_issues().totalCount,
                           open_issues=repo.get_issues(state='open').totalCount,
                           last_updated=repo.updated_at.isoformat())
                
                # Analyze inter-repository references
                for issue in repo.get_issues(state='open'):
                    # Check for cross-repository references in issue body
                    for other_repo in self.repositories:
                        if other_repo in (issue.body or ''):
                            G.add_edge(repo_name, other_repo)
            
            except Exception as e:
                print(f"Error processing repository {repo_name}: {e}")
        
        return G
    
    def generate_repository_insights(self):
        """Generate comprehensive repository insights"""
        dependency_graph = self.build_dependency_graph()
        
        insights = {
            'timestamp': datetime.now().isoformat(),
            'repositories': {},
            'dependencies': list(dependency_graph.edges())
        }
        
        for repo in self.repositories:
            try:
                repo_data = self.gh.get_repo(f'ZubeidHendricks/{repo}')
                
                insights['repositories'][repo] = {
                    'total_issues': repo_data.get_issues().totalCount,
                    'open_issues': repo_data.get_issues(state='open').totalCount,
                    'last_updated': repo_data.updated_at.isoformat()
                }
            
            except Exception as e:
                print(f"Error generating insights for {repo}: {e}")
        
        # Save insights
        os.makedirs('data', exist_ok=True)
        with open('data/repository_insights.json', 'w') as f:
            json.dump(insights, f, indent=2)
        
        return insights

def main():
    token = os.environ.get('GHUB_TOKEN')
    if not token:
        print("GitHub token not found. Set GHUB_TOKEN environment variable.")
        return
    
    try:
        orchestrator = CrossRepositoryOrchestrator(token)
        insights = orchestrator.generate_repository_insights()
        print("Repository insights generated successfully")
    except Exception as e:
        print(f"Error in repository orchestration: {e}")

if __name__ == '__main__':
    main()
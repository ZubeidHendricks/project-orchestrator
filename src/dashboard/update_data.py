#!/usr/bin/env python3
import os
import json
from datetime import datetime
from github import Github
import networkx as nx

class CrossRepositoryOrchestrator:
    def __init__(self, token):
        try:
            self.gh = Github(token)
            self.repositories = [
                'ZubeidHendricks/project-orchestrator',
                'ZubeidHendricks/ai-dev-orchestrator'
            ]
        except Exception as e:
            print(f"Initialization error: {e}")
            raise
    
    def build_dependency_graph(self):
        """Create a dependency network between repositories"""
        try:
            G = nx.DiGraph()
            
            for repo_name in self.repositories:
                repo = self.gh.get_repo(repo_name)
                G.add_node(repo_name, 
                           total_issues=repo.get_issues().totalCount,
                           open_issues=repo.get_issues(state='open').totalCount,
                           last_updated=repo.updated_at.isoformat())
                
                # Analyze inter-repository references
                for issue in repo.get_issues(state='open'):
                    # Check for cross-repository references in issue body
                    for ref_repo in self.repositories:
                        if ref_repo in (issue.body or ''):
                            G.add_edge(repo_name, ref_repo, 
                                       issue_number=issue.number, 
                                       reference_type='issue_link')
            
            return G
        except Exception as e:
            print(f"Graph building error: {e}")
            return nx.DiGraph()
    
    def generate_project_health_report(self):
        """Generate comprehensive project health insights"""
        try:
            dependency_graph = self.build_dependency_graph()
            
            health_report = {
                'timestamp': datetime.now().isoformat(),
                'repositories': {},
                'cross_repo_dependencies': []
            }
            
            # Repository-level insights
            for repo_name in self.repositories:
                try:
                    repo_data = dependency_graph.nodes[repo_name]
                    health_report['repositories'][repo_name] = {
                        'total_issues': repo_data.get('total_issues', 0),
                        'open_issues': repo_data.get('open_issues', 0),
                        'last_updated': repo_data.get('last_updated', 'N/A')
                    }
                except Exception as e:
                    print(f"Error processing {repo_name}: {e}")
            
            # Cross-repository dependency insights
            for edge in dependency_graph.edges(data=True):
                health_report['cross_repo_dependencies'].append({
                    'source': edge[0],
                    'target': edge[1],
                    'issue_number': edge[2].get('issue_number', 'N/A')
                })
            
            # Save insights
            os.makedirs('data', exist_ok=True)
            with open('data/cross_repo_health.json', 'w') as f:
                json.dump(health_report, f, indent=2)
            
            return health_report
        except Exception as e:
            print(f"Health report generation error: {e}")
            return {}

def main():
    token = os.environ.get('GHUB_TOKEN')
    try:
        orchestrator = CrossRepositoryOrchestrator(token)
        health_report = orchestrator.generate_project_health_report()
        print("Cross-Repository Health Report Generated Successfully")
    except Exception as e:
        print(f"Main execution error: {e}")

if __name__ == '__main__':
    main()
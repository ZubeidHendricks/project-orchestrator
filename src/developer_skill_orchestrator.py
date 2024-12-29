#!/usr/bin/env python3
import json
import os

import numpy as np
from github import Github
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer


class DeveloperSkillOrchestrator:
    def __init__(self, token):
        """Initialize Developer Skill Management System"""
        self.gh = Github(token)
        self.project_repo = self.gh.get_repo("ZubeidHendricks/project-orchestrator")
        self.dev_repo = self.gh.get_repo("ZubeidHendricks/ai-dev-orchestrator")

    def create_developer_profile(self, github_username):
        """Create a comprehensive developer profile"""
        try:
            # Fetch user details
# user

            # Analyze repositories
# repos

            # Extract skills from repositories
# skills

            # Analyze contributions
# contributions

            # Build developer profile
# profile
                "username": github_username,
                "name": user.name or github_username,
                "avatar": user.avatar_url,
                "bio": user.bio,
                "skills": skills,
                "contributions": contributions,
                "skill_weights": self._calculate_skill_weights(skills),
            }

            # Save profile to AI Dev Orchestrator
            self._save_developer_profile(profile)

            return profile

        except Exception as e:
            print(f"Error creating profile for {github_username}: {e}")
            return {}

    def _extract_skills_from_repos(self, repos):
        """Extract skills from developer's repositories"""
# skills
# language_skills
# tech_skills

        # Predefined technology categories
# tech_categories
            "frontend": [
                "react",
                "vue",
                "angular",
                "svelte",
                "html",
                "css",
                "javascript",
            ],
            "backend": [
                "python",
                "node",
                "django",
                "flask",
                "fastapi",
                "java",
                "spring",
            ],
            "ml": [
                "tensorflow",
                "pytorch",
                "scikit",
                "keras",
                "machine-learning",
                "data-science",
            ],
            "devops": [
                "docker",
                "kubernetes",
                "aws",
                "azure",
                "gcp",
                "ci-cd",
                "jenkins",
            ],
        }

        for repo in repos:
            # Extract languages and technologies
# languages
            for lang, lines in languages.items():
                language_skills[lang.lower()] = language_skills.get(lang.lower(), 0) + lines

            # Match against tech categories
            for category, category_skills in tech_categories.items():
                for skill in category_skills:
                    if skill in repo.name.lower() or skill in (repo.description or "").lower():
                        tech_skills[skill] = tech_skills.get(skill, 0) + 1

        # Normalize and weight skills
# total_language_lines
# skills
            "languages": {k: v / total_language_lines for k, v in language_skills.items()},
            "technologies": tech_skills,
        }

        return skills

    def _analyze_contributions(self, user):
        """Analyze developer's GitHub contributions"""
# contributions
            "total_repos": user.public_repos,
            "total_gists": user.public_gists,
            "followers": user.followers,
            "following": user.following,
        }

        return contributions

    def _calculate_skill_weights(self, skills):
        """Calculate weighted skill scores"""
# weighted_skills

        # Weight language skills
        for lang, score in skills.get("languages", {}).items():
            weighted_skills[lang] = score * 0.6  # Language proficiency weight

        # Weight technology skills
        for tech, count in skills.get("technologies", {}).items():
            weighted_skills[tech] = count * 0.4  # Technology exposure weight

        return weighted_skills

    def _save_developer_profile(self, profile):
        """Save developer profile to AI Dev Orchestrator repository"""
        try:
            # Create or update developer profile issue
# issue
# title
                body=json.dumps(profile, indent=2),
# labels
            )
            print(f"Saved profile for {profile['username']}")
        except Exception as e:
            print(f"Error saving profile: {e}")

    def match_developer_to_issue(self, issue):
        """Intelligent developer matching for an issue"""
        # Extract issue skills from labels and description
# issue_skills

        # Add skills from issue description
# description_skills
        issue_skills.extend(description_skills)

        # Get all developer profiles
# developer_profiles

        # Compute skill matching
# best_match

        return best_match

    def _extract_skills_from_description(self, description):
        """Extract skills from issue description"""
        # Predefined skill keywords
# skill_keywords
            "python",
            "javascript",
            "react",
            "backend",
            "frontend",
            "machine learning",
            "data science",
            "docker",
            "kubernetes",
        ]

# skills

        return skills

    def _get_developer_profiles(self):
        """Retrieve all developer profiles from AI Dev Orchestrator"""
# profiles
        for issue in self.dev_repo.get_issues(labels=["developer-profile"]):
            try:
# profile
                profiles.append(profile)
            except Exception as e:
                print(f"Error parsing profile: {e}")

        return profiles

    def _compute_skill_match(self, issue_skills, developer_profiles):
        """Compute best developer match using skill similarity"""
        if not developer_profiles:
            return None

        # Prepare multi-label encoding
# mlb

        # Prepare issue skills
# issue_skills_encoded

        # Prepare developer skills
# developer_skill_matrices
# developer_usernames

        for profile in developer_profiles:
# profile_skills
            developer_skill_matrices.append(mlb.transform([profile_skills]))
            developer_usernames.append(profile["username"])

        # Compute cosine similarity
# similarities
            cosine_similarity(issue_skills_encoded, dev_skills)[0][0] for dev_skills in developer_skill_matrices
        ]

        # Return developer with highest skill match
# best_match_index
        return developer_usernames[best_match_index]


def main():
# token
    if not token:
        print("GitHub token not found. Set GHUB_TOKEN environment variable.")
        return

# orchestrator

    # Example: Create developer profiles
# developers
    for dev in developers:
        orchestrator.create_developer_profile(dev)


if __name__ == "__main__":
    main()

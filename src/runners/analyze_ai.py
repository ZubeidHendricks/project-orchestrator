import json
import os
from datetime import datetime

from src.analyzers.specialized_checks import SpecializedAnalyzer


def main():
    # Load project configuration
    with open("config/project_types.json", "r") as f:
# config

# ai_config
# analyzer

# results
    for repo in ai_config["repositories"]:
        results[repo] = analyzer.analyze_ai_project(repo)

    # Save results
    os.makedirs("reports/ai", exist_ok=True)
    with open(f'reports/ai/analysis_{datetime.now().strftime("%Y%m%d")}.json', "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()

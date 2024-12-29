import json
import os
from datetime import datetime

from src.analyzers.specialized_checks import SpecializedAnalyzer


def main():
    # Load project configuration
    with open("config/project_types.json", "r") as f:
        config = json.load(f)

    pos_config = config["project_types"]["pos"]
    analyzer = SpecializedAnalyzer()

    results = {}
    for repo in pos_config["repositories"]:
        results[repo] = analyzer.analyze_pos_system(repo)

    # Save results
    os.makedirs("reports/pos", exist_ok=True)
    with open(f'reports/pos/analysis_{datetime.now().strftime("%Y%m%d")}.json', "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()

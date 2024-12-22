import json
import os
from datetime import datetime

from src.analyzers.specialized_checks import SpecializedAnalyzer


def main():
    # Load project configuration
    with open("config/project_types.json", "r") as f:
        config = json.load(f)

    blockchain_config = config["project_types"]["blockchain"]
    analyzer = SpecializedAnalyzer()

    results = {}
    for repo in blockchain_config["repositories"]:
        results[repo] = analyzer.analyze_blockchain_project(repo)

    # Save results
    os.makedirs("reports/blockchain", exist_ok=True)
    with open(
        f'reports/blockchain/analysis_{datetime.now().strftime("%Y%m%d")}.json', "w"
    ) as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
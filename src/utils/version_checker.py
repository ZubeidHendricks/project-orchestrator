import logging
import sys
from typing import Dict, List, Optional

import pkg_resources


class VersionChecker:
    def __init__(self):
        self.required_versions = {
            "python": "3.10",
            "crewai": "0.1.25",
            "langchain": "0.0.325",
            "pydantic": "2.0.0",
            "typeguard": "4.0.0",
        }
        self.logger = logging.getLogger(__name__)

    def check_python_version(self) -> bool:
        """Check if Python version meets requirements"""
        current_version = sys.version_info
        required_version = tuple(map(int, self.required_versions["python"].split(".")))

        if current_version < required_version:
            self.logger.error(
                f"Python version {'.'.join(map(str, current_version))} is not supported. "
                f"Please use Python {self.required_versions['python']} or higher."
            )
            return False
        return True

    def check_package_versions(self) -> Dict[str, bool]:
        """Check if installed packages meet version requirements"""
        results = {}
        for package, required_version in self.required_versions.items():
            if package == "python":
                continue

            try:
                installed_version = pkg_resources.get_distribution(package).version
                meets_requirement = pkg_resources.parse_version(installed_version) >= pkg_resources.parse_version(
                    required_version
                )
                results[package] = meets_requirement

                if not meets_requirement:
                    self.logger.error(
                        f"{package} version {installed_version} is not supported. "
                        f"Please use version {required_version} or higher."
                    )
            except pkg_resources.DistributionNotFound:
                self.logger.error(f"{package} is not installed.")
                results[package] = False

        return results

    def get_upgrade_commands(self, failed_checks: Dict[str, bool]) -> List[str]:
        """Generate pip commands to upgrade packages that failed version checks"""
        commands = []
        for package, passed in failed_checks.items():
            if not passed:
                version = self.required_versions[package]
                commands.append(f"pip install {package}>={version}")
        return commands

    def verify_environment(self) -> bool:
        """Verify entire environment meets requirements"""
        self.logger.info("Checking environment compatibility...")

        # Check Python version
        python_ok = self.check_python_version()
        if not python_ok:
            return False

        # Check package versions
        package_checks = self.check_package_versions()
        all_packages_ok = all(package_checks.values())

        if not all_packages_ok:
            self.logger.error("Some dependencies need to be upgraded.")
            upgrade_commands = self.get_upgrade_commands(package_checks)
            self.logger.info("Run the following commands to upgrade:")
            for cmd in upgrade_commands:
                self.logger.info(cmd)
            return False

        self.logger.info("Environment check passed!")
        return True

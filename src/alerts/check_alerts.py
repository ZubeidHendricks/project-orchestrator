#!/usr/bin/env python3
import logging
import os
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from src.alerts.alert_manager import AlertManager


def setup_logging():
    """Configure logging for the script."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(os.path.join(project_root, "logs", "check_alerts.log")),
        ],
    )
    return logging.getLogger(__name__)


def main():
    # Setup logging
    logger = setup_logging()

    try:
        # Ensure logs directory exists
        os.makedirs(os.path.join(project_root, "logs"), exist_ok=True)

        # Ensure alerts directory exists
        os.makedirs(os.path.join(project_root, "alerts"), exist_ok=True)

        # Initialize and run alert manager
        logger.info("Initializing Alert Manager")
        alert_manager = AlertManager()

        logger.info("Checking all projects for alerts")
        alert_manager.check_all_projects()

        logger.info("Alert check completed successfully")
        return 0

    except Exception as e:
        logger.error(f"An error occurred during alert check: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())

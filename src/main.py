from config.config import PROJECT_NAME
from src.utils.file_utils import prepare_project_directories
from src.utils.logging_utils import setup_logger


def main() -> None:
    """Initialize the OnboardIQ data workflow foundation."""

    logger = setup_logger()

    logger.info("Starting %s data workflow", PROJECT_NAME)

    prepare_project_directories()

    logger.info("Project directories prepared")
    logger.info("Data workflow foundation initialized")


if __name__ == "__main__":
    main()
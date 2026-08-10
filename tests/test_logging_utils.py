from src.utils.logging_utils import setup_logger


def test_logger_initializes():
    logger = setup_logger("test_logger")

    assert logger.name == "test_logger"
    assert logger.level != 0
    assert len(logger.handlers) >= 2
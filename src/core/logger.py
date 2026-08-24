import sys
from pathlib import Path

from loguru import logger

from config.settings import get_settings

_CONFIGURED = False

LOG_DIR = Path(__file__).resolve().parents[2] / "logs"
LOG_DIR.mkdir(exist_ok=True)


def _configure() -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return

    settings = get_settings()

    logger.remove()  # default handler'ı kaldır

    logger.add(
        sys.stderr,
        level=settings.log_level,
        colorize=True,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
    )

    logger.add(
        LOG_DIR / "app.log",
        level=settings.log_level,
        rotation="5 MB",
        retention=5,
        compression="zip",
        enqueue=True,
        backtrace=False,
        diagnose=False,
    )

    _CONFIGURED = True

def get_logger(name: str):
    _configure()
    return logger.bind(module=name)

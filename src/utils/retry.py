from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.core.logger import get_logger

logger = get_logger(__name__)

def with_retry(exception_types: tuple = (Exception,), attempts: int = 3):
    def _before_sleep(retry_state):
        logger.warning(
            "Yeniden deneniyor (attempt {}): {}".format(
                retry_state.attempt_number, retry_state.outcome.exception()
            )
        )

    return retry(
        reraise=True,
        stop=stop_after_attempt(attempts),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        retry=retry_if_exception_type(exception_types),
        before_sleep=_before_sleep,
    )

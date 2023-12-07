import structlog
from enum import Enum
from typing import Any, MutableMapping


class LogLevel(Enum):
    INFO = "info"
    DEBUG = "debug"
    ERROR = "error"


class LoggingHandler:
    def __init__(self) -> None:
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso", key="@t"),
                structlog.stdlib.add_log_level,
                self.customize_log,
                structlog.processors.EventRenamer("@m"),
                structlog.processors.JSONRenderer(),
            ]
        )
        self.set_logger()

    def set_logger(self) -> None:
        self.__logger = structlog.getLogger()

    def get_logger(self) -> Any:
        return self.__logger

    def customize_log(
        self, logger: Any, log_method: str, event_dict: MutableMapping[str, Any]
    ) -> MutableMapping[str, Any]:
        """Set the log level in a clean format. All the parameters are required."""

        # This part matches the log level with the Enum and assigns it.
        log_level = LogLevel[event_dict["level"].upper()].value
        event_dict["@l"] = log_level

        # If there's an exception, we log it under "@x"
        if "exception" in event_dict:
            event_dict["@x"] = event_dict["exception"]
            event_dict.pop("exception", None)

        # Remove unnecessary keys
        event_dict.pop("level", None)
        event_dict.pop("request_data", None)
        event_dict.pop("error_headers", None)
        event_dict.pop("request_processing_delay", None)

        return event_dict


logging_handler = LoggingHandler()
logger = logging_handler.get_logger()

from enum import Enum

class LogMessageType(Enum):
    """
    The supported types of log messages for the gui logger.
    """
    INFO = "[INFO]"
    ERROR = "[ERROR]"
    SUCCESS = "[SUCCESS]"
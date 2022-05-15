import enum
from logging import CRITICAL

class ImportanceLevel(enum.Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3
    VULNERABLE=4
    MEDIUM=5
    CRITICAL=6
    HIGH=7
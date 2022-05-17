import enum
from logging import CRITICAL

class ImportanceLevel(enum.Enum):
    LOW=0
    INFO = 1
    WARNING = 2
    ERROR = 3
    VULNERABLE=4
    MEDIUM=5
    CRITICAL=6
    HIGH=7

# Working mode indicates 
class WorkingMode(enum.IntEnum):
    Aggresive=1
    Moderate=2
    Stealth=4
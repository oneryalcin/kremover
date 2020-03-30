# All constants and referece to files are defined here
from pathlib import Path

cur_dir = Path(__file__).parent

# Different clients may have different retention periods
# Default is 30 Days
RETENTION_DAYS_DEFAULT = 30

# Clients with non default retention period are defined in this file
RETENTION_CLIENTS_FILE = cur_dir / "retentions" / "retentions.json"

# TEXT PARSERS
# Directory parser is a Text Finite State Machine to identify
# correct data directories conforming to the format

KENTIK_DIR_FORMAT_TEMPLATE = cur_dir / 'validators' / 'kentik_dir_format'


# Logging format
LOGGING_FORMAT = '%(asctime)s %(process)d %(name)s %(levelname)s: %(message)s'
# LOGGING_FORMAT = "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s"

# All constants and referece to files are defined here

# Different clients may have different retention periods
# Default is 30 Days
RETENTION_DAYS_DEFAULT = 30

# Clients with non default retention period are defined in this file
RETENTION_CLIENTS_FILE = "retentions/retentions.json"


## TEXT PARSERS
# Directory parser is a Text Finite State Machine to identify
# correct data directories conforming to the format

KENTIK_DIR_FORMAT_TEMPLATE = 'parsers/kentik_dir_format'

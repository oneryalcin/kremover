import json
import logging
from collections import defaultdict
from kremover.constants import RETENTION_CLIENTS_FILE, RETENTION_DAYS_DEFAULT

logger = logging.getLogger(__name__)


def get_client_retentions(default=RETENTION_DAYS_DEFAULT, clients_file=RETENTION_CLIENTS_FILE):
    """Client retentions policy

    Args:
        default: (int) retention period in (days) by default for a regular client
        clients_file: (:obj:`pathlib.Path`) Path to retentions file for clients have different than default
                      retentions period

    Returns:
          (:obj: `collections.defaultdict`) lookup table for client retentions
    """

    # default retention time is RETENTION_DAYS_DEFAULT
    retentions_dict = defaultdict(lambda: default, key="any_key")

    # Get any specific retention details for clients
    with open(clients_file, 'r') as f:
        clients = json.load(f)

    logger.debug("Client retention policies loaded %s", clients)

    # After update below we have specific retention days for
    # clients and a default retention days of 30 for any others
    retentions_dict.update(clients)

    return retentions_dict

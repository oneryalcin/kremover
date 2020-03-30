import logging
import pathlib
import textfsm
from datetime import datetime, timedelta
from kremover.retentions import get_client_retentions
from kremover.constants import KENTIK_DIR_FORMAT_TEMPLATE

logger = logging.getLogger(__name__)


class FsmBase:
    """Generic Base class for TextFSM

    TextFSM is used for finding directories and files that fits the template FSM

    Args:
        template_file: (:obj:`pathlib.Path`): TextFSM template file describing the directory tree structure

    """

    def __init__(self, template_file):
        try:
            with open(template_file, 'r') as f:
                self.fsm = textfsm.TextFSM(f)
        except Exception as e:
            logger.error(e, exc_info=True)
            raise IOError(f'Cannot find the template file or template file is in wrong format, {template_file}')
        self.header = self.fsm.header

    def parse(self, text):
        return self.fsm.ParseText(text)


class KentikDirectoryFormatFsm(FsmBase):
    """TextFSM parser for Kentik data directory Structure.

    """

    def __init__(self):
        super().__init__(template_file=KENTIK_DIR_FORMAT_TEMPLATE)
        logger.debug('FSM template file %s read successful', KENTIK_DIR_FORMAT_TEMPLATE)


def tstamp_format_validator(fsm_header, fsm_result):
    """Validates the parsed directory datetime structure for a given file.

    KentikDirectoryFormatFsm does loose validation on directory structure. It checks based on regex in template file
    However for example it will still allow month to be 16 as the regex for month is [0-1][0-9]. This module checks
    the validity of datetime structure

    Args:
        fsm_header: (list) List of TextFSM attribute names
        fsm_result: (list) List of TextFSM parsed attribute values for one path

    Returns:
        (dict): validity of the path based on datetime, datetime as `tstamp` and `client` id.

    """
    mapping = {key:val for key,val in zip(fsm_header, fsm_result)}

    date_str = f'{mapping["Year"]}-{mapping["Month"]}-{mapping["Day"]} {mapping["Hour"]}:{mapping["Minute"]}'
    date_format = '%Y-%m-%d %H:%M'

    try:
        tstamp = datetime.strptime(date_str, date_format)
        logger.debug('Object %s timestamp format check successful', fsm_result)
        return {
            "valid": True,
            "client": mapping['ClientName'],
            "tstamp": tstamp
        }
    except ValueError:
        logger.info('Object %s timestamp format check failed', fsm_result)
        return {
            "valid": False,
            "client": mapping['ClientName'],
            "tstamp": None
        }


def verify_dir_tstamp(fsm_header, fsm_results):
    """Validates the parsed directory datetime structure for a given set of files/dirs.

    KentikDirectoryFormatFsm does loose validation on directory structure. It checks based on regex in template file
    However for example it will still allow month to be 16 as the regex for month is [0-1][0-9]. This module checks
    the validity of datetime structure for all given results (Plural)

    Args:
        fsm_header: (list) List of TextFSM attribute names
        fsm_results: (list) List of (list of TextFSM parsed attribute values for one path)

    Returns:
        (list): list of `tstamp_format_validator` validated dicts
    """
    logger.debug('\n---------VERIFYING DIRECTORY CONFORMITY TO TIMESTAMPS------------')

    verified_files = []
    for result in fsm_results:
        tstamp_checked = tstamp_format_validator(fsm_header=fsm_header,
                                                 fsm_result=result)
        if tstamp_checked.get('valid'):
            verified_files.append(
                {
                    "tstamp": tstamp_checked["tstamp"],
                    "client": tstamp_checked["client"],
                    "path": pathlib.Path('/').joinpath(*result)
                }
            )
    logger.debug('\n----VERIFYING DIRECTORY CONFORMITY TO TIMESTAMPS FINISHED--------')
    return verified_files


def find_expired(verified_files, retentions_policy=get_client_retentions()):
    """Finds the files over retention time

    Based on the tstamp and client retentions metadata, decides if the file should be marked for
    deletion.

    Args:
        verified_files: (list) `verify_dir_tstamp` output for evaluation
        retentions_policy: (dict) policy dict for retention days lookup for a given client

    Returns:
        (list) list of dict of (path, client, tstamp) where path is marked for deletion
    """

    logger.debug('\n---------IDENTIFYING EXPIRED FILES FOR DELETION-------------')
    marked_for_del = []
    # get files invalidates the retention period
    for file in verified_files:
        client = file["client"]
        path = file['path']
        client_retention_days = timedelta(days=retentions_policy[client])
        now, file_tstamp =  datetime.utcnow(), file['tstamp']
        age = now - file_tstamp

        # check if file is older than the retention
        if age > client_retention_days:
            # then mark for deletion
            marked_for_del.append(file)
            logger.info('File %s is older (%d days) than %s, marked for deletion',
                        path, age.days, client_retention_days.days)
        else:
            logger.debug('Keeping file %s, retention: %s , age: %d', path, client_retention_days, age.days)

    logger.debug('\n-----IDENTIFYING EXPIRED FILES FOR DELETION COMPLETE--------')
    return marked_for_del

import os
import sys
import logging
import argparse
import pathlib
from kremover.constants import LOGGING_FORMAT
from kremover.utils import json_format
from kremover.validators import KentikDirectoryFormatFsm, verify_dir_tstamp, find_expired

logging.basicConfig(format=LOGGING_FORMAT, level=logging.WARNING)
logger = logging.getLogger('kremover')


def parse_args():
    """Parse command line arguments

    Returns:
        args: (:obj:`ArgumentParser`)
    """

    # Create the parser
    parser = argparse.ArgumentParser(description='Kentik File Remover')

    # Add the arguments
    parser.add_argument('--root-path',
                        type=str,
                        required=True,
                        help='root path to search for deletion')

    parser.add_argument('--set-nice',
                        type=int,
                        required=False,
                        default=10,
                        help='set the nice value, by default 10, it has less \
                              priority over other running processes')

    parser.add_argument('--verbose',
                        action='store_true',
                        help='set logging to DEBUG')

    parser.add_argument('--dryrun',
                        action='store_true',
                        help="Don't delete, just show me marked for deletion")

    # Execute the parse_args() method
    return parser.parse_args()


def delete_dir_if_empty(pth):
    """Recursively removes empty directories.

    Args:
        pth: (:obj:`pathPathlib`)  direrctory or file path

    Returns:
        None
    """
    for child in pth.parent.rglob("*"):
        logger.debug('Checking file %s', child)

        if child.is_file():
            logger.info('It is a file not dir, breaking %s', child)
            return None

    logger.warning('Directory %s is empty, removing', pth)

    try:
        pth.rmdir()
    except FileNotFoundError:
        logger.info("Skipping as the file %s deleted before", pth)

    delete_dir_if_empty(pth.parent)


def main():

    args = parse_args()

    # Set log level to DEBUG if verbose is set
    if args.verbose:
        level = logging.getLevelName('DEBUG')
        logger.setLevel(level)

    # Set the nice value (set default 10)
    os.nice(args.set_nice)

    pid, nice_value = os.getpid(), os.nice(0)
    logger.debug("Current process id: %d, Nice value for PID %d is %d", pid, pid, nice_value)

    # User specifies a directory to search
    root = pathlib.Path(args.root_path)

    # identify all files in the path
    file_generator = (file for file in root.rglob('*') if file.is_file())

    # Initialize Finite State Machine for dir structure
    kentik_fsm = KentikDirectoryFormatFsm()

    # Process all files and FSM will filter files only matching the defined FSM
    for file in file_generator:
        fsm_results = kentik_fsm.parse(str(file))

    # FSM does the initial verification on directory structure,
    # However verify_dir_tstamp will do a second verification to ensure
    # directory format produces correct Year/Month/Day/Hour/Minute format
    # it also returns back tstamp metadata and client_id for next step
    verified_files = verify_dir_tstamp(fsm_header=kentik_fsm.header,
                                       fsm_results=fsm_results)

    # identify files marked for deletion (Don't delete yet), considering
    # custom retention policy per client
    expired = find_expired(verified_files)

    # Do not delete files but show me them along with metadata
    if args.dryrun:
        print(json_format(expired))
        sys.exit()

    # Delete expired files and recursively parent dirs if empty
    for file in expired:
        pth = file['path']
        logger.warning('Unlinking File %s', pth)
        pth.unlink()

        logger.debug('Attempting to remove parent directory if empty')
        delete_dir_if_empty(pth)


if __name__ == "__main__":
    main()

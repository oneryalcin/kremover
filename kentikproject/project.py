import os
import logging
import argparse
import pathlib
from utils import json_format
from validators import KentikDirectoryFormatFsm, verify_dir_tstamp, find_expired


def parse_args():

    # Create the parser
    parser = argparse.ArgumentParser(description='Kentik File Cleaner')

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

def main():

    args = parse_args()

    # Set the nice value (set default 10)
    os.nice(args.set_nice)

    # User specifies a directory to search
    root = pathlib.Path(args.root_path)

    # identify all files in the path
    file_generator =  (file for file in root.rglob('*') if file.is_file())

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
    if args.dry_run:
        print(json_format(expired))
        sys.exit()

    return expired

if __name__ == "__main__":
    main()

import os
import logging
import argparse
import pathlib
from validators import KentikDirectoryFormatFsm, verify_dir_tstamp, find_expired


def main():

    # User specifies a directory to search
    root = pathlib.Path('/tmp/data/')

    # identify all files in user directiory
    file_generator =  (file for file in root.rglob('*') if file.is_file())

    # Initilaize Finite State Machine for directory structure
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

    return expired

if __name__ == "__main__":
    print(main())

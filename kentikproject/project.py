import os
import logging
import argparse
import pathlib
from validators import KentikDirectoryFormatFsm, verify_dir_tstamp, find_expired


def main():

    # User specifies a directory to search
    root = pathlib.Path('/tmp/data/')

    # identify all files in user directiory
    file_generator =  (file_ for file_ in root.rglob('*') if file_.is_file())

    # Initilaize Finite State Machine and fsm
    kentik_fsm = KentikDirectoryFormatFsm()

    for file_ in file_generator:
        # print(file_)
        fsm_results = kentik_fsm.parse(str(file_))


    verified_files = verify_dir_tstamp(fsm_header=kentik_fsm.header,
                                       fsm_results=fsm_results)

    expired = find_expired(verified_files)

    print("-------------------------------\n")
    print(expired)

if __name__ == "__main__":
    main()

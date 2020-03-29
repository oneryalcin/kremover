import pathlib
from datetime import datetime, timedelta

import retentions
from validators import KentikDirectoryFormatFsm, verify_dir_tstamp


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

    # print(kentik_fsm.header)
    # print(fsm_results)
    #
    # print("-------------------------\n")
    # verified_files = []
    # for result in fsm_results:
    #     tstamp_checked = tstamp_format_validator(fsm_header=kentik_fsm.header,
    #                                              fsm_result=result)
    #     if tstamp_checked.get('valid'):
    #         verified_files.append(
    #             {
    #                 "tstamp": tstamp_checked["tstamp"],
    #                 "client": tstamp_checked["client"],
    #                 "path": pathlib.Path('/').joinpath(*result)
    #             }
    #         )
    # print(verified_files)
    verified_files = verify_dir_tstamp(fsm_header=kentik_fsm.header,
                                       fsm_results=fsm_results)

    rets = retentions.get_retentions()
    marked_for_del = []
    # get files invalidates the retention period
    for file in verified_files:
        client = file["client"]
        client_retention_days = timedelta(days=rets[client])

        # check if file is older than the retention
        now, file_tstamp =  datetime.utcnow(), file['tstamp']
        if now - file_tstamp > client_retention_days:
            # then mark for deletion
            marked_for_del.append(file)

    print("-------------------------------\n")
    print(marked_for_del)

if __name__ == "__main__":
    main()

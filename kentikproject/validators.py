import textfsm
from datetime import datetime

from constants import KENTIK_DIR_FORMAT_TEMPLATE


class FsmBase:

    def __init__(self, template_file):
        with open(template_file, 'r') as f:
            self.fsm = textfsm.TextFSM(f)
        self.header = self.fsm.header

    def parse(self, text):
        return self.fsm.ParseText(text)

class KentikDirectoryFormatFsm(FsmBase):

    def __init__(self):
        super().__init__(template_file=KENTIK_DIR_FORMAT_TEMPLATE)



def tstamp_format_validator(fsm_header, fsm_result):
    """
    Validates the parsed directory structure for a given file

    Returns: dict()
    """
    mapping = {key:val for key,val in zip(fsm_header, fsm_result)}

    date_str = f'{mapping["Year"]}-{mapping["Month"]}-{mapping["Day"]} {mapping["Hour"]}:{mapping["Minute"]}'
    date_format = '%Y-%m-%d %H:%M'

    try:
        tstamp = datetime.strptime(date_str, date_format)
        return {
            "valid": True,
            "client": mapping['ClientName'],
            "tstamp" : tstamp
        }
    except ValueError:
        return {
            "valid": False,
            "client": mapping['ClientName'],
            "tstamp": None
        }


def verify_dir_tstamp(fsm_header, fsm_results):
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
    return verified_files

    

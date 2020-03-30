import datetime
from kremover.validators import KentikDirectoryFormatFsm, tstamp_format_validator


def test_KentikDirectoryFormatFsm_populates_some_result():

    fsm = KentikDirectoryFormatFsm()
    result = fsm.parse("/tmp/data/999/1234/2019/08/11/09/56/somefile.bin")
    assert len(result) > 0

    fsm.fsm.Reset()
    result = fsm.parse("ns1:/data/999/1234/2019/08/11/09/56/somefile.bin")
    assert len(result) > 0


def test_KentikDirectoryFormatFsm_has_correct_header():

    fsm = KentikDirectoryFormatFsm()
    assert fsm.header == ["PreviousDirs", "DataDir", "ClientName", "DeviceId", "Year",
                          "Month", "Day", "Hour", "Minute", "FileName"]


def test_KentikDirectoryFormatFsm_populates_correct_result():

    fsm = KentikDirectoryFormatFsm()
    result = fsm.parse("/tmp/data/999/1234/2019/08/11/09/56/somefile.bin")
    assert result[0] == ['/tmp/', 'data/', '999', '1234', '2019', '08', '11', '09', '56', 'somefile.bin']

    fsm.fsm.Reset()
    result = fsm.parse("ns1:/data/999/1234/2019/08/11/09/56/somefile.bin")
    assert result[0] == ['ns1:/', 'data/', '999', '1234', '2019', '08', '11', '09', '56', 'somefile.bin']


def test_KentikDirectoryFormatFsm_skips_if_directory_format_is_wrong():
    # Month is set to 22, a wrong value causing FSM to return empty

    fsm = KentikDirectoryFormatFsm()
    result = fsm.parse("/tmp/data/999/1234/2019/22/11/09/56/somefile.bin")
    assert result == []


def test_tstamp_format_validator_returns_correct_if_directory_structure_is_ok():

    fsm = KentikDirectoryFormatFsm()
    result = fsm.parse("/tmp/data/999/1234/2019/08/11/09/56/somefile.bin")[0]
    expected = {
        'client': '999',
        'tstamp': datetime.datetime(2019, 8, 11, 9, 56),
        'valid': True
    }
    assert tstamp_format_validator(fsm_header=fsm.header, fsm_result=result) == expected


def test_tstamp_format_validator_returns_expected_if_directory_structure_is_NOT_ok():

    # Set month to 13, an invalid month
    fsm = KentikDirectoryFormatFsm()
    result = fsm.parse("ns1:/data/999/1234/2019/13/11/09/56/somefile.bin")[0]
    expected = {
        'client': '999',
        'tstamp': None,
        'valid': False
    }
    assert tstamp_format_validator(fsm_header=fsm.header, fsm_result=result) == expected



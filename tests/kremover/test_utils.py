import pathlib
from datetime import datetime
from kremover.utils import serializer


def test_serializer_datetime():
    time = datetime.utcnow()
    assert isinstance(time, datetime)
    assert serializer(time) == time.__str__()


def test_serializer_pathlib():
    path = pathlib.Path('/tmp')
    assert isinstance(path, pathlib.Path)
    assert serializer(path) == '/tmp'
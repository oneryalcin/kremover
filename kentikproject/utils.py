import json
import pathlib
import datetime

def serializer(obj):
    """
        Datetime and Pathlib serializer helper for Json pretty printing
        By default json won't print if serializing is not supported
    """
    if isinstance(obj, datetime.datetime):
        return obj.__str__()
    if isinstance(obj, pathlib.Path):
        return obj.__str__()

def json_format(data, converter=serializer):
    return json.dumps(data, indent=2, default=converter)

import base64
import pickle
import textwrap
from typing import Any

""" Functions which cannot be used on CLI """


def serialize_to_base64(obj: Any | list, line_length=80) -> str:
    """Serialize an object to base64 string"""
    # Serialize the object to a bytes object using pickle
    serialized = pickle.dumps(obj)
    # Encode the bytes object to a base64-encoded string
    encoded = base64.b64encode(serialized).decode("utf-8")
    # Wrap the base64-encoded string every `line_length` characters
    wrapped = textwrap.fill(encoded, width=line_length)
    return wrapped


def deserialize_from_base64(base64_str: str) -> Any:
    """Deserialize a base64-encoded string to original object"""
    # Decode the base64-encoded string to a bytes object
    decoded = base64.b64decode(base64_str)
    # Deserialize the bytes object to a Python object using pickle
    obj = pickle.loads(decoded)
    return obj

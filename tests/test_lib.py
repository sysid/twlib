from pathlib import Path

import pytest
from twlib.lib import deserialize_from_base64, serialize_to_base64, filter_path

FILES = [
    "file1____________________________________________________________",
    "file2____________________________________________________________",
    "file3____________________________________________________________",
    "file4____________________________________________________________",
    "file5____________________________________________________________",
    "file1____________________________________________________________",
    "file2____________________________________________________________",
    "file3____________________________________________________________",
    "file4____________________________________________________________",
    "file5____________________________________________________________",
]


def test_serialize_to_base64():
    # Serialize the list to a base64-encoded string
    serialized = serialize_to_base64(FILES)

    # Print the serialized string
    print(f"\n{serialized}")
    assert isinstance(serialized, str)


def test_deserialize_to_base64():
    serialized = """
gASVYwEAAAAAAABdlCiMQWZpbGUxX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19f
X19fX19fX19fX19fX19fX19fX19flIxBZmlsZTJfX19fX19fX19fX19fX19fX19fX19fX19fX19fX19f
X19fX19fX19fX19fX19fX19fX19fX19fX19fX1+UjEFmaWxlM19fX19fX19fX19fX19fX19fX19fX19f
X19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX5SMQWZpbGU0X19fX19fX19fX19fX19f
X19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19flIxBZmlsZTVfX19fX19f
X19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX1+UaAFoAmgD
aARoBWUu
    """
    obj = deserialize_from_base64(serialized)
    print(f"\n{obj}")
    assert obj == FILES


@pytest.mark.parametrize(
    ("dir_", "expected"),
    (
        (".venv", True),
        ("/.venv", True),
        ("./noo", False),
        ("./.no.no..", False),
        ("./noo/oooo", False),
        ("./oo/nooo", False),
        ("./oo/venv/.gitter", False),
        ("./oo/venv/.git/bla/blub", True),
        ("./.venv/.git/bla/blub", True),
    ),
)
def test_filter_lks(dir_, expected):
    excludes = (".venv", ".git", "no")
    assert filter_path(Path(dir_), excludes) is expected

    # assert any(part for part in Path(dir_).parts if part in excludes)

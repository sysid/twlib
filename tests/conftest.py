import logging
import shutil
from pathlib import Path

import pytest

from twlib.environment import ROOT_DIR

_log = logging.getLogger(__name__)
log_fmt = r"%(asctime)-15s %(levelname)s %(name)s %(funcName)s:%(lineno)d %(message)s"
logging.basicConfig(format=log_fmt, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S")

SENTINEL = "test_proj-1234"
TEST_PROJ = ROOT_DIR / "tests/resources/test_proj"
REF_PROJ = ROOT_DIR / "tests/resources/ref_proj"
TEMP_DIR = "/tmp/xxx"


# # run fixture before all tests
# @pytest.fixture(autouse=True)
# def test_proj():
#     # scope to class if necessary: https://stackoverflow.com/a/50135020
#     shutil.rmtree(TEMP_DIR, ignore_errors=True)
#     Path(TEMP_DIR).mkdir(parents=True, exist_ok=True)
#
#     shutil.rmtree(TEST_PROJ, ignore_errors=True)
#     shutil.copytree(REF_PROJ, TEST_PROJ)

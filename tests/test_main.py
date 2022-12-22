import datetime
import shutil
from pathlib import Path

import pytest
from typer.testing import CliRunner

from tests.conftest import REF_PROJ, TEMP_DIR, TEST_PROJ
from twlib.environment import ROOT_DIR
from twlib.git_open import app
from twlib.main import _heic2img
from twlib.main import app as twlib
from twlib.main import relative, revert_lks, snake_say

runner = CliRunner()


def test_snake_say():
    snake_say("Hi Thomas")
    assert True


# noinspection PyPep8Naming
class TestGitOpen:
    @pytest.mark.parametrize(
        ("path", "url"),
        ((".", "https://github.com/sysid/py-twlib.git"),),
    )
    def test_git_open(self, mocker, path, url):
        mocked = mocker.patch("twlib.git_open.webbrowser.open")
        result = runner.invoke(app, path)
        print(result.stdout)
        assert result.exit_code == 0
        assert url in result.stdout


class TestEpochConvert:
    @pytest.mark.parametrize(
        ("epoch", "dt", "is_local"),
        (
            ("1347517370000", "2012-09-13 06:22:50\n", False),  # epoch must be str ???
            ("1347517370000", "2012-09-13 08:22:50\n", True),
        ),
    )
    def test_epoch2dt(self, epoch, dt, is_local):
        # result = runner.invoke(app, ["epoch2datetime", epoch, "-v"], input="y\n")
        if is_local:
            result = runner.invoke(twlib, ["epoch2dt", epoch, "--local"])
        else:
            result = runner.invoke(twlib, ["epoch2dt", epoch])
        print(result.stdout)
        assert result.exit_code == 0
        assert result.stdout == dt

    @pytest.mark.parametrize(
        ("dt", "epoch", "is_local"),
        (
            ("2012-09-13 06:22:50", "1347517370000\n", False),  # epoch must be str ???
            ("2012-09-13 08:22:50", "1347517370000\n", True),  # epoch must be str ???
        ),
    )
    def test_dt2epoch(self, mocker, dt, epoch, is_local):
        # result = runner.invoke(app, ["epoch2datetime", epoch, "-v"], input="y\n")
        if is_local:
            mocker.patch(
                "twlib.main.parse",
                return_value=datetime.datetime(2012, 9, 13, 7, 22, 50),
            )  # daylight saving
            result = runner.invoke(twlib, ["dt2epoch", dt, "--local"])
        else:
            result = runner.invoke(twlib, ["dt2epoch", dt])
        print(result.stdout)
        assert result.exit_code == 0
        assert result.stdout == epoch


class TestRelativePath:
    @pytest.mark.parametrize(
        ("source_path", "target_path", "expected"),
        (
            ("/home/xxx/tests/resources", "/resources", "../../resources"),
            ("/home/xxx/tests/resources", "/tmp/resources", "../../../tmp/resources"),
            (
                "/home/xxx/tests/resources/x.txt",
                "/tmp/resources/y.txt",
                "../../../tmp/resources/y.txt",
            ),
        ),
    )
    def test_relative_path(self, source_path, target_path, expected):
        result = relative(source_path, target_path)
        assert result == expected

    @pytest.mark.parametrize(
        ("source_path", "target_path", "expected"),
        (("tests/resources", "tests/resources", "tests/resources"),),
    )
    def test_relative_path(self, source_path, target_path, expected):
        with pytest.raises(ValueError):
            relative(source_path, target_path)


class TestConverter:
    def test_convert_heic(self):
        INPUT_FILE = ROOT_DIR / "tests" / "resources" / "input.heic"
        result = runner.invoke(twlib, ["heic2img", str(INPUT_FILE)])
        print(result.stdout)
        assert result.exit_code == 0

    def test__convert_heic(self):
        INPUT_FILE = ROOT_DIR / "tests" / "resources" / "input.heic"
        OUTPUT_FILE = ROOT_DIR / "tests" / "resources" / "input.jpg"
        OUTPUT_FILE.unlink(missing_ok=True)

        _heic2img(input_file=INPUT_FILE, mode="jpg", out_file=None)
        assert Path(OUTPUT_FILE).exists()

    # noinspection PyPep8Naming
    @pytest.mark.skip("Long running test")
    def test__convert_heic_png_custom_path(self):
        INPUT_FILE = ROOT_DIR / "tests" / "resources" / "input.heic"
        OUTPUT_FILE = Path("/tmp/xxx.png")
        OUTPUT_FILE.unlink(missing_ok=True)

        _heic2img(input_file=INPUT_FILE, mode="png", out_file=str(OUTPUT_FILE))
        assert Path(OUTPUT_FILE).exists()


class TestRevertLks:
    @pytest.fixture(autouse=True)
    def _setup_test_proj(self):
        shutil.rmtree(TEST_PROJ, ignore_errors=True)
        shutil.copytree(REF_PROJ, TEST_PROJ, symlinks=True)

    def test_revert_lks(self):
        revert_lks(dir_=TEST_PROJ)
        assert (TEST_PROJ / "lks/d/.run").is_dir()
        assert (TEST_PROJ / "lks/xxx.txt").is_file()

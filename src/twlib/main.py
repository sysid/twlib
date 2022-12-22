import datetime
import logging
import os
import shutil
from pathlib import Path
from typing import Iterable

import typer
from dateutil.parser import parse
from PIL import Image
from pillow_heif import register_heif_opener

from twlib.lib import filter_path

_log = logging.getLogger(__name__)

register_heif_opener()  # register PILLOW plugin

app = typer.Typer(name="twlib")


@app.command()
def snake_say(
    message: str,
):
    # message = " ".join(sys.argv[1:])
    bubble_length = len(message) + 2
    print(
        rf"""
           {"_" * bubble_length}
          ( {message} )
           {"‾" * bubble_length}
            \
             \    __
              \  [oo]
                 (__)\
                   λ \\
                     _\\__
                    (_____)_
                   (________)Oo°"""
    )


@app.command()
def epoch2dt(
    epoch: int = typer.Argument(..., help="epoch in ms"),
    to_local: bool = typer.Option(False, "-l", "--local", help="In local time"),
):
    """Convert epoch in ms (UTC) to datetime (local or UTC)"""
    if to_local:
        dt = datetime.datetime.fromtimestamp(epoch / 1000).strftime("%Y-%m-%d %H:%M:%S")
    else:
        dt = datetime.datetime.utcfromtimestamp(epoch / 1000).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    typer.echo(dt)


@app.command()
def dt2epoch(
    dt: str = typer.Argument(..., help="datetime string in '%Y-%m-%d %H:%M:%S'"),
    is_local: bool = typer.Option(
        False, "-l", "--local", help="Input is given in local time"
    ),
):
    """Convert naive local datetime (local or UTC) string to epoch in ms (UTC)"""
    if is_local:
        # https://stackoverflow.com/a/39079819
        LOCAL_TIMEZONE = datetime.datetime.now().astimezone().tzinfo

        dt_parsed = parse(dt)  # get naive dt
        dt_parsed = dt_parsed.replace(tzinfo=LOCAL_TIMEZONE)  # localize naive dt
    else:
        dt_parsed = parse(dt)
        dt_parsed = dt_parsed.replace(tzinfo=datetime.timezone.utc)

    epoch = int(dt_parsed.timestamp() * 1000)
    typer.echo(epoch)


@app.command()
def heic2img(input_file: str, *, mode="jpg", out_file: str = None) -> None:
    """
    An HEIC file is a space-saving image format that uses High Efficiency Video Coding (HEVC)
    to compress and store images across your devices.
    Because Apple regularly uses HEIC files, you can easily open them on your Mac with Preview or Photoshop
    """
    _heic2img(input_file=input_file, mode=mode, out_file=out_file)
    typer.secho("Saved {out_file}", fg=typer.colors.GREEN, bold=False)


def _heic2img(input_file: str, mode: str, out_file: str | None) -> None:
    with Image.open(input_file) as img:
        print(
            f"{img.mode=}, {img.size=}, {img.format=}, {img.info.keys()=}, {img.getbands()=}"
        )

        if mode == "jpg":
            if out_file is None:
                out_file = Path(input_file).with_suffix(".jpg")
            Path(out_file).unlink(missing_ok=True)
            Path(out_file).parent.mkdir(parents=True, exist_ok=True)
            img.save(out_file, "JPEG")

        elif mode == "png":
            if out_file is None:
                out_file = Path(input_file).with_suffix(".png")
            Path(out_file).unlink(missing_ok=True)
            Path(out_file).parent.mkdir(parents=True, exist_ok=True)
            img.save(out_file, "PNG")
        else:
            raise ValueError(f"Unknown type {mode}")


@app.command()
def relative(source: str, target: str) -> Path:
    """Calculate the relative path from source to target ."""
    source_path = Path(source).parent
    target_path = Path(target).parent

    if not (source_path.is_absolute() and target_path.is_absolute()):
        raise ValueError("Both source and target must be absolute paths")

    name = Path(
        target
    ).name  # Gotcha: source_path.name is not the same as target_path.name
    rel_path = os.path.relpath(target_path, source_path)
    typer.echo(Path(rel_path) / name)
    return Path(rel_path) / name


@app.command()
def revert_lks(
    dir_: Path = typer.Argument(
        ..., help="Directory containing the lks files", exists=True
    ),
    excludes: list[str] = typer.Option(
        [".venv", ".git"], "-e", "--exclude", help="Exclude dirs/files"
    ),
    dry_run: bool = typer.Option(False, "-d", "--dry-run", help="Dry run"),
    move: bool = typer.Option(False, "-m", "--move", help="Move instead of copy"),
) -> None:
    """Replace symlinks in given directory with their associated files/directories."""
    typer.echo(f"xxx {dir_}")
    _log.info(f"Reverting symlinks in {dir_}")

    if dry_run:
        _log.info("Dry run, no changes will be made")
        func = shutil.copy
    else:
        if move:
            _log.info("Move mode")
        else:
            _log.info("Copy mode")

    symlks = [f for f in dir_.rglob("*") if f.is_symlink()]

    for f in symlks:
        if filter_path(f, excludes):
            continue
        target = f.resolve()

        if dry_run:
            _log.info(f"Copy/move {target} to {f}")
            continue

        f.unlink()
        if target.is_file():
            if move:
                shutil.move(target, f)
                _log.debug(f"Moved {target} to {f}")
            else:
                shutil.copy2(target, f)
                _log.debug(f"Copied {target} to {f}")
        elif target.is_dir():
            if move:
                shutil.move(target, f.parent)
                _log.debug(f"Moved {target} to {f.parent}")
            else:
                shutil.copytree(target, f, symlinks=True)
                _log.debug(f"Copied {target} to {f}")

    typer.secho(f"Reverted {len(symlks)} symlinks", fg=typer.colors.GREEN, bold=False)


@app.callback()
def main(
    verbose: bool = typer.Option(False, "-v", "--verbose", help="verbosity"),
):
    log_fmt = r"%(asctime)-15s %(levelname)-7s %(message)s"
    if verbose:
        logging.basicConfig(
            format=log_fmt, level=logging.DEBUG, datefmt="%m-%d %H:%M:%S"
        )
    else:
        logging.basicConfig(
            format=log_fmt, level=logging.INFO, datefmt="%m-%d %H:%M:%S"
        )


if __name__ == "__main__":
    app()

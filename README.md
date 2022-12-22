# twlib: Library with helpful functions and tools

## git-open
- `git-open(Optional[path])`: Open the remote repo in browser
```
Usage: git-open [OPTIONS] [PATH]

  Open remote github/gitlab repository Add this command to your path, then you
  can use with via `git open .`.

Arguments:
  [PATH]  path in directory of the desired repo.  [default: .]
```

## twlib
- `twlib`: Super useful CLI helper
```
Usage: twlib [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose                   verbosity
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  dt2epoch    Convert naive local datetime (local or UTC) string to epoch...
  epoch2dt    Convert epoch in ms (UTC) to datetime (local or UTC)
  heic2img    An HEIC file is a space-saving image format that uses High...
  relative    Calculate the relative path from source to target .
  revert-lks  Replace symlinks in given directory with their associated...
  snake-say
```

## Setup
```sh
pipx install twlib
```

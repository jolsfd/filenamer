# FileNamer

## Install

For using FileNamer you need Python 3.7+ installed.

Clone Repository:

```
git clone https://github.com/jolsfd/filenamer.git
```

Install requirements.txt:

```
pip3 install -r requirements.txt
```

Recommended:

Create bash alias in _~.bashrc_.

```bash
alias filenamer='python3 YOUR_DIRECTORY'
```

## Usage

```
usage: FileNamer [-h] [-p PATH] [-e [FOLDER ...]] [-a] [--version]

FileNamer rename files in a directory into a format

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  path where FileNamer rename files. Default: working directory
  -e [FOLDER ...], --exclude [FOLDER ...]
                        ignore folders for renaming
  -a, --all             disable Safe Rename
  --version             show program's version number and exit
```

### Path

The path is the directory where FileNamer renames the files.
The default is your working directory where you started the program.

### Safe Rename

When activated the program don't rename files that already renamed.

### Exclude Folders

Exclude Folders when renaming files.

## Settings

### Format

After the first startup you can make your own format in the _settings/settings.json_.
FileNamer takes the creation time of the file.

Time:

"%Y": Year
"$M": Month
"$D": Day
"$h": Hour
"$m": Minute
"$s": Second
"FILENAME": Filename before renaming

Default:

```
"DOC_$Y$M$D_FILENAME"
```

### Document Extensions

The document extensions are the extensions of the files that the FileNamer is renaming.
You can add your own extensions.

### Replace Letters

The replace letters is the letters which replace FileNamer from the old filename with the new letter.

## License

[MIT License](https://github.com/jolsfd/filenamer/blob/main/LICENSE)

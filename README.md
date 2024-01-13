# Whirst
Uses Whisper to automatically generate srt subtitles from a video file.

## Setup
Run `source setup.sh` to create a new venv and fetch dependencies.

On future runs you can use `source venv/bin/activate` to load the virtual environment.

## Use
Command line help info is authoritative.
```
usage: whisrt [-h] [-l LANGUAGE] [-m WHISPER_MODEL] [-o OUTPUT_FILE] input_file

Command line tool for subtitling video/audio files.

positional arguments:
  input_file            The video/audio file to be subtitled.

options:
  -h, --help            show this help message and exit
  -l LANGUAGE, --language LANGUAGE
                        Specify the language for subtitles.
  -m WHISPER_MODEL, --whisper-model WHISPER_MODEL
                        Specify the Whisper model to use.
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Specify the name of the output file.
```

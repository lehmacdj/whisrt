# Whirst
Uses Whisper to automatically generate srt subtitles from a video file.

## Setup
Run `source setup.sh` to create a new venv and fetch dependencies.

On future runs you can use `source venv/bin/activate` to load the virtual environment.

## Installation
Run `pip install .` from outside a virtual environment to install the command line tool `whisrt`.

## Use
Provide a file with an audiostream to generate subtitles for, and optionally specify the language for slightly better results, e.g.:
```bash
whisrt input.mp4 --language=japanese --output input.srt
```

Command line help info has more details, e.g. (may not be up to date with actual executable):
```
usage: whisrt [-h] [-l LANGUAGE] [-m WHISPER_MODEL] [-o OUTPUT_FILE] [--use-transformers] input_file

Command line tool for subtitling video/audio files.

positional arguments:
  input_file            The video/audio file to be subtitled.

options:
  -h, --help            show this help message and exit
  -l LANGUAGE, --language LANGUAGE
                        Specify the language for subtitles. If left unspecified, the language is inferred. For huggingface transformers (e.g. --use-transformers) this is a two letter
                        language code (e.g. '--language=ja'). By default this is a language name (e.g. ('--language=japanese')
  -m WHISPER_MODEL, --whisper-model WHISPER_MODEL
                        Specify the Whisper model to use.
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Specify the name of the output file.
  --use-transformers    Use huggingface transformers for inference.
```

## Troubleshooting
- Sometimes you can get better results by switching to the alternate model (e.g. `--use-transformers` if you didn't use it)
- Especially near the beginning and end of an audio file and for extended periods of silence, sometimes the underlying whisper model halucinates and ruins the generated subtitles. When this happens I'll generally cut up the audio input into a segment that starts where speech starts and then get much better results. Eventually I'd like to use voice diarization/voice activity detection to automatically do this, but I haven't had enough trouble to want to do so yet.
- If you use the above approach might find [this python script](https://github.com/lehmacdj/.dotfiles/blob/main/bin/srt_cleanup.py) useful for splicing together multiple snippets (using the `--shift-seconds` option)

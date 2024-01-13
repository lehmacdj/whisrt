#!/usr/bin/env python

import argparse
import datetime
import os
import sys
import whisper

def main():
    # parse command line arguments
    parser = argparse.ArgumentParser(description="Command line tool for subtitling video/audio files.")
    parser.add_argument("-l", "--language", type=str, help="Specify the language for subtitles.")
    parser.add_argument("-m", "--whisper-model", type=str, default="large-v3", help="Specify the Whisper model to use.")
    parser.add_argument("-o", "--output-file", type=str, help="Specify the name of the output file.")
    parser.add_argument("input_file", type=str, help="The video/audio file to be subtitled.")
    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print("Input file does not exist.")
        return

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = whisper.load_model(args.whisper_model, device="mps")
    result = model.transcribe(args.input_file, language=args.language)

    file_descriptor = open(args.output_file, "w") if args.output_file else sys.stdout
    for i, segment in enumerate(result["segments"], 1):
        caption = render_caption(i, segment["start"], segment["end"], segment["text"])
        file_descriptor.write(caption)

def format_timestamp(seconds):
    if seconds < 0:
        raise ValueError("Timestamp cannot be negative.")
    timedelta = datetime.timedelta(seconds=seconds)
    hours = timedelta.seconds // 3600 + timedelta.days * 24
    minutes = (timedelta.seconds // 60) % 60
    seconds = timedelta.seconds % 60
    milliseconds = timedelta.microseconds // 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def render_caption(i, start, end, text):
    return f"{i}\n{format_timestamp(start)} --> {format_timestamp(end)}\n{text}\n\n"

if __name__ == "__main__":
    main()

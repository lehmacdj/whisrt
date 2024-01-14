#!/usr/bin/env python

import argparse
import datetime
import os
import sys
import transformers
import torch
import whisper

def get_torch_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
        return torch.device("mps")
    else:
        return torch.device("cpu")

def main():
    # parse command line arguments
    parser = argparse.ArgumentParser(description="Command line tool for subtitling video/audio files.")
    parser.add_argument("-l", "--language", type=str, help="Specify the language for subtitles.")
    parser.add_argument("-m", "--whisper-model", type=str, default="large-v3", help="Specify the Whisper model to use.")
    parser.add_argument("-o", "--output-file", type=str, help="Specify the name of the output file.")
    parser.add_argument("--use-transformers", action='store_true', help="Use huggingface transformers for inference.")
    parser.add_argument("input_file", type=str, help="The video/audio file to be subtitled.")
    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print("Input file does not exist.")
        return

    if args.use_transformers:
        pipe = transformers.pipeline(
          "automatic-speech-recognition",
          model=f"openai/whisper-{args.whisper_model}",
          chunk_length_s=30,
          language=args.language,
          device=get_torch_device(),
        )
        result = pipe(args.input_file, return_timestamps=True)
        # the chunks returned from the pipeline are actually the equivalent of segments
        # confusingly huggingface uses the term "chunk" differently for
        # pipeline initialization and in the result
        def to_whisper_segment(chunk):
            return {
                "start": chunk["timestamp"][0],
                "end": chunk["timestamp"][1],
                "text": chunk["text"],
            }
        result = map(to_whisper_segment, result["chunks"])
    else:
        # whisper's native interface doesn't work with mps so we don't pass get_torch_device()
        model = whisper.load_model(args.whisper_model)
        result = model.transcribe(args.input_file, language=args.language)
        result = result["segments"]

    file_descriptor = open(args.output_file, "w") if args.output_file else sys.stdout
    for i, segment in enumerate(result, 1):
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

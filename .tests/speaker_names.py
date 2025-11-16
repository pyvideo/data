import argparse
import json
import sys

from termcolor import colored, cprint

from tools.utils import get_json_files


def check_speaker_names(data_root, verbose=False):
    _, video_paths = get_json_files(data_root)

    invalid_names = []
    # Map of disallowed speaker names to their correct replacements
    replacements = {
        "Glyph Lefkowitz": "Glyph",
    }

    for video_path in video_paths:
        with open(video_path, encoding="UTF-8") as fp:
            video_blob = json.load(fp)
            speakers = video_blob.get("speakers", [])

            for speaker in speakers:
                if speaker in replacements:
                    invalid_names.append((video_path, speaker, replacements[speaker]))

    if invalid_names:
        cprint("Disallowed speaker names found:", "red")
        for path, speaker, replacement in invalid_names:
            speaker = colored(speaker, "red")
            print(f"\t{path}: {speaker}")
            print(f"\t\tUse {colored(replacement, 'green')} instead of {speaker}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data-root",
                        help="directory to search for JSON files")
    parser.add_argument("-v", "--verbose",
                        type=int,
                        help="increase output verbosity")
    args = parser.parse_args()

    check_speaker_names(args.data_root, verbose=args.verbose)


if __name__ == '__main__':
    main()

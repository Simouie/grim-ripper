import os
import sys


def process_files(path, separator):

    # look at all files and directories within the given directory
    # assuming that all WAV files there follow this format
    # tag-name separator permutation-name
    # put each WAV files in a subdirectory according to its name

    for data in os.walk(path):
        for file_name in data[2]:

            if ".wav" not in file_name: continue

            parts = file_name.split(separator)
            if len(parts) != 2: continue 

            tag_name = file_name.split(separator)[0]
            permutation_name = file_name.split(separator)[1]

            new_path = f"{data[0]}\\{tag_name}"
            os.makedirs(new_path, exist_ok=True)
            os.rename(f"{data[0]}\\{file_name}", f"{new_path}\\{permutation_name}")


def check_arguments(count, values):

    if count < 3:
        print(f"python {values[0]} <path-to-directory> <separator>")
        print("path-to-directory: path to directory that contains WAV files")
        print("separator: symbol between tag name and permutation name")
        sys.exit(1)

    if not os.path.isdir(values[1]): 
        print(f"The given path is not a path to a directory!")
        sys.exit(1)


def main(argc, argv):
    check_arguments(argc, argv)
    process_files(argv[1], argv[2])

main(len(sys.argv), sys.argv)

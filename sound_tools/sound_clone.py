import os
import sys
import shutil


def process_files(input_path, output_path):

    # look at all files and directories within the given directory
    # copy all WAV files over to a new directory
    # the hierarchy inside the given directory should be preserved

    for path, d, file_names in os.walk(input_path):
        for file_name in file_names:
            if file_name.lower().endswith(".wav"):
                r_path = path.replace(input_path, "")
                new_path = f"{output_path}{r_path}"
                os.makedirs(new_path, exist_ok=True)
                shutil.copy2(f"{path}\\{file_name}", f"{new_path}\\{file_name}")


def check_arguments(count, values):

    if count < 3:
        print(f"python {values[0]} <full-path-to-input-directory> <full-path-to-output-directory>")
        print("full-path-to-input-directory: path to directory that contains WAV files")
        print("full-path-to-output-directory: path to directory where copies of WAV files should go")
        sys.exit(1)

    if not os.path.isabs(values[1]): 
        print(f"The given path is not a full path to a directory!")
        sys.exit(1)
    
    if not os.path.isabs(values[2]): 
        print(f"The given path is not a full path to a directory!")
        sys.exit(1)


def main(argc, argv):
    check_arguments(argc, argv)
    process_files(argv[1], argv[2])

main(len(sys.argv), sys.argv)

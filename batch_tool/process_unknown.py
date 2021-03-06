import os
import sys
import glob


def process_line(line):

    # assuming input was generated by "tool_sounds.py"
    # if sound type is set to "unknown"
    # replace "unknown" with input from user
    # do not modify input if sound type is not "unknown" 

    new_line = line

    if "unknown" in line:
        print(line[0:-1])
        new_type = input("Replace type with: ")
        new_line = line.replace("unknown", new_type)
        print(new_line)

    return new_line
    

def process_files(path):

    # for each file that ends with ".bat"
    # assuming that it was generated by "tool_sounds.py"
    # replace sound type for any command that has "unknown" as sound type

    for f in glob.glob(f"{path}\\*.bat"):

        # output should go to new file so original can be kept as backup
        # user can start over if mistakes happen

        f_new = f.replace(".bat", "_new.bat")
        with open(f, "r") as i, open(f"{f_new}", "w") as o:

            # examine each line in input file
            # let process_line() handle details
            
            for line in i:
                new_line = process_line(line)
                o.write(new_line)


def check_arguments(count, values):

    if count < 2:
        print(f"python {values[0]} <path-to-directory>")
        sys.exit(1)
    
    if not os.path.isdir(values[1]):
        print("The given path is not a valid!")
        sys.exit(1)


def main(argc, argv):
    check_arguments(argc, argv)
    process_files(argv[1])

main(len(sys.argv), sys.argv)

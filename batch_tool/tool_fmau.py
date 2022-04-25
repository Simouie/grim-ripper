import sys

def main(argc, argv):

    # process arguments

    if argc < 3:
        print(f"{argv[0]} <type> <name> [suffix]")
        sys.exit(1)

    weapType = argv[1]
    weapName = argv[2]
    weapRndr = ""

    if argc > 3:
        weapRndr = f"\\{argv[2]}_{argv[3]}"

    # useful constants

    toolCmd = "tool fp-model-animations-uncompressed"
    masterchief = "objects\\characters\\masterchief\\fp"
    dervish = "objects\\characters\\dervish\\fp"

    # build commands for compiling animations with tool
    
    base = f"dw3\\r3ach\\objects\\weapons\\{weapType}\\{weapName}"

    fp_elite = f"{base}\\animations\\fp_elite"
    fp_spartan = f"{base}\\animations\\fp_spartan"

    toolCmdElite = f"{toolCmd} {fp_elite} {dervish} {base}{weapRndr}\n"
    toolCmdSpartan = f"{toolCmd} {fp_spartan} {masterchief} {base}{weapRndr}\n"

    # write to console and write to file

    print(toolCmdElite + toolCmdSpartan)

    with open("fmau.bat", "a") as output:
        output.write(toolCmdElite + toolCmdSpartan)

main(len(sys.argv), sys.argv)

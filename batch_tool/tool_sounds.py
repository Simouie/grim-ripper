import os
import sys


BATCH_01 = "sounds.bat"
BATCH_02 = "sounds_unknown.bat"

MY_TYPES = {
    "impact": "projectile_impact",
    "hit": "projectile_impact",
    "bounce": "projectile_impact",
    "bnc": "projectile_impact",
    "ricc": "projectile_impact",
    "expl": "projectile_detonation",
    "flyby": "projectile_flyby",
    "_by": "projectile_flyby",
    "attached": "projectile_flyby",
    "fire": "weapon_fire",
    "firing": "weapon_fire",
    "eject": "weapon_fire",
    "tail": "weapon_fire",
    "ready": "weapon_ready",
    "reload": "weapon_reload",
    "load": "weapon_reload",
    "ammo": "weapon_reload",
    "empty": "weapon_empty",
    "dryfire": "weapon_empty",
    "charge": "weapon_charge",
    "charging": "weapon_charge",
    "overheat": "weapon_overheat",
    "heat": "weapon_overheat",
    "oh": "weapon_overheat",
    "vent": "weapon_overheat",
    "idle": "weapon_idle",
    "pose": "weapon_idle",
    "posing": "weapon_idle",
    "melee": "weapon_melee",
    "lunge": "weapon_melee",
    "drop": "object_impacts",
    "lod_far": "weapon_fire_lod",
    "zoom": "game_event",
}

MY_KEYS = sorted([ k for k in MY_TYPES.keys() ])


def guess_type(name):

    # try to determine the appropriate sound type based on the given name 
    # assuming that the name actually has meaningful keywords

    t = "unknown"

    for k in MY_KEYS:
        if k in name: 
            t = MY_TYPES[k]
            break

    # there are various special cases where multiple keywords are present
    # this is going to be ugly but they must handled somehow

    if "lod" in name:
        if t == "projectile_detonation": 
            return "projectile_detonation_lod"
        if t == "weapon_fire": 
            return "weapon_fire_lod"

    if "empty" in name:
        if "reload" in name: 
            return "weapon_reload"
        return "weapon_empty"

    if "charge" in name:
        if "fire" in name:
            return "weapon_fire"
        return "weapon_charge"
    
    return t


def get_relative_path(path):

    # assuming the given path is an absolute path to a directory within the H3EK directory
    # trim the given path to get a relative path that Tool can use

    path_parts = path.split("\\")
    parts_count = len(path_parts)

    for i in range(parts_count):
        if path_parts[i] == "H3EK":
            return "\\".join(path_parts[i + 2:])


def write_command(c, primary_batch_file, secondary_batch_file):

    if c.endswith("unknown\n"):
        secondary_batch_file.write(c)
        return
    
    primary_batch_file.write(c)


def build_command(r_path):

    def print_warning(name, path):
        print(f"WARNING: I have no idea what type of sound '{name}' should be\n{path}")

    sound_name = r_path.split("\\")[-1]
    sound_type = guess_type(sound_name)

    parent_path = ""

    # for sounds that are part of loops

    if sound_name in [ "in", "loop", "out" ]:

        parent_path = "\\".join(r_path.split("\\")[0:-2])
        sound_type = guess_type(parent_path.split("\\")[-1])

        if sound_type == "unknown": 
            print_warning(sound_name, r_path)

        # for sounds that are supposed to loop

        if sound_name == "loop":
            a = f"tool sounds-single-layer {r_path} {sound_type}\n"
            b = f"tool sound-looping {parent_path} {sound_type}\n"
            return a + b

    # for everything else

    if sound_type == "unknown": 
        print_warning(sound_name, r_path)

    return f"tool sounds-single-layer {r_path} {sound_type}\n"


def create_batch_file(full_path):

    # look at all files and directories within the given directory
    # for any directory that contains WAV files 
    # write a command for compiling sounds in that directory

    with open(BATCH_01, "w") as a, open(BATCH_02, "w") as b:
        for path, d, file_names in os.walk(full_path):
            for file_name in file_names:
                if file_name.lower().endswith(".wav"):
                    c = build_command(get_relative_path(path))
                    write_command(c, a, b)
                    break


def check_arguments(count, values):

    if count < 2:
        print(f"python {values[0]} <full-path-to-directory>")
        print("full-path-to-directory: full path to directory that contains WAV files")
        sys.exit(1)

    if not os.path.isabs(values[1]): 
        print(f"The given path is not a full path to a directory!")
        sys.exit(1)


def main(argc, argv):
    check_arguments(argc, argv)
    create_batch_file(argv[1])

main(len(sys.argv), sys.argv)
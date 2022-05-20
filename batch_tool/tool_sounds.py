import os
import sys
import datetime as dt


# create a time stamp based on current date and time
# the time stamp should be written as YYYYMMDD_HHMMSS

TIME_STAMP = dt.datetime.strftime(dt.datetime.now(), "%Y%m%d_%H%M%S")

# files created by this program should have the time stamp in the name

BAT_01 = f"./{TIME_STAMP}_sounds.bat"
BAT_02 = f"./{TIME_STAMP}_sounds_unknown.bat"


# if the name of the sound has one of these keywords
# its sound type probably should be the corresponding value
# sometimes there are multiple keywords in the name
# usually one of them has more importance than the others

MY_TYPES = {
    "impact": [ "projectile_impact", 0 ],
    "hit": [ "projectile_impact", 0 ],
    "bounce": [ "projectile_impact", 0 ],
    "bnc": [ "projectile_impact", 0 ],
    "ricc": [ "projectile_impact", 0 ],
    "detonation": [ "projectile_detonation", 0 ],
    "expl": [ "projectile_detonation", 2 ],
    "flyby": [ "projectile_flyby", 0 ],
    "_by": [ "projectile_flyby", 0 ],
    "attached": [ "projectile_flyby", 0 ],
    "fire": [ "weapon_fire", 1 ],
    "firing": [ "weapon_fire", 1 ],
    "eject": [ "weapon_fire", 0 ],
    "tail": [ "weapon_fire", 0 ],
    "ready": [ "weapon_ready", 1 ],
    "reload": [ "weapon_reload", 1 ],
    "load": [ "weapon_reload", 1 ],
    "ammo": [ "weapon_reload", 0 ],
    "empty": [ "weapon_empty", 0 ],
    "dryfire": [ "weapon_empty", 2 ],
    "charge": [ "weapon_charge", 0 ],
    "charging": [ "weapon_charge", 0 ],
    "overheat": [ "weapon_overheat", 0 ],
    "heat": [ "weapon_overheat", 0 ],
    "oh": [ "weapon_overheat", 0 ],
    "vent": [ "weapon_overheat", 0 ],
    "idle": [ "weapon_idle", 0 ],
    "pose": [ "weapon_idle", 0 ],
    "posing": [ "weapon_idle", 0 ],
    "melee": [ "weapon_melee", 0 ],
    "lunge": [ "weapon_melee", 0 ],
    "drop": [ "object_impacts", 0 ],
    "lod_far": [ "weapon_fire_lod", 1 ],
    "zoom": [ "game_event", 0 ],
}


def guess_type(name):

    # try to determine the appropriate sound type based on the given name 
    # assuming that the name actually has meaningful keywords
    # choose the sound type with the highest priority if there is more than one possible type

    sound_type = "unknown"
    possible_types = []

    for k in MY_TYPES:
        if k in name:
            possible_types.append(MY_TYPES[k])

    if possible_types != []: 
        best_type = possible_types[0]
        for t in possible_types:
            if t[1] > best_type[1]: best_type = t
        sound_type = best_type[0]

    if "lod" in name:
        if sound_type == "projectile_detonation": 
            return "projectile_detonation_lod"
        if sound_type == "weapon_fire": 
            return "weapon_fire_lod"
    
    return sound_type


def get_relative_path(absolute_path):

    # assuming the given path is an absolute path to a directory within the H3EK directory
    # trim the given path to get a relative path that Tool can use

    parts = absolute_path.split("\\")
    parts_count = len(parts)

    for i in range(parts_count):
        if parts[i] == "H3EK":
            return "\\".join(parts[i + 2:])


def write_command(command, primary_batch_file, secondary_batch_file):

    if command.endswith("unknown\n"):
        secondary_batch_file.write(command)
        return
    
    primary_batch_file.write(command)


def build_command(relative_path):

    def print_warning(name, path):
        print(f"WARNING: I have no idea what type of sound '{name}' should be\n{path}")
    
    sound_name = relative_path.split("\\")[-1]
    sound_type = guess_type(sound_name)
    
    # for sounds that are part of loops

    if sound_name in [ "in", "loop", "out" ]:

        # the file name has no keywords needed to determine sound type
        # try using the name of the parent directory of the parent directory

        parent_path = "\\".join(relative_path.split("\\")[0:-2])
        sound_type = guess_type(parent_path.split("\\")[-1])

        if sound_type == "unknown": 
            print_warning(sound_name, relative_path)

        # for sounds that are supposed to loop

        if sound_name == "loop":
            a = f"tool sounds-single-layer \"{relative_path}\" {sound_type}\n"
            b = f"tool sound-looping \"{parent_path}\" {sound_type}\n"
            return a + b

    # for everything else

    if sound_type == "unknown": 
        print_warning(sound_name, relative_path)

    return f"tool sounds-single-layer \"{relative_path}\" {sound_type}\n"


def create_batch_file(full_path):

    # look at all files and directories within the given directory
    # for any directory that contains WAV files 
    # write a command for compiling sounds in that directory

    with open(BAT_01, "w") as a, open(BAT_02, "w") as b:
        for p, d, f in os.walk(full_path):
            for file_name in f:
                if file_name.lower().endswith(".wav"):
                    c = build_command(get_relative_path(p))
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
PURPOSE

This Python program organizes WAV files produced by Reclaimer. Each file will be put into a folder. 
Files that are permutations of the same sound will be put in the same folder.

REQUIREMENTS

You need to have Python installed to use this Python program.
Some experience with command line tools would be nice too.

INSTRUCTIONS

when Reclaimer extracts sounds, the files are named according to a specific format.
That format can be changed in Reclaimer's settings. 
https://github.com/Gravemind2401/Reclaimer/wiki/Settings#sound-extractor

I recommend setting the format as {0}${1} or something similar.
{0} is the tag name, $ is the separator, and {1} is the permutation name.

Enter something like this in Command Prompt:
python sound_organizer.py <path-to-directory> <separator>

path-to-directory: path to directory that contains WAV files
separator: symbol between tag name and permutation name

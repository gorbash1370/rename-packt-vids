""" RENAME PACKT VIDEO FILES in format video1_1.mp4."""

import os
import re

###################### MANUAL COMPLETION SECTION #############################

""" Update Series names only """
# Ensure the spelling and capitalisation exactly matches the Table of Contents
series = {
    # Dictionary: standard Packt video filename, Series# and Series Name."""
    "video1": ["S01", "Mobile Devices"],
    "video2": ["S02", "Networking"], 
    "video3": ["S03", "Hardware"], 
    "video4": ["S04", "Virtualization and Cloud Computing"], 
    "video5": ["S05", "Troubleshooting Hardware and Networking"],
    }

""" Specify target folder containing files to be renamed"""
path_folder = "batch/" # path relative to script location

""" Specify file extension to target"""
ext = ".mp4" # NB: ALL the files in this folder with this file extension will be enumerated and processed!

""" Specify the path to the TOC.txt (Table of Contents) file. """
path_TOC = "batch/TOC.txt"


##############################################################################

""" Processes the Table of Contents .txt file into a list of strings, with all extra characters and newlines removed"""
with open(path_TOC, "r") as file:
    TOC = file.read()
TOCsplit = TOC.split("\n") # returns a list of strings, split at the newlines
# print(TOCsplit)
double_newline = "\n\n"
spaces4 = "    "
spaces8 = "        "
TOCsplitstripped = [s.replace(double_newline, "").replace(spaces4, "").replace(spaces8, "") for s in TOCsplit]
TOCsplitstripped = [item.strip() for item in TOCsplitstripped if item != ''] # remove empty strings and any leading/trailing whitespace around the strings
print(f"{TOCsplitstripped}\n")
# List of strings containing both the Series names and the Episode names mixed.


""" Splits the list into two lists: one with only the series names, and one with only the episode names"""
TOCseriesonly = [item for item in TOCsplitstripped if any(item == s[1] for s in series.values())] # add only the series names, excluding the episode names
display_TOCseriesonly = "\n".join(TOCseriesonly)
print(f"\nThe series names are:\n{display_TOCseriesonly}")
TOCepisodesonly = [item for item in TOCsplitstripped if item not in TOCseriesonly] # remove the series names
display_TOCepisodesonly = "\n".join(TOCepisodesonly)
print(f"\nThe episode names are:\n{display_TOCepisodesonly}")


""" Reads the current video filenames into a sorted list """
# Create list of current filenames of specified format in alphabetical order
original_filenames = [f for f in os.listdir(path_folder) if f.endswith(ext)]
sorted_filenames = sorted(original_filenames)
display_sorted_filenames = "\n".join(sorted_filenames)
print(f"\nIf episode numbers are more than single digit, the filenames will be displayed hire in an incorrect order: {display_sorted_filenames}")


""" Renames the files to ensure that the episode number is surrounded by underscores on both sides """
# Regex pattern to capture the digit before the file extension. This is in order to surround the full digit(s) with underscores either side (otherwise _12 will later be replaced by `01` and `02`)
pattern = re.compile(r'(\d)(\{})$'.format(ext))

for videofile in sorted_filenames:
    print(f"Filename before additional _: {videofile}")
    # Replace match with the same digit as captured followed by an underscore
    new_name = pattern.sub(r'\g<1>_\g<2>', videofile)
    print(f"Filename after additional _: {new_name}")
    # Rename the files on disc
    os.rename(os.path.join(path_folder, videofile), os.path.join(path_folder, new_name))

# sorted_filenames needs recompiling as the files have been renamed
original_filenames = [f for f in os.listdir(path_folder) if f.endswith(ext)]
sorted_filenames = sorted(original_filenames)
display_sorted_filenames = "\n".join(sorted_filenames)
print(f"\n Filenames should now have an episode number bound by underscores on both sides: {display_sorted_filenames}")


"Dictionary for Number Replacements"
# Required to correctly order files with single digit numbers (otherwise 10 ends up before 2, etc)
replacements = {"1": "01", "2": "02", "3": "03", "4": "04", "5": "05", "6": "06", "7": "07", "8": "08", "9": "09"}


""" For the new filename, replace: 
# a) video1 with S01 {series name} 
# b) the single digit episode numbers with a two digit representation (e.g. 1 with 01) so that the files are ordered correctly """

for file in sorted_filenames:
    print(f"Filename before: {file}")
    new_name = file
    for video_name, details in series.items():
        if video_name in file:
            new_name = new_name.replace(video_name, f"{details[0]} " + f"{details[1]}")
    for old_num, new_num in replacements.items():
        if f"_{old_num}_" in new_name:
            new_name = new_name.replace(f"_{old_num}_", f"_{new_num}_")
    print(f"Filename after: {new_name}")
    # Rename the files on disc
    os.rename(os.path.join(path_folder, file), os.path.join(path_folder, new_name))

# sorted_filenames needs recompiling as the files have been renamed
original_filenames = [f for f in os.listdir(path_folder) if f.endswith(ext)]
sorted_filenames = sorted(original_filenames)
display_sorted_filenames = "\n".join(sorted_filenames)
print(f"\nThe filenames should now be in a strictly correct numerical order, (also with the Series name inserted). If they are not, then the files will end up with incorrect names: {display_sorted_filenames}")


""" Checks if the number of files and the number of TOC entries match (i.e if ALL the video files for the full series are present). If not, cut the TOC length to match the files, to prevent an IndexError. See notes in README.md for full warning about TOC.txt entries which do not match the number of files."""

num_files = len(sorted_filenames)
print(f"Number of files: {num_files}")
num_episodes = len(TOCepisodesonly)
print(f"Number of TOC entries: {num_episodes}")
if int(num_files) != int(num_episodes):
    print("Number of files and TOC entries do not match. Cutting TOC length to match files.")
    TOCepisodestouse = TOCepisodesonly[0: len(sorted_filenames)]
else: 
    TOCepisodestouse = TOCepisodesonly

""" Renames the files to include the episode name, writing to disc. """
for index, episode_name in enumerate(TOCepisodestouse):
    print(f"Initial filename: {sorted_filenames[index]}")
    # Replace the _digit_ in the filename with " E{digit} {episode_name}" (file extension remains)
    pattern = re.compile(r'_(\d+)_')
    episode_title = TOCepisodestouse[index]
    new_name = pattern.sub(r' E\g<1> {}'.format(episode_title), sorted_filenames[index])
    print(f"Final filename: {new_name}")
    # Rename the files on disc
    os.rename(os.path.join(path_folder, sorted_filenames[index]), os.path.join(path_folder, new_name))
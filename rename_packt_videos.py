""" RENAME PACKT VIDEO FILES in format video1_1.mp4"""

"""Limitations: 
* 'Series' refers to a module in a full video course. S01 and E01 are used to maintain compatibility with whisper_wrapper.py transcription implementation.
* This Script only works for this EXACT format of file names
* No error handling etc.
* TOC:
* You can run this script on a full set of video files in a single course. You can also run it on an initial slice of the video files: but if you want to run it on a batch of video files which aren't at the START of the course (i.e. you want to run it on series/module 4 and 5, not 1-2-3, then you will have to modify the TOC.txt you supply to remove the earlier series/episodes. This is because the matching of file to new filename runs on a 1:1 basis. If the TOC
* is longer than the number of files, then the script will cut the TOC to match the number of files. (no problems here)
* If the TOC is shorter than the number of files, the script will throw an IndexError.
* If you try to rename just later files (so Module/Series 4 and 5 but not 1-2-3, without modifying the TOC, then the script will rename your files incorrectly. There is no intelligent check to make sure the correct name is being given to the correct file: it is simply processed in strict alphabetical order.)
* It is recommended to create a separate 'backup' folder and copy your originally named video files into it (packt always supply a zip, so they will also be in there if the zip isn't deleted after extraction) just incase there is an error with the renaming process. When the rename is complete, check the video filesizes in alphabetical order between the old and new folders to ensure the rename has happened in the correct order."""

"""Naturally, for your own use, just fill in the strings for the target TOC path and video target path directly. They are imported from config for confidentiality for sharing on GitHub."""

""" SETUP STEPS REQUIRED BEFORE RUNNING THIS SCRIPT:
* Create a TOC 'Table of Contents' txt file by copying the Series & Episode names from overview.html that Packt supplies in the 'Package' folder. See README.md. # Delete only the top line "Table of Contents" from the .txt file # SCREENSHOT
* Update path_TOC
* Update series dictionary (just type in the series or module names)
* Update target folder.
* Looking at TOC, ensure that there aren't any IDENTICAL Episode and Series names: this will mess the entire thing up.

"""
import os
import re
from config import path_TOC, path_folder # don't need these if supplying path string directly in variables below

""" ONLY MANUAL COMPLETION SECTION: Update Series Name only."""
# Ensure the spelling and capitalisation exactly matches the Table of Contents
series = {
    # Dictionary: standard Packt video filename, Series# and Series Name."""
    "video1": ["S01", "Mobile Devices"],
    "video2": ["S02", "Networking"], 
    "video3": ["S03", "Hardware"], 
    "video4": ["S04", "Virtualization and Cloud Computing"], 
    "video5": ["S05", "Troubleshooting Hardware and Networking"],
    }

"Dictionary of Number Replacements"
# Required to correctly order files with single digit numbers (otherwise 10 ends up before 2, etc)
replacements = {"1": "01", "2": "02", "3": "03", "4": "04", "5": "05", "6": "06", "7": "07", "8": "08", "9": "09"}


""" Process the Table of Contents .txt file into a list of strings, with all extra characters and newlines removed"""
path_TOC = r"D:\py_code_all\whisper_test\rename vids\Table of Contents_stripped.txt"
with open(path_TOC, "r") as file:
    TOC = file.read()
TOCsplit = TOC.split("\n") # returns a list of strings, split at the newlines
# print(TOCsplit)
double_newline = "\n\n"
spaces4 = "    "
spaces8 = "        "
TOCsplitstripped = [s.replace(double_newline, "").replace(spaces4, "").replace(spaces8, "") for s in TOCsplit]
TOCsplitstripped = [item for item in TOCsplitstripped if item != ''] # remove empty strings
print(f"{TOCsplitstripped}\n")
# List of strings containing both the Series names and the Episode names mixed.

""" Split the list into two lists: one with only the series names, and one with only the episode names"""
TOCseriesonly = [item for item in TOCsplitstripped if any(item == s[1] for s in series.values())] # add only the series names, excluding the episode names
display_TOCseriesonly = "\n".join(TOCseriesonly)
print(f"\nThe series names are:\n{display_TOCseriesonly}")
TOCepisodesonly = [item for item in TOCsplitstripped if item not in TOCseriesonly] # remove the series names
display_TOCepisodesonly = "\n".join(TOCepisodesonly)
print(f"\nThe episode names are:\n{display_TOCepisodesonly}")


"""Target folder"""
path_folder = r"C:\path\to\your\folder\containingvids" # absolute path
# OR
path_folder = "batch/" # path relative to script location

""".mp4 files"""

ext = ".mp4" # NB: ALL the files in this folder with this file extension will be enumerated and processed!

# Create list of current filenames of specified format in alphabetical order
original_filenames = [f for f in os.listdir(path_folder) if f.endswith(ext)]
sorted_filenames = sorted(original_filenames)
display_sorted_filenames = "\n".join(sorted_filenames)
print(f"\nIf episode numbers are more than single digit, the filenames will be displayed hire in an incorrectorder: {display_sorted_filenames}")

# Regex pattern to capture the digit before the file extension. This is in order to surround the full digit(s) with underscores either side (otherwise _12 will later be replaced by `01` and `02`)
pattern = re.compile(r'(\d)(\{})$'.format(ext))

for videofile in sorted_filenames:
    print(f"Filename before additional _: {videofile}")
    # Replace match with the same digit as captured followed by an underscore
    new_name = pattern.sub(r'\g<1>_\g<2>', videofile)
    print(f"Filename after additional _: {new_name}")
    os.rename(os.path.join(path_folder, videofile), os.path.join(path_folder, new_name))

# sorted_filenames needs recompiling as the files have been renamed
original_filenames = [f for f in os.listdir(path_folder) if f.endswith(ext)]
sorted_filenames = sorted(original_filenames)
display_sorted_filenames = "\n".join(sorted_filenames)
print(f"\n Filenames should now have an episode number bound by underscores on both sides: {display_sorted_filenames}")

# Replace 
# a) video1 with S01 {series name} 
# b) the single digit episode numbers with a two digit representation (e.g. 1 with 01) so that the files are ordered correctly
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
    os.rename(os.path.join(path_folder, file), os.path.join(path_folder, new_name))

# Sorted_filenames needs recompiling as the files have been renamed
original_filenames = [f for f in os.listdir(path_folder) if f.endswith(ext)]
sorted_filenames = sorted(original_filenames)
display_sorted_filenames = "\n".join(sorted_filenames)
print(f"\nThe filenames should now be in a strictly correct numerical order, (also with the Series name inserted). If they are not, then the files will end up with incorrect names: {display_sorted_filenames}")

# Check if the number of files and the number of TOC entries match (i.e if ALL the video files for the full series are present). If not, cut the TOC length to match the files, to prevent an IndexError
num_files = len(sorted_filenames)
print(f"Number of files: {num_files}")
num_episodes = len(TOCepisodesonly)
print(f"Number of TOC entries: {num_episodes}")
if int(num_files) != int(num_episodes):
    print("Number of files and TOC entries do not match. Cutting TOC length to match files.")
    TOCepisodestouse = TOCepisodesonly[0: len(sorted_filenames)]
else: 
    TOCepisodestouse = TOCepisodesonly

for index, episode_name in enumerate(TOCepisodestouse):
    print(f"Initial filename: {sorted_filenames[index]}")
    # want to replace the _digit_ in the filename with " E{digit} {episode_name}" (file extension should remain)
    pattern = re.compile(r'_(\d+)_')
    episode_title = TOCepisodestouse[index]
    new_name = pattern.sub(r' E\g<1> {}'.format(episode_title), sorted_filenames[index])
    print(f"Final filename: {new_name}")
    os.rename(os.path.join(path_folder, sorted_filenames[index]), os.path.join(path_folder, new_name))
    
# Intro rename_packt_vids
This is a simple script, written in 'Novice Python', to perform the fairly niche task of renaming Packt video course files according to the module (series) and episode title. 

Packt video course files are named formulaically: `video1_2.mp4` is (Series / Module 1, Episode 2).  
This script will rename files in this format: `S01 Mobile Devices - E02 Laptop Hardware and Components.mp4`. This use of `Sxx` and `Exx` is designed to feed into [whisper_wrapper](www.github.com/gorbash1370/whisper_wrapper) which will automatically detect `S01` and `E02` to populate the header fields in the transcript from the audio or video file name. 

[![Before and After](https://github.com/gorbash1370/rename_packt_vids/blob/main/misc/before_after_smaller.png)](https://github.com/gorbash1370/rename_packt_vids/blob/main/misc/before_after_large.png)

[![Series and Episodes](https://github.com/gorbash1370/rename_packt_vids/blob/main/misc/TOC_txt_small_annot.png)](https://github.com/gorbash1370/rename_packt_vids/blob/main/misc/TOC_txt_large_annot.PNG)


# Program Structure
* Single file `rename_packt_videos.py`.  

* No dependencies.

# Program Operation (high level)
* Reads the list of series and episodes in the TOC.txt, removes the extra lines and spacing to produce a clean list of the series and episode names `TOCsplitstripped`.
* References the `series` dictionary (user populated) and creates a list just of the series names `TOCseriesonly`.
* Creates a list of everything else in the TOC.txt (i.e. the episode names) to create a list of episode names `TOCepisodesonly`.
* Reads the video file names into a list (if the episode number in a series goes over 9, the order of the names will be incorrect at this point, which will be corrected later).
* Script surrounds the digit in the video file name with a trailing _ to isolate the complete number.
* Script adds a leading 0 to single digit numbers to ensure the alphanumeric order is correct.
* Script replaces "video1" with `S01 series_name`,"video2" with `S02 series_name`, etc.
* Script renames the video files on disc with these partial names, and reorders the list representation of their names (now strictly alphanumeric). The order is now a correct match for the TOC.txt entries.
* After checking that there are at least enough TOC.txt episode names for all the files, the script writes the correct episode name to the video file name on disc.


# Notes
* Script only works for this EXACT format of file names: `video1_1.mp4`, `video1_2.mp4`, `video1_3.mp4` etc, where `video1` means `series1` and the final `1.mp4`/`2.mp4`/`3.mp4` are the episode numbers. All the Packt downloaded videos I've seen follow this format.
* The word 'series' has been used throughout to maintain compatiblity with the [whisper_wrapper](https://github.com/gorbash1370/whisper_wrapper), however these can be thought of as 'modules' into which the course is divided. 
* There is no error handling. 
* Recommendation: copy the originally-named video files into a separate 'backup' folder (Packt supply their video files in zip, so there will always be a backup if the zip is kept after extraction) just incase there is an error with the renaming process. 
* Recommendation: When the rename is complete, check the filesizes of the renamed videos, in sorted order, against the ordered filesizes in 'backup' folder. Exact matches indicate files have been renamed correctly.
    - Alternatively, comment out the lines `os.rename(os.path.join(path_folder, file), os.path.join(path_folder, new_name))`, run the script and check the print statements to verify that the new names are correct. Then, uncomment the `os.rename` lines and run the script again to rename the files.
* There are a lot of terminal print statements, in order to verify at every stage that the correct renaming is taking place. They can always be commented out once you're happy with how the script works.


# User setup
1) Create a `TOC.txt` (Table of Contents) file: open the `overview.html` Packt supplies, copy the module/series and filenames, paste into a text file, save:  
[![overview.html to TOC.txt](https://github.com/gorbash1370/rename_packt_vids/blob/main/misc/overview_html_to_TOC_text_small.png)](https://github.com/gorbash1370/rename_packt_vids/blob/main/misc/overview_html_to_TOC_text_large.png)  
2) Check that there aren't any IDENTICAL series and episode names in the TOC.txt. If there are, the script will get confused and the files won't map correctly. If this happens, rename the episode (i.e. just put a 1 at the end of it. So, if there's a series called "Networking" and an episode (anywhere in the course) also called "Networking", you'd rename the episode to "Networking1" or "Networking_" or similar).  
**_You do not need to do ANYTHING to the formatting. Don't reorder any lines, don't move the series names around, don't take the series names out. The script will do everything to process the names._**  


It should look like this:  
[![TOC.txt](https://github.com/gorbash1370/rename_packt_vids/blob/main/misc/TOC_txt_small.PNG)](https://github.com/gorbash1370/rename_packt_vids/blob/main/misc/TOC_txt_large_annotated.png)

3) Populate `path_TOC` with the path to the `TOC.txt` file you created via copy/pasting the headings from the `overview.html` supplied in the Packt course .zip folder.  
![variable_strings](https://github.com/gorbash1370/rename_packt_vids/blob/main/misc/paths_string_options_.png)

4) Update the series dictionary with the series / module names only (the final string).
![Series Dictionary](https://github.com/gorbash1370/rename_packt_vids/blob/main/misc/series_dictionary_.png)

5) Populate `path_folder` with the path to the folder containing the video files you want to rename.    
6) Specify the `ext` variable with the file extension of the video files you want to rename (i.e. `.mp4`).  

And it's good to go!


# Notes about the TOC.txt file
[![overview.html Annotated](https://github.com/gorbash1370/rename_packt_vids/blob/main/misc/series_episodes_annot_small.PNG)](https://github.com/gorbash1370/rename_packt_vids/blob/main/misc/series_episodes_annot_large.PNG)  

[![TOC.txt Annotated](https://github.com/gorbash1370/rename_packt_vids/blob/main/misc/TOC_txt_small_annot.png)](https://github.com/gorbash1370/rename_packt_vids/blob/main/misc/TOC_txt_large_annot.PNG)   

It is important to understand that the transfer of new filename > video file is only partially intelligent. The script DOES pick out the series names and use these correctly for the `Sxx` part of the filename. And it does enforce strict alphanumeric ordering of the video file processing order (by adding a leading 0 before single digit numbers). 

But, episodes just map in the order they appear in TOC.txt onto the strictly ascending alphanumeric order of the video files, 1:1. Therefore:
- The simplest way to use this script is on a full course of videos: that way, the TOC episode list will exactly match the number of video files. 
- If you supply a partial course, _starting at the beginning_, the script will handle this situation. This will mean the list of episodes extracted from the TOC is longer than the number of files: the script will just trim the number of episode entries to match the number of the videos.
- However, if your batch of video files are NOT from the start of the course (i.e. you want to run renaming on episodes in series/module 4 and 5, but not on series 1, series 2, series 3), then you will have to remove the earlier series/episodes from TOC.txt.
- If the number of episodes from TOC.txt is less than the number of files, the script will throw an IndexError.

# gorbash1370 Disclaimer
This is an amateur project built mainly for coding practice, therefore please always inspect code before running. Use at your own risk!


# Licence
[Licence](https://github.com/gorbash1370/rename_packt_vids/tree/main/LICENSE)


# If you enjoy this project...
- If you find any bugs or errors, please do let me know.
- Please consider sending me some project feedback or any suggestions for improvement!
- [BuyMeACawfee](https://www.buymeacoffee.com/gorbash1370)

_Last code update 2024-02-21_
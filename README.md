# Intro
This is a simple script, written in 'Novice Python', to perform the fairly niche task of renaming Packt video course files according to the module (series) and episode title. 

Packt video course files are named formulaically: `video1_2.mp4` is (Series / Module 1, Episode 2). This script will rename files `S01 Mobile Devices - E02 Laptop Hardware and Components.mp4`. This use of `Sxx` and `Exx` is designed to feed into [whisper_wrapper](www.github.com/gorbash1370/whisper_wrapper) which will automatically detect `S01` and `E02` to populate the header fields in the transcript.


# Program Structure
Single file `rename_packt_videos.py`: this is all you need if you complete he user variables `path_TOC` and `path_folder` as strings directly within the file. 
![variable_strings](https://github.com/gorbash1370/rename_packt_vids/misc/paths_string_options)
Alternatively you can use a `config.py` file to import these variables.
![](https://github.com/gorbash1370/rename_packt_vids/misc/imports_optional.PNG)
No dependencies.

# Program Operation (high level)

# Notes
The word 'series' has been used throughout to maintain compatiblity with the [whisper_wrapper](www.github.com/gorbash1370/whisper_wrapper), however these could probably also be thought of as modules into which the course is divided. 


# User setup


# Limitations


# gorbash1370 Disclaimer
This is an amateur project built mainly for coding practice, therefore...
* Commentary may appear excessive (learning 'notes')
* Some code is expanded (rather than shortened & simplified) for learning clarity.
* I'm not a professional or trained Dev, so please always inspect code before running. Use at your own risk!


# Licence
[Licence]()


# If you enjoy this project...
- If you find any bugs or errors, please do let me know.
- Please consider sending me some project feedback or any suggestions for improvement!
- [BuyMeACawfee](https://www.buymeacoffee.com/gorbash1370)

_Last code update 2024-02-16_

[![Alt text for thumbnail](thumbnail_image_url)](larger_image_url)

![alt text](vids_before_naming.PNG) 

![alt text](overview_html_highlighted_large.PNG)
![alt text](overview_html_large.PNG)
![alt text](path_string_options.PNG)
![alt text](series_dictionary.PNG)
![alt text](TOC_txt_large.PNG)
![alt text](TOC_txt_large_annot.PNG)
![alt text](vids_after_naming.PNG)
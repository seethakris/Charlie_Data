# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 13:35:15 2015
@author: seetha

For Light Data Analysis
Take user input in this file and call other routines
"""

## Enter Main Folder containing stimulus folders to create text files

Tiff_File ='/Users/seetha/Desktop/Charlie_Data/Ala1uM_Trial5_Z=2_C=1.tif'
filename_save_prefix = 'Hb_Time285' ## Prefix this to the name of the result.

#Experiment parameters
#X and Y size of image- if there are images that dont have this resolution, they will be resized
img_size_x = 256
img_size_y = 512

### If you need to crop pixels on the side ########
img_size_crop_y1 = 0 #How many pixels to crop on x and y axis. If none say 0
img_size_crop_y2 = 0
img_size_crop_x1 = 0 #How many pixels to crop on x and y axis. If none say 0
img_size_crop_x2 = 0

# Time period within which to do the analysis
time_start = 0
time_end = 86

#Stimulus on and off time and define onset and offset times of the light stimulus
stimulus_pulse = 1 

if stimulus_pulse == 1:
    stimulus_on_time = [46] # On time for each pulse
    stimulus_off_time = [65] # Off time for each pulse

    
## Median filter - threshold
median_filter_threshold = 1

## If you want to normalize using a baseline, specify starting and ending timepoints
delta_ff = 1 ## If 0, dont do deltaf/f. If 1, do it
f0_start = 0
f0_end = 5
######################################################################



######################################################################
########################## Run Scripts ###############################

# Go into the main function that takes thunder data and 
from create_heatmaps import create_heatmaps_individual
Working_Directory = Tiff_File[0:Tiff_File.rfind('/')+1]
name_for_saving_files = filename_save_prefix + '_' + Tiff_File[Tiff_File.rfind('/')+1:-4]

create_heatmaps_individual(Tiff_File, Working_Directory, name_for_saving_files, \
img_size_x, img_size_y, img_size_crop_x1, img_size_crop_x2, img_size_crop_y1, img_size_crop_y2,  \
time_start,time_end, median_filter_threshold, stimulus_on_time, stimulus_off_time, delta_ff , f0_start, f0_end)





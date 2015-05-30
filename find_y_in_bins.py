# -*- coding: utf-8 -*-
"""
Created on Thu May 28 23:40:35 2015

@author: seetha
"""
############################# User Input ##############################
Folder_Name = '/Users/seetha/Desktop/Charlie_Data/'
Text_File_Name = '150515 kiss1f346 NTDSS fish 1.txt'

#Height of tank
Y_start = 0
Y_end = 256

### Frames per second 
fps = 7

###### Specify bins in seconds #######
ybin_start = [10, 150]
ybin_end = [80, 180]




################################## Main Script ###########################
from numpy import array, where, logical_and, size, zeros, int, vstack
import pandas as pd 
import os 
from copy import copy
filesep = os.path.sep
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import matplotlib.pyplot as plt

#############Create Figures Directory and PDF
Figure_PDFDirectory = Folder_Name + 'Figures/'
if not os.path.exists(Figure_PDFDirectory):
        os.makedirs(Figure_PDFDirectory) 

#Create directory for Csv files
CSV_Directory = Folder_Name + 'CSV/'

name_csv_file_50 = 'Number_of_Frames_below_50.csv'
name_csv_file_25 = 'Number_of_Frames_below_25.csv'

if not os.path.exists(CSV_Directory):
        os.makedirs(CSV_Directory) 
        
### Get 1/2 y and 1/4 Y #########3########
Y_50_percent = Y_end-(Y_end-Y_start)/2
Y_25_percent = Y_end-(Y_end-Y_start)/4

Colors = sns.color_palette('Set2', len(ybin_start))

### Get all text files        
Txt_Files_in_Folder = [f for f in os.listdir(Folder_Name) if f.endswith('.txt')]    

#####Initialize frame counts
Count_50_percent = zeros((len(Txt_Files_in_Folder), len(ybin_start)), dtype = int)
Count_25_percent = zeros((len(Txt_Files_in_Folder), len(ybin_start)), dtype = int)
Bins = list()

sns.set_context('talk')
sns.axes_style('darkgrid')

for index, Text_File_Name in enumerate(Txt_Files_in_Folder):
    
    name_for_saving_files = Text_File_Name[:-4] + '_Frames in specific bins'
    pp = PdfPages(Figure_PDFDirectory+name_for_saving_files+'.pdf')
    
    print "Analysing" + Text_File_Name
    All_Data = pd.read_csv(Folder_Name+Text_File_Name, header=0, delimiter='\t')
    
    # Seprate X and Y coordinates
    Y = array(All_Data[' "Y"'])
    X = array(All_Data[' "X"'])
    
    ## Plot frames below 50 and 25 percent in different bins with different colors
        
    fig1 = plt.figure()
    ax1 = plt.subplot((221))
    ax1.plot(X,Y, color=sns.xkcd_rgb['light navy blue'], lw=2)
    plt.ylim((Y_end, Y_start))
    plt.title('Frames with fish below 50 percent of tank')

    
    ax2 = plt.subplot((222))
    ax2.plot(X,Y, color=sns.xkcd_rgb['light navy blue'], lw=2)
    plt.ylim((Y_end, Y_start))
    plt.title('Frames with fish below 25 percent of tank')
    
    ax3 = plt.subplot((223))
    
    ## Get all Frames. 
    Frames_50_percent = where(Y>Y_50_percent)[0]
    Frames_25_percent = where(Y>Y_25_percent)[0]
        
    
    for jj in xrange(0,len(ybin_start)):
        ### Convert seconds to frames and count
        ybin_start_frame = ybin_start[jj]*fps
        ybin_end_frame = ybin_end[jj]*fps        
                
        ## Number of frames 
        Frames_50_percent_bin = where(logical_and(Frames_50_percent>=ybin_start_frame\
        , Frames_50_percent<=ybin_end_frame))[0]        
        Count_50_percent[index,jj] = size(Frames_50_percent_bin)
        
        Frames_25_percent_bin = where(logical_and(Frames_25_percent>=ybin_start_frame\
        , Frames_25_percent<=ybin_end_frame))[0]
        Count_25_percent[index,jj] = size(Frames_25_percent_bin)
        
        ## Plot frames below 50 and 25 percent in different bins with different colors
        ax1.plot(X[Frames_50_percent[Frames_50_percent_bin]], Y[Frames_50_percent[Frames_50_percent_bin]], 'o',markersize=8, color = Colors[jj])
        ax2.plot(X[Frames_25_percent[Frames_25_percent_bin]], Y[Frames_25_percent[Frames_25_percent_bin]], 'o', markersize=8, color = Colors[jj])
        
        ax3.plot(vstack([Count_50_percent[index,jj],Count_25_percent[index,jj]]), '*', markersize = 10, color=Colors[jj])       
        plt.locator_params(axis = 'x', nbins = len(ybin_start))
        
        # String file from bins
        if index == 0:
            Bins.append((str(ybin_start[jj])+ 's To ' + str(ybin_end[jj]) + 's'))
    
    ### Some plotting aesthetics
    plt.ylabel('Number of frames')
    labels = [item.get_text() for item in ax3.get_xticklabels()]
    labels[1] = 'Below 50%'
    labels[2] = 'Below 25%'
    
    ax3.set_xticklabels(labels)
    plt.xlim((-0.1,1.1))
    Legend_String = copy(Bins)
    Legend_String.insert(0,'All Frames')
    ax2.legend(Legend_String, loc='lower center', bbox_to_anchor=(0.5,-0.5), fancybox=True, shadow = True)

    ### Save plot    
    fig1 = plt.gcf()
    pp.savefig(fig1)
    plt.close()

    pp.close()
    
       
#### Prepare pandas to store as csv
Frame_count_in_bins_50 = pd.DataFrame(index = Txt_Files_in_Folder)
Frame_count_in_bins_25 = pd.DataFrame(index = Txt_Files_in_Folder)


for jj in xrange(0,len(ybin_start)):
    
    if index == 0 and jj == 0:
        
        Frame_count_in_bins_50 = pd.DataFrame({Bins[jj]:Count_50_percent[:,jj]}, index = Txt_Files_in_Folder)
        Frame_count_in_bins_25 = pd.DataFrame({Bins[jj]:Count_25_percent[:,jj]}, index = Txt_Files_in_Folder)

    else:            
        
        Frame_count_in_bins_50 = pd.concat((Frame_count_in_bins_50, pd.DataFrame({Bins[jj]:Count_50_percent[:,jj]}, index = Txt_Files_in_Folder)), axis = 1)
        Frame_count_in_bins_25 = pd.concat((Frame_count_in_bins_25, pd.DataFrame({Bins[jj]:Count_25_percent[:,jj]}, index = Txt_Files_in_Folder)), axis = 1)

## Save as csv
Frame_count_in_bins_25.to_csv((CSV_Directory+name_csv_file_25))
Frame_count_in_bins_50.to_csv((CSV_Directory+name_csv_file_50))
        
        
    
    
    
    
    
    
    
    
    

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 12:45:57 2015

@author: seetha
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 20 19:02:09 2015

@author: seetha
"""

##### User Input ######
Folder_Name = '/Users/seetha/Desktop/Charlie_Data/Data/'

#Height of tank
Y_start = 0
Y_end = 256

Frames_per_sec = 7 
Pixels_to_mm = 0.39
Standard_deviation_for_darting = 6
Speed_threshold_for_pausing = 3.5
Number_of_bins_for_freezing = 5

### Import Some libraries #############
from numpy import array, all, where,ones, arange, logical_and, size, zeros, int, float, sqrt, std
import pandas as pd 
import os 
filesep = os.path.sep
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import matplotlib.pyplot as plt
import time

################################## Main Script ##################################
#Create Figures Directory and PDF
Figure_PDFDirectory = Folder_Name + 'Figures/'
if not os.path.exists(Figure_PDFDirectory):
        os.makedirs(Figure_PDFDirectory) 

#Create directory for Csv files
CSV_Directory = Folder_Name + 'CSV/'
if not os.path.exists(CSV_Directory):
        os.makedirs(CSV_Directory) 
        
################################## Load Data ######################################
Txt_Files_in_Folder = [f for f in os.listdir(Folder_Name) if (f.endswith('.txt') or f.endswith('.csv'))]    

######### Initialise all variable ####################
Darting_bins_count = zeros(size(Txt_Files_in_Folder), dtype=int)
Pausing_bins_count = zeros(size(Txt_Files_in_Folder), dtype=int)
Froze_bins_count = zeros(size(Txt_Files_in_Folder), dtype=int)
    
for index, Text_File_Name in enumerate(Txt_Files_in_Folder):
    
    print "Analysing" + Text_File_Name
   

    ################ For saving as csv #############################
    csv_file_per_fish = Text_File_Name[:-4] + '_Speed_Analysis.csv'
    
    ################  Load Data #####################################
    if Text_File_Name.find(".csv") > 0: #As CSV
        All_Data = pd.read_csv(Folder_Name+Text_File_Name, header=0, delimiter=',')
    else: #As text
        All_Data = pd.read_csv(Folder_Name+Text_File_Name, header=0, delimiter='\t')
    
    ############  Seprate X and Y coordinates ######################
    Y = array(All_Data[' "Y"'])
    X = array(All_Data[' "X"'])
    
    #### Correct Frames to have exact number of bins 
    if size(X)%Frames_per_sec != 0:
#        print "Number of Frames " + str(size(X)) + " not divisible by " + str(Frames_per_sec) + " Resizing..."
        Y = Y[:-(size(X)%Frames_per_sec)]
        X = X[:-(size(X)%Frames_per_sec)]

        
    ######### Find Speed in pixels and bins ############
    
    ### Initialize variables
        
    count = 0
    Bin_Number = zeros((size(X)/Frames_per_sec), dtype=int)
    Speed_bin_pixel = zeros((size(X)/Frames_per_sec), dtype=float)
    Speed_bin_mm = zeros((size(X)/Frames_per_sec), dtype=float)
    
    ### Collect bins and sum distance travelled in the bins
    for ii in range(0,size(X), Frames_per_sec):
        Bin_Number[count] = count 
        X_bin = X[ii:ii+Frames_per_sec]
        Y_bin = Y[ii:ii+Frames_per_sec]
        Distance_bin = zeros(Frames_per_sec-1, dtype=float)
        for jj in range(0,Frames_per_sec-1):
            Distance_bin[jj] = sqrt(pow(X_bin[jj]-X_bin[jj+1],2) + pow(Y_bin[jj]-Y_bin[jj+1],2))
        
        Speed_bin_pixel[count] = sum(Distance_bin)
        Speed_bin_mm[count] = sum(Distance_bin)*Pixels_to_mm
        count = count + 1
        
    
    ### Calculate parameters based on speed ######################
    Std_speed = std(Speed_bin_mm)
    Darting_bins_count[index] = size(Speed_bin_mm[Speed_bin_mm>(Standard_deviation_for_darting*Std_speed)])
    Pausing_bins_count[index] = size(Speed_bin_mm[Speed_bin_mm<Speed_threshold_for_pausing]) 
    Paused_bins = (Speed_bin_mm<Speed_threshold_for_pausing)*1
    
    count = 0
    ii = 0
    Froze_bins = zeros(size(Paused_bins), dtype=int)
    while ii < size(Paused_bins):
        if Paused_bins[ii] == 1:
#            print "Freezing at bin...." + str(ii)
            if all(Paused_bins[ii:ii+Number_of_bins_for_freezing]==1):
                count += 1
                Froze_bins[ii] = 1
                Froze_bins_count[index] = count
                ii = ii + Number_of_bins_for_freezing
            else:
                ii = ii + 1
        else:
            ii = ii + 1
            
    ########## Save Data for individual fish ##############
    Fish_Speed_Data = pd.DataFrame({'Bin_Number':Bin_Number, 'Speed (pixel/bin)':Speed_bin_pixel,\
    'Speed(pixel/mm)':Speed_bin_mm, 'Pause':Paused_bins, 'Freezing':Froze_bins})
    Fish_Speed_Data = Fish_Speed_Data.reindex(columns=['Bin_Number', 'Speed (pixel/bin)', 'Speed(pixel/mm)',\
    'Pause','Freezing'])
    Fish_Speed_Data.to_csv(CSV_Directory+csv_file_per_fish)

############ Save data for all fish #############################
All_Fish_Speed_Data = pd.DataFrame({'Fish_Name':Txt_Files_in_Folder, 'Darting Count':Darting_bins_count,\
'Pausing Count':Pausing_bins_count, 'Freezing Count': Froze_bins_count})
All_Fish_Speed_Data = All_Fish_Speed_Data.reindex(columns=['Fish_Name', 'Darting Count', 'Pausing Count', 'Freezing Count'])
All_Fish_Speed_Data.to_csv(CSV_Directory+'Speed_Parameters_AllFish.csv')

########## Plot all data ######################################
with sns.axes_style('darkgrid'):
    colors = ["pale red", "medium green", "denim blue"]
    ################### Arrange for plotting #######################
    name_file = 'Speed_Parameters_AllFish_Plot'    
    pp = PdfPages(Figure_PDFDirectory+name_file+'.pdf')          
    sns.set_context("poster")  
    for ii in xrange(0, size(Txt_Files_in_Folder)):
        for jj in xrange(1,4):
            ax1 = plt.plot(ii, All_Fish_Speed_Data.ix[ii,jj],\
            's', markersize=20, markeredgecolor='white', \
            markeredgewidth=2, markerfacecolor=sns.xkcd_rgb[colors[jj-1]])
            plt.xticks(arange(0, size(Txt_Files_in_Folder)+1, 1.0),\
            Txt_Files_in_Folder, rotation = 'vertical')
            plt.xlim(-1, size(Txt_Files_in_Folder))

            plt.legend(['Darting', 'Pausing', 'Freezing'])
    
    ax1 = plt.gcf()
    plt.show()
    pp.savefig(ax1) #Save as pdf
    plt.close()

    pp.close()
    


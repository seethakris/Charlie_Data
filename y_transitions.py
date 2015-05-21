# -*- coding: utf-8 -*-
"""
Created on Wed May 20 19:02:09 2015

@author: seetha
"""
from numpy import array, where, logical_and, size
import pandas as pd 
import os 
filesep = os.path.sep
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import matplotlib.pyplot as plt

##### User Input ######
Folder_Name = '/Users/seetha/Desktop/Charlie_Data/'
Text_File_Name = '150515 kiss1f346 NTDSS fish 1.txt'

#Height of tank
Y_start = 0
Y_end = 256


################################## Main Script ##################################
#Create Figures Directory and PDF
Figure_PDFDirectory = Folder_Name + 'Figures/'
if not os.path.exists(Figure_PDFDirectory):
        os.makedirs(Figure_PDFDirectory) 
name_file = Text_File_Name[:-4] + 'Fish_Behavior_Plots'    
pp = PdfPages(Figure_PDFDirectory+name_file+'.pdf')          
sns.set_context("poster")  

#Load Data
All_Data = pd.read_csv(Text_File_Name, header=0, delimiter='\t')

# Seprate X and Y coordinates
Y = array(All_Data[' "Y"'])
X = array(All_Data[' "X"'])

Y_mid = (Y_end-Y_start)/2 #Mid Line

## Find number of frames where fish crossed midline
Y_before = Y[1:]
Y_after = Y[:-1]

Frames = where(logical_and(Y_before<Y_mid, Y_after>=Y_mid))[0]

## Save the crossed frames, X,Y - [Before, After]
crossed_Frames_X = array([X[Frames], X[Frames+1]]).transpose()
crossed_Frames_Y = array([Y[Frames], Y[Frames+1]]).transpose()

## Plot Fish trajestory with midline
with sns.axes_style("darkgrid"):
    ax = plt.plot(X,Y) #Plot all points
    for ii in xrange(0,size(Frames,0)):
        ax= plt.plot(crossed_Frames_X[ii,:],crossed_Frames_Y[ii,:], '-', color='r') #Points where the fish crossed the midline
        ax = plt.plot(crossed_Frames_X[ii,0], crossed_Frames_Y[ii,0],'o', color = 'g', markersize=8) #Mark green o for the first frame
        ax = plt.plot(crossed_Frames_X[ii,1],crossed_Frames_Y[ii,1],'o', color = 'm', markersize=8) # Mark red o for next frame
        
    ax = plt.axhline(y=Y_mid, linestyle='-', color='k', linewidth=3)
    plt.gca().invert_yaxis()
    
    ax = plt.gcf()
    pp.savefig(ax) #Save as pdf
    plt.close()

pp.close()


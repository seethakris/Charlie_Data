# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 18:16:12 2015

@author: seetha
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 15:16:53 2015
Create a variety of text file according to input
@author: chad
"""

#Import relevant libraries
import numpy as np #for numerical operations on arrays
import PIL as pil # for image resizing

import os
filesep = os.path.sep

import matplotlib.pyplot as plt #for plotting
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
from libtiff import TIFF #for reading multiTiffs
from scipy import ndimage


def create_heatmaps_individual(Tiff_File, Working_Directory, name_for_saving_files,  \
img_size_x, img_size_y, img_size_crop_x1, img_size_crop_x2, img_size_crop_y1, img_size_crop_y2,  \
time_start,time_end, median_filter_threshold, stimulus_on_time, stimulus_off_time, delta_ff, f0_start, f0_end):

    pp = create_pdf(Working_Directory, name_for_saving_files) #To save as pdf
    
    #Send the file paths to get tiff files and convert them to mat and crop or resize appropriately
    data_filtered_mat = convert_tiff_to_mat(Tiff_File, img_size_x, img_size_y,\
    img_size_crop_x1, img_size_crop_x2, img_size_crop_y1, img_size_crop_y2, median_filter_threshold)    
    
    
    #Plot figures
    print "Plotting Heatmaps..."
    plot_pdf(data_filtered_mat, name_for_saving_files+' Filtered', pp) 
    
    #Create proper matrix for textfile
    get_heatmap(data_filtered_mat, name_for_saving_files,\
    pp,stimulus_on_time, stimulus_off_time, delta_ff, f0_start, f0_end)
    
    #Save as textfile
    pp.close()        
    
############################ Converts tiff files to numpy arrays and resizes and crops image if required
def convert_tiff_to_mat(Tiff_File, img_size_x, img_size_y,\
    img_size_crop_x1, img_size_crop_x2, img_size_crop_y1, img_size_crop_y2, median_filter_threshold):     
    
    tif1 = TIFF.open(Tiff_File, mode='r') #Open multitiff 
     #Initialize data matrix based on number of planes in the multitiff        
    count_t = 0
    for image in tif1.iter_images():
        count_t = count_t + 1  
        
    data_filtered = np.zeros((img_size_x-(img_size_crop_x1+img_size_crop_x2), img_size_y-(img_size_crop_y1+img_size_crop_y2), count_t), dtype=np.uint8)
    
    data_filtered = get_tif_images_filtered(data_filtered, tif1, \
    img_size_x, img_size_y, img_size_crop_x1,img_size_crop_x2, img_size_crop_y1, \
    img_size_crop_y2,median_filter_threshold)
    
    
    return data_filtered
     

def get_tif_images_filtered(data_filtered, tif, \
img_size_x, img_size_y, img_size_crop_x1,img_size_crop_x2, img_size_crop_y1, \
img_size_crop_y2,median_filter_threshold): 
        
    #Store tiff in numpy array data
    count_t = 0
    for image in tif.iter_images():
        if image.dtype == 'uint16':
            if count_t==0:
                print "Converting to uint8..."
            image = np.uint8(image/255)
        ##Resizing if required
        if np.size(image,1)!=img_size_y or np.size(image,0)!=img_size_x:
            if count_t==0:
                print "Resizing image..."
            temp_image = pil.Image.fromarray(image)
            temp_image1 = np.array(temp_image.resize((img_size_y, img_size_x), pil.Image.NEAREST)) 
            temp_image1.transpose()
        else:
            temp_image1 = image
        
        #Cropping unwanted pixels if required
        if img_size_crop_x1!= 0 and img_size_crop_y1!=0:
            if count_t==0:
                print "Cropping x and y pixels.."
            temp_image2 = temp_image1[img_size_crop_x1:-img_size_crop_x2, img_size_crop_y1:-img_size_crop_y2]
        elif img_size_crop_x1!=0 and img_size_crop_y1==0:
            if count_t==0:
                print "Cropping only x pixels.."
            temp_image2 = temp_image1[img_size_crop_x1:-img_size_crop_x2, :]
        elif img_size_crop_x1==0 and img_size_crop_y1!=0:
            if count_t==0:                
                print "Cropping only x pixels.."
            temp_image2 = temp_image1[:, img_size_crop_y1:-img_size_crop_y2]
        else:
            temp_image2 = temp_image1        
        data_filtered[:,:,count_t] = ndimage.median_filter(temp_image2, median_filter_threshold)
        
        count_t=count_t+1
        
    return data_filtered
         
    
### Create backend Pdf pages for saving
def create_pdf(Working_Directory, name_for_saving_files):
        
    # To plot as PDF create directory
    Figure_PDFDirectory = Working_Directory
    pp = PdfPages(Figure_PDFDirectory+name_for_saving_files+'_CheckRawData.pdf')
    return pp
    
        
        
def plot_pdf(data, name_for_saving_figures, pp):
    #Plot average data over time for reviewingin grayscale      
    with sns.axes_style("white"):
        data = np.transpose(data,(1,0,2))
        fig1 = plt.imshow(np.mean(data, axis=2), cmap='gray')
        
        plt.title(name_for_saving_figures)
        plt.axis('off')
        fig1 = plt.gcf()
        pp.savefig(fig1)
        plt.close()
            
#Create numpy arrays to save as textfiles 
def get_heatmap(data_mat, name_for_saving_files,  pp,stimulus_on_time, stimulus_off_time,delta_ff, f0_start, f0_end):
    
    #Plot heatmap for validation 
    A1 = np.reshape(data_mat, (np.size(data_mat,0)*np.size(data_mat,1), np.size(data_mat,2)))
    if delta_ff == 1:
        delta_ff_A1 = np.zeros(np.shape(A1))
        for ii in xrange(0,np.size(A1,0)):
            delta_ff_A1[ii,:] = (A1[ii,:]-np.mean(A1[ii,f0_start:f0_end]))/(np.std(A1[ii,f0_start:f0_end])+0.1)
        B = np.argsort(np.mean(delta_ff_A1, axis=1))  
        print np.max(delta_ff_A1)
    else:
        B = np.argsort(np.mean(A1, axis=1)) 
        print np.max(A1)

    with sns.axes_style("white"):
        C = A1[B,:][-2000:,:]

        fig2 = plt.imshow(C,aspect='auto', cmap='jet', vmin = np.min(C), vmax = np.max(C))
        
        plot_vertical_lines_onset(stimulus_on_time)
        plot_vertical_lines_offset(stimulus_off_time)
        plt.title(name_for_saving_files)
        plt.colorbar()
        fig2 = plt.gcf()
        pp.savefig(fig2)
        plt.close()
    
  
def plot_vertical_lines_onset(stimulus_on_time):
    for ii in xrange(0,np.size(stimulus_on_time)):
        plt.axvline(x=stimulus_on_time[ii], linestyle='-', color='k', linewidth=1)

def plot_vertical_lines_offset(stimulus_off_time):
    for ii in xrange(0,np.size(stimulus_off_time)):
        plt.axvline(x=stimulus_off_time[ii], linestyle='--', color='k', linewidth=1)
        
    
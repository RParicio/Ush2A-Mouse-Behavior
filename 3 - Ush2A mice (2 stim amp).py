# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 17:02:44 2018

@author: Admin
"""

import matplotlib.pyplot as plt
import pylab as pl
import numpy as np
import h5py
import pickle

# ----------------------------------------------------------------------------
animal = 4
directory = 'C:/Users/Admin/Desktop/Ush Py Files/2 3V1V 12.5.18/animal004/session001/data.h5'
save_PSTH = True  # If True, we create a 'pickle' file with the PSTH saved, that we can later load

# ----------------------------------------------------------------------------
# Settings
square = False
calculate_basic = True
optogenetics = True
lick_rate = False
mean_latency = False
PSTH = True
PSTH_optogenetics = False
full_PSTH = True
plot_basic =False
plot_hits = False
plot_light = False

baseline = 32.
threshold = 0.2
time_window = 4000
time_window_catch = 4000
length_of_stim = 4000

ratio_time = 1000
ratio_time_float = ratio_time*1.

#------------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# We load the H5PY file 
  
with h5py.File(directory,'r') as hf:
    #print('List of arrays in this file: \n', hf.keys())
    data = hf.get('data')
    np_data = np.array(data)
    #print('Shape of the array dataset_1: \n', np_data.shape)
    
# ----------------------------------------------------------------------------
# We find out how many time points we have in our data (i.e. how many samples were taken)
number_of_time_points = len(np_data)

# ----------------------------------------------------------------------------
# We read all the data. Each array will be composed of different information:
# 1st column (0) --> time point                             dtype = '<u4'
# 2nd column (1) --> finished late  (0 = no; 1 = yes)       dtype = 'u1'
# 3rd column (2) --> temp out                               dtype = '<f4'
# 4th column (3) --> temp in                                dtype = '<f4'
# 5th column (4) --> lick in                                dtype = '<f4'
# 6th column (5) --> stim           (0 = no; 1 = yes)       dtype = 'u1'
# 7th column (6) --> catch          (0 = no; 1 = yes)       dtype = 'u1'
# 8th column (7) --> lick           (0 = no; 1 = yes)       dtype = 'u1'
# 9th column (8) --> reward         (0 = no; 1 = yes)       dtype = 'u1'
# 10th column (9) --> light         (0 = no; 1 = yes)       dtype = 'u1'
# 11th column (10) --> backlight    (0 = no; 1 = yes)       dtype = 'u1'
# 12th column (11) --> square       (0 = no; 1 = yes)       dtype = 'u1'

# NOTE: STIM COLUMN INCLUDES BOTH STIMULI AND FALSE STIMULI (CATCH)!!

array_time_raw = []
array_finished_late = []
array_temp_out = []
array_temp_in = []
array_lick_in = []
array_stim = []
array_catch = []
array_lick = []
array_reward = []
array_light = []
array_backlight = []
array_square = []

for i in range (0,len(np_data),1):
    array_time_raw.append(np_data[i][0])
    #array_finished_late.append(np_data[i][1])
    array_temp_out.append(np_data[i][2])
    array_temp_in.append(np_data[i][3])
    #array_lick_in.append(np_data[i][4])
    array_stim.append(np_data[i][5])
    array_catch.append(np_data[i][6])
    array_lick.append(np_data[i][7])
    #array_reward.append(np_data[i][8])
    if square == False:    
        array_light.append(np_data[i][9])
        array_backlight.append(np_data[i][10])
    if square == True:    
        array_square.append(np_data[i][11])

if square == False:
    array_square = array_light        
# ----------------------------------------------------------------------------
# We "fix" the array time, so it starts from 0 and it is displayed in seconds 
array_time = np.arange(len(np_data))
factor = 1000.
array_time = [x / factor for x in array_time]

# ----------------------------------------------------------------------------
# We transform the stim array (contains also catch) into a true stimuli array
array_true_stim = np.array(array_stim)-np.array(array_catch)

'''
# We shorten the true stim array, taking into account the time window in which a lick is recognized
for i in range(0,len(array_true_stim)-1,1):
    if array_true_stim[i] == 0 and array_true_stim[i+1] == 1:
        for e in range(i+time_window,length_of_stim-time_window,1):
            array_true_stim[e] = 0
'''
# ----------------------------------------------------------------------------
# We calculate the basic parameters for our behavioral task (hits, catch)

if calculate_basic == True:
                
    stim_times = []
    stim_already = False    
    for i in range(0,len(array_true_stim),1):
        if stim_already == False:
            if array_true_stim[i] == 1:
                stim_times.append(i)
                stim_already = True
        if stim_already == True:
            if array_true_stim[i] == 0:
                stim_already = False
                
    #--------------------------------------------------------------------------
    # We split the stim_times into 2 lists: one for each stimulus amplitude
    #--------------------------------------------------------------------------
    stim_times_amplitudes = []
    for s in stim_times:
        amplitude = []
        for i in range(s,s+time_window,1):
            amplitude.append(array_temp_out[i])
        stim_times_amplitudes.append(np.max(amplitude))
    stim_times_1 = [] # Stimulus times for Amplitude #1, which will be lower
    stim_times_2 = [] # Stimulus times for Amplitude #2, which will be higher
    amplitude_1 = np.min(stim_times_amplitudes)
    amplitude_2 = np.max(stim_times_amplitudes)
    for i in range(0,len(stim_times),1):
        if stim_times_amplitudes[i] == amplitude_1:
            stim_times_1.append(stim_times[i])
        elif stim_times_amplitudes[i] == amplitude_2:
            stim_times_2.append(stim_times[i])
    #--------------------------------------------------------------------------
      
    catch_stim_times = []    
    catch_trial_already = False    
    for i in range(0,len(array_catch),1):
        if catch_trial_already == False:
            if array_catch[i] == 1:
                catch_stim_times.append(i)
                catch_trial_already = True
        if catch_trial_already == True:
            if array_catch[i] == 0:
                catch_trial_already = False
            
    hit_times = []
    hit_latencies = []
    hit_already = False
    '''for i in range(0,len(array_true_stim),1):
        if array_true_stim[i] == 1 and hit_already == False:
            if array_lick[i] == 1:
                hit_times.append(i)
                hit_latencies.append(i-stim_times[-1])
                hit_already = True
        elif array_true_stim[i] == 0 and hit_already == True:
            hit_already = False
    '''
    # We obtain the hit times and latencies for both types of stimulus    
    hit_times_1 = []
    hit_latencies_1 = []   
    for i in stim_times_1:
        hit_already = False
        for e in range(i,i+time_window,1):
            if array_lick[e] == 1 and hit_already == False:
                hit_times_1.append(e)
                hit_latencies_1.append((e-i)/1000.)
                hit_already = True
    hit_times_2 = []
    hit_latencies_2 = []   
    for i in stim_times_2:
        hit_already = False
        for e in range(i,i+time_window,1):
            if array_lick[e] == 1 and hit_already == False:
                hit_times_2.append(e)
                hit_latencies_2.append((e-i)/1000.)
                hit_already = True
                
    
    catch_times = []
    catch_latencies = []
    for i in catch_stim_times:
        catch_already = False
        for e in range(i,i+time_window,1):
            if array_lick[e] == 1 and catch_already == False:
                catch_times.append(e)
                catch_latencies.append((e-i)/1000.)
                catch_already = True

        
# -----------------------------------------------------------------------------
print '-------------------------------------------------------------------'    
print 'Hits, low amplitude: ',len(hit_times_1),'/',len(stim_times_1)
print 'Hits, high amplitude: ',len(hit_times_2),'/',len(stim_times_2)
print 'Catch:',len(catch_times),'/',len(catch_stim_times)
print '-------------------------------------------------------------------'
print 'Hit ratio, Low amp: ',round(100*((len(hit_times_1)-0.)/len(stim_times_1)),2),'%'
print 'Hit ratio, High amp: ',round(100*((len(hit_times_2)-0.)/len(stim_times_2)),2),'%'
print 'Catch ratio: ',round(100*((len(catch_times)-0.)/len(catch_stim_times)),2),'%'
print '-------------------------------------------------------------------'
print 'Mean hit latency, low amp:',np.mean(hit_latencies_1),'ms'
print 'Mean hit latency, high amp:',np.mean(hit_latencies_2),'ms'
print 'Mean catch latency:',np.mean(catch_latencies),'ms'
print '-------------------------------------------------------------------'
print ''
        
        
# 'Pickle' data saving      
if save_PSTH == True:
    filename_PSTH = 'mouse%s.py' % (animal)
    save_directory = 'C:/Users/Admin/Desktop/Ush2A Hits Low Amp/%s' % (filename_PSTH) 
    with open(save_directory, 'wb') as f:
        pickle.dump(hit_latencies_1, f)
    save_directory = 'C:/Users/Admin/Desktop/Ush2A Hits High Amp/%s' % (filename_PSTH) 
    with open(save_directory, 'wb') as f:
        pickle.dump(hit_latencies_2, f)
    save_directory = 'C:/Users/Admin/Desktop/Ush2A Catch/%s' % (filename_PSTH) 
    with open(save_directory, 'wb') as f:
        pickle.dump(catch_latencies, f)
    print 'Data has been saved in target directory'


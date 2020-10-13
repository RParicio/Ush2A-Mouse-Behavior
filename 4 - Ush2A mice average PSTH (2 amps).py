# -*- coding: utf-8 -*-
"""
Created on Tue Sep 04 14:55:17 2018

@author: Admin
"""

"""
Created on Thu Jun 14 13:44:25 2018

@author: Admin
"""

import pickle
import pylab as pl
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------
# Settings
# -----------------------------------------------------------------------------
PSTH_from_choice = 1 # Seconds before the stimulus
PSTH_to_choice = 4 # Seconds after the stimulus (stimulus lasts 4 seconds)  
bin_range = np.arange(-PSTH_from_choice,PSTH_to_choice,0.1) # 0.1 equals 100 miliseconds per bin
second_PSTH = True # If we want to compare 2 PSTHs in the same graph
top_error_only = True
limit_50_licks = False
bar_width = 0.1
#------------------------------------------------------------------------------
# We load files from all mice, we obtain all latencies, and a list with a sublist for each mouse
# -----------------------------------------------------------------------------
hit_latencies = []
all_latencies = []
all_histograms = []
mice_means = []
print 'PSTH',1
print '-------------------'

mice = (1,2,4)

for i in mice:
    
    filename = 'mouse%s.py' % (i)
    directory = 'C:/Users/Admin/Desktop/Python Scripts (Behavior)/Fred Ush2A Python codes (4Sept2018)/Data Fred multiple stimuli Ush2A mice/Latency pickle files/3V/%s' % (filename)    

    with open(directory, 'rb') as f:
        hit_latencies_individual = pickle.load(f)

    if limit_50_licks == True:
        if len(hit_latencies_individual) > 50:
            print 'Mouse',i,'Limited to 50 licks'
            while len(hit_latencies_individual) > 50:
                hit_latencies_individual.pop()
   
    hit_latencies.extend(hit_latencies_individual)
    all_latencies.append(hit_latencies_individual)
            
    histogram_individual,bin_edges = np.histogram(hit_latencies_individual,bins=bin_range)
    bin_centres = (bin_edges[:-1] + bin_edges[1:])/2.
    print 'Mouse',i,'Number of licks:',len(hit_latencies_individual)    
    all_histograms.append(histogram_individual)
    
    mice_means.append(np.array(hit_latencies_individual).mean())
    print 'Mouse',i,'mean is:',np.array(hit_latencies_individual).mean()

#------------------------------------------------------------------------------
# We set the plotting settings and we plot
# -----------------------------------------------------------------------------
pl.figure(facecolor='white')
pl.subplot(221)
pl.subplot(221).spines["top"].set_visible(False)  
pl.subplot(221).spines["right"].set_visible(False)
pl.subplot(221).yaxis.set_ticks_position('left')
pl.subplot(221).xaxis.set_ticks_position('bottom')
pl.subplot(221)
pl.title('Lick Latency')
pl.xlabel("Time from Stimulus Onset (s)", fontsize=16)  
pl.ylabel("Licks / 100ms Bin", fontsize=16)

pl.subplot(223)
second_hist,bin_edges = np.histogram(hit_latencies,bins=bin_range)
pl.plot(bin_centres,second_hist/len(mice))

pl.subplot(222)
histogram_total, bin_edges = np.histogram(hit_latencies,bins=bin_range)
pl.title('All licks')
pl.bar(bin_centres,histogram_total, align='center',width=bar_width,color ='#cd5c5c')
pl.axvline(np.array(hit_latencies).mean(), color='red', linestyle='dashed', linewidth=2)
pl.axvline(np.median(np.array(hit_latencies)), color='red', linewidth=2)

#------------------------------------------------------------------------------
# Make an average histogram, and error bars array, and plot them
# -----------------------------------------------------------------------------
mean_hist = []
error_hist = []
for i in range(0,len(all_histograms[1]),1):
    collect_values = [item[i] for item in all_histograms]
    mean_hist.append(np.array(collect_values).mean())
    error_hist.append(stats.sem(collect_values))

# Show only the top bar of the error bars ---------------------------------
if top_error_only ==True:    
    one_side_error = []
    zeros = []
    for i in range(0,len(error_hist),1):
        zeros.append(0)
    one_side_error.append(zeros)
    one_side_error.append(error_hist)
    error_hist = one_side_error
#--------------------------------------------------------------------------    
pl.subplot(221)
pl.bar(bin_centres,mean_hist,width=bar_width, linewidth=0, color ='red',yerr=error_hist, align='center', alpha=0.9, ecolor='#cd5c5c')
pl.axvline(np.array(mice_means).mean(), color='red', linestyle='dashed', linewidth=2)
pl.axvline(np.median(np.array(mice_means)), color='red', linewidth=2)

    
#------------------------------------------------------------------------------
# Second PSTH
#------------------------------------------------------------------------------
if second_PSTH == True:

    hit_latencies2 = []
    all_latencies2 = []
    all_histograms2 = []
    mice_means2 = []
    print 'PSTH',2
    print '-------------------'

    mice2 = mice

    for i in mice2:
        
        filename = 'mouse%s.py' % (i)
        directory = 'C:/Users/Admin/Desktop/Python Scripts (Behavior)/Fred Ush2A Python codes (4Sept2018)/Data Fred multiple stimuli Ush2A mice/Latency pickle files/1V/%s' % (filename)    

        with open(directory, 'rb') as f:
            hit_latencies_individual2 = pickle.load(f)
            
        if limit_50_licks == True:
            if len(hit_latencies_individual2) > 50:
                print 'Mouse',i,'Limited to 50 licks'
                while len(hit_latencies_individual2) > 50:
                    hit_latencies_individual2.pop()
    
        hit_latencies2.extend(hit_latencies_individual2)
        all_latencies2.append(hit_latencies_individual2)

        histogram_individual2,bin_edges = np.histogram(hit_latencies_individual2,bins=bin_range)
        bin_centres = (bin_edges[:-1] + bin_edges[1:])/2.
        print 'Mouse',i,'Number of licks:',len(hit_latencies_individual2)        
        all_histograms2.append(histogram_individual2)
        
        mice_means2.append(np.array(hit_latencies_individual2).mean())
        print 'Mouse',i,'mean is:',np.array(hit_latencies_individual2).mean()

    pl.subplot(222)
    histogram_total2, bin_edges = np.histogram(hit_latencies2,bins=bin_range)
    pl.bar(bin_centres,histogram_total2,align='center',width=bar_width,color ='grey',alpha=0.6)    
    pl.axvline(np.array(hit_latencies2).mean(), color='grey', linestyle='dashed', linewidth=2)
    pl.axvline(np.median(np.array(mice_means2)), color='grey', linewidth=2)

    mean_hist2 = []
    error_hist2 = []
    for i in range(0,len(all_histograms2[1]),1):
        collect_values = [item[i] for item in all_histograms2]
        mean_hist2.append(np.array(collect_values).mean())
        error_hist2.append(stats.sem(collect_values))

    # Show only the top bar of the error bars ---------------------------------
    if top_error_only ==True:    
        one_side_error = []
        zeros = []
        for i in range(0,len(error_hist2),1):
            zeros.append(0)
        one_side_error.append(zeros)
        one_side_error.append(error_hist2)
        error_hist2 = one_side_error
    #--------------------------------------------------------------------------
    
    pl.subplot(221)
    pl.bar(bin_centres,mean_hist2,width=bar_width,linewidth=0, color ='grey', align='center', alpha=0.7, yerr=error_hist2, ecolor='grey',capsize=5) 
    pl.axvline(np.array(mice_means2).mean(), color='grey', linestyle='dashed', linewidth=2)
    pl.axvline(np.median(np.array(mice_means2)), color='grey', linewidth=2)
    
    









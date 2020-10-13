# Ush2A-Mouse-Behavior
Custom-made Python scripts to analyze raw behavioral files

These scripts go through our raw behavioral files stored in .hdf5 format. They analyze data from the mouse detection task, where mice (either WT or Ush2A-knockouts) are trained to report tactile stimuli delivered to their forepaw. 
Each detection session for each mouse has a raw data .hdf5 file. The scripts #1 (1 amplitude type / session) and #3 (2 amplitude types / session) are equivalent, and they read these files. They calculate data such as hit rates, false alarm rates and average latencies for each mouse. They also create a small file containing an array of all lick latencies to investigate the response times of mice. These small files ("pickles") can then be loaded with scripts #2 and #4, respectively.


Brief script explanation (for multi-amplitude data. For sessions with 1 single amplitude, replace #3 by #1, and replace #4 by #2):
---------------------------------------------------------------------
The first script is named "3 - Ush2A mice (2 stim amp).py". 

This code will go through the raw data, split all stimulus trials in 2 categories: "High" and "Low", and analyze them separately. In the files you gave me, you always used 2 amplitudes in the same session (2&4V, and 1&3V). So this code works for both cases. 
It creates 3 latency ("pickle") files: high amplitude, low amplitude and catch latencies. These are simply lists of lick latencies for each stimulus type.

To make it work:

- 1: At the top of the code (after the import functions), write which animal you analyze (the saved file with the latencies will be named "mouseX", where X is the number of mouse). 

- 2: As always, write the directory of the file, just below the animal variable.

- 3: At the bottom, write the disk location where the latency file will be created. 
I recommend making a "High amplitude" and a "Low amplitude" folder. Then, analyze all animals with conditions of 4&2 Volts. Then, copy the files to new folders ("4V" and "2V"). Finally, analyze all animals with conditions of 1&3 Volts, and you can rename the "High amplitude" and "Low amplitude" folders into "3V" and "1V" respectively. This way, you will now have 4 folders with amplitude-specific latencies and you can compare all combinations, with the other code. 

---------------------------------------------------------------------
The second script is named "4 - Ush2A mice average PSTH (2 amps).py". 

This code will load latency files of your choice and plot them in the top left graph. The first PSTH will be in red and the second in grey (it can be changed). It will also give you the average latency of each mouse, in the console. 

To make it work:

- 1: Write which mice you want to include in your PSTH plot (search for variable "mice", quite at the top).

- 2: Write the directory where the latency files (that you want to load) are located, for both cases.

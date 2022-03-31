# Population analyses from Schroeder et al. 2022

This repository containts the raw data and all code to go from raw data to figures. It also contains the intermediate versions of the data, so you don't necessarily need to run the entire pipeline. See [Control of neocortical memory by long-range inhibition in layer 1](https://doi.org/10.1101/2022.02.07.479360 ) for the preprint. 


## Data folder
* Raw data in 'data/raw_data.mat'
* Meaning of variables in 'data/codebook.xlsx'
* The analysis don't use the raw data, but load separate files for each mice. 
These files can be found in 'data/per_mouse'. The folder contains subfolders 'AFC' and 'PC' with the conditioned and pseudo-conditioned mice, respectively. It also contains the same data, but split across boutons that based on their response during recall. For example
'AFC_exc_csm' contains all boutons that increased their activoity during the CS-. 
* Run the matlab scripts 'preprocess_data_AFC.m' or 'preprocess_data_PC.m' to re-compute the 'per_mouse' data from 'raw_data.mat'
* 

## Scripts folder
* Preprocessing scripts, see previous point.
* Scripts that conduct the analyses, save the data and the figures. 

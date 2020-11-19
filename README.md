# Merge multiple output fields from Finnish Meteorological Institute Probabilistic Precipitation Nowcasting system (FMI-PPN) into one 

Containerized python code for combining several FMI-PPN nowcasting system (see documentation at https://github.com/fmidev/fmippn-oper) output HDF5 files. Used for parallel running of FMI-PPN. The FMI-PPN output files to be merged should be from runs that use same input files and (at least almost) same configuration parameters. The configuration parameters that can be different are seed and number of ensemble members. Apart from number of ensemble members the metadata stays the same after mergeing the files, only the datasets are copied and renamed.

## Files

combine_ppn_outputs.py : The python code that does the actual mergeing.
Dockerfile : Dockerfile to build the needed python environment image for running the code.
requirements.txt : List of needed python packages
run_combine_ppn_outputs.sh : Example bash run scripts for running the container using podman and volume mounts for input and output data.


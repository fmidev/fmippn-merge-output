import os
import h5py
import argparse
import numpy as np

# Tuuli Perttula 2020
# tuuli.perttula@fmi.fi

def combine_fmippn_h5_files(f1,f2):
    """ This function combines two FMIPPN HDF5 ODIM format output files.
    Ensemble members from file2 are added to file1. The names of 
    ensemble members from file2 are modified so that the numbering continues 
    from the last member of file1. 

    Also ensemble_size attribute is modified to match the new total number 
    of ensemble members.

    It is assumed that all configurations in files 1 and 2 are the
    same except the seed value. Note that the seed attributes are not modified.

    Keyword arguments:
    f1 -- h5py file object for FMIPPN ODIM HDF5-file to which we copy the members from file 2 f1=h5py.File(file1, 'a')
    f2 -- h5py file object for FMIPPN ODIM HDF5-file from which we copy the members to file1 f2=h5py.File(file2, 'r')
    """

    #Moved outside of the function to save time
    #f1=h5py.File(file1, 'a')
    #f2=h5py.File(file2, 'r')
    
    # Read ensemble size from attributes
    ensemble_size_file1=int(f1['/how'].attrs.__getitem__('ensemble_size'))
    ensemble_size_file2=int(f2['/how'].attrs.__getitem__('ensemble_size'))

    # Read nowcast_timestep and max_leadtime from attributes and calculate
    # number of timesteps
    nowcast_timestep_file2 = int(f2['/how'].attrs.__getitem__('nowcast_timestep'))
    max_leadtime_file2 = int(f2['/how'].attrs.__getitem__('max_leadtime'))
    num_timesteps_file2=int(max_leadtime_file2/nowcast_timestep_file2)

    for member in range(1,ensemble_size_file2+1):
        for leadtime in range(1,num_timesteps_file2+1):

            dset_name=f"/dataset{leadtime}/data{member}/data"
            dset_what_group=f"/dataset{leadtime}/data{member}/what"
            
            new_member=member+ensemble_size_file1
            new_dset_name=f"/dataset{leadtime}/data{new_member}/data"
            new_dset_what_group=f"/dataset{leadtime}/data{new_member}/what"
            
            dset=f2[dset_name]
            #Copy the dataset from file2 to newly created dataset in file1
            f1.create_group(new_dset_name)
            f2.copy(dset_name,f1[new_dset_name])

            #Copy /dataset/data/what group
            f1.create_group(new_dset_what_group)
            f2.copy(dset_what_group,f1[new_dset_what_group])

            
    #Give new value to attribute meta/configuration/ENSEMBLE size 
    new_ensemble_size=(ensemble_size_file1+ensemble_size_file2)
    print('new_ensemble_size', new_ensemble_size)
    f1['/how'].attrs.modify('ensemble_size',new_ensemble_size)

    #Moved outside of the function to save time
    #f1.close()
    #f2.close()
    
def main():    

    print("Input files:",options.inputfilelist)
    
    #Copy file1 to output filename
    cp_command='cp ' + options.inputfilelist[0] + ' ' + options.outfile
    os.system(cp_command)

    #Append file1 with ensemble members from rest of the input files
    if len(options.inputfilelist) >= 2:

        f1=h5py.File(options.outfile, 'a')

        for inputfile in options.inputfilelist[1:]:
            f2=h5py.File(inputfile, 'r')
            combine_fmippn_h5_files(f1,f2)
            f2.close()

        f1.close()

        
if __name__ == "__main__":

    #Parse commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--outfile',
                        default='combined_fmippn_output.h5',
                        type=str,
                        help='New filename for combined FMIPPN output file.')
    parser.add_argument('--inputfilelist',
                        nargs='+',
                        help='List of FMIPPN HDF5-files to combine')
    options = parser.parse_args()

    main()

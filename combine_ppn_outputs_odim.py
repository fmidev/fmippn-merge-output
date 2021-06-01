import os
import h5py
import argparse
import numpy as np

# Tuuli Perttula 2020
# tuuli.perttula@fmi.fi

def combine_fmippn_h5_files(file1,file2):
    """ This function combines two FMIPPN HDF5 ODIM format output files.
    Ensemble members from file2 are added to file1. The names of 
    ensemble members from file2 are modified so that the numbering continues 
    from the last member of file1. 

    Also ensemble_size attribute is modified to match the new total number 
    of ensemble members.

    It is assumed that all configurations in files 1 and 2 are the
    same except the seed value. Note that the seed attributes are not modified.

    Keyword arguments:
    file1 -- FMIPPN ODIM HDF5-file to which we add members
    file2 -- FMIPPN ODIM HDF5-file from which we copy the members to file1
    """

    f1=h5py.File(file1, 'a')
    f2=h5py.File(file2, 'r')
    
    # Read ensemble size and number of timesteps from attributes
    ensemble_size_file1=int(f1['/how'].attrs.__getitem__('ensemble_size'))
    ensemble_size_file2=int(f2['/how'].attrs.__getitem__('ensemble_size'))
    num_timesteps_file2=int(f2['/how'].attrs.__getitem__('num_timesteps'))

    print(ensemble_size_file1,ensemble_size_file2,num_timesteps_file2)

    for member in range(1,ensemble_size_file2+1):
        for leadtime in range(1,num_timesteps_file2+1):

            #dset_name="/member-" + f"{member:02d}" + "/leadtime-" + f"{leadtime:02d}"
            dset_name=f"/dataset{leadtime}/data{member}/data"
            dset_what_group=f"/dataset{leadtime}/data{member}/what"
            
            new_member=member+ensemble_size_file1

            #new_dset_name="/member-" + f"{new_member:02d}" + "/leadtime-" + f"{leadtime:02d}"
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
    #f1['/how'].attrs.modify('ensemble_size',np.string_([str(new_ensemble_size)]))
    f1['/how'].attrs.modify('ensemble_size',new_ensemble_size)
            
    f1.close()
    f2.close()

    
def main():    

    print("Input files:",options.inputfilelist)
    
    #Copy file1 to output filename
    cp_command='cp ' + options.inputfilelist[0] + ' ' + options.outfile
    os.system(cp_command)

    #Append file1 with ensemble members from rest of the input files   
    if len(options.inputfilelist) >= 2:
        for inputfile in options.inputfilelist[1:]:
            combine_fmippn_h5_files(options.outfile,inputfile)

    
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

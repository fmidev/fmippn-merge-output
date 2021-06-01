#!/bin/bash

# exit when any command fails
set -e

# Set paths and variables
DOMAIN=${DOMAIN:-"ravake_hdf5"}
#LATEST_TIMESTAMP=`ls -t /data/output/$DOMAIN/fmippn-3 | head -n1 | awk -F "_" '{print $3}' | awk -F "." '{print $1}'`
LATEST_TIMESTAMP=`ls -t /home/perttula/ppn_output/ravake_hdf5/nowcast1/nc_ens* | tail -n 1 | xargs -n1 basename | awk -F "_" '{print $3}' | awk -F "." '{print $1}'`
TIMESTAMP=${TIMESTAMP:-$LATEST_TIMESTAMP}
FILENAME=${FILENAME:-"nc_ens_${TIMESTAMP}.h5"}
#PPNOUTDIR=${PPNOUTDIR:-"/data/output/$DOMAIN"}
PPNOUTDIR=${PPNOUTDIR:-"/home/perttula/ppn_output/$DOMAIN"}
#INDIR1=${INDIR1:-"$PPNOUTDIR/fmippn-1"}
#INDIR2=${INDIR2:-"$PPNOUTDIR/fmippn-2"}
#INDIR3=${INDIR3:-"$PPNOUTDIR/fmippn-3"}
INDIR1=${INDIR1:-"$PPNOUTDIR"}                                                                                                                 
INDIR2=${INDIR2:-"$PPNOUTDIR"}                                      
INDIR3=${INDIR3:-"$PPNOUTDIR"}
MERGEOUTDIR=${MERGEOUTDIR:-"$PPNOUTDIR/combined_ensemble"}

#List of directories:
INDIR_LIST=${INDIR_LIST:-$PPNOUTDIR/nowcast1 $PPNOUTDIR/nowcast2 $PPNOUTDIR/nowcast3 $PPNOUTDIR/nowcast4}

echo "Combining PPN output files calculated for DOMAIN:" $DOMAIN "and TIMESTAMP:" $TIMESTAMP

# Make temporary input folder and copy files with different names                                                                                       
TEMPDIR=${TEMPDIR:-"$PPNOUTDIR/mergetmp_${DOMAIN}_$TIMESTAMP"}
cmd="mkdir -p $TEMPDIR"
echo $cmd
eval $cmd

# Copy original input files to tempdir with different names
i=1
CONTAINER_INFILELIST=""
for INDIR in $INDIR_LIST; do
    INFILE=$TEMPDIR/infile${i}.h5
    cmd="cp $INDIR/$FILENAME $INFILE"
    echo $cmd
    eval $cmd

    CONTAINER_INFILE=/input/infile${i}.h5
    CONTAINER_INFILELIST="${CONTAINER_INFILELIST} ${CONTAINER_INFILE}"
    echo "CONTAINER_INFILELIST=${CONTAINER_INFILELIST}"
    ((i+=1))
done

# Build from Dockerfile
#podman build --tag combining_fmippn_output -f Dockerfile_odim

# Run with volume mounts
podman run \
	--rm \
	--env "outdir=/output" \
	--env "outfile=$FILENAME" \
	--env "infilelist=$CONTAINER_INFILELIST" \
	--mount type=bind,source=$TEMPDIR,target=/input \
	--mount type=bind,source=$MERGEOUTDIR,target=/output \
	--security-opt label=disable \
	combining_fmippn_output:latest

#Remove temporary folder
rm -fr $TEMPDIR

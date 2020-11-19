#/bin/bash

# exit when any command fails
set -e

# Set paths and variables
DOMAIN=${DOMAIN:-"europe"}
LATEST_TIMESTAMP=`ls -t /data/output/$DOMAIN/fmippn-3 | head -n1 | awk -F "_" '{print $2}' | awk -F "." '{print $1}'`
TIMESTAMP=${TIMESTAMP:-$LATEST_TIMESTAMP}
FILENAME=${FILENAME:-"nc_${TIMESTAMP}.h5"}
PPNOUTDIR=${PPNOUTDIR:-"/data/output/$DOMAIN"}
INDIR1=${INDIR1:-"$PPNOUTDIR/fmippn-1"}
INDIR2=${INDIR2:-"$PPNOUTDIR/fmippn-2"}
INDIR3=${INDIR3:-"$PPNOUTDIR/fmippn-3"}
MERGEOUTDIR=${MERGEOUTDIR:-"$PPNOUTDIR/combined_ensemble"}

echo "Combining PPN output files calculated for DOMAIN:" $DOMAIN "and TIMESTAMP:" $TIMESTAMP

# Make temporary input folder and copy files with different names
TEMPDIR=${TEMPDIR:-"$PPNOUTDIR/mergetmp_${DOMAIN}_$TIMESTAMP"}
mkdir -p $TEMPDIR
cp $INDIR1/$FILENAME $TEMPDIR/infile1.h5
cp $INDIR2/$FILENAME $TEMPDIR/infile2.h5
cp $INDIR3/$FILENAME $TEMPDIR/infile3.h5

# Build from Dockerfile
#podman build --tag combining_fmippn_output .

# Run with volume mounts
podman run \
	--rm \
	--env "outdir=/output" \
	--env "outfile=$FILENAME" \
	--env "indir=/input" \
	--env "infile1=infile1.h5" \
	--env "infile2=infile2.h5" \
	--env "infile3=infile3.h5" \
	--mount type=bind,source=$TEMPDIR,target=/input \
	--mount type=bind,source=$MERGEOUTDIR,target=/output \
	--security-opt label=disable \
	combining_fmippn_output:latest

#Remove temporary folder
rm -fr $TEMPDIR


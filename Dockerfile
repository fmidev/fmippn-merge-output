# set base image (host OS)
FROM python:3.8

# Workdir and input/output/log dir
WORKDIR .
RUN mkdir input
RUN mkdir output
RUN mkdir log

# copy the dependencies file to the working directory
COPY requirements.txt .

#Copy executable (later from Github...)
COPY combine_ppn_outputs.py .

# install dependencies
RUN pip install -r requirements.txt

# command to run on container start
ENV outdir "/output"
ENV outfile "nc_test.h5"
ENV indir "/input"
ENV infile1 "infile1.h5"
ENV infile2 "infile2.h5"
ENV infile3 "infile3.h5"
ENTRYPOINT python combine_ppn_outputs.py --outfile=$outdir/$outfile --inputfilelist $indir/$infile1 $indir/$infile2 $indir/$infile3 

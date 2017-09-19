#!/bin/env python
# SRAFixer.py
# by Brendan Kohrn, January 15, 2015
# edited by Jorge Boucas, December 30, 2015
# 
# This program is meant to refomat reads downladed from the SRA
# (http://www.ncbi.nlm.nih.gov/sra/), including the example data set 
# (http://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?run=SRR1613972).  
# It is necessary because when the reads are downloaded from the SRA, 
# they are given a different label than they had going into it, which  
# causes an error if the reads are fed straight into tag_to_header.py.
# This program fixes that error.
#
# Example: 
# tag_to_header.py is expecting the name line of a fastq to look 
# something like 
# @HWI-7001239F_017:1:1101:1226:2127/1
# but when it comes out of SRA, it looks like 
# @SRR1613972.1.1 1 length=101
#
# This program will change the read name to be
# @SRR1613972.1.1:1:length=101:1:1/1

import sys
import os.path
import gzip
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--infile', dest = 'infile', 
                    help = 'Input raw fastq file.  ', 
                    required=True)
parser.add_argument('--outfile', dest = 'outfile', 
                    help = 'Output fastq file.  ', 
                    required=True)
o = parser.parse_args()

extension = os.path.splitext(o.infile)[1]
if extension == ".gz":
    infile = gzip.open(o.infile, 'r')
else:
    infile = open(o.infile, 'r')

if not os.path.exists(os.path.dirname(o.outfile)):
    os.makedirs(os.path.dirname(o.outfile))
outfile = open(o.outfile, 'w')

readsProcessed = 0
pair=o.infile.split(".fastq")[0]
pair=pair[len(pair)-1]

for line in infile:
    if readsProcessed % 100000 == 0:
        print("Reads Processed: %s" % readsProcessed)
	if '@' in line or '+' in line:
        
        readNum = line.split(' ')[0].split('.')[1]
        repLine = "%s:%s:%s/%s\n" %(line.strip().replace(' ', ':'),readNum,readNum,pair)
        outfile.write(repLine)
        if '@' in line: readsProcessed += 1
    else:
        outfile.write(line)
    
infile.close()
outfile.close()

#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import argparse
from argparse import RawTextHelpFormatter
        
##args = docopt.docopt(__doc__)
#out_dir = args['--output_folder']
 

p = argparse.ArgumentParser(description = '- Merging three NPZ files (each file + interaction area)',
                            formatter_class=RawTextHelpFormatter)
p.add_argument('-dataA','--inputA','-i', required= True, help='Input trRossetta NPZ file')
p.add_argument('-dataB','--inputB','-j', required= True, help='Input trRossetta NPZ file')
p.add_argument('-dataAB','--inputAB','-k', required= True, help='Input trRossetta NPZ file(s) for the mergedsequence',nargs="+")
#p.add_argument('-seq','--sequence','-s', required= True, help='sequence file to identify domain baorders')
p.add_argument('-out','--output','-o', required= True, help='output NPX file')
#parser.add_argument('--nargs', nargs='+')
ns = p.parse_args()


bin_step = 0.5
bins = np.array([2.25+bin_step*i for i in range(36)])


rstA = np.load(ns.inputA)
rstB = np.load(ns.inputB)
rstAB=[]
for i in ns.inputAB:
    rstAB += [np.load(ns.inputAB[0])]



distA = rstA["dist"].shape[0]
distB = rstB["dist"].shape[0]
distAB = rstAB[0]["dist"].shape[0]


if distA+distB != distAB:
    print ("Not correct sized of distnance matrices",distA,distB,distAB)
    exit(-1)

for r in rstAB:
    if r["dist"].shape[0] !=distAB:
        print ("Not correct sized of distance matrices",d,rstAB[r]["dist"].shape[0],distAB)
        exit(-1)

new_rst = {'dist' : [], 'omega' : [], 'theta' : [], 'phi' : [] } # , 'rep' : []}    

# first we merge the full length ones.
for f in rstAB[0].files:
    new_rst[f]=rstAB[0][f]


    
# Take the one with the lowsest  probability to not have a distance
# To speed up things we only do this for intrachan
for d in range(1,len(rstAB)):
    for i in range(distA):
        for j in range(distA+1,distB):
            orgprob = new_rst["dist"][i, j, 0]
            newprob = rstAB[d]["dist"][i, j, 0]
            if newprob < orgprob:
                for f in rstAB[0].files:
                    new_rst[f][i,j]=rstAB[d][f][i,j]
                    new_rst[f][j,i]=rstAB[d][f][j,i]

                    
# Then we add the     
for i in rstAB[0].files:
    A=rstA[i]
    B=rstB[i]
    AB=rstAB[0][i]
    AB[0:distA,0:distA]=A    
    AB[distA:,distA:]=B    
    new_rst[i]=AB

np.savez_compressed(ns.output, dist=new_rst['dist'], omega=new_rst['omega'], theta=new_rst['theta'], phi=new_rst['phi']) #, rep=new_rst['rep'])

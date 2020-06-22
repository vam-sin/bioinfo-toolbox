#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import argparse
from argparse import RawTextHelpFormatter
        
##args = docopt.docopt(__doc__)
#out_dir = args['--output_folder']
 

p = argparse.ArgumentParser(description = '- plotting trRosetta maps-',
                            formatter_class=RawTextHelpFormatter)
p.add_argument('-data','--input','-i', required= True, help='Input trRossetta NPZ file')
p.add_argument('-dataB','--inputB','-j', required= False, help='Input second trRossetta NPZ file for reversed order merged files')
p.add_argument('-dom','--domain','-d', required= False, help='positions of domain borders', nargs='+')
p.add_argument('-seq','--sequence','-s', required= False, help='sequence file to identify domain baorders')
p.add_argument("--sepseq","-sep","-S",required=False, help='Separation sequence between protein in MSA' ,default="AAAAAAAAAAAAAAAAAAAA")
p.add_argument('-out','--output','-o', required= False, help='output image')
#parser.add_argument('--nargs', nargs='+')
ns = p.parse_args()

input_file = np.load(ns.input)
bin_step = 0.5
bins = np.array([2.25+bin_step*i for i in range(36)])
dist = input_file["dist"]
p_len = dist.shape[0]
res = np.zeros((p_len, p_len))
res.fill(20)
np.fill_diagonal(res, 4)


borders=[]
if ns.sequence:
    sepseq=ns.sepseq
    from Bio import SeqIO
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
    #import A3MIO
    # We can read it as fasta as we only care about the first sequence withouth gaps
    import re
    with open(ns.sequence, "r") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            seq=record
            #print (record)
            break
    #print (re.finditer(sepseq,str(seq.seq)))
    #print (re.findall("AAAAAAAAA","XXAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAS"))
    #print (ns.sequence)    
    #print (seq,seq.seq)    
    ns.domain=[]
    for m in re.finditer(sepseq,str(seq.seq)):
        borders+=[m.start()]
        #print(m.start(), m.group())
        for i in range(m.start(),m.start()+len(sepseq)):
            ns.domain+=[i]

# If we have two inputs put one at each diagonal but             
if ns.inputB:
    input_fileB = np.load(ns.inputB)
    distA=dist
    distB = input_fileB["dist"]
    p_lenB = distB.shape[0]
    #resB = np.zeros((p_len, p_len))
    #resB.fill(20)
    #np.fill_diagonal(resB, 4)
    if (p_len != p_lenB):
        print ("NPZ files of differnet lengths")
        sys.exit(1)
    if (len(borders)!=1):
        print ("Not two chains",borders)
        sys.exit(1)
    shiftA=borders[0]
    seplen=len(sepseq)
    shiftB=p_len-1-borders[0]-seplen
    for i in range(shiftA+seplen,p_len-1):
        for j in range(i+1,p_len-1):
            dist[i, j, 0:]=distB[i-shiftA+1-seplen, j-shiftA+1-seplen, 0:]
    for i in range(shiftB):
        for j in range(i+1,shiftB):
            dist[i+shiftA+seplen, j+shiftA+seplen, 0:]=distB[i, j, 0:]
    for i in range(shiftB+seplen,p_len-1):
        for j in range(shiftB):
            dist[i, j, 0:]=distB[j, i, 0:]
             

#print (ns.domain)
for i in range(p_len-1):
    #for j in range(i+1):
    for j in range(p_len-1):
        prob = dist[i, j, 0]
        if prob > 0.5:
            continue
        d_slice = dist[i, j, 1:]
        mean_dist = np.sum(np.multiply(bins, d_slice/np.sum(d_slice)))
        res[i, j] = mean_dist
        #res[j, i] = mean_dist

borders+=[p_len-1]        
startx=0
average=[]
mindist=[]
numdist=[]
x=0
y=0
# We only do this for two domains at the moment
if (ns.sequence):
    for m in borders:
        starty=0
        for n in borders:
            mindist+=[9999]
            average+=[0]
            numdist+=[0]
            #print (x,mindist,average,startx,starty,m,n)
            z=0
            
            for i in range(startx,m):
                for j in range(starty,n):
                    # Avoid sequene separated by less than 5 resideus

                    if np.abs(i-j)<5: continue
                    #print (i,j)
                    prob = dist[i, j, 0]
                    average[x]+=1-prob
                    z+=1
                    if prob > 0.5:
                        continue
                    numdist[x]+=1
                    d_slice = dist[i, j, 1:]
                    mean_dist = np.sum(np.multiply(bins, d_slice/np.sum(d_slice)))
                    mindist[x]=min(mean_dist,mindist[x])
            average[x]=average[x]/z
            x+=1
            starty=n+len(sepseq)
        startx=m+len(sepseq)
        
# o        
#sys.exit()
        
fig = plt.figure()
ax = fig.add_subplot(111)
#fig, (ax1, ax2) = plt.subplots(ncols=2)
#ax2=ax.twin()
cax = ax.matshow(res, cmap="hot")
#print (res)
if type(ns.domain) is list:
    for cut in ns.domain:
        #x=[0,p_len-1,cut,cut]
        #y=[cut,cut,0,p_len-1]
        x=[0,p_len-1]
        y=[float(cut),float(cut)]
        #print (x,y)
        ax.plot(x,y,lw=3,c="b",alpha=0.2)
        ax.plot(y,x,lw=3,c="b",alpha=0.2)
    #ax.set(xlim=[0,500],ylim=[0,500])
ax.set(title=ns.input)
fig.colorbar(cax)
if ns.output:
    fig.savefig(ns.output)
#plt.show()
print (ns.input,np.round(average,3),np.round(mindist,3),np.round(numdist,3))
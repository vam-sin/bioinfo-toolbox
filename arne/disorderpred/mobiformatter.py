#!/usr/bin/env python3
import pickle
import h5py
import numpy as np
import os
from Bio import SeqIO
import re
import pandas as pd
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC

codons = [
'ATA', 'ATC', 'ATT', 'ATG', 'ACA', 'ACC', 'ACG', 'ACT', 
'AAC', 'AAT', 'AAA', 'AAG', 'AGC', 'AGT', 'AGA', 'AGG',                  
'CTA', 'CTC', 'CTG', 'CTT', 'CCA', 'CCC', 'CCG', 'CCT', 
'CAC', 'CAT', 'CAA', 'CAG', 'CGA', 'CGC', 'CGG', 'CGT', 
'GTA', 'GTC', 'GTG', 'GTT', 'GCA', 'GCC', 'GCG', 'GCT', 
'GAC', 'GAT', 'GAA', 'GAG', 'GGA', 'GGC', 'GGG', 'GGT', 
'TCA', 'TCC', 'TCG', 'TCT', 'TTC', 'TTT', 'TTA', 'TTG', 
'TAC', 'TAT', 'TGC', 'TGT', 'TGG']

nuc_encode = {
'A':[1,0,0,0],
'T':[0,1,0,0],
'C':[0,0,1,0],
'G':[0,0,0,1]}

res_encode = {
'A':[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
'R':[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
'N':[0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
'D':[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
'C':[0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
'Q':[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
'E':[0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
'G':[0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
'H':[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
'I':[0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
'L':[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
'K':[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
'M':[0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
'F':[0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
'P':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
'S':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
'T':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
'W':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
'Y':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
'V':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]}

label = {'S':0, 'X':0.5, 'C':0.5, 'D':1}

##### codon wise one-hot encoding table
pos = 0
cod_encode = {}
for codon in codons: 
    cod_encode[codon] = []
    for n in range(61): 
        if n == pos: cod_encode[codon].append(1)
        else: cod_encode[codon].append(0)
    pos += 1
#####

data_dir = "/home/arnee/git/paper_proks_vs_euks_proteins/data/"

df_reference_file = data_dir  + "df_reference.csv"
df_reference = pd.read_csv(df_reference_file)
taxid2gc = df_reference.set_index("TaxID").to_dict()["GC%"]



#            try:
#                gc=float(taxid2gc[int(tax_id)])


fasta_dir="uniprot/"
with open('mobidata_K.pickle','rb') as f:
    data = pickle.load(f)

memo2taxid={}
with open(data_dir+'speclist.txt') as fp:
    for line in fp:
        if re.match('.*:\sN=',line):
            s=line.split()
            taxid=s[2].replace(':','')
            mnemonic=s[0]
            memo2taxid[mnemonic]=taxid

    
outlist = open('formatted_list','w')
out = h5py.File('formatted_data_GC_GCgenomic_kingdom.h5py', 'w')
for key in data:                                                                ##### key: uniprot/MobiDB ID
    #print (key)
    fastafile=fasta_dir+key+".fasta"
    GCgenomic=0.0
    for record in SeqIO.parse(fastafile, "fasta"):
        #print("%s %i" % (record.id, len(record)))
        bar,id,name=record.id.split("|") 
        #print (record.id,id,name)
        prot,taxname=name.split("_") 
        try:
            GCgenomic=float(taxid2gc[int(memo2taxid[taxname])])
        except:
            continue
    print (key,name,taxname,GCgenomic)
    if not GCgenomic>0:continue
    if 'rna' not in data[key]: continue
    if 'GC%' not in data[key]: continue
    gc=data[key]['GC%']
    if data[key]['kingdom']=='A':
        k=[1,0,0]
    elif data[key]['kingdom']=='B':
        k=[0,1,0]
    elif data[key]['kingdom']=='E':
        k=[0,0,1]
    else:
        k=[0,0,0]
    #mobidata[code.rstrip()]['GC%']
    pro = []                                                                    ##### one-hot encoded aa
    for aa in data[key]['sequence']:
        if aa in res_encode: pro.append(res_encode[aa][:])
        else: break                                                             ##### break sequences with atypical/unknown aa

    rna = []                                                                    ##### one-hot encoded nucleotides
    for pos in range(0, len(data[key]['rna']), 3):
        cod = data[key]['rna'][pos:pos+3]
        if cod in cod_encode: rna.append(cod_encode[cod][:])
        else: break                                                             ##### break sequences with atypical/unknown nucl

    GC = []                                                                    ##### GC-frequency (real number=
    for i in data[key]['sequence']:
        GC.append(gc)


    kingdom = []                                                                    ##### one-hot encoded kingdom
    for i in data[key]['sequence']:
        kingdom.append(k)
        
    if len(rna) == len(pro) and len(rna) == len(data[key]['sequence']):         ##### skip sequences with inconsistencies

        firstpos = data[key]['disorder'][0][0]                                  ##### disordered region format of mobiDB: [[firstpos, lastpos, label],[firstpos,lastpos,label],...]
        lastpos = data[key]['disorder'][-1][1]                                  ##### labels: D - disorder, S - structure, C - conflict, X - unknown
        for el in data[key]['disorder']:                                        
            if (lastpos-firstpos)+1 < len(pro) and lastpos <= len(pro):         ##### finds region labellings shorter than whole protein sequences 
                for pos in range(el[0]-1, el[1]):
                    pro[pos].append(label[el[-1]])
                    rna[pos].append(label[el[-1]])
            else:                                                               
                for pos in range(el[0]-firstpos, el[1]+1-firstpos):
                    pro[pos].append(label[el[-1]])
                    rna[pos].append(label[el[-1]])
        for pos in range(len(rna)):                                             ##### fills incomplete positions with 'unknown' label
            if len(pro[pos])<21: pro[pos].append(0.5)
            if len(rna[pos])<62: rna[pos].append(0.5)

        out.create_group(key)
        out[key].create_dataset('pro', data=np.array(pro, dtype=np.float32).reshape(len(pro), 21) , chunks=True, compression="gzip")
        out[key].create_dataset('rna', data=np.array(rna, dtype=np.float32).reshape(len(rna), 62), chunks=True, compression="gzip")
        out[key].create_dataset('GC', data=np.array(GC, dtype=np.float32).reshape(len(pro), 1), chunks=True, compression="gzip")
        out[key].create_dataset('kingdom', data=np.array(kingdom, dtype=np.float32).reshape(len(pro), 3), chunks=True, compression="gzip")
        outlist.write(key+'\n')

out.close()
outlist.close()


#!/bin/bash -lx
#SBATCH --output=proq3.%A_%a.out
#SBATCH --error=proq3.%A_%a.out
#SBATCH --array=1-335
#SBATCH -c 1
#SBATCH -t 3-00:00:00
#SBATCH -A SNIC2016-10-22

export PATH=$PATH:/pfs/nobackup/home/m/mircomic/EMBOSS-6.6.0/build/bin/
export R_LIBS="/pfs/nobackup/home/m/mircomic/R_libs"
export PYTHONPATH=$PYTHONPATH:"/pfs/nobackup/home/m/mircomic/python2.7/dist-packages/"
export THEANO_FLAGS='base_compiledir=/pfs/nobackup/home/a/arnee/python2.7/dist-packages/.theano'

offset=$2
list=$1
pos=$(($SLURM_ARRAY_TASK_ID + $offset))
#id=`tail -n+$pos IDs_29.0_test_done_300.txt | head -n1`
id=`tail -n+$pos $list | head -n1`

#id="PF00001.18"

dir=`pwd`/$id

scratch=$SNIC_TMP/arnee/ProQ3/$id/
mkdir -p $scratch


cd $scratch
# just in case the files are not compressed (should be fixed)

# rsync -ar $dir/confold_2.5_m50_proq3/ ./confold_2.5_m50_proq3/


#cd /pfs/nobackup/home/a/arnee/mircom/


/pfs/nobackup/home/a/arnee/mircom/bin/proq3/run_proq3.sh -fasta $dir/${id}*.fa -outpath ./ -only-build-profile

sleep 10 # waiting for filesystem

for i in $dir/*cm.tar.gz $dir/conf*[04].tar.gz  $dir/*_mem.tar.gz
do
    tar -zxf $i
    j=`basename $i .tar.gz`
    if [ ! -s $dir/${j}_proq3.tar.gz ]
    then
	ls $j/stage1/${id}*.pdb > qa.input
	sleep 10 # waiting for filesystem 
	mkdir  $j_proq3
	/pfs/nobackup/home/a/arnee/mircom/bin/proq3/run_proq3.sh  -l qa.input -profile ${scratch}${id}.????_?.fasta -outpath ${j}_proq3 --deep yes
	sleep 10 # waiting for filesystem
	tar -zcvf $dir/${j}_proq3.tar.gz ${j}_proq3 # --remove-files
	rm -r ${j}_proq3
	rm -r ${j}/
    fi
done

cd $dir/../

#!/bin/bash
# draw the histogram given the file in the format
# #topology comparison of four states
# #
# # format of the file to make the plot
# #Idx th_TM2TM th_TM2GAP  TM2TM TM2GAP TM2SEQ      Count
# 0         0.1       0.5 79.078 11.985  8.938    1251454
# 1         0.2       0.5 78.129 12.112  9.759    1259967
# 2         0.3       0.5 76.990 12.232 10.778    1266940
# 3        0.33       0.5 76.990 12.232 10.778    1266940
# 4         0.4       0.5 75.453 12.369 12.178    1271642
# 5         0.5       0.5 73.028 12.538 14.434    1273468
# 6         0.6       0.5 68.945 12.536 18.519    1273728

usage="
Usage: $0 datafile
Description: 
Options:
    -outstyle|-o png|term|eps : set the output, default = terminal
    -outpath <path>           : set the output path, default =./
    -mode 0|1
    -h|--help                 : print this help message and exit

Created 2012-08-31, updated 2012-09-11, Nanjiang Shu 
"
PrintHelp(){
    echo "$usage"
}

if [ $# -lt 1 ]; then
    PrintHelp
    exit
fi

outputStyle=eps
outpath=""
dataFile=
xlabel="Threshold of fraction of TM2GAP"
ylabel="Percentages of TM mapping classes"
isNonOptionArg=false
mode=0 #
#0 for TM2TM
#1 for TM2GAP

while [ "$1" != "" ]; do
    if [ "$isNonOptionArg" == "true" ]; then 
        dataFile=$1
        isNonOptionArg=false
    elif [ "$1" == "--" ]; then
        isNonOptionArg=true
    elif [ "${1:0:1}" == "-" ]; then
        case $1 in
            -h|--help) PrintHelp; exit;;
            -outstyle|--outstyle|-o) outputStyle=$2;shift;;
            -xlabel|--xlabel) xlabel="$2";shift;;
            -ylabel|--ylabel) ylabel="$2";shift;;
            -mode|--mode)mode=$2;shift;;
            -outpath|--outpath) outpath=$2;shift;;
            -*) echo "Error! Wrong argument: $1"; exit;;
        esac
    else
        dataFile=$1
    fi
    shift
done

if [ "$outpath" == "" ] ; then
    outpath=`dirname $dataFile`
fi
mkdir -p $outpath
#dataFile=/tmp/t2.txt

if [ ! -f "$dataFile" ]; then 
    echo "Error! dataFile = \"$dataFile\" does not exist. Exit..."
    exit
fi

basename=`basename "$dataFile"` 
if [ $mode -eq 0 ]; then
    xlabel="Threshold of fraction of TM2TM"
    colx=2
else
    xlabel="Threshold of fraction of TM2GAP"
    colx=3
fi

outputSetting=
case $outputStyle in
    term*)
    outputSetting=
    ;;
    png)
    outfile=$outpath/$basename.png
    outputSetting="
set terminal png enhanced
set output '$outfile' 
    "
    ;;
    eps)
    outfile=$outpath/$basename.eps
    pdffile=$outpath/$basename.pdf
    outputSetting="
set term postscript eps color
set output '$outfile' 
    "
    ;;
esac

/usr/bin/gnuplot -persist<<EOF 
$outputSetting
set style line 1 lt 1 lw 1 lc rgb "red"
set style line 2 lt 1 lw 1 lc rgb "blue" 
set style line 3 lt 1 lw 1 lc rgb "green"
set style line 4 lt 1 lw 1 lc rgb "violet"
set style line 5 lt 1 lw 1 lc rgb "cyan" 
set style line 6 lt 1 lw 1 lc rgb "orange"
set style line 7 lt 1 lw 1 lc rgb "grey40"
set style line 8 lt 1 lw 1 lc rgb "grey70"

set title ""
set xlabel "$xlabel"  font "Arial, 16"
set ylabel "$ylabel"  font "Arial, 16"
set key top center outside
#set key bottom center outside
#set key invert
#set label 1 at 3.5, 110
#set label 1 "Number of cases"

set yrange[0:]
set style data linespoints 
#set style histogram rowstacked
#set style fill solid border -1
#set boxwidth 0.8
set tics font 'Times-Roman,16'
set bmargin 5

plot \
    '$dataFile' using 4:xtic($colx)   title 'TM2TM' ls 1 , \
    ''          using 5:xtic($colx)   title 'TM2GAP' ls 2, \
    ''          using 6:xtic($colx)   title 'TM2SEQ' ls 3
#    ''          using (\$1):(\$3+\$4+\$5+\$6+\$7+3):9 title '' with labels
EOF

case $outputStyle in
    eps) my_epstopdf $outfile
        echo "Histogram image output to $pdffile"
        if [ -s "$pdffile" ]; then
            rm -f "$outfile"
        fi
        ;;
    *) echo "Histogram image output to $outfile" ;;
esac



#
# VBF
#

ls ../searches/hww2l2v/*/hww*_2j_*_7TeV.txt   | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale7TeV.py"}' | /bin/sh
ls ../searches/hww2l2v/*/hww*_2j_*_8TeV.txt   | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale8TeV.py"}' | /bin/sh


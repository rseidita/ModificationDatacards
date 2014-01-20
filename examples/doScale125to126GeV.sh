
#
# VH
#

ls ../searches/vhww/*/hww*_vh2j_*_7TeV.txt   | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale7TeV.py"}' | /bin/sh
ls ../searches/vhww/*/hww*_vh2j_*_8TeV.txt   | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale8TeV.py"}' | /bin/sh

# ls ../searches/hww2l2v/*/*_2j_shape_7TeV.txt | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale7TeV.py"}' | /bin/sh
# ls ../searches/hww2l2v/*/*_2j_shape_8TeV.txt | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale8TeV.py"}' | /bin/sh


#     ls ../RepositoryDataCard126/summer2013/searches/hww2l2v/*/*_2j_shape_7TeV.txt | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale7TeV.py"}'
#     ls ../RepositoryDataCard126/summer2013/searches/hww2l2v/*/*_2j_shape_7TeV.txt | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale7TeV.py"}' | /bin/sh

#     ls ../RepositoryDataCard126/summer2013/searches/vhww/*/hww*_vh2j_*_7TeV.txt | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale7TeV.py"}'
#     ls ../RepositoryDataCard126/summer2013/searches/vhww/*/hww*_vh2j_*_7TeV.txt | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale7TeV.py"}' | /bin/sh


#     ls ../RepositoryDataCard126/summer2013/searches/hww2l2v/*/*_2j_shape_8TeV.txt | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale8TeV.py"}'
#     ls ../RepositoryDataCard126/summer2013/searches/hww2l2v/*/*_2j_shape_8TeV.txt | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale8TeV.py"}' | /bin/sh

#     ls ../RepositoryDataCard126/summer2013/searches/vhww/*/hww*_vh2j_*_8TeV.txt | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale8TeV.py"}'
#     ls ../RepositoryDataCard126/summer2013/searches/vhww/*/hww*_vh2j_*_8TeV.txt | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale8TeV.py"}' | /bin/sh

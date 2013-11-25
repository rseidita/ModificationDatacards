ModificationDatacards
=====================

Several scripts to modify datacards

# Scale one sample by a factor

    python ScaleOneSample.py  -d hwwof_2j_shape_7TeV.txt    -i inputScale7TeV.py
    
and for multi-modifications:

    ls ../RepositoryDataCard126/summer2013/searches/hww2l2v/*/*_2j_shape_7TeV.txt | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale7TeV.py"}'
    ls ../RepositoryDataCard126/summer2013/searches/hww2l2v/*/*_2j_shape_7TeV.txt | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale7TeV.py"}' | /bin/sh
    
    ls ../RepositoryDataCard126/summer2013/searches/vhww/*/hww*_vh2j_*_7TeV.txt | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale7TeV.py"}'
    ls ../RepositoryDataCard126/summer2013/searches/vhww/*/hww*_vh2j_*_7TeV.txt | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale7TeV.py"}' | /bin/sh
    
    
    ls ../RepositoryDataCard126/summer2013/searches/hww2l2v/*/*_2j_shape_8TeV.txt | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale8TeV.py"}'
    ls ../RepositoryDataCard126/summer2013/searches/hww2l2v/*/*_2j_shape_8TeV.txt | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale8TeV.py"}' | /bin/sh
    
    ls ../RepositoryDataCard126/summer2013/searches/vhww/*/hww*_vh2j_*_8TeV.txt | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale8TeV.py"}'
    ls ../RepositoryDataCard126/summer2013/searches/vhww/*/hww*_vh2j_*_8TeV.txt | awk '{print "python ScaleOneSample.py  -d "$1"    -i inputScale8TeV.py"}' | /bin/sh

    
# Change the name of one sample

    python ChangeName.py  -d hwwof_2j_shape_7TeV.txt  -i inputName.py
    
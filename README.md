ModificationDatacards
=====================

Several scripts to modify datacards

Example working folder:

    cmsneu
    /afs/cern.ch/user/a/amassiro/Limit/ModificationDatacards



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

    python ChangeName.py        -d   hww-19.36fb.mH125.txt    -i   inputName.py


# Scale one nuisance

    python ScaleOneNuisance.py  -d   hww-19.36fb.mH125.txt    -i   inputScaleNuisance.py

# Transform gmN into lnN

  transform gmN into lnN.
  To easy perform signal injection without any bias (bug in combine?) and to remove gmN in case of "many" events in control region

    python TransformGmN.py  -d   hww-19.36fb.mH125.txt


# Transform shape datacard into cut based one

  transform a shape based datacard into a cut based one.
  To be performed for:
    * check of the gain of shape analysis, w.r.t just merging
    * easy read a simple cut based analysis, created through the shape package

    python TransformShapeToCutBased.py  -d   hww-19.36fb.mH125_toBeUsed.txt



e.g.

    python ../ScaleOneNuisance.py  -d   hwwof_0j_shape_8TeV.txt  -i   ../inputScaleNuisance.py
    cd /afs/cern.ch/user/a/amassiro/scratch0/VBF/Limit/CMSSW_6_1_0/src
    export SCRAM_ARCH=slc5_amd64_gcc462
    cmsenv
    cd -
    combine hwwof_0j_shape_8TeV.txt  -M MaxLikelihoodFit  --rMin=-1 --expectSignal=1 -t -1

    combineCards.py -S sf0j=hwwsf_0j_cut_8TeV.txt sf1j=hwwsf_1j_cut_8TeV.txt of0j=hwwof_0j_shape_8TeV.txt of1j=hwwof_1j_shape_8TeV.txt > total.txt

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


# Clone one sample:
  clone one sample into a sample with a new name. Used to split VH into ZH and WH

    python CloneSample.py    hww-19.36fb.mH125.sf_0j_shape.txt     -i   inputClonedName.py


# Remove one sample:
  remove one sample from the datacard. Used to remove useless (0) ttH sample

    python RemoveSample.py   hww-19.36fb.mH125.sf_0j_shape.txt    -i   inputRemoveName.py





# Specific examples



e.g.

    python ../ScaleOneNuisance.py  -d   hwwof_0j_shape_8TeV.txt  -i   ../inputScaleNuisance.py
    cd /afs/cern.ch/user/a/amassiro/scratch0/VBF/Limit/CMSSW_6_1_0/src
    export SCRAM_ARCH=slc5_amd64_gcc462
    cmsenv
    cd -
    combine hwwof_0j_shape_8TeV.txt  -M MaxLikelihoodFit  --rMin=-1 --expectSignal=1 -t -1

    combineCards.py -S sf0j=hwwsf_0j_cut_8TeV.txt sf1j=hwwsf_1j_cut_8TeV.txt of0j=hwwof_0j_shape_8TeV.txt of1j=hwwof_1j_shape_8TeV.txt > total.txt


e.g. for ww


    cd /afs/cern.ch/user/a/amassiro/Limit/ModificationDatacards
    mkdir ww
    scp amassiro@cmsneu:/home/amassiro/Latinos/Shape/playground/WW?Fcut?jet.tgz ww/
    cd ww
    tar -xf WWDFcut0jet.tgz
    mv datacards  WWDFcut0jet
    tar -xf WWDFcut1jet.tgz
    mv datacards  WWDFcut1jet
    tar -xf WWSFcut0jet.tgz
    mv datacards  WWSFcut0jet
    tar -xf WWSFcut1jet.tgz
    mv datacards  WWSFcut1jet

    cd WWDFcut0jet
    python ../../TransformShapeToCutBased.py  -d   hww-19.36fb.mH125.of_0j_shape.txt
    cd ..
    cd WWDFcut1jet
    python ../../TransformShapeToCutBased.py  -d   hww-19.36fb.mH125.of_1j_shape.txt
    cd ..
    cd WWSFcut0jet
    python ../../TransformShapeToCutBased.py  -d   hww-19.36fb.mH125.sf_0j_shape.txt
    cd ..
    cd WWSFcut1jet
    python ../../TransformShapeToCutBased.py  -d   hww-19.36fb.mH125.sf_1j_shape.txt
    cd ..

    rm -r WW?Fcut?jet/shapes/




e.g. for svn datacards https://svnweb.cern.ch/cern/wsvn/cmshcg/trunk/summer2013/

   mkdir couplings
   cd couplings
   svn co  svn+ssh://amassiro@svn.cern.ch/reps/cmshcg/trunk/summer2013/couplings/vhww

change VH into ZH and WH: 1.2427/0.4300 = WH/ZH:
  WH = 74%
  ZH = 26%



   svn co  svn+ssh://amassiro@svn.cern.ch/reps/cmshcg/trunk/summer2013/searches/hww2l2v
   svn co  svn+ssh://amassiro@svn.cern.ch/reps/cmshcg/trunk/summer2013/searches/vhww










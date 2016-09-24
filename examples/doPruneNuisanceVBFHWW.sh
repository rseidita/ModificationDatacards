
#
# VBF 2 jet
#

cd ~/Framework/Combine/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd -


ls /afs/cern.ch/user/a/amassiro/Framework/CMSSW_8_0_5/src/PlotsConfigurations/Configurations/VBF/datacards/*/*/*.txt  | grep -v "pruned"  |   \
    awk '{print "python PruneDatacard.py  -d "$1" -o "$1".pruned.txt --suppressNegative=True  --suppressFluctuationError=True -i examples/input_nuisances_to_prune_aggressive.py"}'   | /bin/sh


# clean samples
ls /afs/cern.ch/user/a/amassiro/Framework/CMSSW_8_0_5/src/PlotsConfigurations/Configurations/VBF/datacards/*_top_*/*/*.txt  | grep "pruned" | grep -v "filtered" |   \
    awk '{print "python RemoveSample.py   "$1" -o "$1".filtered.txt    -i examples/inputRemoveNameVBF.py"}'   | /bin/sh


ls /afs/cern.ch/user/a/amassiro/Framework/CMSSW_8_0_5/src/PlotsConfigurations/Configurations/VBF/datacards/*_dytt_*/*/*.txt  | grep "pruned" | grep -v "filtered" |   \
    awk '{print "python RemoveSample.py   "$1" -o "$1".filtered.txt    -i examples/inputRemoveNameVBF.py"}'   | /bin/sh

        
    

ls /afs/cern.ch/user/a/amassiro/Framework/CMSSW_8_0_5/src/PlotsConfigurations/Configurations/VBF/Moriond/datacards/*/*/*.txt  | grep -v "pruned"  |   \
    awk '{print "python PruneDatacard.py  -d "$1" -o "$1".pruned.txt --suppressNegative=True   -i examples/input_nuisances_to_prune.py"}'      | /bin/sh

    
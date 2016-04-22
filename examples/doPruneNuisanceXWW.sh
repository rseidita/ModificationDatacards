
#
# XWW 0/1 jet
#
        
ls /afs/cern.ch/user/a/amassiro/Framework/CMSSW_7_6_3/src/PlotsConfigurations/Configurations/EXO/WWlvlv/datacards/*/*/*.txt  | grep -v "pruned"  |   \
    awk '{print "python PruneDatacard.py  -d "$1" -o "$1".pruned.txt    -i examples/input_nuisances_to_prune.py"}' | /bin/sh


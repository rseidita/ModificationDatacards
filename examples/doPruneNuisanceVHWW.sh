
#
# VH 2 jet
#


ls /afs/cern.ch/user/a/amassiro/Framework/CMSSW_8_0_5/src/PlotsConfigurations/Configurations/VH2j/datacards/*/*/*.txt  | grep -v "pruned"  |   \
    awk '{print "python PruneDatacard.py  -d "$1" -o "$1".pruned.txt --suppressNegative=True   -i examples/input_nuisances_to_prune.py"}' | /bin/sh


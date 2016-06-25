
#
# ggH 0/1 jet
#

# python PruneDatacard.py  \
#         -d /afs/cern.ch/user/a/amassiro/Framework/CMSSW_7_6_3/src/PlotsConfigurations/Configurations/ggHTest/datacards/hww2l2v_13TeV_em_0j/mllVSmth/datacard.txt  \
#         -o /afs/cern.ch/user/a/amassiro/Framework/CMSSW_7_6_3/src/PlotsConfigurations/Configurations/ggHTest/datacards/hww2l2v_13TeV_em_0j/mllVSmth/datacard.txt  \
#         -i examples/input_nuisances_to_prune.py    
        
# ls /afs/cern.ch/user/a/amassiro/Framework/CMSSW_7_6_3/src/PlotsConfigurations/Configurations/ggH/datacards/*/*/*.txt  | grep -v "pruned"  |   \
#     awk '{print "python PruneDatacard.py  -d "$1" -o "$1".pruned.txt    -i examples/input_nuisances_to_prune.py"}' | /bin/sh
# 

ls /afs/cern.ch/user/a/amassiro/Framework/CMSSW_8_0_5/src/PlotsConfigurations/Configurations/ggH/datacards/*/*/*.txt  | grep -v "pruned"  |   \
    awk '{print "python PruneDatacard.py  -d "$1" -o "$1".pruned.txt  --suppressNegative=True    -i examples/input_nuisances_to_prune.py"}' | /bin/sh

ls /afs/cern.ch/user/a/amassiro/Framework/CMSSW_8_0_5/src/PlotsConfigurations/Configurations/ggH/Moriond/datacards/*/*/*.txt  | grep -v "pruned"  |   \
    awk '{print "python PruneDatacard.py  -d "$1" -o "$1".pruned.txt  --suppressNegative=True    -i examples/input_nuisances_to_prune.py"}' | /bin/sh

    
ls /afs/cern.ch/user/a/amassiro/Framework/CMSSW_8_0_5/src/PlotsConfigurations/Configurations/ggH2j/datacards/*/*/*.txt  | grep -v "pruned"  |   \
    awk '{print "python PruneDatacard.py  -d "$1" -o "$1".pruned.txt  --suppressNegative=True    -i examples/input_nuisances_to_prune.py"}' | /bin/sh


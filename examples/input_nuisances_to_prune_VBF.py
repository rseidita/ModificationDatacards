#
# Nuisances to prune
#
# nuisancesToPrune.update({'HRname'  : 'string'})
# 
#
# remove niusance that matches "string" in the name
#

nuisancesToPrune.update({'statMC'  : '*ibin_*_stat*'})

nuisancesToPrune.update({'fakeEle': '*fake_ele_stat*'})
nuisancesToPrune.update({'fakeMu' : '*fake_mu_stat*'})



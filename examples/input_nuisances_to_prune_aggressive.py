#
# Nuisances to prune
#
# nuisancesToPrune.update({'HRname'  : 'string'})
# 
#
# remove niusance that matches "string" in the name
#

nuisancesToPrune.update({'statMC'  : '*ibin_*_stat*'})

nuisancesToPrune.update({'jetScale': '*CMS_scale_j*'})

nuisancesToPrune.update({'fakeEle': '*fake_ele*'})
nuisancesToPrune.update({'fakeMu' : '*fake_mu*'})

nuisancesToPrune.update({'btagBC'   : '*ICHEP_btag_bc*'})
nuisancesToPrune.update({'btagUDSG' : '*ICHEP_btag_udsg*'})



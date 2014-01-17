#
# Code to remove one sample from the datacard
#

import re
from sys import argv
import os.path
from optparse import OptionParser
from math import sqrt,fabs

parser = OptionParser()
parser.add_option("-i", "--input", dest="nameFileChange", help="file with samples to remove (e.g. ttH)", default='blabla.py')

(options, args) = parser.parse_args()
options.bin = True # fake that is a binary output, so that we parse shape lines
options.noJMax = False
options.nuisancesToExclude = ''
options.stat = False


nameFactor = {}
if os.path.exists(options.nameFileChange):
    handle = open(options.nameFileChange,'r')
    exec(handle)
    handle.close()
print "nameFactor = ", nameFactor

import sys
sys.path.append('tools')
from DatacardParser import *

DC = parseCard(file(args[0]), options)
nuisToConsider = [ y for y in DC.systs ]

#for nuis in nuisToConsider:
    #if nuis[2] == 'gmN': gmN = nuis[3][0]
    #else               : gmN = 0
    #for channel in nuis[4]:
        ##print channel
        #if channel not in errors.keys(): errors[channel] = {}
        #for process in nuis[4][channel]:
            #if nuis[2] == 'gmN': gmN = nuis[3][0]
            #if nuis[4][channel][process] == 0: continue
            ##print nuis[2],gmN
            #if gmN != 0:
                #newError = nuis[4][channel][process] * sqrt(gmN) / DC.exp[channel][process]
            #else:
                ##print nuis[4][channel][process]
                #if not isinstance ( nuis[4][channel][process], float ) :
                    ## [0.95, 1.23]
                ##if len(nuis[4][channel][process]) == 2 :
                    #newError = fabs((nuis[4][channel][process][1]-nuis[4][channel][process][0])/2.)   # symmetrized
                #else : 
                    #newError = fabs(1-nuis[4][channel][process])
            #if process in errors[channel].keys():
                #errors[channel][process] += newError*newError
            #else:
                #errors[channel][process] = newError*newError

#for channel in errors:
    #for process in errors[channel]:
        #errors[channel][process] = sqrt(errors[channel][process])

#for x in DC.exp:
    #for y in DC.exp[x]:
        #print "%10s %10s %10.2f +/- %10.2f (rel = %10.2f)" % (x,y,DC.exp[x][y],DC.exp[x][y]*errors[x][y],errors[x][y])



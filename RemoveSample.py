#
# Code to remove one sample from the datacard
#

import re
from sys import argv
import os.path
from optparse import OptionParser
from math import sqrt,fabs

parser = OptionParser()
parser.add_option("-i", "--input",  dest="nameFileChange", help="file with samples to remove (e.g. ttH)", default='blabla.py')
parser.add_option("-o", "--output", dest="nameOutFileDC",  help="file where to dump the new DC", default='test.txt')

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



# copy header
# everything up to "observation", included

lines = open (args[0], 'r').read().split ('\n')

header = []

foundSecondTimeBin = 0
for line in lines:
  tempLine = line.split (' ')
  tempLine = filter(lambda a: a != '', tempLine)
  if len(tempLine)>0  and   tempLine[0] == 'bin' :    # the second time "bin" is the big list --> not in the header!
      foundSecondTimeBin = foundSecondTimeBin+1      
  if (foundSecondTimeBin <= 1) : header.append (line)


print header

print "#####################################"
#print DC.list_of_bins
listOfBins = DC.list_of_bins()
for binIterator in listOfBins:
    print binIterator
print "#####################################"


# write new datacard
filename = options.nameOutFileDC
f = open(filename, 'w')

# header
for line in header: f.write (line + '\n')
f.write ("---------------------------------------------------------------------------------------------------- \n")
# bin name
f.write ("bin                                 ")
for channel in DC.exp:
    for process in DC.exp[channel]:
        #print nameFactor.keys() --> ['WJet', 'ttH', 'qqH', 'VV']
        if (process not in nameFactor.keys()) or (process in nameFactor.keys() and (nameFactor[ process ] != "" and nameFactor[ process ] != channel)) :
            f.write ("%13s " % channel)
f.write("\n")

# process names (a.k.a. process)
f.write ("process                            ")
for channel, samples  in DC.exp.items():
    #print samples
    for process,rate in samples.items():
    #for process in DC.exp[channel]:
        if (process not in nameFactor.keys()) or (process in nameFactor.keys() and (nameFactor[ process ] != "" and nameFactor[ process ] != channel)) :
            f.write ("%13s " % process)
            #print "process = ",process

f.write("\n")

# indices numbers: -1  0  1  2  3 ...
f.write ("process                            ")
for channel, samples  in DC.exp.items():
    numSig = 0
    numBkg = 1
    for process,rate in samples.items():
        if (process not in nameFactor.keys()) or (process in nameFactor.keys() and (nameFactor[ process ] != "" and nameFactor[ process ] != channel)) :
            if DC.isSignal[process] :
                f.write ("%13d " % numSig)
                numSig = numSig - 1
            else :
                f.write ("%13d " % numBkg)
                numBkg = numBkg + 1
f.write("\n")

# rate
f.write ("rate ")
for channel, samples  in DC.exp.items():
    for process,rate in samples.items():
        if (process not in nameFactor.keys()) or (process in nameFactor.keys() and (nameFactor[ process ] != "" and nameFactor[ process ] != channel)) :
            f.write ("%9.4f " % DC.exp[channel][process] )
f.write("\n")

f.write ("---------------------------------------------------------------------------------------------------- \n")

# systematics
## list of [(name of uncert, boolean to indicate whether to float this nuisance or not, type, list of what additional arguments (e.g. for gmN), keyline element)]
for nuis in nuisToConsider:
    f.write ("%25s" % nuis[0]) # name
    if nuis[2] != 'gmN':
        f.write ("%10s" % nuis[2]) #lnN
    else :
        f.write ("%5s" % nuis[2]) # gmN
        f.write ("%5s" % nuis[3][0]) # Ncontrol

    f.write (" ")

    for channel, samples  in DC.exp.items():
        for process,rate in samples.items(): 
            if (process not in nameFactor.keys()) or (process in nameFactor.keys() and (nameFactor[ process ] != "" and nameFactor[ process ] != channel)) :
                if channel in nuis[4]:
                    if process in nuis[4][channel] :
                        if not isinstance ( nuis[4][channel][process], float ) :
                        # [0.95, 1.23]  ---> from 0.95/1.23
                            f.write ("   {0:4.3f}/{1:4.3f}".format(nuis[4][channel][process][0], nuis[4][channel][process][1]))
                        else :
                            if (nuis[4][channel][process] != 0) :
                                f.write ("%9.4f" % nuis[4][channel][process])
                            else :
                                f.write ("%13s" % "-")
                    else :
                        f.write ("%13s" % "-")
                else :
                    f.write ("%13s" % "-")
    f.write("\n")
f.close ()





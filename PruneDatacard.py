#!/usr/bin/python

######################################
# workaround to disable pyroot parser!
import sys
tmpargv = sys.argv
sys.argv = [ '-b','-n' ]
import ROOT
from ROOT import TFile, TH1F, TCanvas, gStyle, TLine
sys.argv = tmpargv
from optparse import OptionParser
######################################

import re
import os
import subprocess
import operator
from commands import getstatusoutput
from operator import itemgetter

import fnmatch

import math

import string

######################################

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

def PruneDatacard (datacardname, datacardnameOut, nameFileConfiguration) :

    # open the datacard file

    #currentFolder = getstatusoutput ('pwd')[1]
    #datacardname = currentFolder + '/' +  datacardname 
    print 'Opening original input datacard: ', datacardname
    lines = open (datacardname, 'r').read().split ('\n')
    nametag = datacardname.split ('/')[-1].replace ('.txt', '')
    thepath = datacardname.replace (nametag + '.txt', '')

    print "nametag = ",nametag
    print "thepath = ",thepath
    print "datacardnameOut = ", datacardnameOut

    # read datacard and separate bin, sample, rate, ...

    systime = 0
    header = []
    binName = []
    longListBin = [] # the bin list just before systematics
    sampleName = []
    reducedsampleName = [] # remove duplicate!
    sampleRate = []
    observation = []
    systematics = []
    systematicsName = []
    longListRateIndex = []
    rootFiles = {}
    firstTimeBin = True
    firstTimeProcess = True
    for line in lines:
      if '---' in line : continue
      if systime == 0 :
        tempLine = line.split (' ')
        tempLine = filter(lambda a: a != '', tempLine)
        #print " line.split (' ')[0] = ", line.split (' ')[0], "\n"
        if len(tempLine) == 0 : continue #skip if empty
        if tempLine[0] == 'bin' and firstTimeBin:
          binName = line.split (' ')
          binName = filter(lambda a: a != 'bin', binName)
          binName = filter(lambda a: a != '', binName)
          firstTimeBin = False
        elif tempLine[0] == 'bin':
          longListBin.append(line)
        elif tempLine[0] == 'observation' :
          observation.append(line)
        elif tempLine[0] == 'process' and firstTimeProcess:
          sampleName = line.split (' ')
          sampleName = filter(lambda a: a != 'process', sampleName)
          sampleName = filter(lambda a: a != '', sampleName)
          firstTimeProcess = False
        elif tempLine[0] == 'process':
          longListRateIndex.append(line)
        elif tempLine[0] == 'rate' :
          systime = 1
          sampleRate = line.split (' ')
          sampleRate = filter(lambda a: a != 'rate', sampleRate)
          sampleRate = filter(lambda a: a != '', sampleRate)
        else :
          header.append (line)
          # 0 1 2 3
          #shapes * hwwof_1j_shape_7TeV hwwof_1j.input_7TeV.root histo_$PROCESS histo_$PROCESS_$SYSTEMATIC
        if tempLine[0] == 'shapes' :
            tempRootList = line.split (' ')
            tempRootList = filter(lambda a: a != '', tempRootList)
            if tempRootList[1] == '*' :
              rootFiles[tempRootList[2]] = tempRootList[3]
      else:
        systematics.append (line)
        systematicsName.append (line.split (' ')[0])

    # clean empty systematics
    systematics = [elem for elem in systematics if len (elem.split ()) > 0]
    systematicsName = [elem for elem in systematicsName if len (elem.split ()) > 0]

    #print "header = ", header, "\n\n"
    #print "binName = ", binName, "\n\n"
    #print "sampleName = ", sampleName, "\n\n"
    #print "sampleRate = ", sampleRate, "\n\n"
    #print "systematics = ", systematics, "\n\n"
    #print "systematicsName = ", systematicsName, "\n\n"
    #print " --------------------------------------------------------------- "

    nuisancesToPrune = {}
    if os.path.exists(nameFileConfiguration):
      handle = open(nameFileConfiguration,'r')
      exec(handle)
      handle.close()

    print "nuisancesToPrune = ", nuisancesToPrune


    ## modify name with nameFactor
    #newNuisanceName = []
    #for name in systematicsName:
      #newName = name
      #if name in nameFactor :
         #newName = nameFactor[ name ]
      #newNuisanceName.append(newName)

    # remove duplicates in "sampleName"
    # used in scaling histograms in case of "matching"
    # and in case the same sample name is used in several "bin"
    # NB: the order is not preserved, but who cares!
    reducedsampleName = list(set(sampleName))

    # modify sample rate in root file!

    for rootFileBin in rootFiles:
      print "rootFile[", rootFileBin, "] = ",rootFiles[rootFileBin]
      # check if root file is present (the name must end with .root)
      matchfile = re.search(".root", rootFiles[rootFileBin])
      if not matchfile:
       continue
      rootFile = ROOT.TFile.Open(str(thepath)+"/"+str(rootFiles[rootFileBin]))

      # get the histograms
      histograms = {}
      for k in rootFile.GetListOfKeys():
        h = k.ReadObj()
        # only 1d histograms supported
        histoName = h.GetName()
        match = re.search("histo_", histoName)
        if not match:
          continue
        histograms[h.GetName()] = h

      # modify the histograms
      #outFile = ROOT.TFile.Open(str(thepath)+"/"+str(rootFiles[rootFileBin]+".new.root"),'recreate')


      #for histoName, histogram in histograms.iteritems():
        #for nuisance in systematicsName :
           #for sample in reducedsampleName:
             #match = bool("histo_"+str(sample)+"_"+str(nuisance)+"Down" == histoName) or bool("histo_"+str(sample)+"_"+str(nuisance)+"Up" == histoName)
             #if match:
               #if nuisance in nameFactor :
                 #newName = nameFactor[ nuisance ]

                 #nameTemp    = "histo_"+str(sample)+"_"+str(nuisance)
                 #newnameTemp = "histo_"+str(sample)+"_"+str(newName)
                 ##string.replace(s, old, new[, maxreplace])
                 #newhistoName = string.replace(histoName, nameTemp, newnameTemp, 1)
                 #print "newhistoName",newhistoName
                 #histogram.SetName(newhistoName)

      ## save new root file
      #for n,h in histograms.iteritems():
        #h.Write()
      #outFile.Close()

      #os.system ("mv "+str(thepath)+"/"+str(rootFiles[rootFileBin])+".new.root "+str(thepath)+"/"+str(rootFiles[rootFileBin]))
      #print "mv "+str(thepath)+"/"+str(rootFiles[rootFileBin])+".new.root "+str(thepath)+"/"+str(rootFiles[rootFileBin])


    # write new datacard
    filename = datacardnameOut
    f = open(filename, 'w')

    # header
    for line in header: f.write (line + '\n')

    f.write ("---------------------------------------------------------------------------------------------------- \n")
    # bin name
    f.write ("bin ")
    for it in range (len (binName)) :
      f.write (binName[it] + ' ')
    f.write ("\n")

    # observation
    for it in range (len (observation)) :
      f.write (observation[it] + '\n')

    f.write ("---------------------------------------------------------------------------------------------------- \n")
    # long list of bin
    for it in range (len (longListBin)) :
      f.write (longListBin[it] + '\n')

    # process names (a.k.a. samples)
    f.write ("process ")
    for it in range (len (sampleName)) :
      f.write (sampleName[it] + ' ')
    f.write ("\n")

    # long list of rate indexes
    for it in range (len (longListRateIndex)) :
      f.write (longListRateIndex[it] + '\n')


    # rate
    f.write ("rate ")
    for it in range (len (sampleRate)) :
      f.write (str(sampleRate[it]) + ' ')
    f.write ("\n")


    # systematics
    f.write ("---------------------------------------------------------------------------------------------------- \n")
    numSyst = 0
    for nuisance in systematicsName :
      #if nuisance in nameFactor :
        #newName = nameFactor[ nuisance ]
        ## change nuisance name
        #print "systematics : ",nuisance, " --> ", newName
        #tempsystematics = systematics[numSyst].split (' ')
        #tempsystematics = filter(lambda a: a != '', tempsystematics)

        #f.write (newName)
        #f.write (" ")

        #for itSampleSyst in range(len(tempsystematics)):
          #if itSampleSyst >=1 :
              #f.write(" ")
              #f.write(tempsystematics[itSampleSyst])
              #f.write(" ")
        #f.write ("\n")
      #else :
        #f.write (systematics[numSyst] + '\n')

      numSyst+=1


    f.close ()



######################################


if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-d", "--datacard",           dest="datacardInput",          help="datacard name", metavar="DATACARD")
    parser.add_option("-o", "--outdatacard",        dest="datacardOutput",         help="datacard name output", metavar="DATACARD")
    parser.add_option("-i", "--inputConfiguration", dest="nameFileConfiguration",  help="name configuration file with nuisances to remove", default='blabla.py')

    (options, args) = parser.parse_args()

    PruneDatacard (options.datacardInput, options.datacardOutput, options.nameFileConfiguration)



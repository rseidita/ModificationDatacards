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

######################################



# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

def ScaleOneNuisance (datacardname,systScale) :

    # open the datacard file

    currentFolder = getstatusoutput ('pwd')[1]
    datacardname = currentFolder + '/' +  datacardname 
    print 'Opening original input datacard: ', datacardname
    lines = open (datacardname, 'r').read().split ('\n')
    nametag = datacardname.split ('/')[-1].replace ('.txt', '')
    thepath = datacardname.replace (nametag + '.txt', '')

    print "nametag = ",nametag
    print "thepath = ",thepath

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
    systematicsType = []
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

        tempsystematicsName = line.split (' ')
        tempsystematicsName = filter(lambda a: a != '', tempsystematicsName)
        if (len (tempsystematicsName) >= 1) :
          systematicsName.append (tempsystematicsName[0])
          systematicsType.append (tempsystematicsName[1]) # gmN, lnN, shape ...


    # clean empty systematics
    systematics = [elem for elem in systematics if len (elem.split ()) > 0]
    systematicsName = [elem for elem in systematicsName if len (elem.split ()) > 0]
    systematicsType = [elem for elem in systematicsName if len (elem.split ()) > 0]


    #print "header = ", header, "\n\n"
    #print "binName = ", binName, "\n\n"
    #print "sampleName = ", sampleName, "\n\n"
    #print "sampleRate = ", sampleRate, "\n\n"
    #print "systematics = ", systematics, "\n\n"
    #print "systematicsName = ", systematicsName, "\n\n"
    #print "systematicsType = ", systematicsType, "\n\n"
    #print " --------------------------------------------------------------- "

    systScaleFactor = {}
    if os.path.exists(systScale):
      handle = open(systScale,'r')
      exec(handle)
      handle.close()

    print "systScaleFactor = ", systScaleFactor

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
      outFile = ROOT.TFile.Open(str(thepath)+"/"+str(rootFiles[rootFileBin]+".new.root"),'recreate')

      for histoName, histogram in histograms.iteritems():

        # modify nuisance systScaleFactor (check samples that are affected)
        numSystType = 0
        for systType in systematicsType:
          if systType == "shape" : # only shape here!
            if systematicsName[numSystType] in systScaleFactor :
              # change root file histogram
              # look for which samples are affected
              for sample in reducedsampleName:
                #print "histoName = ",histoName
                matchUp = bool("histo_"+str(sample)+"_"+systematicsName[numSample]+"Up"   == histoName)
                matchDo = bool("histo_"+str(sample)+"_"+systematicsName[numSample]+"Down" == histoName)

                if matchUp or matchDo:
                  additionalScale = float(systScaleFactor[systematicsName[numSystType]])
                  # what to do now?
                  # 1) get the nominal
                  # 2) sum the errors
                  # 3) scale the errors
                  histogram.Sumw2()
                  histogram.Scale(additionalScale)

          numSystType+=1


      # save new root file
      for n,h in histograms.iteritems():
        h.Write()
      outFile.Close()

      os.system ("mv "+str(thepath)+"/"+str(rootFiles[rootFileBin])+".new.root "+str(thepath)+"/"+str(rootFiles[rootFileBin]))
      print "mv "+str(thepath)+"/"+str(rootFiles[rootFileBin])+".new.root "+str(thepath)+"/"+str(rootFiles[rootFileBin])


    # write new datacard
    filename = str(thepath) + '/' + str(nametag) + '.txt'
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
    numSystType = 0
    for systType in systematicsType:
      if systType != "shape" and  systType != "gmN" :
        # shape already taken into account in the root file histogram
        # gmN cannot be scaled properly with this method!
        if systematicsName[numSystType] in systScaleFactor :
          # print "systematics : ",systematics[numSystType]
          # now scale
          tempsystematics = systematics[numSystType].split (' ')
          tempsystematics = filter(lambda a: a != '', tempsystematics)

          f.write (tempsystematics[0])
          f.write (" ")
          f.write (tempsystematics[1])
          f.write (" ")

          for itSampleSyst in range(len(tempsystematics)):
            f.write (" ")
            if itSampleSyst >=2 and tempsystematics[itSampleSyst] != "-" :
             additionalScale = float(systScaleFactor[systematicsName[numSystType]])
             currentValue = float(tempsystematics[itSampleSyst])  # 1.10 or 0.90
             currentValue = currentValue - 1.00    #0.10 or -0.10
             currentValue = currentValue * additionalScale
             f.write (str(currentValue+1.00))
          f.write ("\n")
        else :
          f.write (systematics[numSystType] + '\n')
      else :
        f.write (systematics[numSystType] + '\n')

      numSystType+=1

    f.close ()



######################################


if __name__ == '__main__':


    #if len (sys.argv) < 2 :
        #print 'input datacard folder missing\n'
        #exit (1)

    parser = OptionParser()
    parser.add_option("-d", "--datacard", dest="datacardInput", help="datacard name", metavar="DATACARD")
    parser.add_option("-i", "--input", dest="systScale", help="systematic scaling (e.g. Wjets scaled by a factor 1.5)", default='blabla.py')
 
    (options, args) = parser.parse_args()

    ScaleOneNuisance (options.datacardInput,options.systScale)



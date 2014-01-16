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

def TransformShapeToCutBased (datacardname) :

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
    completeSampleNameLine = []
    sampleName = []
    reducedsampleName = [] # remove duplicate!
    completeSampleRateLine = []
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
          completeSampleNameLine.append(line)
          sampleName = line.split (' ')
          sampleName = filter(lambda a: a != 'process', sampleName)
          sampleName = filter(lambda a: a != '', sampleName)
          firstTimeProcess = False
        elif tempLine[0] == 'process':
          longListRateIndex.append(line)
        elif tempLine[0] == 'rate' :
          systime = 1
          completeSampleRateLine.append(line)
          sampleRate = line.split (' ')
          sampleRate = filter(lambda a: a != 'rate', sampleRate)
          sampleRate = filter(lambda a: a != '', sampleRate)
        else :
          header.append (line)
          # 0 1 2 3
          #shapes * hwwof_1j_shape_7TeV hwwof_1j.input_7TeV.root histo_$PROCESS histo_$PROCESS_$SYSTEMATIC
        if tempLine[0] == 'shapeN2' or tempLine[0] == 'shapes' :
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
    systematicsType = [elem for elem in systematicsType if len (elem.split ()) > 0]


    #print "header = ", header, "\n\n"
    #print "binName = ", binName, "\n\n"
    #print "sampleName = ", sampleName, "\n\n"
    #print "sampleRate = ", sampleRate, "\n\n"
    #print "systematics = ", systematics, "\n\n"
    #print "systematicsName = ", systematicsName, "\n\n"
    #print "systematicsType = ", systematicsType, "\n\n"
    #print " --------------------------------------------------------------- "


    # remove duplicates in "sampleName"
    # NB: the order is not preserved, but who cares!
    reducedsampleName = list(set(sampleName))




    # look for shape nuisances
    # if found calculate the effect on each sample and translate into a number  0.95/1.10  -> 5% down, 10% up

    numSystType = 0
    for systType in systematicsType:
      if systType == "shape" or systType == "shapeN2" : # only shape here!

        print "systematics : ",systematics[numSystType]
        tempsystematics = systematics[numSystType].split (' ')
        tempsystematics = filter(lambda a: a != '', tempsystematics)

        #  tempsystematics[0] -> the name
        #  tempsystematics[1] -> the type: "shape" or "shapeN2"

        for itSampleSyst in range(len(tempsystematics)):
          if itSampleSyst >=2 and tempsystematics[itSampleSyst] != "-" :
            # possible global scale of the nuisance (sign may be important for correlation?)
            tempScale = float(tempsystematics[itSampleSyst])

            nameSamepleWithThisNuisance = sampleName[itSampleSyst-2]

            # get root file and calculate the uncertainty
            histograms = {}
            for rootFileBin in rootFiles:
              #print "rootFile[", rootFileBin, "] = ",rootFiles[rootFileBin]
              # check if root file is present (the name must end with .root)
              matchfile = re.search(".root", rootFiles[rootFileBin])
              if not matchfile:
                continue
              rootFile = ROOT.TFile.Open(str(thepath)+"/"+str(rootFiles[rootFileBin]))

              # get the histograms
              foundAll = 0
              for k in rootFile.GetListOfKeys():
                h = k.ReadObj()
                # only 1d histograms supported
                histoName = h.GetName()

                # histo_SAMPLENAME_NUISANCENAME
                # histo_WJet_CMS_8TeV_hww_WJet_of_2jtche05_stat_bin1

                match = bool("histo_"+str(nameSamepleWithThisNuisance)+"_"+tempsystematics[0]+"Up"   == histoName)
                if match:
                  histograms["Up"] = h
                  foundAll+=1

                match = bool("histo_"+str(nameSamepleWithThisNuisance)+"_"+tempsystematics[0]+"Down" == histoName)
                if match:
                  histograms["Down"] = h
                  foundAll+=1

                match = bool("histo_"+str(nameSamepleWithThisNuisance) == histoName)
                if match:
                  histograms["Nominal"] = h
                  foundAll+=1

              #print "  foundAll = ", foundAll
              if foundAll != 3 :
                print " ERROR: syst = ", tempsystematics[0]
                #integralUp      = 1.00
                #integralDown    = 1.00
                #integralNominal = 1.00

              else :
                integralUp      = histograms["Up"].Integral()
                integralDown    = histograms["Down"].Integral()
                integralNominal = histograms["Nominal"].Integral()

                if integralNominal == 0:
                  integralNominal = 1.0
                  integralUp      = 1.00
                  integralDown    = 1.00

              rootFile.Close()


            # calculate nuisance
            tempsystematics[itSampleSyst] = str( round ( ( (1.00 - (integralNominal-integralDown) / integralNominal ) * tempScale ) , 3 ))   + "/" + str(   round(  (1.00 + (integralUp - integralNominal) / integralNominal ) * tempScale ,  3) )
            print " now:: ",tempsystematics[0],"  :: ",nameSamepleWithThisNuisance," = ",tempsystematics[itSampleSyst]


        # correct nuisance
        tempNewNuisance = ""

        #  tempsystematics[0] -> the name
        #  tempsystematics[1] -> the type: "shape" or "shapeN2"

        for itSampleSyst in range(len(tempsystematics)):
          tempNewNuisance =  tempNewNuisance + tempsystematics[itSampleSyst]
          tempNewNuisance =  tempNewNuisance + "  "

        systematics[numSystType] = tempNewNuisance

      numSystType = numSystType + 1



    print " write new datacard "

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
    for it in range (len (completeSampleNameLine)) :
      f.write (completeSampleNameLine[it] + '\n')

    #f.write ("process ")
    #for it in range (len (sampleName)) :
      #f.write (sampleName[it] + ' ')
    #f.write ("\n")

    # long list of rate indexes
    for it in range (len (longListRateIndex)) :
      f.write (longListRateIndex[it] + '\n')


    # rate
    for it in range (len (completeSampleRateLine)) :
      f.write (completeSampleRateLine[it] + '\n')
    #f.write ("rate ")
    #for it in range (len (sampleRate)) :
      #f.write (str(sampleRate[it]) + ' ')
    #f.write ("\n")


    # systematics
    f.write ("---------------------------------------------------------------------------------------------------- \n")
    numSystType = 0
    for systType in systematicsType:
      if systType == "shapeN2" or systType == "shape" :
        #print "systematics : ",systematics[numSystType]

        tempsystematics = systematics[numSystType].split (' ')
        tempsystematics = filter(lambda a: a != '', tempsystematics)

        f.write (tempsystematics[0].ljust(48-6))
        f.write ("lnN".ljust(15))

        for itSampleSyst in range(len(tempsystematics)):
          if itSampleSyst >=2 :
              f.write(tempsystematics[itSampleSyst].ljust(15))
        f.write ("\n")
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

    (options, args) = parser.parse_args()

    TransformShapeToCutBased (options.datacardInput)



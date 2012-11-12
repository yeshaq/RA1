import ROOT as r
import os


models = ["T2bb","T1bbbb"]
htBins = ["275_scaled","325_scaled","375"]
weightedOrNot = ["","wPdfWeights"]

for weightSwitch in weightedOrNot :
    for model in models :
        haddString = ""
        for htBin in htBins :
            haddString += "%s_%s_calo_ge2_%s.root "%(model,htBin,weightSwitch)
        haddCmd = "hadd %s_275_calo_ge2_%s.root "%(model,weightSwitch) + haddString     
        print haddCmd
        os.system(haddCmd)


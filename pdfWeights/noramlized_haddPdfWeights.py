import ROOT as r
import os


models = ["T2bb","T1bbbb"]
htBins = ["275_scaled","325_scaled","375"]
#weightedOrNot = ["","wPdfWeights"]
weightedOrNot = ["","gencteq66","genMSTW2008nlo68cl"]
scaleSlices = ["","normalized_"]

for weightSwitch in weightedOrNot :
    for model in models :
        for scale in scaleSlices :
            haddString = ""
            for htBin in htBins :
                haddString += "%s%s_%s_%s.root "%(scale,model,htBin,weightSwitch)
                haddCmd = "hadd -f %s%s_275_%s.root "%(scale,model,weightSwitch) + haddString     
            print haddCmd
            os.system(haddCmd)


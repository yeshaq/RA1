import ROOT as r
import os


models = ["T2bb","T1bbbb_nnpdf_ct10"][1:2]
htBins = ["275_scaled","325_scaled","375"]
mods_and_pdfs = [("T1bbbb",["","_gencteq66","_genMSTW2008nlo68cl"]),("T1bbbb_nnpdf",["","_genNNPDF21"]),("T1bbbb_ct10",["","_genct10"])]
for modAndPdf in mods_and_pdfs:
    for variation in modAndPdf[1] :
        haddString = ""
        for htBin in htBins :
            haddString += "output/acc_%s_%s%s.root "%(modAndPdf[0],htBin,variation)
        haddCmd = "hadd output/acc_%s_275%s.root "%(modAndPdf[0],variation) + haddString     
        print haddCmd
        os.system(haddCmd)



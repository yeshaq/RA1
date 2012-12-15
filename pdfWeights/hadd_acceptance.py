import ROOT as r
import common as c
import os

mods_and_pdfs = c.mods_and_pdfs
for modAndPdf in mods_and_pdfs :
    modAndPdf[1].append("")
    for variation in modAndPdf[1] :
        haddString = ""
        for htBin in c.htbins :
            if variation : 
                haddString += "output/acc_%s_%s_%s.root "%(modAndPdf[0],htBin[0],variation)
                haddCmd = "hadd output/acc_%s_275_%s.root "%(modAndPdf[0],variation) + haddString     
            else : 
                haddString += "output/acc_%s_%s.root "%(modAndPdf[0],htBin[0])
                haddCmd = "hadd output/acc_%s_275.root "%modAndPdf[0] + haddString     
        print haddCmd
        os.system(haddCmd)



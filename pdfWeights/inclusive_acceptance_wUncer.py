import ROOT as r
import common as c
import os, math

canvas = r.TCanvas()
canvas.SetRightMargin(0.2)
canvas.SetTickx()
canvas.SetTicky()

htBins = [c.htbins[0][0].strip("_scaled")]

for modAndPdf in c.mods_and_pdfs :
    for ht in htBins :
        for pdfSet in modAndPdf[1] :
            #epsFileName = "output/acc_%s_%s.eps"%(modAndPdf[0],ht,pdfSet)
            numFile = r.TFile("output/acc_%s_%s.root"%(modAndPdf[0].replace("_nnpdf_ct10",""),ht),"READ")
            numHist = numFile.Get("nEvents")
            
            denFile = r.TFile("output/acc_%s_%s_%s.root"%(modAndPdf[0],ht,pdfSet),"READ")
            denHist = []
            for i in range(c.nPdfDict[pdfSet]) : 
                denHist.append(denFile.Get("nEvents_%s_%s"%(pdfSet,i)))
            result = numHist.Clone()
            result.Divide(denHist[0])
    
            result.SetTitle(";m_{parent} (GeV);m_{LSP} (GeV);ratio") 
            result.SetMarkerStyle(20)
            result.SetStats(False)
            
            for xbin in range(denHist[0].GetXaxis().GetNbins()) :
                for ybin in range(denHist[0].GetYaxis().GetNbins()) :
                    if (ybin*25 > xbin*25 - 175) or (xbin*25 <= 300)  : result.SetBinContent(xbin,ybin,0.0) 


            for xbin in range(denHist[0].GetXaxis().GetNbins()) :
                for ybin in range(denHist[0].GetYaxis().GetNbins()) :
                    if (result.GetBinContent(xbin,ybin)) == 0.0 : continue
                    centralAcc = denHist[0].GetBinContent(xbin,ybin)
                    dPlus = 0.
                    dMinus = 0.
                    #wp = 0.
                    #wm = 5.
                    if centralAcc == 0 : continue 
                    for i in range(c.nPdfDict[pdfSet]/2) :
                        wp = denHist[2*i+1].GetBinContent(xbin,ybin)/denHist[0].GetBinContent(xbin,ybin) - 1
                        wm = denHist[2*i+2].GetBinContent(xbin,ybin)/denHist[0].GetBinContent(xbin,ybin) - 1
                        if (wp>wm) :
                            if (wp<0.) : wp = 0.
                            if (wm>0.) : wm = 0.
                            dPlus  += wp*wp
                            dMinus += wm*wm
                        if (wp<wm) :
                            if (wm<0.) : wm = 0.
                            if (wp>0.) : wp = 0.
                            dPlus  += wm*wm
                            dMinus += wp*wp

                    if (dPlus>0)  : dPlus = math.sqrt(dPlus)
                    if (dMinus>0) : dMinus = math.sqrt(dMinus)
                    if denHist[0].GetBinContent(xbin,ybin) > 0  : 
                        print "---------------------------------------------------------------------------------------------"
                        print "centr. accept = %.3f"%(100*centralAcc)
                        print "ie. %.3f relative variation with respect to original PDF"%((100*(centralAcc-numHist.GetBinContent(xbin,ybin))/numHist.GetBinContent(xbin,ybin)))
                        result.SetBinContent(xbin,ybin,(100*(centralAcc-numHist.GetBinContent(xbin,ybin))/numHist.GetBinContent(xbin,ybin)))
                        print "Relative uncertianty with respect to central member: +%.3f / -%.3f"%(100*dPlus,100*dMinus)

import ROOT as r
import common as c 

canvas = r.TCanvas()
canvas.SetRightMargin(0.2)
canvas.SetTickx()
canvas.SetTicky()

def numerAndDenom(histName, befDir,afDir) :
    d = {}
    beforeHist = befDir.Get(histName) 
    d["before"] = beforeHist.Clone()
    afterHist = afDir.Get(histName)
    d["after"] = afterHist.Clone()
    return d

def rebinT2cc(hist, nRebinX, nRebinY) :
    hist.RebinX(nRebinX)
    hist.RebinY(nRebinY)
    return hist

for weight in c.weights :
    if weight == "" :
        for modAndPdf in c.mods_and_pdfs :
            for ht in c.htbins :
                rtfile = "%s/%s_calo_ge2_%s/%s_plots.root"%(c.version,ht[0],weight,modAndPdf[0])

#                if "T2cc" in modAndPdf[0] :
#                    beforeHist = r.TH2D("nEvents_before","nEvents",35,100,275,50,10,260)
#                    afterHist =  r.TH2D("nEvents_after","nEvents",35,100,275,50,10,260)                
#                else :
#                    beforeHist = r.TH2D("nEvents_before","nEvents",81,0,2025,81,0,2025)
#                    afterHist =  r.TH2D("nEvents_after","nEvents",81,0,2025,81,0,2025)
#                    
                infile = r.TFile(rtfile,"READ")
                befdir = infile.GetDirectory("master/progressPrinter/label/scanHistogrammer/")
                befkeylist = befdir.GetListOfKeys()        

                for key in befkeylist :
                    if key.ReadObj().GetName() == "nEvents":
                        before = key.ReadObj()
                        beforeHist = before.Clone()
                        beforeHist = c.resizeHisto(beforeHist, 35, 100, 275, 50, 10, 260)
                        beforeHist = c.shift2DHistos(beforeHist, -0.5, -0.5, 5, 1)
                        beforeHist.Draw("colz")
                        canvas.Print("test.pdf")
                afdir = infile.GetDirectory(ht[1])
                afkeylist = afdir.GetListOfKeys()
                for key in afkeylist :
                    if key.ReadObj().GetName() == "nEvents":
                        after = key.ReadObj()
                        afterHist = after.Clone()
                        afterHist = c.resizeHisto(afterHist, 35, 100, 275, 50, 10, 260)
                        afterHist = c.shift2DHistos(afterHist, -0.5, -0.5, 5, 1)
                        afterHist.Divide(beforeHist)
                outfile = r.TFile("output/acc_%s_%s.root"%(modAndPdf[0],ht[0]),"RECREATE") 
                afterHist.Write()
                            
    if weight == "wPdfWeights" :
        for modAndPdf in c.mods_and_pdfs :
            for pdfSet in modAndPdf[1] :
                for ht in c.htbins :
                    rtfile = "%s/%s_calo_ge2_%s/%s_plots.root"%(c.version,ht[0],weight,modAndPdf[0])

                    if "T2cc" in modAndPdf[0] :
                        beforeHist = r.TH2D("nEvents_before","nEvents",35,100,275,50,10,260)
                        afterHist =  r.TH2D("nEvents_after","nEvents",35,100,275,50,10,260)                
                    else :
                        beforeHist = r.TH2D("nEvents_before","nEvents",81,0,2025,81,0,2025)
                        afterHist =  r.TH2D("nEvents_after","nEvents",81,0,2025,81,0,2025)
            
                    infile = r.TFile(rtfile,"READ")
                    befdir = infile.GetDirectory("master/progressPrinter/label/scanHistogrammer/")
                    befkeylist = befdir.GetListOfKeys()
                    outfile = r.TFile("output/acc_%s_%s_%s.root"%(modAndPdf[0],ht[0],pdfSet),"RECREATE") 

                    afdir = infile.GetDirectory(ht[1])
                    afkeylist = afdir.GetListOfKeys()
                    histList = ["nEvents_%s_%s"%(pdfSet,i) for i in range(c.nPdfDict[pdfSet])]
                    varInAcc ={} 

                    for xbin in range(afkeylist[0].ReadObj().GetXaxis().GetNbins()) :
                        for ybin in range(afkeylist[0].ReadObj().GetYaxis().GetNbins()) :
                                if not afkeylist[0].ReadObj().GetBinContent(xbin,ybin) == 0.0 :
                                    mpair = (xbin,ybin)
                                    varInAcc["Acceptance_%s_%s"%mpair] = r.TH1D("Acceptances_%s_%s"%mpair, "Acceptances_%s_%s"%mpair, 2000, 0, .55)
                    for ihist,hist in enumerate(histList) :
                         histos = numerAndDenom(hist,befdir,afdir)
                         result = histos["after"].Clone()
                         result.Divide(histos["before"])
                         for xbin in range(result.GetXaxis().GetNbins()) :
                            for ybin in range(result.GetYaxis().GetNbins()) :
                                mpair = (xbin,ybin)
                                acc = []
                                #if xbin == 3 and ybin == 3 : varInAcc.Fill((xbin*5)+90,((ybin*5)+10), 100*result.GetBinContent(xbin,ybin))
                                #if not result.GetBinContent(xbin,ybin) == 0.0 : varInAcc.Fill(100*result.GetBinContent(xbin,ybin))
                                acc.append(xbin)
                                acc.append(ybin)
                                if not result.GetBinContent(xbin,ybin) == 0.0 : varInAcc["Acceptance_%s_%s"%mpair].Fill(100*result.GetBinContent(xbin,ybin))
                         result = c.resizeHisto(result, 35, 100, 275, 50, 10, 260)
                         result = c.shift2DHistos(result, -0.5, -0.5, 5, 1)
                         print "Start:"
                         print ht[0]
                         print pdfSet 
                         print hist
                         print result.GetXaxis().GetNbins()
                         print result.GetYaxis().GetNbins()
                         print result.GetBinContent(1,2)
                         print "End"
                         print ""
                         result.Write()
                    for key in varInAcc : varInAcc[key].Write()

                         


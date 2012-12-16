import ROOT as r
import common as c 

def numerAndDenom(histName, befDir,afDir) :
    d = {}
    beforeHist = befDir.Get(histName) 
    d["before"] = beforeHist.Clone()
    afterHist = afDir.Get(histName)
    d["after"] = afterHist.Clone()
    return d


for weight in c.weights :
    if weight == "" :
        for modAndPdf in c.mods_and_pdfs :
            for ht in c.htbins :
                rtfile = "%s/%s_calo_ge2_%s/%s_plots.root"%(c.version,ht[0],weight,modAndPdf[0])
                beforeHist = r.TH2D("nEvents_before","nEvents",81,0,2025,81,0,2025)
                afterHist =  r.TH2D("nEvents_after","nEvents",81,0,2025,81,0,2025)
                infile = r.TFile(rtfile,"READ")
                befdir = infile.GetDirectory("master/progressPrinter/label/scanHistogrammer/")
                befkeylist = befdir.GetListOfKeys()        
                for key in befkeylist :
                    if key.ReadObj().GetName() == "nEvents":
                        before = key.ReadObj()
                        beforeHist = before.Clone()
                afdir = infile.GetDirectory(ht[1])
                afkeylist = afdir.GetListOfKeys()
                for key in afkeylist :
                    if key.ReadObj().GetName() == "nEvents":
                        after = key.ReadObj()
                        afterHist = after.Clone()  
                afterHist.Divide(beforeHist)
                outfile = r.TFile("output/acc_%s_%s.root"%(modAndPdf[0],ht[0]),"RECREATE") 
                afterHist.Write()
                            
    if weight == "wPdfWeights" :
        for modAndPdf in c.mods_and_pdfs :
            for pdfSet in modAndPdf[1] :
                for ht in c.htbins :
                    rtfile = "%s/%s_calo_ge2_%s/%s_plots.root"%(c.version,ht[0],weight,modAndPdf[0])
                    beforeHist = r.TH2D("nEvents_before","nEvents",81,0,2025,81,0,2025)
                    afterHist =  r.TH2D("nEvents_after","nEvents",81,0,2025,81,0,2025)
                    infile = r.TFile(rtfile,"READ")
                    befdir = infile.GetDirectory("master/progressPrinter/label/scanHistogrammer/")
                    befkeylist = befdir.GetListOfKeys()
                    outfile = r.TFile("output/acc_%s_%s_%s.root"%(modAndPdf[0],ht[0],pdfSet),"RECREATE") 
                    afdir = infile.GetDirectory(ht[1])
                    afkeylist = afdir.GetListOfKeys()
                    histList = ["nEvents_%s_%s"%(pdfSet,i) for i in range(c.nPdfDict[pdfSet])]
                    for hist in histList :
                         histos = numerAndDenom(hist,befdir,afdir)
                         result = histos["after"].Clone()
                         result.Divide(histos["before"])
                         result.Write()

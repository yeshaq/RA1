import ROOT as r
import common as c
import os,subprocess

r.gROOT.SetBatch(True)
r.gErrorIgnoreLevel = r.kError

def modelParser(toBeParsed = "", parsed = "") :
    parsed = toBeParsed.replace("_nnpdf","").replace("_ct10","")
    return parsed

def rebinT2cc(hist, nRebinX, nRebinY) :
    hist.RebinX(nRebinX)
    hist.RebinY(nRebinY)
    return hist



for jet in ["pf","calo"]:
        scaleFile = r.TFile("%s/%sJet_pn_T2cc.root"%(c.version,jet),"READ")##
        outfile = r.TFile("normalized_acc_output/%s/%sJet_normalized.root"%(c.version,jet),"UPDATE") 
        for modAndPdf in c.mods_and_pdfs :
            for pdfSet in modAndPdf[1] :

                scaleHist = scaleFile.Get("eff_T2cc" if not "MSTW" in pdfSet else "eff_T2cc_mstw")
        
                #for iweight in range(c.nPdfDict[pdfSet]) :
                print "ScaleHist has %d Y bins"%scaleHist.GetYaxis().GetNbins()
                print "--------"
                print "scale @ (%d,%d) = %s"%(2,8,scaleHist.GetBinContent(2,8))
                rtfile = "%s/%s_pv_T2cc.root"%(c.version,modAndPdf[2])
                infile = r.TFile(rtfile,"READ")
                infile.Get._creates = True
                befdir = infile.GetDirectory("")
                befkeylist = befdir.GetListOfKeys()        
                for key in befkeylist :
                    if "before" in key.GetName() or "eff" in key.GetName(): continue
                    after = key.ReadObj()
                    hist = after.Clone()
                    before = infile.Get("before_T2cc_nEvents_%s_%s"%tuple(hist.GetName().split("_")[-2:]))
                    eff = infile.Get("eff_T2cc_%s_%s"%tuple(hist.GetName().split("_")[-2:]))
                    if "mstw" in hist.GetName():
                        before = infile.Get("before_T2cc_mstw_nEvents_%s_%s"%tuple(hist.GetName().split("_")[-2:]))
                        eff = infile.Get("eff_T2cc_mstw_%s_%s"%tuple(hist.GetName().split("_")[-2:]))
                    #eff = infile.Get(hist.GetName().replace("after","eff").replace("_nEvents",""))
                    
                    
                    print "Weight index is %s"%hist.GetName()
                    print "hist has %d Y bins"%hist.GetYaxis().GetNbins()
                    print "Original Hist @ (%d,%d) = %s"%(2,8,hist.GetBinContent(2,8))
                    hist.Multiply(scaleHist)
                    hist.Divide(eff)
                    print "Scaled Hist @ (%d,%d) = %s"%(2,8,hist.GetBinContent(2,8))
                    hist.Divide(before)
                    hist.SetName(hist.GetName().replace("after","eff").replace("_nEvents","").replace("_mstw",""))
                    hist.SetTitle(hist.GetName())
                    ##eff.SetName(hist.GetName().replace("after","eff").replace("_nEvents","").replace("_mstw",""))
                    ##eff.SetTitle(hist.GetName())

                    ##eff.Write()
                    outfile.cd()
                    hist.Write("",r.TObject.kOverwrite)
                    


                                     


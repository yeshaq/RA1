import ROOT as r
import common as c
import os,subprocess

def modelParser(toBeParsed = "", parsed = "") :
    parsed = toBeParsed.replace("_nnpdf","").replace("_ct10","")
    return parsed

def rebinT2cc(hist, nRebinX, nRebinY) :
    hist.RebinX(nRebinX)
    hist.RebinY(nRebinY)
    return hist


for weight in c.weights :
    if weight == "" :
        for modAndPdf in c.mods_and_pdfs :
            for ht in c.htbins :
                rtfile = "%s/%s_calo_ge2_%s/%s_plots.root"%(c.version,ht[0],weight,modAndPdf[0])
                outfile = r.TFile("limit_format_output/%s_%s.root"%(modAndPdf[0],ht[0]),"RECREATE") 

#                if "T2cc" in modAndPdf[0] :
#                    m0_m12_mChi_noweight = r.TH2D("m0_m12_mChi_noweight","Dummy Histo",35,100,260,50,10,260)
#                else :
#                    m0_m12_mChi_noweight = r.TH2D("m0_m12_mChi_noweight","Dummy Histo",81,0,2025,81,0,2025)

                for dirname in c.dirNames :
                    outfile.mkdir(dirname)
                    outfile.cd(dirname)
                outfile.Write()
                infile = r.TFile(rtfile,"READ")
                befdir = infile.GetDirectory("master/progressPrinter/label/scanHistogrammer/")
                befkeylist = befdir.GetListOfKeys()        
                for key in befkeylist :
                    if key.ReadObj().GetName() == "nEvents":
                        before = key.ReadObj()
                        m0_m12_mChi_noweight = before.Clone()
                        if "T2cc" in modAndPdf[0] : 
                            m0_m12_mChi_noweight = c.resizeHisto(m0_m12_mChi_noweight, 35, 100, 275, 50, 10, 260)
                            m0_m12_mChi_noweight = c.shift2DHistos(m0_m12_mChi_noweight, -0.5, -0.5, 5, 1)
                        m0_m12_mChi_noweight.SetName("m0_m12_mChi_noweight")
                        outfile.cd("smsScan_before")
                        m0_m12_mChi_noweight.Write("",r.TObject.kOverwrite)
                afdir = infile.GetDirectory(ht[1])
                afkeylist = afdir.GetListOfKeys()
                histList375 = []
                for key in afkeylist :
                    if key.ReadObj().GetName() in c.keyNames :
                        keyName = key.ReadObj().GetName()
                        if (ht[0] == "375" and "ge4j_ge4b" in keyName) :
                            histList375.append(key.ReadObj())
                        after = key.ReadObj()
                        keyName = keyName.replace("nEvents_","")
                        keyName = keyName.split("_")
                        njet = keyName[0]
                        nbjet = keyName[1]
                        keyName.remove(njet)
                        keyName.remove(nbjet)
                        htbin = "_".join(keyName)
                        m0_m12_mChi_noweight = after.Clone()
                        if "T2cc" in modAndPdf[0] : 
                            m0_m12_mChi_noweight = c.resizeHisto(m0_m12_mChi_noweight, 35, 100, 275, 50, 10, 260)
                            m0_m12_mChi_noweight = c.shift2DHistos(m0_m12_mChi_noweight, -0.5, -0.5, 5, 1)
                        m0_m12_mChi_noweight.SetName("m0_m12_mChi_noweight")
                        print "m0_m12_mChi_noweight has %d Y bins"%m0_m12_mChi_noweight.GetYaxis().GetNbins()
                        outdir = "smsScan_%s_%s_AlphaT55_%s"%(nbjet,njet,htbin)
                        outfile.cd(outdir)
                        m0_m12_mChi_noweight.Write("",r.TObject.kOverwrite)
                if ht[0] == "375" :
                    if "T2cc" in modAndPdf[0] :
                        tmp375 = r.TH2D("tmp375","tmp375",34,90,260,50,10,260)
                    else : 
                        tmp375 = r.TH2D("tmp375","tmp375",81,0,2025,81,0,2025)                
                    for hist375 in histList375 :
                        tmp375.Add(hist375)
                    m0_m12_mChi_noweight = tmp375.Clone()
                    if "T2cc" in modAndPdf[0] : 
                        m0_m12_mChi_noweight = c.resizeHisto(m0_m12_mChi_noweight, 35, 100, 275, 50, 10, 260)
                        m0_m12_mChi_noweight = c.shift2DHistos(m0_m12_mChi_noweight, -0.5, -0.5, 5, 1)
                    tmp375.Delete()
                    m0_m12_mChi_noweight.SetName("m0_m12_mChi_noweight")
                    m0_m12_mChi_noweight.SetTitle("m0_m12_mChi_noweight")
                    outfile.cd("smsScan_ge4b_ge4j_AlphaT55_375")
                    m0_m12_mChi_noweight.Write("",r.TObject.kOverwrite)
                             
    if weight == "wPdfWeights" :
        for modAndPdf in c.mods_and_pdfs :
            for pdfSet in modAndPdf[1] :
                for iweight in range(c.nPdfDict[pdfSet]) :
            		alt_keyNames = []
            		for keyName in c.keyNames :
            		    alt_keyNames.append(keyName + "_%s_%s"%(pdfSet,iweight))
                	for ht in c.htbins :
            		     rtfile = "%s/%s_calo_ge2_%s/%s_plots.root"%(c.version,ht[0],weight,modAndPdf[0])
            		     outfile = r.TFile("limit_format_output/%s_%s_%s.root"%(modAndPdf[0],ht[0],pdfSet),"UPDATE") 
#                	     if "T2cc" in modAndPdf[0] :
#                	         m0_m12_mChi_noweight = r.TH2D("m0_m12_mChi_noweight_%s"%iweight,"Dummy Histo",35,100,275,50,10,260)
#                	     else :
#                	         m0_m12_mChi_noweight = r.TH2D("m0_m12_mChi_noweight_%s"%iweight,"Dummy Histo",81,0,2025,81,0,2025)
            		     for dirname in c.dirNames :
            		         if not outfile.GetDirectory(dirname) : outfile.mkdir(dirname)
            		         outfile.cd(dirname)
            		     #outfile.Write()
            		     infile = r.TFile(rtfile,"READ")
            		     infile.Get._creates = True
            		     befdir = infile.GetDirectory("master/progressPrinter/label/scanHistogrammer/")
            		     befkeylist = befdir.GetListOfKeys()        
            		     for key in befkeylist :
            		         if key.ReadObj().GetName() == "nEvents_%s_%s"%(pdfSet,iweight):
            		             before = key.ReadObj()
            		             m0_m12_mChi_noweight = before.Clone()
                                     if "T2cc" in modAndPdf[0] : 
                                         m0_m12_mChi_noweight = c.resizeHisto(m0_m12_mChi_noweight, 35, 100, 275, 50, 10, 260)
                                         m0_m12_mChi_noweight = c.shift2DHistos(m0_m12_mChi_noweight, -0.5, -0.5, 5, 1)
                                     m0_m12_mChi_noweight.SetName("m0_m12_mChi_noweight_%s"%iweight)
                                     print "Weight index is %s"%iweight
                	             print "m0_m12_mChi_noweight has %d Y bins"%m0_m12_mChi_noweight.GetYaxis().GetNbins()
            		             print "%s_%s_%s"%(ht[0],modAndPdf[0],pdfSet)
            		             print "Original Before Hist @ (%d,%d) = %s"%(1,8,m0_m12_mChi_noweight.GetBinContent(1,8))
            		             print "Not scaled: Before Hist @ (%d,%d) = %s"%(1, 8,m0_m12_mChi_noweight.GetBinContent(1,8))
            		             outfile.cd("smsScan_before")
            		             m0_m12_mChi_noweight.Write("",r.TObject.kOverwrite)
            		     afdir = infile.GetDirectory(ht[1])
            		     afkeylist = afdir.GetListOfKeys()
            		     histList375 = []
            		     for key in afkeylist :
            		         if key.ReadObj().GetName() in alt_keyNames :
            		             keyName = key.ReadObj().GetName()                            
            		             if (ht[0] == "375" and "ge4j_ge4b" in keyName) :
            		                 histList375.append(key.ReadObj())
            		             after = key.ReadObj()
            		             keyName = keyName.replace("nEvents_","").replace("_%s_%s"%(pdfSet,iweight),"")
            		             keyName = keyName.split("_")
            		             njet = keyName[0]
            		             nbjet = keyName[1]
            		             keyName.remove(njet)
            		             keyName.remove(nbjet)
            		             htbin = "_".join(keyName)
            		             m0_m12_mChi_noweight = after.Clone()
                                     if "T2cc" in modAndPdf[0] :
                                         m0_m12_mChi_noweight = c.resizeHisto(m0_m12_mChi_noweight, 35, 100, 275, 50, 10, 260)
                                         m0_m12_mChi_noweight = c.shift2DHistos(m0_m12_mChi_noweight, -0.5, -0.5, 5, 1)
            		             m0_m12_mChi_noweight.SetName("m0_m12_mChi_noweight_%s"%iweight)
            		             outdir = "smsScan_%s_%s_AlphaT55_%s"%(nbjet,njet,htbin)
            		             outfile.cd(outdir)
            		             m0_m12_mChi_noweight.Write("",r.TObject.kOverwrite)
                	     if ht[0] == "375" :
                	        if "T2cc" in modAndPdf[0] :
                	             tmp375 = r.TH2D("tmp375","tmp375",34,90,260,50,10,260)
                	        else : 
                	             tmp375 = r.TH2D("tmp375","tmp375",81,0,2025,81,0,2025)                
            		        for hist375 in histList375 :
            		            tmp375.Add(hist375)
            		        m0_m12_mChi_noweight = tmp375.Clone()
                                if "T2cc" in modAndPdf[0] :
                                    m0_m12_mChi_noweight = c.resizeHisto(m0_m12_mChi_noweight, 35, 100, 275, 50, 10, 260)
                                    m0_m12_mChi_noweight = c.shift2DHistos(m0_m12_mChi_noweight, -0.5, -0.5, 5, 1)
            		        tmp375.Delete()
            		        m0_m12_mChi_noweight.SetName("m0_m12_mChi_noweight_%s"%iweight)
            		        m0_m12_mChi_noweight.SetTitle("m0_m12_mChi_noweight_%s"%iweight)
            		        outfile.cd("smsScan_ge4b_ge4j_AlphaT55_375")
            		        m0_m12_mChi_noweight.Write("",r.TObject.kOverwrite)


                                     


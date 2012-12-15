import ROOT as r
import os,subprocess

version = ["v1","v2","v3","v4"][3]

afadd_275 = "master/progressPrinter/label/scanHistogrammer/monster/hbheNoise/multiplicity/multiplicity/l1Filter/physicsDeclaredFilter/lowestUnPrescaledTriggerFilter/jetPtSelector/jetPtSelector/jetEtaSelector/value/value/multiplicity/multiplicity/multiplicity/multiplicity/multiplicity/histogrammer/value/deadEcalFilter/cleanJetHtMhtHistogrammer/alphaHistogrammer/histogrammer/value/value/histogrammer/histogrammer/histogrammer/cleanJetHtMhtHistogrammer/histogrammer/histogrammer/histogrammer/label/scanHistogrammer/"

afadd_375 = afadd_275.replace("lowestUnPrescaledTriggerFilter/", "").replace("jetEtaSelector/value/value/multiplicity/","jetEtaSelector/value/multiplicity/")
afadd_325 = afadd_275.replace("lowestUnPrescaledTriggerFilter/", "")

histPrefix = ["nEvents"]
dirPrefix = ["smsScan"]
bJets = []
nJets = ["le3j","ge4j"]
nJetsMod =["le3j_AlphaT55","ge4j_AlphaT55"]
for nbjet in range(4) :
    bJets.append("eq%db"%nbjet)
bJets.append("ge4b")

hts =  ["%s_%s"%(375+100*i, 475+100*i) for i in range(5)]
hts.append("275_325")
hts.append("325_375")
hts.append("875")

dirName = []
dirNames = []
keyName = []
keyNames = []
dirNames.append("smsScan_before")
for bJet in bJets :
    for nJet in nJetsMod :
        for ht in hts :
            tmp = [dirPrefix[0],bJet,nJet,ht]
            tmp2 = [histPrefix[0],nJet,bJet,ht,]
            keyName = "_".join(tmp2).replace("AlphaT55_","")
            dirName = "_".join(tmp)
            dirNames.append(dirName)
            keyNames.append(keyName)
dirNames.append("smsScan_ge4b_ge4j_AlphaT55_375")
htbins = [("275_scaled",afadd_275),("325_scaled",afadd_325),("375",afadd_375)][0:3]
weights = ["","wPdfWeights"][0:2]

mods_and_pdfs = [("T1bbbb",["gencteq66","genMSTW2008nlo68cl"]),
                 ("T1bbbb_nnpdf",["genNNPDF21"]),
                 ("T1bbbb_nnpdf_ct10",["genct10"]),
                 ("T2bb",["gencteq66","genMSTW2008nlo68cl"]),
                 ("T2bb_nnpdf",["genNNPDF21"]),
                 ("T2bb_nnpdf_ct10",["genct10"])][0:3]

def modelParser(toBeParsed = "", parsed = "") :
    parsed = toBeParsed.replace("_nnpdf","").replace("_ct10","")
    return parsed

for weight in weights :
    if weight == "" :
        for modAndPdf in mods_and_pdfs :
            for ht in htbins :
                rtfile = "%s/%s_calo_ge2_%s/%s_plots.root"%(version,ht[0],weight,modAndPdf[0])
                outfile = r.TFile("output/%s_%s.root"%(modAndPdf[0].replace("nnpdf_ct10","ct10"),ht[0]),"RECREATE") 
                m0_m12_mChi_noweight = r.TH2D("m0_m12_mChi_noweight","Dummy Histo",81,0,2025,81,0,2025)
                for dirname in dirNames :
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
                        m0_m12_mChi_noweight.SetName("m0_m12_mChi_noweight")
                        outfile.cd("smsScan_before")
                        m0_m12_mChi_noweight.Write("",r.TObject.kOverwrite)
                afdir = infile.GetDirectory(ht[1])
                afkeylist = afdir.GetListOfKeys()
                histList375 = []
                for key in afkeylist :
                    if key.ReadObj().GetName() in keyNames :
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
                        m0_m12_mChi_noweight.SetName("m0_m12_mChi_noweight")
                        outdir = "smsScan_%s_%s_AlphaT55_%s"%(nbjet,njet,htbin)
                        outfile.cd(outdir)
                        m0_m12_mChi_noweight.Write("",r.TObject.kOverwrite)
                if ht[0] == "375" :
                    tmp375 = r.TH2D("tmp375","tmp375",81,0,2025,81,0,2025)                
                    for hist375 in histList375 :
                        tmp375.Add(hist375)
                    m0_m12_mChi_noweight = tmp375.Clone()
                    tmp375.Delete()
                    m0_m12_mChi_noweight.SetName("m0_m12_mChi_noweight")
                    m0_m12_mChi_noweight.SetTitle("m0_m12_mChi_noweight")
                    outfile.cd("smsScan_ge4b_ge4j_AlphaT55_375")
                    m0_m12_mChi_noweight.Write("",r.TObject.kOverwrite)
                             
    if weight == "wPdfWeights" :
        for modAndPdf in mods_and_pdfs :
            for pdfSet in modAndPdf[1] :
            	alt_keyNames = []
            	for keyName in keyNames :
            	    alt_keyNames.append(keyName + "_%s_0"%pdfSet)
                for ht in htbins :
            	     scaleFile = r.TFile("output/acc_ratio_%s_275_%s.root"%(modAndPdf[0].replace("nnpdf_ct10","ct10"),pdfSet),"READ")
            	     scaleHist = scaleFile.Get("acc_ratio_%s_275_%s"%(modAndPdf[0].replace("nnpdf_ct10","ct10"),pdfSet))
            	     print "--------"
            	     print "scale @ (%d,%d) = %s"%(20,15,scaleHist.GetBinContent(20,15))
            	     rtfile = "%s/%s_calo_ge2_%s/%s_plots.root"%(version,ht[0],weight,modAndPdf[0])
            	     outfile = r.TFile("output/%s_%s_%s_normalized.root"%(modAndPdf[0].replace("nnpdf_ct10","ct10"),ht[0],pdfSet),"RECREATE") 
            	     m0_m12_mChi_noweight = r.TH2D("m0_m12_mChi_noweight","Dummy Histo",81,0,2025,81,0,2025)
            	     for dirname in dirNames :
            	         outfile.mkdir(dirname)
            	         outfile.cd(dirname)
            	     outfile.Write()
            	     infile = r.TFile(rtfile,"READ")
            	     infile.Get._creates = True
            	     befdir = infile.GetDirectory("master/progressPrinter/label/scanHistogrammer/")
            	     befkeylist = befdir.GetListOfKeys()        
            	     for key in befkeylist :
            	         if key.ReadObj().GetName() == "nEvents_%s_0"%pdfSet:
            	             before = key.ReadObj()
            	             m0_m12_mChi_noweight = before.Clone()
            	             m0_m12_mChi_noweight.SetName("m0_m12_mChi_noweight")
            	             print "%s_%s_%s"%(ht[0],modAndPdf[0].replace("nnpdf_ct10","ct10"),pdfSet)
            	             print "Original Before Hist @ (%d,%d) = %s"%(20,15,m0_m12_mChi_noweight.GetBinContent(20,15))
            	             m0_m12_mChi_noweight.Divide(scaleHist)
            	             print "Scaled (1/scale) Before Hist @ (%d,%d) = %s"%(20,15,m0_m12_mChi_noweight.GetBinContent(20,15))
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
            	             keyName = keyName.replace("nEvents_","").replace("_%s_0"%pdfSet,"")
            	             keyName = keyName.split("_")
            	             njet = keyName[0]
            	             nbjet = keyName[1]
            	             keyName.remove(njet)
            	             keyName.remove(nbjet)
            	             htbin = "_".join(keyName)
            	             m0_m12_mChi_noweight = after.Clone()
            	             m0_m12_mChi_noweight.SetName("m0_m12_mChi_noweight")
            	             outdir = "smsScan_%s_%s_AlphaT55_%s"%(nbjet,njet,htbin)
            	             outfile.cd(outdir)
            	             m0_m12_mChi_noweight.Write("",r.TObject.kOverwrite)
                     if ht[0] == "375" :
            	        tmp375 = r.TH2D("tmp375","tmp375",81,0,2025,81,0,2025)                
            	        for hist375 in histList375 :
            	            tmp375.Add(hist375)
            	        m0_m12_mChi_noweight = tmp375.Clone()
            	        tmp375.Delete()
            	        m0_m12_mChi_noweight.SetName("m0_m12_mChi_noweight")
            	        m0_m12_mChi_noweight.SetTitle("m0_m12_mChi_noweight")
            	        outfile.cd("smsScan_ge4b_ge4j_AlphaT55_375")
            	        m0_m12_mChi_noweight.Write("",r.TObject.kOverwrite)

                                     


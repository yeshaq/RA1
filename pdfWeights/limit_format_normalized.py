import ROOT as r
import os,subprocess

afadd_275 = "master/progressPrinter/label/scanHistogrammer2/monster/hbheNoise/multiplicity/multiplicity/l1Filter/physicsDeclaredFilter/lowestUnPrescaledTriggerFilter/jetPtSelector/jetPtSelector/jetEtaSelector/value/value/multiplicity/multiplicity/multiplicity/multiplicity/multiplicity/histogrammer/value/deadEcalFilter/cleanJetHtMhtHistogrammer/alphaHistogrammer/histogrammer/value/value/histogrammer/histogrammer/histogrammer/cleanJetHtMhtHistogrammer/histogrammer/histogrammer/histogrammer/label/scanHistogrammer2/"

afadd_375 = afadd_275.replace("lowestUnPrescaledTriggerFilter/", "").replace("jetEtaSelector/value/value/multiplicity/","jetEtaSelector/value/multiplicity/")
afadd_325 = afadd_275.replace("lowestUnPrescaledTriggerFilter/", "")

prefixes = ["smsScan"]
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
for prefix in prefixes :
    for bJet in bJets :
        for nJet in nJetsMod :
            for ht in hts :
                tmp = [prefix,bJet,nJet,ht]
                tmp2 = [prefix,nJet,bJet,ht,"After"]
                keyName = "_".join(tmp2).replace("AlphaT55_","")
                dirName = "_".join(tmp)
                dirNames.append(dirName)
                keyNames.append(keyName)
dirNames.append("smsScan_ge4b_ge4j_AlphaT55_375")
htbins = [("275_scaled",afadd_275),("325_scaled",afadd_325),("375",afadd_375)][0:3]
weights = ["","wPdfWeights"][0:2]
models = ["T2bb","T1bbbb"][0:2]
pdfSets = ["gencteq66","genMSTW2008nlo68cl","genNNPDF20"][0:2]

for weight in weights :
    if weight == "" :
        for model in models :
            for ht in htbins :
                
                rtfile = "%s_calo_ge2_%s/%s_plots.root"%(ht[0],weight,model)
                outfile = r.TFile("%s_%s.root"%(model,ht[0]),"RECREATE") 
                m0_m12_mChi_noweight = r.TH2D("m0_m12_mChi_noweight","Dummy Histo",81,0,2025,81,0,2025)
                for dirname in dirNames :
                    outfile.mkdir(dirname)
                    outfile.cd(dirname)
                outfile.Write()
                infile = r.TFile(rtfile,"READ")
                befdir = infile.GetDirectory("master/progressPrinter/label/scanHistogrammer2/")
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
                        keyName = keyName.replace("smsScan_","").replace("_After","")
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
        for pdfSet in pdfSets :
         if not pdfSet == "genNNPDF20" :    
            alt_keyNames = []
            for keyName in keyNames :
                alt_keyNames.append(keyName.replace("After","%s_0_After"%pdfSet))
            for model in models :
                for ht in htbins :
                    scaleFile = r.TFile("%s_275_%s_acc_ratio.root"%(model,pdfSet),"READ")
                    scaleHist = scaleFile.Get("%s_275_%s_acc_ratio"%(model,pdfSet))
                    print "--------"
                    print "scale @ (%d,%d) = %s"%(24,22,scaleHist.GetBinContent(24,22))
                    rtfile = "%s_calo_ge2_%s/%s_plots.root"%(ht[0],weight,model)
                    outfile = r.TFile("%s_%s_%s_normalized.root"%(model,ht[0],pdfSet),"RECREATE") 
                    m0_m12_mChi_noweight = r.TH2D("m0_m12_mChi_noweight","Dummy Histo",81,0,2025,81,0,2025)
                    for dirname in dirNames :
                        outfile.mkdir(dirname)
                        outfile.cd(dirname)
                    outfile.Write()
                    infile = r.TFile(rtfile,"READ")
                    infile.Get._creates = True
                    befdir = infile.GetDirectory("master/progressPrinter/label/scanHistogrammer2/")
                    befkeylist = befdir.GetListOfKeys()        
                    for key in befkeylist :
                        if key.ReadObj().GetName() == "nEvents_%s_0"%pdfSet:
                            before = key.ReadObj()
                            m0_m12_mChi_noweight = before.Clone()
                            m0_m12_mChi_noweight.SetName("m0_m12_mChi_noweight")
                            print "%s_%s_%s"%(ht[0],model,pdfSet)
                            print "Original Before Hist @ (%d,%d) = %s"%(24,22,m0_m12_mChi_noweight.GetBinContent(24,22))
                            m0_m12_mChi_noweight.Divide(scaleHist)
                            print "Scaled (1/scale) Before Hist @ (%d,%d) = %s"%(24,22,m0_m12_mChi_noweight.GetBinContent(24,22))
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
                            keyName = keyName.replace("smsScan_","").replace("_After","").replace("_%s_0"%pdfSet,"")
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
         else :
             histList = [] 
             for model in models :
                 for ht in htbins :
                     rtfile = "%s_calo_ge2_%s/%s_plots.root"%(ht[0],weight,model)
                     outfile = r.TFile("%s_%s_%s.root"%(model,ht[0],pdfSet),"RECREATE") 
                     m0_m12_mChi_noweight = r.TH2D("m0_m12_mChi_noweight","Dummy Histo",81,0,2025,81,0,2025)
                     for dirname in dirNames :
                         outfile.mkdir(dirname)
                         outfile.cd(dirname)
                     outfile.Write()
                     infile = r.TFile(rtfile,"READ")
                     infile.Get._creates = True
                     befdir = infile.GetDirectory("master/progressPrinter/label/scanHistogrammer2/")
                     befkeylist = befdir.GetListOfKeys()        
                     for key in befkeylist :
                         if pdfSet in key.ReadObj().GetName() :
                             before = key.ReadObj()
                             histList.append(before.Clone())
                             tmp = r.TH2D("tmp","tmp",81,0,2025,81,0,2025)
                             for hist in histList :
                                 tmp.Add(hist)
                             tmp.Scale(1/30.)
                             m0_m12_mChi_noweight = tmp.Clone()
                             tmp.Delete()
                             m0_m12_mChi_noweight.SetName("m0_m12_mChi_noweight")
                             m0_m12_mChi_noweight.SetTitle("m0_m12_mChi_noweight")
                             outfile.cd("smsScan_before")
                             m0_m12_mChi_noweight.Write("",r.TObject.kOverwrite)
                     afdir = infile.GetDirectory(ht[1])
                     afkeylist = afdir.GetListOfKeys()
                     histoList = []
                     histList = []
                     keyNameList = []
                     for key2 in afkeylist :
                              if "genNNPDF20_" in key2.ReadObj().GetName() :
                                    keyNameList.append(key2.ReadObj().GetName())
                     histList375 = []
                     for nJet2 in nJets :
                         for bJet2 in bJets :
                             for ht2 in hts :
                                 if any("%s_%s_%s_genNNPDF20_0"%(nJet2,bJet2,ht2) in s for s in keyNameList) :
                                     tmp2 = r.TH2D("tmp2","tmp2",81,0,2025,81,0,2025)
                                     for i in range(30) :
                                         tmpKey = afdir.GetKey("smsScan_%s_%s_%s_genNNPDF20_%d_After"%(nJet2,bJet2,ht2,i))
                                         tmp2.Add(tmpKey.ReadObj())
                                     tmp2.SetName("smsScan_%s_%s_%s_genNNPDF20_After"%(nJet2,bJet2,ht2))
                                     tmp2.Scale(1/30.)
                                     if (ht[0] == "375" and "ge4j_ge4b" in tmp2.GetName()) :
                                         tmp375_2 = tmp2.Clone()
                                         histList375.append(tmp375_2)                                         
                                     m0_m12_mChi_noweight = tmp2.Clone()
                                     tmp2.Delete()
                                     m0_m12_mChi_noweight.SetName("m0_m12_mChi_noweight")
                                     m0_m12_mChi_noweight.SetTitle("m0_m12_mChi_noweight")
                                     outdir = "smsScan_%s_%s_AlphaT55_%s"%(bJet2,nJet2,ht2)
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

                                     


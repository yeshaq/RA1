import ROOT as r


version = ["v1","v2","v3","v4"][3]

afadd_275 = "master/progressPrinter/label/scanHistogrammer/monster/hbheNoise/multiplicity/multiplicity/l1Filter/physicsDeclaredFilter/lowestUnPrescaledTriggerFilter/jetPtSelector/jetPtSelector/jetEtaSelector/value/value/multiplicity/multiplicity/multiplicity/multiplicity/multiplicity/histogrammer/value/deadEcalFilter/cleanJetHtMhtHistogrammer/alphaHistogrammer/histogrammer/value/value/histogrammer/histogrammer/histogrammer/cleanJetHtMhtHistogrammer/histogrammer/histogrammer/histogrammer/label/scanHistogrammer/"

afadd_375 = afadd_275.replace("lowestUnPrescaledTriggerFilter/", "").replace("jetEtaSelector/value/value/multiplicity/","jetEtaSelector/value/multiplicity/")
afadd_325 = afadd_275.replace("lowestUnPrescaledTriggerFilter/", "")



htbins = [("275_scaled",afadd_275),("325_scaled",afadd_325),("375",afadd_375)][0:3]
weights = ["","wPdfWeights"][0:2]
mods_and_pdfs = [("T1bbbb",["gencteq66","genMSTW2008nlo68cl"]),("T1bbbb_nnpdf",["genNNPDF21"]),("T1bbbb_nnpdf_ct10",["genct10"])]
for weight in weights :
    if weight == "" :
        for modAndPdf in mods_and_pdfs :
            for ht in htbins :
                rtfile = "%s/%s_calo_ge2_%s/%s_plots.root"%(version,ht[0],weight,modAndPdf[0])
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
                outfile = r.TFile("output/acc_%s_%s.root"%(modAndPdf[0].replace("nnpdf_ct10","ct10"),ht[0]),"RECREATE") 
                afterHist.Write()
                            
    if weight == "wPdfWeights" :
#        for pdfSet in pdfSets :
#            for model in models :
        for modAndPdf in mods_and_pdfs :
            for pdfSet in modAndPdf[1] :
                for ht in htbins :
                    rtfile = "%s/%s_calo_ge2_%s/%s_plots.root"%(version,ht[0],weight,modAndPdf[0])
                    beforeHist = r.TH2D("nEvents_before","nEvents",81,0,2025,81,0,2025)
                    afterHist =  r.TH2D("nEvents_after","nEvents",81,0,2025,81,0,2025)
                    infile = r.TFile(rtfile,"READ")
                    befdir = infile.GetDirectory("master/progressPrinter/label/scanHistogrammer/")
                    befkeylist = befdir.GetListOfKeys()        
                    for key in befkeylist :
                        if key.ReadObj().GetName() == "nEvents_%s_0"%(pdfSet):
                            before = key.ReadObj()
                            beforeHist = before.Clone()
                    afdir = infile.GetDirectory(ht[1])
                    afkeylist = afdir.GetListOfKeys()
                    for key in afkeylist :
                        if key.ReadObj().GetName() == "nEvents_%s_0"%(pdfSet):
                            after = key.ReadObj()
                            afterHist = after.Clone()  
                    afterHist.Divide(beforeHist)
                    outfile = r.TFile("output/acc_%s_%s_%s.root"%(modAndPdf[0].replace("nnpdf_ct10","ct10"),ht[0],pdfSet),"RECREATE") 
                    afterHist.Write()

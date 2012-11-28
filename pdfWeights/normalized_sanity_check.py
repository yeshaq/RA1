import ROOT as r



afadd_275 = "master/progressPrinter/label/scanHistogrammer/monster/hbheNoise/multiplicity/multiplicity/l1Filter/physicsDeclaredFilter/lowestUnPrescaledTriggerFilter/jetPtSelector/jetPtSelector/jetEtaSelector/value/value/multiplicity/multiplicity/multiplicity/multiplicity/multiplicity/histogrammer/value/deadEcalFilter/cleanJetHtMhtHistogrammer/alphaHistogrammer/histogrammer/value/value/histogrammer/histogrammer/histogrammer/cleanJetHtMhtHistogrammer/histogrammer/histogrammer/histogrammer/label/scanHistogrammer/"

afadd_375 = afadd_275.replace("lowestUnPrescaledTriggerFilter/", "").replace("jetEtaSelector/value/value/multiplicity/","jetEtaSelector/value/multiplicity/")
afadd_325 = afadd_275.replace("lowestUnPrescaledTriggerFilter/", "")



htbins = [("275_scaled",afadd_275),("325_scaled",afadd_325),("375",afadd_375)][0:3]
weights = ["","wPdfWeights"][0:2]
models = ["T2bb","T1bbbb"][0:2]
pdfSets = ["gencteq66","genMSTW2008nlo68cl","genNNPDF20"][0:2]
scaleSlices = ["","normalized_"]

for weight in weights :
    if weight == "" :
        for model in models :
            for ht in htbins :
                for scale in scaleSlices :  
                    rtfile = "%s_calo_ge2_%s/%s_plots.root"%(ht[0],weight,model)
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
                    outfile = r.TFile("%s%s_%s_.root"%(scale,model,ht[0]),"RECREATE") 
                    afterHist.Write()
                            
    if weight == "wPdfWeights" :
        for pdfSet in pdfSets :
            for model in models :
                for ht in htbins :
                    for scale in scaleSlices :  
                        rtfile = "%s_calo_ge2_%s/%s_plots.root"%(ht[0],weight,model)
                        scaleFile = r.TFile("%s_275_%s_acc_ratio.root"%(model,pdfSet))
                        scaleHist = scaleFile.Get("%s_275_%s_acc_ratio"%(model,pdfSet))                    
                        beforeHist = r.TH2D("nEvents_before","nEvents",81,0,2025,81,0,2025)
                        afterHist =  r.TH2D("nEvents_after","nEvents",81,0,2025,81,0,2025)
                        infile = r.TFile(rtfile,"READ")
                        befdir = infile.GetDirectory("master/progressPrinter/label/scanHistogrammer/")
                        befkeylist = befdir.GetListOfKeys()        
                        for key in befkeylist :
                            if key.ReadObj().GetName() == "nEvents_%s_0"%(pdfSet):
                                before = key.ReadObj()
                                beforeHist = before.Clone()
                                if not scale == "" : beforeHist.Divide(scaleHist)
                        afdir = infile.GetDirectory(ht[1])
                        afkeylist = afdir.GetListOfKeys()
                        for key in afkeylist :
                            if key.ReadObj().GetName() == "nEvents_%s_0"%(pdfSet):
                                after = key.ReadObj()
                                afterHist = after.Clone()  
                        afterHist.Divide(beforeHist)
                        outfile = r.TFile("%s%s_%s_%s.root"%(scale,model,ht[0],pdfSet),"RECREATE") 
                        afterHist.Write()

version = ["v1","v2","v3","v4"][3]

afadd_275 = "master/progressPrinter/label/scanHistogrammer/monster/hbheNoise/multiplicity/multiplicity/l1Filter/physicsDeclaredFilter/lowestUnPrescaledTriggerFilter/jetPtSelector/jetPtSelector/jetEtaSelector/value/value/multiplicity/multiplicity/multiplicity/multiplicity/multiplicity/histogrammer/value/deadEcalFilter/cleanJetHtMhtHistogrammer/alphaHistogrammer/histogrammer/value/value/histogrammer/histogrammer/histogrammer/cleanJetHtMhtHistogrammer/histogrammer/histogrammer/histogrammer/label/scanHistogrammer/"
afadd_375 = afadd_275.replace("lowestUnPrescaledTriggerFilter/", "").replace("jetEtaSelector/value/value/multiplicity/","jetEtaSelector/value/multiplicity/")
afadd_325 = afadd_275.replace("lowestUnPrescaledTriggerFilter/", "")



htbins = [("275_scaled",afadd_275),("325_scaled",afadd_325),("375",afadd_375)][0:3]
weights = ["","wPdfWeights"][0:2]
mods_and_pdfs = [("T1bbbb",["gencteq66","genMSTW2008nlo68cl"]),
                 ("T1bbbb_nnpdf_ct10",["genNNPDF21","genct10"]),
                 ("T2bb",["gencteq66","genMSTW2008nlo68cl"]),
                 ("T2bb_nnpdf_ct10",["genNNPDF21","genct10"]),
                 ("T2cc_nnpdf_ct10",["genNNPDF21","genct10"])][4:5]

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

nPdfDict = {"gencteq66":45,"genMSTW2008nlo68cl":41,"genct10":53,"genNNPDF21":101}


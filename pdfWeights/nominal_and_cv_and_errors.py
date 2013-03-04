import math, ROOT as r
import common as c 

def numerAndDenom(histName, befDir,afDir) :
    d = {}
    beforeHist = befDir.Get(histName) 
    d["before"] = beforeHist.Clone()
    afterHist = afDir.Get(histName)
    d["after"] = afterHist.Clone()
    return d

def MasterEquation(denHist, pdfSet, xbin, ybin) :
    print "---------------------------------------------------------------------------------------------"
    result = []
    centralAcc = denHist[0].GetBinContent(xbin,ybin)
    dPlus = 0.
    dMinus = 0.
	#wp = 0.
	#wm = 5.
    if centralAcc == 0 : return
    for i in range(c.nPdfDict[pdfSet]/2) :
	    #wp = denHist[2*i+1].GetBinContent(xbin,ybin)/denHist[0].GetBinContent(xbin,ybin) - 1
	    #wm = denHist[2*i+2].GetBinContent(xbin,ybin)/denHist[0].GetBinContent(xbin,ybin) - 1
        wp = denHist[2*i+1].GetBinContent(xbin,ybin)-denHist[0].GetBinContent(xbin,ybin) 
        wm = denHist[2*i+2].GetBinContent(xbin,ybin)-denHist[0].GetBinContent(xbin,ybin) 

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

        print pdfSet
        print xbin, ybin
        print "Central Value nEvents = %.3f"%(centralAcc)
        result.append(centralAcc)
        #print "ie. %.3f%% relative variation with respect to original PDF"%((100*(centralAcc-numHist.GetBinContent(xbin,ybin))/numHist.GetBinContent(xbin,ybin)))
        #result.SetBinContent(xbin,ybin,(100*(centralAcc-numHist.GetBinContent(xbin,ybin))/numHist.GetBinContent(xbin,ybin)))
        factor = 1
        if "ct" in pdfSet :
            factor = 1.0/1.645
        print "Uncertianty with respect to central member: +%.3f / -%.3f"%(dPlus*factor,dMinus*factor)
        result.append(dPlus*factor)
        result.append(dMinus*factor)
    return result


def stdDev(mean, dev, xbin, ybin) :
    d = [ (i.GetBinContent(xbin,ybin) - mean) ** 2 for i in dev]
    stddev = math.sqrt(sum(d) / len(d))
    return stddev

def nnpdfErrorCalc(denHist, pdfSet, xbin, ybin) :
    centralAcc = denHist[0].GetBinContent(xbin,ybin)
    dev = denHist[1:]
    stddev = stdDev(centralAcc, dev, xbin, ybin)
    print "---------------------------------------------------------------------------------------------"
    print pdfSet
    print xbin, ybin
    print "centr. accept = %.3f"%(centralAcc)
    #print "ie. %.3f%% relative variation with respect to original PDF"%((100*(centralAcc-numHist.GetBinContent(xbin,ybin))/numHist.GetBinContent(xbin,ybin)))
    #result.SetBinContent(xbin,ybin,(100*(centralAcc-numHist.GetBinContent(xbin,ybin))/numHist.GetBinContent(xbin,ybin)))
    print "Uncertianty with respect to central member: +%.3f / -%.3f"%(stddev,stddev)



for weight in c.weights :
#    if weight == "" :
#        for modAndPdf in c.mods_and_pdfs :
#            	for ht in c.htbins :
#            	    rtfile = "output/%s_%s.root"%(modAndPdf[0],ht[0])
#            	    if "T2cc" in modAndPdf[0] :
#            	        beforeHist = r.TH2D("nEvents_before","nEvents",34,90,260,50,10,260)
#            	        afterHist =  r.TH2D("nEvents_after","nEvents",34,90,260,50,10,260)                
#            	    else :
#            	        beforeHist = r.TH2D("nEvents_before","nEvents",81,0,2025,81,0,2025)
#            	        afterHist =  r.TH2D("nEvents_after","nEvents",81,0,2025,81,0,2025)
#            	    infile = r.TFile(rtfile,"READ")
#            	    befdir = infile.GetDirectory("smsScan_before")
#            	    befkeylist = befdir.GetListOfKeys()        
#            	    for key in befkeylist :
#            	        if key.ReadObj().GetName() == "m0_m12_mChi_noweight":
#            	            before = key.ReadObj()
#            	            beforeHist = before.Clone()
#            	    afdir = infile.GetDirectory(ht[1])
#            	    afkeylist = afdir.GetListOfKeys()
#            	    for key in afkeylist :
#            	        if key.ReadObj().GetName() == "m0_m12_mChi_noweight":
#            	            after = key.ReadObj()
#            	            afterHist = after.Clone()  
#            	    afterHist.Divide(beforeHist)
#            	    outfile = r.TFile("output_werrors/acc_%s_%s.root"%(modAndPdf[0],ht[0]),"RECREATE") 
#            	    afterHist.Write()
#                            
    if weight == "wPdfWeights" :
        for modAndPdf in c.mods_and_pdfs :
            for pdfSet in modAndPdf[1] :
                for ht in c.htbins :
                    rtfile = "output/%s_%s_%s_normalized.root"%(modAndPdf[0],ht[0],pdfSet)            
                    infile = r.TFile(rtfile,"READ")
                    outfile = r.TFile(infile.GetName().replace("output","output_werrors"),"UPDATE")
                    outfile_werrors = r.TFile(infile.GetName().replace("output","output_werrors").replace("normalized","normalized_werrors"),"UPDATE")
                    for dirkey in infile.GetListOfKeys() :
                        if not outfile.GetDirectory(dirkey.GetName()) : outfile.mkdir(dirkey.GetName())
                        if not outfile_werrors.GetDirectory(dirkey.GetName()) : outfile_werrors.mkdir(dirkey.GetName())
                    if "T2cc" in modAndPdf[0] :
                        m0_m12_mChi_noweight = r.TH2D("m0_m12_mChi_noweight","Dummy Histo",34,90,260,50,10,260)
                    else :
                        m0_m12_mChi_noweight = r.TH2D("m0_m12_mChi_noweight","Dummy Histo",81,0,2025,81,0,2025)
                    for dirkey in infile.GetListOfKeys() :
                        dirName = dirkey.ReadObj().GetName()
                        if not dirName == "smsScan_before" :
                            dirName = dirName.replace("smsScan_","")
                            dirName = dirName.replace("AlphaT55_","")
                            dirName = dirName.split('_')
                            bj = dirName[0]
                            nj = dirName[1]
                            dirName.remove(bj)
                            dirName.remove(nj)
                        histList = []
                        for histkey in dirkey.ReadObj().GetListOfKeys() :
                            histList.append(histkey.ReadObj())
                        if histList :
	                        for xbin in range(histList[0].GetXaxis().GetNbins()) :
	                            for ybin in range(histList[0].GetYaxis().GetNbins()) :
                                        if (histList[0].GetBinContent(xbin,ybin)) == 0.0 : continue
	                                if "NNPDF" not in pdfSet :
                                            if dirkey.GetName() == "smsScan_before" :
                                                cv_and_errors = MasterEquation(histList, pdfSet, xbin, ybin)
                                                m0_m12_mChi_noweight.SetBinContent(xbin,ybin,cv_and_errors[0])
                                                
                                        else :
                                            if dirkey.GetName() == "smsScan_before" :
                                                nnpdfErrorCalc(histList, pdfSet, xbin, ybin)
                                
#                    dirList = infile.GetListOfKeys()
#                    befkeylist = befdir.GetListOfKeys()
#
#                    outfile = r.TFile("output/acc_%s_%s_%s.root"%(modAndPdf[0],ht[0],pdfSet),"RECREATE") 
#                    #afdir = infile.GetDirectory(ht[1])
#                    DirList = afdir.GetListOfKeys()
#                    histList = ["m0_m12_mChi_noweight_%s"%i for i in range(c.nPdfDict[pdfSet])]
#                    for hist in histList :
#                         histos = numerAndDenom(hist,befdir,afdir)
#                         result = histos["after"].Clone()
#                         result.Divide(histos["before"])
#                         result.Write()

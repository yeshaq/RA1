import common as c
import ROOT as r
from array import array

canvas = r.TCanvas()
canvas.SetRightMargin(0.2)
canvas.SetTickx()
canvas.SetTicky()

htBinDict = {"275_325":1, "325_375":2,"375_475":3,"475_575":4,"575_675":5,"675_775":6,"775_875":7,"875":8}
htbins = ["275_scaled","325_scaled","375"]
cat = {}

nomRootFiles = []
varRootFiles = []
nomFiles = ["limit_format_output/T2cc_%s.root"%i for i in htbins]
varFiles = ["limit_format_output/T2cc_nnpdf_ct10_%s_genct10.root"%i for i in htbins]

massPairs = [[125,95],[175,95],[200,140]][0:3]
multiplicityPairs = [["eq0b","le3j"],["eq1b","le3j"]][0:2]


def categorizeDirectory(dirName):

    dirName = dirName.split("_")
    cat["nb"] = dirName[0] 
    cat["nj"] = dirName[1]
    dirName.remove(cat["nj"])
    dirName.remove(cat["nb"])
    cat["ht"] = "_".join(dirName)
    return cat


for ifile in nomFiles :
    nomRootFiles.append(r.TFile(ifile, "READ"))

for ifile in varFiles :
    varRootFiles.append(r.TFile(ifile, "READ"))

for multiplicityPair in multiplicityPairs:
	for masses in massPairs:
                nomHistograms = []
                nomBeforeHistograms = []
                varHistograms = []
                varBeforeHistograms = []
		for nomRootFile in nomRootFiles :
			for dirkey in nomRootFile.GetListOfKeys() :
		            dirName = dirkey.ReadObj().GetName()
		            for histkey in dirkey.ReadObj().GetListOfKeys() :
			        dirName = dirName.replace("smsScan_","").replace("AlphaT55_","")
		                if dirName == "before" : nomBeforeHistograms.append(histkey.ReadObj())
			        if not dirName ==  "before" :
			            cat = categorizeDirectory(dirName)
			            hist = histkey.ReadObj()
			            if (cat["nb"] == multiplicityPair[0] and cat["nj"] == multiplicityPair[1]) :
			                for xbin in range(hist.GetXaxis().GetNbins()) :
			                    for ybin in range(hist.GetYaxis().GetNbins()) :
			                        mStop = 100 + ((xbin)*25)
			                        mLsp =  10 + ((ybin)*5)
			                        if not mStop == masses[0] : continue
			                        if not mLsp ==  masses[1] : continue
			                        value = hist.GetBinContent(xbin+1,ybin+1)
			                        bins = array("d", [275.0,325.0,375.0,475.0,575.0,675.0,775.0,875.0,975.0])
			                        htHist = r.TH1D("acc_vs_ht_%s_%s_%s_%d_%d"%(cat["nb"],cat["nj"],cat["ht"],xbin+1,ybin+1),
		                                                "Acceptance vs. HT, mStop = %s, mLSP = %s, %s, %s"%(mStop,mLsp,cat['nb'],cat['nj']), 8, bins)
			                        if not value == 0.0 :
			                            htHist.SetBinContent(htBinDict[cat["ht"]], hist.GetBinContent(xbin+1,ybin+1))
			                            nomHistograms.append(htHist)

		for varRootFile in varRootFiles :
			for dirkey in varRootFile.GetListOfKeys() :
		            dirName = dirkey.ReadObj().GetName()
		            for histkey in dirkey.ReadObj().GetListOfKeys() :
			        dirName = dirName.replace("smsScan_","").replace("AlphaT55_","")
		                if dirName == "before" : varBeforeHistograms.append(histkey.ReadObj())
		                hist = histkey.ReadObj()                
		                if "_0" not in hist.GetName() : continue
			        if not dirName ==  "before" :
			            cat = categorizeDirectory(dirName)
			            if (cat["nb"] == multiplicityPair[0] and cat["nj"] == multiplicityPair[1]) :
			                for xbin in range(hist.GetXaxis().GetNbins()) :
			                    for ybin in range(hist.GetYaxis().GetNbins()) :
			                        mStop = 100 + ((xbin)*25)
			                        mLsp =  10 + ((ybin)*5)
			                        if not mStop == masses[0] : continue
			                        if not mLsp ==  masses[1] : continue
			                        value = hist.GetBinContent(xbin+1,ybin+1)
			                        bins = array("d", [275.0,325.0,375.0,475.0,575.0,675.0,775.0,875.0,975.0])
			                        htHist = r.TH1D("ct10_acc_vs_ht_%s_%s_%s_%d_%d"%(cat["nb"],cat["nj"],cat["ht"],xbin+1,ybin+1),
		                                                "Acceptance vs. HT, mStop = %s, mLSP = %s, %s, %s"%(mStop,mLsp,cat['nb'],cat['nj']), 8, bins)
			                        if not value == 0.0 :
			                            htHist.SetBinContent(htBinDict[cat["ht"]], hist.GetBinContent(xbin+1,ybin+1))
			                            varHistograms.append(htHist)
		
		fracHistograms = [x.Clone() for x in varHistograms]
		for fracHist,nomHist in zip(fracHistograms,nomHistograms):
		    fracHist.Divide(nomHist)
		fracBeforeHistograms = [ x.Clone() for x in varBeforeHistograms]
		for fracBefHist,nomBefHist in zip(fracBeforeHistograms,nomBeforeHistograms) : 
		    fracBefHist.Divide(nomBefHist)
		
		nomHistograms[0].Draw()
		for nomHist in nomHistograms :
		    mbins = nomHist.GetName()[-4:]
		    mbins = mbins.split("_")
		    mStopBin = int(mbins[0])
		    mLspBin = int(mbins[1])
		    title = nomHist.GetTitle()
		    nomHist.SetTitle(title.replace("Acceptance","Events"))
		    nomHist.SetStats(False)
		    nomHist.SetMarkerColor(2)
		    nomHist.Draw("same")
                canvas.Print("limit_format_output/nEvents_vs_ht_%s_%s_%s_%s.pdf"%(mStopBin,mLspBin,multiplicityPair[0],multiplicityPair[1]))
                canvas.Clear()
		for varHist in varHistograms :
		    mbins = varHist.GetName()[-4:]
		    mbins = mbins.split("_")
		    mStopBin = int(mbins[0])
		    mLspBin = int(mbins[1])
		    varHist.Scale(1/varBeforeHistograms[0].GetBinContent(mStopBin,mLspBin))
		    varHist.SetMarkerColor(1)
		    varHist.SetMarkerSize(3)
		canvas.Clear()
		fracHistograms[0].Draw()    
		for fracHist in fracHistograms :
		    mbins = fracHist.GetName()[-4:]
		    mbins = mbins.split("_")
		    mStopBin = int(mbins[0])
		    mLspBin = int(mbins[1])
		    fracHist.Scale(1/fracBeforeHistograms[0].GetBinContent(mStopBin,mLspBin))
		    fracHist.SetMaximum(1.4)
		    fracHist.SetMinimum(.9)
		    fracHist.SetMarkerColor(1)
		    fracHist.SetMarkerSize(3)
		    title =  fracHist.GetTitle()
		    print title
		    fracHist.SetTitle(title.replace("Acceptance","Acc. Ratio CT10/CTEQ6L1")) 
		    fracHist.SetStats(False)
		    fracHist.Draw("same")
		
		
		canvas.Print("limit_format_output/acc_vs_ht_%s_%s_%s_%s.pdf"%(mStopBin,mLspBin,multiplicityPair[0],multiplicityPair[1]))
                canvas.Clear()
                

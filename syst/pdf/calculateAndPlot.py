import ROOT as r
import common as c
import os, math
from array import array
canvas = r.TCanvas()
canvas.SetRightMargin(0.2)
canvas.SetTickx()
canvas.SetTicky()

max_central_deviation = 0.0
max_error = 0.0

def envelopeCvAndUn(cvs, uncertHigh, uncertLow) :
	#http://www.hep.ucl.ac.uk/pdf4lhc/PDF4LHCrecom.pdf
	cv_1 = max([x + s for x,s in zip(cvs,uncertHigh)])
	cv_2 = min([x - s for x,s in zip(cvs,uncertLow)])
	cv = 0.5 * (cv_1 + cv_2)
	un = 0.5 * (cv_1 - cv_2)
	return cv, un

def MakeCvAndErrorTGraph(histName, x, xl, xh, nominal, mstop, mlsp, pdfSetOrder) :
	envCv, envUn = envelopeCvAndUn(x,xl,xh)
	x.append(envCv)
	xl.append(envUn)
	xh.append(envUn)
	x.append(nominal[0])
	cv = array("d", x)
	y = array("d", [1.2,1.4,1.6,1.8,2.0])
	cvl = array("d", xl) 
	cvh = array("d", xh)
        nom = array("d", nominal)
	#print mstop, mlsp
	compHist = r.TGraphAsymmErrors(len(x),cv,y,cvl,cvh)
	compHist.SetMarkerStyle(33)
	compHist.SetMarkerSize(1.6)

	compHist.SetName("%s_%s"%(mstop,mlsp))
	epsFileName = "output_cv_and_errors/%s/acc_cv_and_errors_%s_%s.eps"%(c.version,mstop,mlsp)
	noDots = epsFileName.replace(".0","")
	xMax = compHist.GetHistogram().GetXaxis().GetXmax()
	compHist.GetXaxis().SetLabelSize(.05)

	null = r.TH2D("null","", 1, 0.0, 2*xMax, 5, 1.1, 2.1)
	null.SetStats(False)
	yAxis = null.GetYaxis()
	xAxis = null.GetXaxis()
	yAxis.SetLabelSize(.11)
	xAxis.SetLabelSize(.08)
	labels = [x.replace("gen","").replace("nlo68cl","") for x in pdfSetOrder]
	labels.append("Envel. Calc")
	labels.append("CTEQ6L1")
	for i,label in enumerate(labels) :
		yAxis.SetBinLabel(1+i, label)
	null.SetTitle("Central value and uncertainties for mStop = %s, mLSP = %s"%(mstop,mlsp) );
	r.gStyle.SetTitleFontSize(0.08);
	null.Draw()
	compHist.Draw("p")

	canvas.Size(6,1.2)
	canvas.SetWindowSize(1600,900)

	canvas.Print(noDots)
	os.system("epstopdf "+ noDots)
	os.remove(noDots)
 	compHist.Write("",r.TObject.kOverwrite)
	return [envCv, envUn, nominal[0]]

def MakeRelativeAccChangeTGraph(histName, x, xl, xh, nominal, mstop, mlsp, pdfSetOrder) :
	## comment  avg = x + (xh - xl)/2 
	envCv, envUn = envelopeCvAndUn(x,xl,xh)
	x.append(envCv)
	xl.append(envUn)
	xh.append(envUn)
	avg = [first_term + second_term for first_term,second_term in zip(x,[(high - low)/2. for low, high in zip(xh,xl)])]  
	relchange = [averaged/nominal[0] for averaged in avg]
	cv = array("d", x)
	y = array("d", [1.2,1.4,1.6,1.8])
	relch = array("d", relchange)
	compHist = r.TGraphAsymmErrors(len(x),relch,y)
	compHist.SetMarkerStyle(33)
	compHist.SetMarkerSize(1.6)
	compHist.SetName("%s_%s"%(mstop,mlsp))
	epsFileName = "output_cv_and_errors/%s/acc_relative_change_%s_%s.eps"%(c.version,mstop,mlsp)
	noDots = epsFileName.replace(".0","")

	xMax = compHist.GetHistogram().GetXaxis().GetXmax()
	compHist.GetXaxis().SetLabelSize(.05)

	null = r.TH2D("null","", 1, 0.85, 1.15, 4, 1.1, 1.9)
	null.SetStats(False)
	yAxis = null.GetYaxis()
	xAxis = null.GetXaxis()
	yAxis.SetLabelSize(.11)
	xAxis.SetLabelSize(.08)
	labels = [x.replace("gen","").replace("nlo68cl","") for x in pdfSetOrder]
	labels.append("Envel. Calc")
	for i,label in enumerate(labels) :
		yAxis.SetBinLabel(1+i, label)
	null.SetTitle("Avg. relative change in acceptance for mStop = %s, mLSP = %s"%(mstop,mlsp));
	r.gStyle.SetTitleFontSize(0.08);
	null.Draw()

	compHist.Draw("p")

	canvas.Size(6,1.2)
	canvas.SetWindowSize(1600,900)
	
	canvas.Print(noDots)
	os.system("epstopdf "+ noDots)
	os.remove(noDots)
 	#compHist.Write("",r.TObject.kOverwrite)
	#compHist.Write()


def MasterEquation(numHist, denHist, pdfSet, xbin, ybin, result) :
	centralAcc = denHist[0].GetBinContent(xbin,ybin)
	dPlus = 0.
	dMinus = 0.
	if centralAcc == 0 : return
	for i in range(c.nPdfDict[pdfSet]/2) :
	    wp = denHist[2*i+1].GetBinContent(xbin,ybin)/denHist[0].GetBinContent(xbin,ybin) - 1
	    wm = denHist[2*i+2].GetBinContent(xbin,ybin)/denHist[0].GetBinContent(xbin,ybin) - 1
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
	    result.SetBinContent(xbin,ybin,(100*(centralAcc-numHist.GetBinContent(xbin,ybin))/numHist.GetBinContent(xbin,ybin)))
	    factor = 1
	    if "ct" in pdfSet :
		    factor = 1.0/1.645
	    up = dPlus*factor*centralAcc
	    down = dMinus*factor*centralAcc
	    tmp = [centralAcc, up, down, numHist.GetBinContent(xbin,ybin)] 
	    return tmp
def stdDev(mean, dev, xbin, ybin) :
    d = [ (i.GetBinContent(xbin,ybin) - mean) ** 2 for i in dev]
    stddev = math.sqrt(sum(d) / len(d))
    return stddev

def nnpdfErrorCalc(numHist, denHist, pdfSet, xbin, ybin) :
    centralAcc = denHist[0].GetBinContent(xbin,ybin)
    dev = denHist[1:]
    stddev = stdDev(centralAcc, dev, xbin, ybin)
    tmp = [centralAcc, stddev, stddev,numHist.GetBinContent(xbin,ybin)]
    return tmp

def initHistos(histosDict, ra1cat) :

    histos = {}
    for key in histosDict:
        hist = histosDict[key]
        blah = r.TH2D(hist[0]+"_%s_%s"%ra1cat,hist[1]+", (%s, %s)"%ra1cat,hist[2][0],hist[2][1],hist[2][2],hist[2][3],hist[2][4],hist[2][5])
	if hist[3] :
		blah.SetMinimum(hist[3])
		blah.SetMaximum(hist[4])
        histos[key] = blah
    return histos


def shift2DHistos(histos, shiftX = 0.0 , shiftY = 0.0, rebinX = 0.0, rebinY = 0.0) :

    hists = {}
    for key in histos :
	    
        hist = histos[key]
        histName = hist.GetName()
        histTitle = hist.GetTitle()
	zMax = hist.GetMaximum()
	zMin = hist.GetMinimum()
	if not rebinX == 0.0 :
		hist.Rebin2D(rebinX,rebinY)

        xAxis = hist.GetXaxis()
        yAxis = hist.GetYaxis()

        nXbins = xAxis.GetNbins()
        nYbins = yAxis.GetNbins()

        xMin = xAxis.GetXmin()
        yMin = yAxis.GetXmin()

        xMax = xAxis.GetXmax()
        yMax = yAxis.GetXmax()

        dXbin = (xMax - xMin) / nXbins
        dYbin = (yMax - yMin) / nYbins

        shiftedXmin = xMin + shiftX*dXbin
        shiftedXmax = xMax + shiftX*dXbin

        shiftedYmin = yMin + shiftY*dYbin
        shiftedYmax = yMax + shiftY*dYbin
	

        shiftedHist = r.TH2D(histName, histTitle, nXbins, shiftedXmin, shiftedXmax, nYbins, shiftedYmin, shiftedYmax)
        for xbin in range(nXbins) :
            for ybin in range(nYbins) :
                shiftedHist.SetBinContent(xbin+1,ybin+1,hist.GetBinContent(xbin+1,ybin+1))
	shiftedHist.SetMinimum(zMin)
	shiftedHist.SetMaximum(zMax)
        hists[key] = shiftedHist
    return hists

def drawAndPrint(histos) :
	w = 1200
	h = 600
	canvas = r.TCanvas("c","c", w, h)
	#canvas.SetWindowSize(w + (w - c.GetWw()),h + (h - c.GetWh()))
	canvas.SetWindowSize(w + 100, h + 100)
        #canvas.Size(0,0)
	#canvas.SetWindowSize(600,600)
	for key in histos:
		hist = histos[key]
		hist.SetTitle("%s;m_{stop} (GeV);m_{LSP} (GeV);"%(hist.GetTitle())) 
#		if "frac" in hist.GetName() :
#			hist.SetTitle(";m_{stop} (GeV);m_{LSP} (GeV); percentage")
		epsFileName = "output_cv_and_errors/%s/"%c.version + hist.GetName() + ".eps" 
		hist.Draw("colz")
		hist.SetStats(False)
		canvas.Print(epsFileName)
		os.system("epstopdf " + epsFileName)
		os.remove(epsFileName)

def writeHistos(histos,jet):
	for hist in histos:
		f = r.TFile("output_cv_and_errors/%s/%sJet_%s.root"%(c.version,jet,hist),"RECREATE")		       
		histos[hist].Write()
		f.Close()
		pass


def main(ra1cat=("ge4j","eq0b"),jet=None):
	
	cv_and_errors = {}
	cv = {}
	cv_up= {}
	cv_dn = {}
	nominal = {}
	pdfSetOrder = []
	for modAndPdf in c.mods_and_pdfs :
		for pdfSet in modAndPdf[1] :
	            if not pdfSet: continue
	            numFile = r.TFile("%s/%sJet_pn_T2cc.root"%(c.version,jet),"READ")
		    if "MSTW" in pdfSet:
			    numHist = numFile.Get("eff_T2cc_mstw_%s_%s" % ra1cat if ra1cat else "eff_T2cc_mstw")
		    else:
			    numHist = numFile.Get("eff_T2cc_%s_%s" % ra1cat if ra1cat else "eff_T2cc")
	            
	            denFile = r.TFile("normalized_acc_output/%s/%sJet_normalized.root"%(c.version,jet),"READ")
	            denHist = []
	            for i in range(c.nPdfDict[pdfSet]) : 
			    denHist.append(denFile.Get("eff_T2cc_%s_%s_%s"%("%s_%s" %ra1cat,pdfSet,i) if ra1cat else "eff_T2cc_%s_%s"%(pdfSet,i)))
	            result = numHist.Clone()
	    
	            result.SetTitle(";m_{parent} (GeV);m_{LSP} (GeV);") 
	            result.SetMarkerStyle(20)
	            result.SetStats(False)
	
	
	            for xbin in range(denHist[0].GetXaxis().GetNbins()) :
	                for ybin in range(denHist[0].GetYaxis().GetNbins()) :
	                    if (result.GetBinContent(xbin+1,ybin+1)) == 0.0 : continue	                    
			    if (denHist[0].GetBinContent(xbin+1,ybin+1)) == 0.0 : continue
	                    if "NNPDF" not in pdfSet :
			        cv_and_errors["%s_%s_%s"%(pdfSet,xbin+1,ybin+1)] = MasterEquation(numHist, denHist, pdfSet, xbin+1, ybin+1, result)
				cv["%s_%s_%s"%(pdfSet,xbin+1,ybin+1)] = cv_and_errors["%s_%s_%s"%(pdfSet,xbin+1,ybin+1)][0]
				cv_up["%s_%s_%s"%(pdfSet,xbin+1,ybin+1)] = cv_and_errors["%s_%s_%s"%(pdfSet,xbin+1,ybin+1)][1]
				cv_dn["%s_%s_%s"%(pdfSet,xbin+1,ybin+1)] = cv_and_errors["%s_%s_%s"%(pdfSet,xbin+1,ybin+1)][2]
				nominal["%s_%s_%s"%(pdfSet,xbin+1,ybin+1)] = cv_and_errors["%s_%s_%s"%(pdfSet,xbin+1,ybin+1)][3]
	                    else :
	                        cv_and_errors["%s_%s_%s"%(pdfSet,xbin+1,ybin+1)] = nnpdfErrorCalc(numHist, denHist, pdfSet, xbin+1, ybin+1)
				cv["%s_%s_%s"%(pdfSet,xbin+1,ybin+1)] = cv_and_errors["%s_%s_%s"%(pdfSet,xbin+1,ybin+1)][0]
				cv_up["%s_%s_%s"%(pdfSet,xbin+1,ybin+1)] = cv_and_errors["%s_%s_%s"%(pdfSet,xbin+1,ybin+1)][1]
				cv_dn["%s_%s_%s"%(pdfSet,xbin+1,ybin+1)] = cv_and_errors["%s_%s_%s"%(pdfSet,xbin+1,ybin+1)][2]
				nominal["%s_%s_%s"%(pdfSet,xbin+1,ybin+1)] = cv_and_errors["%s_%s_%s"%(pdfSet,xbin+1,ybin+1)][3]
			    if not pdfSet in pdfSetOrder : pdfSetOrder.append(pdfSet)
	
	compFile = r.TFile("output_cv_and_errors/%s/%sJet_inclusive_cv_acc_werrrors.root"%(c.version,jet),"UPDATE")			
	nominal_tmp = nominal
	cv_list = {}
	cv_up_list = {}
	cv_dn_list = {}
	nominal_list = {}
	
	
	for modAndPdf in c.mods_and_pdfs :
	        for pdfSet in modAndPdf[1] :
			if not pdfSet: continue
			for key in cv :
				if pdfSet in key :
					if not key.replace("%s_"%pdfSet,"") in cv_list : cv_list[key.replace("%s_"%pdfSet,"")] = []
					if not key.replace("%s_"%pdfSet,"") in cv_up_list : cv_up_list[key.replace("%s_"%pdfSet,"")] = []
					if not key.replace("%s_"%pdfSet,"") in cv_dn_list : cv_dn_list[key.replace("%s_"%pdfSet,"")] = []
					if not key.replace("%s_"%pdfSet,"") in nominal_list : nominal_list[key.replace("%s_"%pdfSet,"")] = []
			
					cv_list[key.replace("%s_"%pdfSet,"")].append(cv[key])
					cv_up_list[key.replace("%s_"%pdfSet,"")].append(cv_up[key])
					cv_dn_list[key.replace("%s_"%pdfSet,"")].append(cv_dn[key])
					nominal_list[key.replace("%s_"%pdfSet,"")].append(nominal_tmp[key])
	
	


	envCv_and_envUn = {}
	for key in cv_list :
		mstop_mlsp_bins = key.split("_")
		mstop = ((float(mstop_mlsp_bins[0])-1)*25)+100
		mlsp = ((float(mstop_mlsp_bins[1])-1)*5)+10
		envCv_and_envUn[key] = MakeCvAndErrorTGraph(key, cv_list[key], cv_dn_list[key], cv_up_list[key], nominal_list[key], mstop, mlsp, pdfSetOrder) 	
		MakeRelativeAccChangeTGraph(key, cv_list[key], cv_dn_list[key], cv_up_list[key], nominal_list[key], mstop, mlsp, pdfSetOrder) 	
	if not ra1cat: ra1cat = ("incl","ra1cat")
	binning = [11,87.5,362.5,70,7.5,357.5]
	histosDict = {"envCvHist_%s_%s"%ra1cat: ["acc_cv_m0_m12","Central Value Acceptance from Envelope Formula", binning, None, None],
	              "envUpHist_%s_%s"%ra1cat: ["acc_pSigma_m0_m12","+1 #sigma Acceptance from Envelope Formula", binning, None, None,],
	              "envDnHist_%s_%s"%ra1cat: ["acc_mSigma_m0_m12","-1 #sigma Acceptance from Envelope Formula",binning, None, None],
	              "envCvRelHist_%s_%s"%ra1cat: ["acc_cvRel_m0_m12","Central Value Acceptance from Envelope Formula Relative to Nominal", binning, 0.0, .3],#0.95, 1.14],
	              "envUpRelHist_%s_%s"%ra1cat: ["acc_pSigmaRel_m0_m12","+1 #sigma Acceptance from Envelope Formula Relative to Nominal", binning, 0.95, 1.21],
	              "envDnRelHist_%s_%s"%ra1cat: ["acc_mSigmaRel_m0_m12","-1 #sigma Acceptance from Envelope Formula Relative to Nominal", binning, 0.9, 1.08],
	              "envFracUncHist_%s_%s"%ra1cat : ["acc_SigmaFrac_m0_m12","Fractional Uncertainty  #sigma(acceptance) / C.V.(acceptance)", binning, 0.01, 0.08]}
	
	
	histos = initHistos(histosDict, ra1cat)
	
	for key in envCv_and_envUn:
		mstop_mlsp_bins = key.split("_")
		mstop_bin = mstop_mlsp_bins[0]
		mlsp_bin = mstop_mlsp_bins[1]
		histos["envCvHist_%s_%s"%ra1cat].SetBinContent(int(mstop_bin),int(mlsp_bin),envCv_and_envUn[key][0])
		histos["envUpHist_%s_%s"%ra1cat].SetBinContent(int(mstop_bin),int(mlsp_bin),envCv_and_envUn[key][0]+envCv_and_envUn[key][1])
		histos["envDnHist_%s_%s"%ra1cat].SetBinContent(int(mstop_bin),int(mlsp_bin),envCv_and_envUn[key][0]-envCv_and_envUn[key][1])
		#histos["envCvRelHist_%s_%s"%ra1cat].SetBinContent(int(mstop_bin),int(mlsp_bin),envCv_and_envUn[key][0]/envCv_and_envUn[key][2])
		histos["envCvRelHist_%s_%s"%ra1cat].SetBinContent(int(mstop_bin),int(mlsp_bin),abs((envCv_and_envUn[key][0]-envCv_and_envUn[key][2])/envCv_and_envUn[key][2]))
		histos["envUpRelHist_%s_%s"%ra1cat].SetBinContent(int(mstop_bin),int(mlsp_bin),(envCv_and_envUn[key][0]+envCv_and_envUn[key][1])/envCv_and_envUn[key][2])
		histos["envDnRelHist_%s_%s"%ra1cat].SetBinContent(int(mstop_bin),int(mlsp_bin),(envCv_and_envUn[key][0]-envCv_and_envUn[key][1])/envCv_and_envUn[key][2])
		histos["envFracUncHist_%s_%s"%ra1cat].SetBinContent(int(mstop_bin),int(mlsp_bin),(envCv_and_envUn[key][1])/envCv_and_envUn[key][0])
	
	#shiftedHistos = shift2DHistos(histos, -0.5, -0.5, 5, 1)
	shiftedHistos = histos
	
	#drawAndPrint(shiftedHistos)
	writeHistos(shiftedHistos,jet)
	compFile.Close()

for jet in ["pf","calo"]:
	for ra1cat in c.ra1cats[1:]:
	        main(ra1cat=ra1cat,jet=jet)
	os.system("cd output_cv_and_errors/%s/; python hadd.py" % c.version)

import ROOT as r
import common as c
import os, math
from array import array
canvas = r.TCanvas()
canvas.SetRightMargin(0.2)
canvas.SetTickx()
canvas.SetTicky()

htBins = [c.htbins[0][0].strip("_scaled")]

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
	epsFileName = "output_cv_and_errors/acc_cv_and_errors_%s_%s.eps"%(mstop,mlsp)
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
	epsFileName = "output_cv_and_errors/acc_relative_change_%s_%s.eps"%(mstop,mlsp)
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


def MasterEquation(numHist, denHist, pdfSet, xbin, ybin) :
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
#	    print "---------------------------------------------------------------------------------------------"
#	    print pdfSet
#	    print xbin, ybin
#	    print "centr. accept = %.3f%%"%(100*centralAcc)
#	    print "ie. %.3f%% relative variation with respect to original PDF"%((100*(centralAcc-numHist.GetBinContent(xbin,ybin))/numHist.GetBinContent(xbin,ybin)))
	    result.SetBinContent(xbin,ybin,(100*(centralAcc-numHist.GetBinContent(xbin,ybin))/numHist.GetBinContent(xbin,ybin)))
	    factor = 1
	    if "ct" in pdfSet :
		    factor = 1.0/1.645
#	    print "Relative uncertianty with respect to central member: +%.3f%% / -%.3f%%"%(100*dPlus*factor,100*dMinus*factor)
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
#    print "---------------------------------------------------------------------------------------------"
#    print pdfSet
#    print xbin, ybin
#    print "centr. accept = %.3f%%"%(100*centralAcc)
#    print "ie. %.3f%% relative variation with respect to original PDF"%((100*(centralAcc-numHist.GetBinContent(xbin,ybin))/numHist.GetBinContent(xbin,ybin)))
#    result.SetBinContent(xbin,ybin,(100*(centralAcc-numHist.GetBinContent(xbin,ybin))/numHist.GetBinContent(xbin,ybin)))
#    print "Relative uncertianty with respect to central member: +%.3f%% / -%.3f%%"%(100*stddev/centralAcc,100*stddev/centralAcc)
    tmp = [centralAcc, stddev, stddev,numHist.GetBinContent(xbin,ybin)]
    return tmp

def initHistos(histosDict) :

    histos = {}
    for key in histosDict:
        hist = histosDict[key]
        blah = r.TH2D(hist[0],hist[1],hist[2][0],hist[2][1],hist[2][2],hist[2][3],hist[2][4],hist[2][5])
	if hist[3] :
		blah.SetMinimum(hist[3])
		blah.SetMaximum(hist[4])
	print 	hist[4], blah.GetMaximum()
        histos[key] = blah
    return histos


def shift2DHistos(histos, shiftX = 0.0 , shiftY = 0.0) :

    hists = {}
    for key in histos :
	    
        hist = histos[key]
        histName = hist.GetName()
        histTitle = hist.GetTitle()
	zMax = hist.GetMaximum()
	print zMax
	zMin = hist.GetMinimum()
	hist.Rebin2D(5,2)

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
	

        print nXbins, nYbins, xMin, yMin, xMax, yMax, shiftedXmin, shiftedXmax
        shiftedHist = r.TH2D(histName, histTitle, nXbins, shiftedXmin, shiftedXmax, nYbins, shiftedYmin, shiftedYmax)
        for xbin in range(nXbins) :
            for ybin in range(nYbins) :
                shiftedHist.SetBinContent(xbin+1,ybin+1,hist.GetBinContent(xbin+1,ybin+1))
	shiftedHist.SetMinimum(zMin)
	shiftedHist.SetMaximum(zMax)
        hists[key] = shiftedHist
    return hists

def drawAndPrint(histos) :
	
	canvas.Size(0,0)
	canvas.SetWindowSize(800,600)
	for key in histos:
		hist = histos[key]
		hist.SetTitle("%s;m_{stop} (GeV);m_{LSP} (GeV);"%(hist.GetTitle())) 
#		if "frac" in hist.GetName() :
#			hist.SetTitle(";m_{stop} (GeV);m_{LSP} (GeV); percentage")
		epsFileName = "output_cv_and_errors/" + hist.GetName() + ".eps" 
		hist.Draw("colz")
		hist.SetStats(False)
		canvas.Print(epsFileName)
		os.system("epstopdf " + epsFileName)
		os.remove(epsFileName)





cv_and_errors = {}
cv = {}
cv_up= {}
cv_dn = {}
nominal = {}
pdfSetOrder = []
for modAndPdf in c.mods_and_pdfs :
        for pdfSet in modAndPdf[1] :
            numFile = r.TFile("output/acc_%s_275.root"%(modAndPdf[0].replace("_nnpdf_ct10","")),"READ")
            numHist = numFile.Get("nEvents")
            
            denFile = r.TFile("output/acc_%s_275_%s.root"%(modAndPdf[0],pdfSet),"READ")
            denHist = []
            for i in range(c.nPdfDict[pdfSet]) : 
                denHist.append(denFile.Get("nEvents_%s_%s"%(pdfSet,i)))
            result = numHist.Clone()
    
            result.SetTitle(";m_{parent} (GeV);m_{LSP} (GeV);") 
            result.SetMarkerStyle(20)
            result.SetStats(False)

            if "T2cc" not in modAndPdf[0] :
                    print "removing ISR region"
	            for xbin in range(denHist[0].GetXaxis().GetNbins()) :
	                for ybin in range(denHist[0].GetYaxis().GetNbins()) :
	                    if (ybin*25 > xbin*25 - 175) or (xbin*25 <= 300)  : result.SetBinContent(xbin,ybin,0.0) 
	

            for xbin in range(denHist[0].GetXaxis().GetNbins()) :
                for ybin in range(denHist[0].GetYaxis().GetNbins()) :
                    if (result.GetBinContent(xbin,ybin)) == 0.0 : continue
                    if "NNPDF" not in pdfSet :
		        cv_and_errors["%s_%s_%s"%(pdfSet,xbin,ybin)] = MasterEquation(numHist, denHist, pdfSet, xbin, ybin)
			cv["%s_%s_%s"%(pdfSet,xbin,ybin)] = cv_and_errors["%s_%s_%s"%(pdfSet,xbin,ybin)][0]
			cv_up["%s_%s_%s"%(pdfSet,xbin,ybin)] = cv_and_errors["%s_%s_%s"%(pdfSet,xbin,ybin)][1]
			cv_dn["%s_%s_%s"%(pdfSet,xbin,ybin)] = cv_and_errors["%s_%s_%s"%(pdfSet,xbin,ybin)][2]
			nominal["%s_%s_%s"%(pdfSet,xbin,ybin)] = cv_and_errors["%s_%s_%s"%(pdfSet,xbin,ybin)][3]
                    else :
                        cv_and_errors["%s_%s_%s"%(pdfSet,xbin,ybin)] = nnpdfErrorCalc(numHist, denHist, pdfSet, xbin, ybin)
			cv["%s_%s_%s"%(pdfSet,xbin,ybin)] = cv_and_errors["%s_%s_%s"%(pdfSet,xbin,ybin)][0]
			cv_up["%s_%s_%s"%(pdfSet,xbin,ybin)] = cv_and_errors["%s_%s_%s"%(pdfSet,xbin,ybin)][1]
			cv_dn["%s_%s_%s"%(pdfSet,xbin,ybin)] = cv_and_errors["%s_%s_%s"%(pdfSet,xbin,ybin)][2]
			nominal["%s_%s_%s"%(pdfSet,xbin,ybin)] = cv_and_errors["%s_%s_%s"%(pdfSet,xbin,ybin)][3]
		    if not pdfSet in pdfSetOrder : pdfSetOrder.append(pdfSet)

compFile = r.TFile("output_cv_and_errors/inclusive_cv_acc_werrrors.root","UPDATE")			
nominal_tmp = nominal
cv_list = {}
cv_up_list = {}
cv_dn_list = {}
nominal_list = {}


for modAndPdf in c.mods_and_pdfs :
        for pdfSet in modAndPdf[1] :
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
	mstop = ((float(mstop_mlsp_bins[0])-1)*5)+90
	mlsp = ((float(mstop_mlsp_bins[1])-1)*5)+10
	envCv_and_envUn[key] = MakeCvAndErrorTGraph(key, cv_list[key], cv_dn_list[key], cv_up_list[key], nominal_list[key], mstop, mlsp, pdfSetOrder) 	
	MakeRelativeAccChangeTGraph(key, cv_list[key], cv_dn_list[key], cv_up_list[key], nominal_list[key], mstop, mlsp, pdfSetOrder) 	

binning = [35,100,275,50,10,260]
histosDict = {"envCvHist": ["acc_cv_m0_m12","Central Value Acceptance from Envelope Formula", binning, None, None],
              "envUpHist": ["acc_pSigma_m0_m12","+1 #sigma Acceptance from Envelope Formula", binning, None, None,],
              "envDnHist": ["acc_mSigma_m0_m12","-1 #sigma Acceptance from Envelope Formula",binning, None, None],
              "envCvRelHist": ["acc_cvRel_m0_m12","Central Value Acceptance from Envelope Formula Relative to Nominal", binning, 0.95, 1.14],
              "envUpRelHist": ["acc_pSigmaRel_m0_m12","+1 #sigma Acceptance from Envelope Formula Relative to Nominal", binning, 0.95, 1.21],
              "envDnRelHist": ["acc_mSigmaRel_m0_m12","-1 #sigma Acceptance from Envelope Formula Relative to Nominal", binning, 0.9, 1.08],
              "envFracUncHist" : ["acc_SigmaFrac_m0_m12","Fractional Uncertainty  #sigma(acceptance) / C.V.(acceptance)", binning, 0.02, 0.08]}


histos = initHistos(histosDict)

for key in envCv_and_envUn:
	mstop_mlsp_bins = key.split("_")
	mstop_bin = mstop_mlsp_bins[0]
	mlsp_bin = mstop_mlsp_bins[1]
	histos["envCvHist"].SetBinContent(int(mstop_bin)-2,int(mlsp_bin),envCv_and_envUn[key][0])
	histos["envUpHist"].SetBinContent(int(mstop_bin)-2,int(mlsp_bin),envCv_and_envUn[key][0]+envCv_and_envUn[key][1])
	histos["envDnHist"].SetBinContent(int(mstop_bin)-2,int(mlsp_bin),envCv_and_envUn[key][0]-envCv_and_envUn[key][1])
	histos["envCvRelHist"].SetBinContent(int(mstop_bin)-2,int(mlsp_bin),envCv_and_envUn[key][0]/envCv_and_envUn[key][2])
	histos["envUpRelHist"].SetBinContent(int(mstop_bin)-2,int(mlsp_bin),(envCv_and_envUn[key][0]+envCv_and_envUn[key][1])/envCv_and_envUn[key][2])
	histos["envDnRelHist"].SetBinContent(int(mstop_bin)-2,int(mlsp_bin),(envCv_and_envUn[key][0]-envCv_and_envUn[key][1])/envCv_and_envUn[key][2])
	histos["envFracUncHist"].SetBinContent(int(mstop_bin)-2,int(mlsp_bin),(envCv_and_envUn[key][1])/envCv_and_envUn[key][0])

shiftedHistos = shift2DHistos(histos, -0.5)
drawAndPrint(shiftedHistos)

compFile.Close()

#isr,jec,pdf,btag,deadecal,
import ROOT as r
import math

def quadSum(l) :
    return math.sqrt(sum([x**2 for x in l]))

def findMinAndMax(d) :
    for k,v in d.iteritems():
        if v == 0.0 : continue 
        if minAndMax[k] == (None,None):
            minAndMax[k] = (v,v)
        else:
            minAndMax[k] = (min(v,minAndMax[k][0]),
                            max(v,minAndMax[k][1]))
    
ra1cats=[]
for njet in ["le3j","ge4j"]:
    for bjet in ["eq0b","eq1b","eq2b","eq3b","ge4b"]:
        if njet == "le3j" and bjet =="ge4b" :continue
        ra1cats.append((njet,bjet))

canvas = r.TCanvas()
canvas.SetRightMargin(0.2)
canvas.SetTickx()
canvas.SetTicky()


for jet in ["calo", "pf"]:
    outFile = r.TFile("%sJet_totalUnc.root"%jet,"RECREATE")            
    jec = r.TFile("../jec/%s_jecUnc.root"%jet,"READ")
    isr = r.TFile("../isr/%s_isrUnc.root"%jet,"READ")
    btag = r.TFile("../btag/%s_btagUnc.root"%jet,"READ")
    pdf = r.TFile("../pdf/output_cv_and_errors/v9/%sJet_envCvRelHist.root"%jet,"READ")
    canvas.Clear()
    pdfFile = "%sJet_totalUnc.pdf"%jet
    canvas.Print(pdfFile+"[", "Lanscape")
    for ra1cat in ra1cats:
	
	    jecUp = jec.Get("%s_up_%s"%(jet,"%s_%s"%ra1cat))
	    jecDn = jec.Get("%s_dn_%s"%(jet,"%s_%s"%ra1cat))
	    isrUp = isr.Get("%s_up_%s"%(jet,"%s_%s"%ra1cat))
	    isrDn = isr.Get("%s_dn_%s"%(jet,"%s_%s"%ra1cat))
	    bUp = btag.Get("%s_up_%s"%(jet,"%s_%s"%ra1cat))
	    bDn = btag.Get("%s_dn_%s"%(jet,"%s_%s"%ra1cat))
	    pVar = pdf.Get("acc_cvRel_m0_m12_%s_%s"%ra1cat)
	    
	    dE = .03
	    
	    tFile = r.TFile("../jec/375_%sJet_ge2j_jn_in_pn.root"%jet,"READ")
	    templateHist = tFile.Get("after_nEvents")
	    outHist = templateHist.Clone("totatUnc_%s_%s" % ra1cat)
	    minAndMax = {"j":(None,None),
	                 "i":(None,None),
	                 "b":(None,None),
	                 "p":(None,None),
                         "t":(None,None),}
            nBins=0
            Avg=0.0
	    for xbin in range(templateHist.GetXaxis().GetNbins()):
	        for ybin in range(templateHist.GetYaxis().GetNbins()):
	            if templateHist.GetBinContent(xbin,ybin) :

                        if jecUp and jecDn:
                            j = max(jecUp.GetBinContent(xbin,ybin),jecDn.GetBinContent(xbin,ybin))
                        if isrUp and isrDn:
                            i = max(isrUp.GetBinContent(xbin,ybin),isrDn.GetBinContent(xbin,ybin))
	                b = max(bUp.GetBinContent(xbin,ybin),bDn.GetBinContent(xbin,ybin))
	                p = pVar.GetBinContent(xbin,ybin)
                        if p > .5: p =0.0
                        t = quadSum([i,j,b,dE,p])
	                outHist.SetBinContent(xbin,ybin,t)
	                d = dict(zip(["j","i","b","p","t"],[j,i,b,p,t]))
	                findMinAndMax(d)
                        if any([i,j,b,p]) : 
                            nBins +=1
                            Avg += quadSum([i,j,b,p,dE])
                        else:
                            outHist.SetBinContent(xbin,ybin,0.0)
		            
            print jet,ra1cat,minAndMax, "avg",Avg/nBins
            outFile.cd()
	    #outHist.SetMaximum(.3)
	    outHist.SetTitle("Total T2cc Uncertainty, (%s,%s)"%ra1cat)
	    outHist.GetYaxis().SetRangeUser(0,350)
	    
	    outHist.GetXaxis().SetRangeUser(0,330)
	    outHist.Draw("colztext")
            canvas.Print(pdfFile)
	    outHist.Write()
    canvas.Print(pdfFile+"]")
    outFile.Close()

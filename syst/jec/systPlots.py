import ROOT as r
import os
import math

def error(x, y):
    f = x/y - 1
    dx = 1/y
    dy = -x/(y**2)
    #abs(f)*math.sqrt((oE/o)**2 + (pE/p)**2)
    return math.sqrt((dx)**2 + (dy)**2)
    
def relativeChange(var, num):
    for xbin in range(num.GetXaxis().GetNbins()):
        for ybin in range(num.GetYaxis().GetNbins()):
            if num.GetBinContent(xbin,ybin) < 1e-8:
                var.SetBinContent(xbin,ybin,0.0)
                continue
            v = var.GetBinContent(xbin,ybin)
            if var.GetBinContent(xbin,ybin) > 0.0:
                eOverc = var.GetBinError(xbin,ybin,)/var.GetBinContent(xbin,ybin) 
                
            if eOverc > .20:
                #print "c",var.GetBinContent(xbin,ybin)
                #print "e",var.GetBinError(xbin,ybin,)
                #print "e/c", eOverc 
                #print "--"
                var.SetBinContent(xbin,ybin,0.0)
                continue
            n = num.GetBinContent(xbin,ybin)
            top = v - n
            top = top/n
            if top > .40 : 
                print top,eOverc
            if abs(top) < 1e-8 : continue
            var.SetBinContent(xbin,ybin,abs(top))
            #var.SetBinError(xbin,ybin,abs(top)*error(v,n))

    return var 


def trimLowStats(hist):
    for xbin in range(hist.GetXaxis().GetNbins()):
        for ybin in range(hist.GetYaxis().GetNbins()):
            if hist.GetBinContent(xbin,ybin)<1e-17: continue
            if (hist.GetBinError(xbin,ybin))>1.0:
                hist.SetBinContent(xbin,ybin,0.0)

    return hist

for jet in ["calo","pf"]:
    canvas = r.TCanvas()
    canvas.SetRightMargin(0.2)
    canvas.SetTickx()
    canvas.SetTicky()
    psFileName = "%s_jecUnc.pdf" % (jet)
    canvas.Print(psFileName+"[", "Lanscape")
    outFile = r.TFile("%s_jecUnc.root" % jet,"RECREATE")    
    dct = {"vn":"375_%sJet_ge2j_jn_in_pn"%jet,
           "vu":"375_%sJet_ge2j_ju_in_pn"%jet,
           "vd":"375_%sJet_ge2j_jd_in_pn"%jet}


    vn = r.TFile(dct["vn"]+".root","READ")
    vu = r.TFile(dct["vu"]+".root","READ")
    vd = r.TFile(dct["vd"]+".root","READ")
    keys = vn.GetListOfKeys()

    for k in keys:
        #if "le3j_eq3b" in k.GetName(): continue
        nom = vn.Get(k.GetName())
        up = vu.Get(k.GetName())
        dn = vd.Get(k.GetName())

        upResult = up.Clone("%s_up_%s" % (jet,k.GetName().replace("after_","").replace("nEvents_","")))
        upResult = relativeChange(upResult, nom)
        #upResult = trimLowStats(upResult)
        upResult.SetTitle(upResult.GetTitle()+", nominal + Unc.")
        upResult.Draw("colztext")
        #upResult.SetMinimum(0.001)
        canvas.Print(psFileName)

        dnResult = dn.Clone("%s_dn_%s" % (jet,k.GetName().replace("after_","").replace("nEvents_","")))
        dnResult = relativeChange(dnResult, nom)
        #dnResult = trimLowStats(dnResult)
        dnResult.SetTitle(dnResult.GetTitle()+", nominal - Unc.")
        #dnResult.SetMinimum(0.001)
        dnResult.Draw("colztext")
        canvas.Print(psFileName)
        
        outFile.cd()
        upResult.Write()
        dnResult.Write()
    canvas.Close(psFileName+"]")
    


import ROOT as r
import os

def relativeChange(var, num):
    for xbin in range(num.GetXaxis().GetNbins()):
        for ybin in range(num.GetYaxis().GetNbins()):
            if num.GetBinContent(xbin,ybin) < 1e-8:
                var.SetBinContent(xbin,ybin,0.0)
                continue
            top = var.GetBinContent(xbin,ybin) - num.GetBinContent(xbin,ybin)
            top = top/num.GetBinContent(xbin,ybin)
            var.SetBinContent(xbin,ybin,abs(top))
    return var 


def trimLowStats(hist):
    for xbin in range(hist.GetXaxis().GetNbins()):
        for ybin in range(hist.GetYaxis().GetNbins()):
            if hist.GetBinContent(xbin,ybin)<1e-8: continue
            if (hist.GetBinError(xbin,ybin)/hist.GetBinContent(xbin,ybin))>1.0:
                hist.SetBinContent(xbin,ybin,0.0)

    return hist

for jet in ["calo","pf"]:
    canvas = r.TCanvas()
    canvas.SetRightMargin(0.2)
    canvas.SetTickx()
    canvas.SetTicky()
    psFileName = "%s_jecUnc.pdf" % (jet)
    canvas.Print(psFileName+"[", "Lanscape")

    dct = {"jn":"375_%sJet_ge2j_jn_pn"%jet,
           "ju":"375_%sJet_ge2j_ju_pn"%jet,
           "jd":"375_%sJet_ge2j_jd_pn"%jet}


    jn = r.TFile(dct["jn"]+".root","READ")
    ju = r.TFile(dct["ju"]+".root","READ")
    jd = r.TFile(dct["jd"]+".root","READ")
    keys = jn.GetListOfKeys()
    for k in keys:
        if "le3j_eq3b" in k.GetName(): continue
        nom = jn.Get(k.GetName())
        up = ju.Get(k.GetName())
        dn = jd.Get(k.GetName())

        upResult = up.Clone("%s_up" % jet)
        upResult = relativeChange(upResult, nom)
        upResult = trimLowStats(upResult)
        upResult.SetTitle(upResult.GetTitle()+", nominal + Unc.")
        upResult.Draw("colztext")
        upResult.SetMinimum(0.001)
        canvas.Print(psFileName)

        dnResult = dn.Clone("%s_dn" % jet)
        dnResult = relativeChange(dnResult, nom)
        dnResult = trimLowStats(dnResult)
        dnResult.SetTitle(dnResult.GetTitle()+", nominal - Unc.")
        dnResult.SetMinimum(0.001)
        dnResult.Draw("colztext")
        canvas.Print(psFileName)
    canvas.Close(psFileName+"]")
    


import ROOT as r
import os, math, re

canvas = r.TCanvas()
canvas.SetRightMargin(0.16)
#canvas.SetLeftMargin(.13)
canvas.SetTickx()
canvas.SetTicky()
r.gStyle.SetNumberContours(40)
models = ["T2bb","T1bbbb"][0:1]
pdfSets = ["ct61","ct10","ct66","ms08","nn21"][0:6]
histos = ["ExpectedUpperLimit", "UpperLimit"]
dirs = ["v3_normalized"]
suffix = ["","_normalized"][0]

UpperLimitDict = {"name":"UpperLimit",
                     "label":"#sigma^{NLO+NLL} #pm1 #sigma theory",
                     "lineStyle":1, "lineWidth":3, "color":r.kBlack}
ExpectedUpperlimitDict = {"name":"ExpectedUpperLimit",
                     "label":"Expected Limit #pm1 #sigma exp.",
                     "lineStyle":7, "lineWidth":3, "color":r.kViolet}


for model in models :
    for histo in histos :
        for pdfSet in pdfSets :
            epsFileName = "output_fullScale/%s_%s%s_%s_ratio.eps"%(model,pdfSet,suffix,histo)
            numFile = r.TFile("%s/%s_%s.root"%(dirs[0],model,pdfSets[0]),"READ")
            numHist = numFile.Get(histo)
            denFile = r.TFile("%s/%s_%s%s.root"%(dirs[0],model,pdfSet,suffix),"READ")
            if pdfSet == "ct61" : denFile = r.TFile("%s/%s_%s.root"%(dirs[0],model,pdfSet),"READ")
            denHist = denFile.Get(histo)
            result = numHist.Clone()
            result.Divide(denHist)
            title = re.findall('[A-Z][^A-Z]*', '%s'%histo.replace("_2D_shifted",""))    
            title = " ".join(title)
            print title
            result.SetTitle("Ratio of %s %s on #sigma;m_{sbottom} (GeV);m_{LSP} (GeV);ratio of %s on #sigma"%(model,title,histo.replace("_2D_shifted",""))) 
            result.SetTitleSize(.048,"X")
            result.SetTitleSize(.048,"Y")
            result.SetTitleSize(.048,"Z")
            result.SetMarkerStyle(20)
            result.SetStats(False)

            if "T1bbbb" in model :
                result.SetMaximum(1.3)
                result.SetMinimum(0.9)
                result.GetXaxis().SetLabelSize(.05)
                result.GetYaxis().SetLabelSize(.05)
                result.GetZaxis().SetLabelSize(.05)
                result.GetYaxis().SetTitleOffset(.985)
                result.GetZaxis().SetTitleOffset(.985)
                result.GetXaxis().SetRangeUser(287.5,1400)
                result.GetYaxis().SetRangeUser(0.,1225)

            if "T2bb" in model :
                result.SetMaximum(1.3)
                result.SetMinimum(0.9)
                result.GetXaxis().SetLabelSize(.05)
                result.GetYaxis().SetLabelSize(.05)
                result.GetZaxis().SetLabelSize(.05)
                result.GetYaxis().SetTitleOffset(.985)
                result.GetZaxis().SetTitleOffset(.985)
                #result.GetXaxis().SetRangeUser(287.5,900)
                result.GetXaxis().SetRangeUser(287.5,1200)
                #result.GetYaxis().SetRangeUser(0,725)
                result.GetYaxis().SetRangeUser(0,1025)
            result.Draw("colz")
            ##limit curve TGraph#
            limitCurveFile = r.TFile("%s/%s_hcp.root"%(dirs[0],model),"READ")
            limitCurveGraph = limitCurveFile.Get(histo+"_graph")
            limitCurveGraph.SetLineStyle(1)
            limitCurveGraph.SetLineColor(r.kBlack)
            limitCurveGraph.SetLineWidth(3)
            if "Expected" in histo :
                limitCurveGraph.SetLineStyle(7)
                limitCurveGraph.SetLineColor(r.kViolet)
                limitCurveGraph.SetLineWidth(3)
            limitCurveGraph.Draw("same")


            canvas.Print(epsFileName)
#            result.Write()
           
            os.system("epstopdf "+ epsFileName)
            os.remove(epsFileName)
 


#for model in models :
#    for histo in histos :
#        for pdfSet in pdfSets :
#            epsFileName = "output_fullScale/%s_%s%s_%s.eps"%(model,pdfSet,suffix,histo)
#            origFile = r.TFile("%s/%s_%s%s.root"%(dirs[0],model,pdfSet,suffix),"READ")
#            if pdfSet == "cteq61l" : origFile = r.TFile("%s/%s_%s.root"%(dirs[0],model,pdfSet),"READ")
#            origHist = origFile.Get(histo)
#
#            result = origHist.Clone()
#            title = re.findall('[A-Z][^A-Z]*', '%s'%histo.replace("_2D_shifted",""))
#            title = " ".join(title)
#            print title
#            result.SetTitle("%s %s on #sigma;m_{sbottom} (GeV);m_{LSP} (GeV);%s on #sigma (pb)"%(model,title,histo.replace("_2D_shifted","")))
#            result.SetTitleSize(.048,"X")
#            result.SetTitleSize(.048,"Y")
#            result.SetTitleSize(.048,"Z")
#            result.GetYaxis().SetTitleOffset(.985)
#            result.GetZaxis().SetTitleOffset(.985)
#
#            result.SetMarkerStyle(20)
#            result.SetStats(False)
#
#            if "T1bbbb" in model :
#                result.SetMaximum(10)
#                result.SetMinimum(.001)
#                canvas.SetLogz()
#                result.GetXaxis().SetLabelSize(.05)
#                result.GetYaxis().SetLabelSize(.05)
#                result.GetZaxis().SetLabelSize(.05)
#
#            if "T2bb" in model :
#                result.GetXaxis().SetRangeUser(0,1200)
#                result.GetYaxis().SetRangeUser(0.,1200)
#                result.SetMaximum(10)
#                result.SetMinimum(.001)
#                canvas.SetLogz()
#                result.GetXaxis().SetLabelSize(.05)
#                result.GetYaxis().SetLabelSize(.05)
#                result.GetZaxis().SetLabelSize(.05)
#            result.Draw("colz")
#            
#            canvas.Print(epsFileName)
##            result.Write()                                                                                                                                                                                  
#
#            os.system("epstopdf "+ epsFileName)
#            os.remove(epsFileName)

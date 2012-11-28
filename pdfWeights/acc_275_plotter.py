import ROOT as r
import os, subprocess

canvas = r.TCanvas()
canvas.SetRightMargin(0.2)
canvas.SetTickx()
canvas.SetTicky()

models = ["T2bb","T1bbbb"]
HTbins = ["275","275_scaled","325_scaled","375","875"][0:1]
pdfSets = ["","genMSTW2008nlo68cl", "gencteq66","genNNPDF20"][0:3]
scaleSlices = ["","normalized_"]

for model in models :

    for ht in HTbins :

        for pdfSet in pdfSets :
            for scale in scaleSlices :

                epsFileName = "%sacc_%s_%s_%s.eps"%(scale,model,ht,pdfSet)
                numFile = r.TFile("%s%s_%s_%s.root"%(scale,model,ht,pdfSet),"READ")
                hist =  numFile.Get("nEvents")
                if not pdfSet == "" : hist =  numFile.Get("nEvents_%s_0"%pdfSet)
                result = hist.Clone()
    
                result.SetTitle(";m_{parent} (GeV);m_{LSP} (GeV);Acceptance") 
                result.SetMarkerStyle(20)
                result.SetStats(False)
            
                if "T1bbbb" in model :
                    result.SetMaximum(.34)
                    result.SetMinimum(0.0)
                    line = r.TLine(300,125,2025,1850)
                    line2 = r.TLine(300,50,300,125)
                    lineDiag = r.TLine(100,100,2025,2025)
                
                if "T2bb" in model :
                    result.GetXaxis().SetRangeUser(0,1200)
                    result.GetYaxis().SetRangeUser(0,1200)
                    result.SetMaximum(0.34)
                    result.SetMinimum(0.00)
                    line = r.TLine(300,125,1225,1050)
                    #line = r.TLine(300,125,1200,1025)
                    line2 = r.TLine(300,50,300,125)
                    lineDiag = r.TLine(100,100,1225,1225)

                result.Draw("colz")
                
                lineDiag.SetLineStyle(2)
                line.SetLineWidth(2)
                line2.SetLineWidth(2)
                lineDiag.SetLineWidth(2)
           
                line.Draw("lsame")
                line2.Draw("lsame")
                lineDiag.Draw("lsame")
                
                canvas.Print(epsFileName)
                os.system("epstopdf "+ epsFileName)
                os.remove(epsFileName)

import ROOT as r
import os, subprocess
import glob



canvas = r.TCanvas()
canvas.SetRightMargin(0.2)
canvas.SetTickx()
canvas.SetTicky()

models = ["T2bb","T1bbbb"]
HTbins = ["275","275_scaled","325_scaled","375","875"]
pdfSets = ["genMSTW2008nlo68cl", "gencteq66"]

for model in models :

    for ht in HTbins :

            epsFileName = "%s_%s_%s_acc_ratio.eps"%(model,ht,"cteq66OverMstw")
            numFile = r.TFile("%s_%s_calo_ge2_wPdfWeights.root"%(model,ht),"READ")
            numHist = numFile.Get("nEvents_%s_0"%pdfSets[0])
    
            denFile = r.TFile("%s_%s_calo_ge2_wPdfWeights.root"%(model,ht),"READ")
            denHist = denFile.Get("nEvents_%s_0"%pdfSets[1])


            result = numHist.Clone()
            result.Divide(denHist)
    
            result.SetTitle(";m_{parent} (GeV);m_{LSP} (GeV);ratio") 
            result.SetMarkerStyle(20)
            result.SetStats(False)

            if "T1bbbb" in model :
                result.SetMaximum(1.12)
                result.SetMinimum(0.95)
                if "875" in ht :
                    result.SetMaximum(1.12)
                    result.SetMinimum(0.95)
                line = r.TLine(300,125,2025,1850)
                #line = r.TLine(300,125,1200,1025)
                line2 = r.TLine(300,50,300,125)
                lineDiag = r.TLine(100,100,2025,2025)
                
            if "T2bb" in model :
                result.GetXaxis().SetRangeUser(0,1200)
                result.GetYaxis().SetRangeUser(0,1200)
                result.SetMaximum(1.08)
                result.SetMinimum(0.98)
                if "875" in ht :
                    result.SetMaximum(1.08)
                    result.SetMinimum(0.98)
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
            result.Write()


           
            os.system("epstopdf "+ epsFileName)
            os.remove(epsFileName)




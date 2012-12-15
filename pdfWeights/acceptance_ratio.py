import ROOT as r
import os, subprocess
import glob


canvas = r.TCanvas()
canvas.SetRightMargin(0.2)
canvas.SetTickx()
canvas.SetTicky()
version = ["v1","v2","v3"][2]

models = ["T2bb","T1bbbb_nnpdf_ct10"][1:2]
HTbins = ["275","275_scaled","325_scaled","375","875"][0:1]
pdfSets = ["genMSTW2008nlo68cl", "gencteq66","genNNPDF20","genct10"][3:4]
mods_and_pdfs = [("T1bbbb",["gencteq66","genMSTW2008nlo68cl"]),("T1bbbb_nnpdf",["genNNPDF21"]),("T1bbbb_ct10",["genct10"])]
for modAndPdf in mods_and_pdfs :
    for ht in HTbins :
        for pdfSet in modAndPdf[1] :
            epsFileName = "output/%s_%s_%s_acc_ratio.eps"%(modAndPdf[0],ht,pdfSet)
            numFile = r.TFile("output/acc_%s_%s.root"%(modAndPdf[0],ht),"READ")
            numHist = numFile.Get("nEvents")
    
            denFile = r.TFile("output/acc_%s_%s_%s.root"%(modAndPdf[0],ht,pdfSet),"READ")
            denHist = denFile.Get("nEvents_%s_0"%pdfSet)
            
            result = numHist.Clone()
            result.Divide(denHist)
    
            result.SetTitle(";m_{parent} (GeV);m_{LSP} (GeV);ratio") 
            result.SetMarkerStyle(20)
            result.SetStats(False)
            

            
            if "T1bbbb" in modAndPdf[0] :
                result.SetMaximum(1.15)
                result.SetMinimum(0.85)
                line = r.TLine(300,125,2025,1850)
                #line = r.TLine(300,125,1200,1025)
                line2 = r.TLine(300,50,300,125)
                lineDiag = r.TLine(100,100,2025,2025)
                
            if "T2bb" in modAndPdf[0] :
                result.GetXaxis().SetRangeUser(0,1200)
                result.GetYaxis().SetRangeUser(0,1200)
                result.SetMaximum(1.15)
                result.SetMinimum(0.85)

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
            outfile = r.TFile("output/acc_ratio_%s_%s_%s.root"%(modAndPdf[0],ht,pdfSet),"RECREATE")
            result.SetName("acc_ratio_%s_%s_%s"%(modAndPdf[0],ht,pdfSet))
            result.Write()
           
            os.system("epstopdf "+ epsFileName)
            os.remove(epsFileName)




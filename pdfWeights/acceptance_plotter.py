import ROOT as r
import common as c
import os, subprocess



canvas = r.TCanvas()
canvas.SetRightMargin(0.2)
canvas.SetTickx()
canvas.SetTicky()

#mods_and_pdfs = [("T1bbbb",["","_gencteq66","_genMSTW2008nlo68cl"]),("T1bbbb_nnpdf",["","_genNNPDF21"]),("T1bbbb_ct10",["","_genct10"])]
mods_and_pdfs = c.mods_and_pdfs
htbins = [c.htbins[0][0].strip("_scaled")]
for modAndPdf in mods_and_pdfs :
    tmp = ["_"+w for w in modAndPdf[1]]
    tmp.append("")
    for ht in htbins :
        for pdfSet in tmp :
            epsFileName = "output/acc_%s_%s%s.eps"%(modAndPdf[0],ht,pdfSet)
            accFile = r.TFile("output/acc_%s_%s%s.root"%(modAndPdf[0],ht,pdfSet),"READ")
            accHist = accFile.Get("nEvents")
            if not pdfSet == "" :  accHist = accFile.Get("nEvents%s_0"%pdfSet)
            result = accHist.Clone()
    
            result.SetTitle(";m_{parent} (GeV);m_{LSP} (GeV);acceptance") 
            result.SetMarkerStyle(20)
            result.SetStats(False)
            
            if "T1bbbb" in modAndPdf[0] :
                line = r.TLine(300,125,2025,1850)
                #line = r.TLine(300,125,1200,1025)
                line2 = r.TLine(300,50,300,125)
                lineDiag = r.TLine(100,100,2025,2025)
                
            if "T2bb" in modAndPdf[0] :
                result.GetXaxis().SetRangeUser(0,1200)
                result.GetYaxis().SetRangeUser(0,1200)

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




import ROOT as r
import common as c
import os



canvas = r.TCanvas()
canvas.SetRightMargin(0.2)
canvas.SetTickx()
canvas.SetTicky()
r.gStyle.SetNumberContours(40)
htBins = [c.htbins[0][0].strip("_scaled")]

def modelParser(toBeParsed = "", parsed = "") :
    parsed = toBeParsed.strip("_nnpdf_ct10")
    return parsed

for modAndPdf in c.mods_and_pdfs :
    for ht in htBins :
        for pdfSet in modAndPdf[1] :
            epsFileName = "output_fullScale/%s_%s_%s_acc_ratio.eps"%(modAndPdf[0],ht,pdfSet)
            #numFile = r.TFile("output/acc_%s_%s.root"%(modelParser(modAndPdf[0]),ht),"READ")
            #print "Using nominal pdf found in %s for numerator of ratio"%"output/acc_%s_%s.root"%(modelParser(modAndPdf[0]),ht)            
            numFile = r.TFile("output/acc_%s_%s.root"%(modAndPdf[0],ht),"READ")
            print "Using nominal pdf found in %s for numerator of ratio"%"output/acc_%s_%s.root"%(modAndPdf[0],ht)            

            numHist = numFile.Get("nEvents")
    
            denFile = r.TFile("output/acc_%s_%s_%s.root"%(modAndPdf[0],ht,pdfSet),"READ")
            outfile = r.TFile("output/acc_ratio_%s_%s_%s.root"%(modAndPdf[0],ht,pdfSet),"RECREATE")
            for i in range(c.nPdfDict[pdfSet]) :
	            denHist = denFile.Get("nEvents_%s_%s"%(pdfSet,i))
	            
	            result = numHist.Clone()
	            result.Divide(denHist)
	    
	            result.SetTitle(";m_{parent} (GeV);m_{LSP} (GeV);ratio") 
	            result.SetMarkerStyle(20)
	            result.SetStats(False)

                    if "T2cc" not in modAndPdf[0] :
                    
                        for xbin in range(result.GetXaxis().GetNbins()) :
                            for ybin in range(result.GetYaxis().GetNbins()) :
                                if (ybin*25 > xbin*25 - 175) or (xbin*25 <= 300)  : result.SetBinContent(xbin,ybin,0.0) 

	            
	            if "T1bbbb" in modAndPdf[0] :
	                result.SetMaximum(1.3)
	                result.SetMinimum(0.9)
	                result.GetXaxis().SetRangeUser(300,1400)
                        result.GetYaxis().SetRangeUser(0,1225)
	                line = r.TLine(300,125,2025,1850)
	                #line = r.TLine(300,125,1200,1025)
	                line2 = r.TLine(300,50,300,125)
	                lineDiag = r.TLine(100,100,2025,2025)
	                
	            if "T2bb" in modAndPdf[0] :
	                #result.GetXaxis().SetRangeUser(300,900)
	                #result.GetYaxis().SetRangeUser(0,725)
	                result.GetXaxis().SetRangeUser(300,1200)
	                result.GetYaxis().SetRangeUser(0,1025)
                        result.SetMaximum(1.3)
	                result.SetMinimum(0.9)
	
	                line = r.TLine(300,125,1225,1050)
	                #line = r.TLine(300,125,1200,1025)
	                line2 = r.TLine(300,50,300,125)
	                lineDiag = r.TLine(100,100,1225,1225)

	            if "T2cc" in modAndPdf[0] :
	                result.GetXaxis().SetRangeUser(100,300)
	                result.GetYaxis().SetRangeUser(0, 300)
                        result.RebinY(2)
                        result.RebinX(5)
                        result.SetMaximum(1.1)
	                result.SetMinimum(0.85)
	
	            result.Draw("colz")

                    if "T2cc" not in modAndPdf[0] :
	
		            lineDiag.SetLineStyle(2)
		           
		            line.SetLineWidth(2)
		            line2.SetLineWidth(2)
		            lineDiag.SetLineWidth(2)
	
		           
		            #line.Draw("lsame")
		            #line2.Draw("lsame")
		            #lineDiag.Draw("lsame")
		           
	            canvas.Print(epsFileName)
	
	            result.SetName("acc_ratio_%s_%s_%s_%s"%(modAndPdf[0],ht,pdfSet,i))
	            result.Write()
	           
	            if i == 0 :
                        os.system("epstopdf "+ epsFileName)
                    os.remove(epsFileName)

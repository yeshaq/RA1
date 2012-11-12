import ROOT as r
import os, math




canvas = r.TCanvas()
canvas.SetRightMargin(0.2)
canvas.SetTickx()
canvas.SetTicky()

models = ["T2bb"]#,"T1bbbb"]
HTbins = ["275"]#,"275_scaled","325_scaled","375"])
pdfSets = [["genMSTW2008nlo68cl", 41], ["gencteq66", 45],["genNNPDF20", 30]]

for model in models :

    for ht in HTbins :

        for pdfSet in pdfSets :

            epsFileName = "%s_%s_%s_acc_ratio.eps"%(model,ht,pdfSet[0])
            numFile = r.TFile("%s_%s_calo_ge2_.root"%(model,ht),"READ")
            numHist = numFile.Get("nEvents")
            
            denFile = r.TFile("%s_%s_calo_ge2_wPdfWeights.root"%(model,ht),"READ")
            denHist = []
            for i in range(pdfSet[1]) : 
                denHist.append(denFile.Get("nEvents_%s_%s"%(pdfSet[0],i)))
            
            result = numHist.Clone()
            result.Divide(denHist[0])
    
            result.SetTitle(";m_{parent} (GeV);m_{LSP} (GeV);ratio") 
            result.SetMarkerStyle(20)
            result.SetStats(False)
            
            envelFile = r.TFile("envel_%s_%s.root"%(model,ht),"UPDATE")
            centralHist = r.TH2D("centralValue_%s_%s"%(ht,pdfSet[0]),"centralValue_%s_%s"%(ht,pdfSet[0]),81,0,2025,81,0,2025)
            uncertUpHist = r.TH2D("uncertUpValue_%s_%s"%(ht,pdfSet[0]),"uncertUpValue_%s_%s"%(ht,pdfSet[0]),81,0,2025,81,0,2025)
            uncertDownHist = r.TH2D("uncertDownValue_%s_%s"%(ht,pdfSet[0]),"uncertUpValue_%s_%s"%(ht,pdfSet[0]),81,0,2025,81,0,2025)

            for xbin in range(1,denHist[0].GetXaxis().GetNbins()) :   # ISR cut-off
                for ybin in range(1,denHist[0].GetYaxis().GetNbins()) :
                    if (ybin > xbin - 7) : result.SetBinContent(xbin,ybin,0.0) 
                    if (xbin <= 12) : result.SetBinContent(xbin,ybin,0.0) 
            
            if not pdfSet[0] == "genNNPDF20" : 
                for xbin in range(1,denHist[0].GetXaxis().GetNbins()) :
                    for ybin in range(1,denHist[0].GetYaxis().GetNbins()) :
                        if (result.GetBinContent(xbin,ybin)) == 0.0 : continue
                        centralAcc = denHist[0].GetBinContent(xbin,ybin)
                        dPlus = 0.
                        dMinus = 0.
                        if centralAcc == 0 : continue 
                        for i in range(pdfSet[1]/2) :
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
                            centralAcceptRelVar = (centralAcc-numHist.GetBinContent(xbin,ybin))/numHist.GetBinContent(xbin,ybin)
                            print "---------------------------------------------------------------------------------------------"
                            print pdfSet[0]
                            print "mGl = %s GeV, mLSP = %s GeV"%(xbin*25,ybin*25)
                            print "centr. accept = %.2f%%"%(100*centralAcc)
                            print "ie. %.2f%% relative variation with respect to original PDF"%(100*centralAcceptRelVar)
                            result.SetBinContent(xbin,ybin,(100*(centralAcc-numHist.GetBinContent(xbin,ybin))/numHist.GetBinContent(xbin,ybin)))
                            if pdfSet[0] == "gencteq66" : dPlus/1.645, dMinus/1.645
                            centralHist.SetBinContent(xbin,ybin,centralAcc)
                            uncertUpHist.SetBinContent(xbin,ybin,dPlus*centralAcc)
                            uncertDownHist.SetBinContent(xbin,ybin,dMinus*centralAcc)
                            print centralHist.GetBinContent(xbin,ybin)
                            
                            #"centralHist_%s_%s"%(ht,pdfSet[0]) = result.Clone()
                            #"centralHist_%s_%s"%(ht,pdfSet[0]).SetBinContent(xbin,ybin,centralAcc)
                            #print dPlus*centralAcc
                            #print dMinus*centralAcc
                            print "Relative uncertianty with respect to central member: +%.2f%% / -%.2f%% "%(100*dPlus,100*dMinus)
                                        
            else :
                for xbin in range(1,denHist[0].GetXaxis().GetNbins()) :
                    for ybin in range(1,denHist[0].GetYaxis().GetNbins()) :
                        if (result.GetBinContent(xbin,ybin)) == 0.0 : continue
                        mean_accept = 0
                        sq_std_accept = 0
                        std_accept = 0
                        for i in range(pdfSet[1]) :
                            mean_accept += denHist[i].GetBinContent(xbin,ybin)/pdfSet[1]
                                                        
                        for i in range(pdfSet[1]) :
                            sq_std_accept += (denHist[i].GetBinContent(xbin,ybin)-mean_accept)*(denHist[i].GetBinContent(xbin,ybin)-mean_accept)/(pdfSet[1]-1)  
                        std_accept = math.sqrt(sq_std_accept)
#                        print "---------------------------------------------------------------------------------------------"
#                        print pdfSet[0]
#                        print "xbin = %s, ybin = %s"%(xbin,ybin)
#                        print "mGl = %s GeV, mLSP = %s GeV"%(xbin*25,ybin*25)
#                        print "mean accept = %.2f%%"%(100*mean_accept)
#                        print "ie. %.2f%% relative variation with respect to original PDF"%((100*(mean_accept-numHist.GetBinContent(xbin,ybin))/numHist.GetBinContent(xbin,ybin)))
                        result.SetBinContent(xbin,ybin,(100*(mean_accept-numHist.GetBinContent(xbin,ybin))/numHist.GetBinContent(xbin,ybin)))
#                        print "Relative uncertianty with respect to central member: +- %.2f%%"%(100*std_accept)
#            centralHist.Write()
#            uncertUpHist.Write()
#            uncertDownHist.Write()


            if "T1bbbb" in model :
                result.SetMaximum(1.2)
                result.SetMinimum(0.5)
                if "875" in ht :
                    result.SetMaximum(1.2)
                    result.SetMinimum(0.20)
                line = r.TLine(300,125,2025,1850)
                #line = r.TLine(300,125,1200,1025)
                line2 = r.TLine(300,50,300,125)
                lineDiag = r.TLine(100,100,2025,2025)
                
            if "T2bb" in model :
                result.GetXaxis().SetRangeUser(0,1200)
                result.GetYaxis().SetRangeUser(0.,1200)
#                result.SetMaximum(1.02)
#                result.SetMinimum(0.80)
                result.SetMaximum(15.0)
                result.SetMinimum(0.0)
                if "875" in ht :
                    result.SetMaximum(1.30)
                    result.SetMinimum(0.5)
                line = r.TLine(300,125,1225,1050) # y = x - 225
                #line = r.TLine(300,125,1200,1025)
                line2 = r.TLine(300,0,300,125)
                lineDiag = r.TLine(0,0,1225,1225)

            result.Draw("colz")

            lineDiag.SetLineStyle(2)
           
            line.SetLineWidth(2)
            line2.SetLineWidth(2)
            lineDiag.SetLineWidth(2)
           
            line.Draw("lsame")
            line2.Draw("lsame")
            lineDiag.Draw("lsame")
           
            canvas.Print(epsFileName)
#            result.Write()


           
            os.system("epstopdf "+ epsFileName)
            os.remove(epsFileName)
 
#
#
#Take the central value x = 0:5max(x1+s1; x2+s2; x3+s3)+min(x1s1; x2s2; x3s3))
#
#and the symmetric error s = 0:5max(x1+s1; x2+s2; x3+s3)min(x1s1; x2s2; x3s3))
#
#where x1; x2; x3 are the central values of MSTW08, NNPDF2.0, CTEQ6.6 respectively and
#
#s1; s2; s3 are their 68% CL uncertainties.

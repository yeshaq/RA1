import ROOT as r

Debug = True

version = ["v8","v9"][1]

weights = ["pn","pv"][0:2]
mods_and_pdfs = [("T2cc",["genMSTW2008nlo68cl","genNNPDF21","genct10"], "caloJet")]

nPdfDict = {"gencteq66":45,"genMSTW2008nlo68cl":41,"genct10":53,"genNNPDF21":101}

ra1cats = [""]
for njet in ["le3j","ge4j"]:
    for bjet in ["eq0b","eq1b","eq2b","eq3b","ge4b"]:
        if njet == "le3j" and bjet =="ge4b" :continue
        ra1cats.append((njet,bjet))


def shift2DHistos(hist, shiftX = 0.0 , shiftY = 0.0, rebinX = 0.0, rebinY = 0.0, extraBins = 0) :


    histName = hist.GetName()

    histTitle = hist.GetTitle()
    zMax = hist.GetMaximum()
    zMin = hist.GetMinimum()
    if not rebinX == 0.0 :
        hist.Rebin2D(rebinX,rebinY)

    xAxis = hist.GetXaxis()
    yAxis = hist.GetYaxis()

    nXbins = xAxis.GetNbins()
    nYbins = yAxis.GetNbins()

    xMin = xAxis.GetXmin()
    yMin = yAxis.GetXmin()
    
    xMax = xAxis.GetXmax()
    yMax = yAxis.GetXmax()
    
    dXbin = (xMax - xMin) / nXbins
    dYbin = (yMax - yMin) / nYbins
    
    shiftedXmin = xMin + shiftX*dXbin
    shiftedXmax = xMax + shiftX*dXbin
    
    shiftedYmin = yMin + shiftY*dYbin
    shiftedYmax = yMax + shiftY*dYbin
	

    shiftedHist = r.TH2D(histName, histTitle, nXbins, shiftedXmin, shiftedXmax, nYbins, shiftedYmin, shiftedYmax + extraBins)
    for xbin in range(nXbins) :
        for ybin in range(nYbins) :
            shiftedHist.SetBinContent(xbin+1,ybin+1,hist.GetBinContent(xbin+1,ybin+1))
    shiftedHist.SetMinimum(zMin)
    shiftedHist.SetMaximum(zMax)
    return shiftedHist



def resizeHisto(hist, rnXbins, loX, hiX, rnYbins, loY, hiY) :

    histName = hist.GetName()
    histTitle = hist.GetTitle()
    zMax = hist.GetMaximum()
    zMin = hist.GetMinimum()

    xAxis = hist.GetXaxis()
    yAxis = hist.GetYaxis()

    nXbins = xAxis.GetNbins()
    nYbins = yAxis.GetNbins()

    xMin = xAxis.GetXmin()
    yMin = yAxis.GetXmin()
    
    xMax = xAxis.GetXmax()
    yMax = yAxis.GetXmax()

    dXbin = (xMax - xMin) / nXbins
    dYbin = (yMax - yMin) / nYbins

    deltaLoXbins = (loX - xMin) / dXbin
    deltaLoYbins = (loY - yMin) / dYbin

 
    resizednXbins = (hiX - loX) / dXbin
    resizednYbins = (hiY - loY) / dYbin
    resizedHist = r.TH2D(histName, histTitle, rnXbins, loX, hiX, rnYbins, loY, hiY)
    for xbin in range(nXbins) :
        for ybin in range(nYbins) :
            resizedHist.SetBinContent(xbin+1 ,ybin+1, hist.GetBinContent(xbin+(1+int(deltaLoXbins)), ybin+1 + int(deltaLoYbins)))
    resizedHist.SetMinimum(zMin)
    resizedHist.SetMaximum(zMax)
    return resizedHist

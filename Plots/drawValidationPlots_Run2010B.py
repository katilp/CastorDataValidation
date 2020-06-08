#!/usr/bin/env python
##################################################################
# This is the default stuff, and should not be changed

# import general system and ROOT functions
import ROOT
from ROOT import *
from array import array
import os,re,sys,math

# import CFF specific functions
from CastorDataValidation.Plots.Util import *
from CastorDataValidation.Plots.DrawUtil import *
import CastorDataValidation.Plots.Style

# set the CFF style
style = CastorDataValidation.Plots.Style.setStyle()
style.SetPalette(1)
style.SetPaintTextFormat("4.1f")

##################################################################

# user specific code
# manually draw your stuff from different files/histograms

# read in all files
file_run2010 = ROOT.TFile("../Run2010ABAnalyzer/CASTOR_test_Run2010B.root")
file_pythia84C = ROOT.TFile("../Run2010ABAnalyzer/CASTOR_test_Run2010AMC.root")

# legends
Run2010name = "Run2010B"
Pythia8 = "Pythia8 4C"

# get common histograms
hevents_run2010 = ROOT.TH1D(file_run2010.Get("analyzer/hEventSelection"))
Nevents_run2010 = hevents_run2010.GetBinContent(4) # all events that passed full event selection
print "events in Run2010B data used for normalisation:", Nevents_run2010

hevents_pythia84C = ROOT.TH1D(file_pythia84C.Get("analyzer/hEventSelection"))
Nevents_pythia84C = hevents_pythia84C.GetBinContent(4) # all events that passed full event selection
Ntot_pythia84C = hevents_pythia84C.GetBinContent(1) # all events in the sample for lumi calculation
print "events in Pythia8 4C used for normalisation:", Nevents_pythia84C

cRHmap1 = makeCMSCanvas()
cRHmap1.SetName("RHmap1")

# plot rechit map
hRHmap1 = ROOT.TH2D(file_run2010.Get("analyzer/hRecHit_map"))
hRHmap1.Scale(1./Nevents_run2010)
hRHmap1.GetYaxis().SetTitle("module")
hRHmap1.GetXaxis().SetTitle("sector Run2010B data")
hRHmap1.Draw("COLZ")

cRHmap1.Print("cRHmap1_Run2010B.pdf")

cRHmap2 = makeCMSCanvas()
cRHmap2.SetName("RHmap2")

# plot rechit map
hRHmap2 = ROOT.TH2D(file_pythia84C.Get("analyzer/hRecHit_map"))
hRHmap2.Scale(1./Nevents_pythia84C)
hRHmap2.GetYaxis().SetTitle("module")
hRHmap2.GetXaxis().SetTitle("sector Pythia8 4C")
hRHmap2.Draw("COLZ")

cRHmap2.Print("cRHmap2_Pythia84C_Run2010B.pdf")


# plot rechit occupancy
cRHoccupancy1 = makeCMSCanvas()
cRHoccupancy1.SetName("RHoccupancy1")
hRHoccupancy1 = ROOT.TH2D(file_run2010.Get("analyzer/hRecHit_occupancy"))
hRHoccupancy1.Scale(1./Nevents_run2010)
hRHoccupancy1.GetYaxis().SetTitle("occupancy, module")
hRHoccupancy1.GetXaxis().SetTitle("sector Run2010B data")
hRHoccupancy1.Draw("COLZ TEXT")

cRHoccupancy1.Print("cRHoccupancy1_Run2010B.pdf")


ceflow = makeCMSCanvas()
ceflow.SetName("eflow")
#ceflow.cd().SetLogy()

# plot total energies
heflow1 = ROOT.TH1D(file_run2010.Get("analyzer/hCASTOR_totalE_80rechits"))
heflow1.SetLineColor(1)
heflow1.SetLineWidth(2)
heflow1.Scale(1./heflow1.Integral())
heflow1.GetYaxis().SetTitle("(1/N)dN/dE")
heflow1.GetXaxis().SetTitle("energy [GeV] (80 rechits)")
heflow1.GetYaxis().SetRangeUser(0.0,0.045)
heflow1.GetXaxis().SetRangeUser(0,1400)
heflow1.SetMarkerStyle(20)
heflow1.Draw()
print "eflow 80 rechits Run2010B data = ", heflow1.GetMean()

heflow1_pythia84C = ROOT.TH1D(file_pythia84C.Get("analyzer/hCASTOR_totalE_80rechits"))
heflow1_pythia84C.SetLineColor(2)
heflow1_pythia84C.SetLineWidth(2)
heflow1_pythia84C.Scale(1./heflow1_pythia84C.Integral())
heflow1_pythia84C.Draw("same")
print "eflow 80 rechits Pythia8 4C = ", heflow1_pythia84C.GetMean()

# add legend for 2 entries
leflow = makeLegend(3)
leflow.AddEntry(heflow1,"Run2010B")
leflow.AddEntry(heflow1_pythia84C,"Pythia8 4C")
leflow.Draw()

ceflow.Print("ceflow_"+"Run2010B.pdf")

cmodules = makeCMSCanvas()
cmodules.SetName("modules")

# plot mean energy vs module
hmodules1 = ROOT.TH1D(file_run2010.Get("analyzer/hRecHit_module"))
hmodules1.SetLineColor(1)
hmodules1.SetLineWidth(2)
hmodules1.Scale(1./Nevents_run2010)
hmodules1.GetYaxis().SetTitle("<E> [GeV]")
hmodules1.GetXaxis().SetTitle("module")
hmodules1.GetYaxis().SetRangeUser(0,150)
hmodules1.SetMarkerStyle(20)
hmodules1.SetMarkerColor(1)
hmodules1.SetFillColor(ROOT.kYellow)
for ibin in range(1,hmodules1.GetNbinsX()+1):
    hmodules1.SetBinError(ibin,hmodules1.GetBinContent(ibin)*0.15) # set 15% uncertainty

hmodules1.Draw("E2")

hmodules2 = ROOT.TH1D(file_pythia84C.Get("analyzer/hRecHit_module"))
hmodules2.SetLineColor(2)
hmodules2.SetLineWidth(2)
hmodules2.Scale(1./Nevents_pythia84C)
hmodules2.Draw("same")

# add legend for 2 entries
lmodules = makeLegend(3)
lmodules.AddEntry(hmodules1,"Run2010B")
lmodules.AddEntry(hmodules2,"Pythia8 4C")
lmodules.Draw()

cmodules.Print("cmodules_"+"Run2010B.pdf")

cmodules_norm = makeCMSCanvas()
cmodules_norm.SetName("modules_norm")

# plot mean energy vs module
hmodules_norm1 = ROOT.TH1D(file_run2010.Get("analyzer/hRecHit_module"))
hmodules_norm1.SetLineColor(1)
hmodules_norm1.SetLineWidth(2)
hmodules_norm1.GetXaxis().SetRangeUser(0,5)
hmodules_norm1.Scale(100./hmodules_norm1.Integral())
hmodules_norm1.GetYaxis().SetTitle("Fraction [%]")
hmodules_norm1.GetXaxis().SetTitle("module")
hmodules_norm1.GetYaxis().SetRangeUser(0,53)
hmodules_norm1.SetMarkerStyle(20)
hmodules_norm1.SetFillColor(ROOT.kYellow)
for ibin in range(1,hmodules_norm1.GetNbinsX()+1):
    hmodules_norm1.SetBinError(ibin,hmodules_norm1.GetBinContent(ibin)*0.15) # set 15% uncertainty

hmodules_norm1.Draw("E2")

hmodules_norm2 = ROOT.TH1D(file_pythia84C.Get("analyzer/hRecHit_module"))
hmodules_norm2.SetLineColor(2)
hmodules_norm2.SetLineWidth(2)
hmodules_norm2.GetXaxis().SetRangeUser(0,5)
hmodules_norm2.Scale(100./hmodules_norm2.Integral())
hmodules_norm2.Draw("same")

# add legend for 2 entries
lmodules_norm = makeLegend(3)
lmodules_norm.AddEntry(hmodules_norm1,"Run2010B")
lmodules_norm.AddEntry(hmodules_norm2,"Pythia8 4C")
lmodules_norm.Draw()

cmodules_norm.Print("cmodules_norm_"+"Run2010B.pdf")

csectors = makeCMSCanvas()
csectors.SetName("sectors")

# plot mean energy vs sector
hsectors1 = ROOT.TH1D(file_run2010.Get("analyzer/hRecHit_sector"))
hsectors1.SetLineColor(1)
hsectors1.SetLineWidth(2)
hsectors1.Scale(1./Nevents_run2010)
hsectors1.GetYaxis().SetTitle("<E> [GeV]")
hsectors1.GetXaxis().SetTitle("sector")
hsectors1.GetYaxis().SetRangeUser(4,49)
hsectors1.SetMarkerStyle(20)
hsectors1.SetFillColor(ROOT.kYellow)
for ibin in range(1,hsectors1.GetNbinsX()+1):
    hsectors1.SetBinError(ibin,hsectors1.GetBinContent(ibin)*0.15) # set 15% uncertainty

hsectors1.Draw("E2")

hsectors2 = ROOT.TH1D(file_pythia84C.Get("analyzer/hRecHit_sector"))
hsectors2.SetLineColor(2)
hsectors2.SetLineWidth(2)
hsectors2.Scale(1./Nevents_pythia84C)
hsectors2.Draw("same")

# add legend for 2 entries
lsectors = makeLegend(3)
lsectors.AddEntry(hsectors1,"Run2010B")
lsectors.AddEntry(hsectors2,"Pythia8 4C")
lsectors.Draw()

csectors.Print("csectors_"+"Run2010B.pdf")

csectors_norm = makeCMSCanvas()
csectors_norm.SetName("sectors_norm")

# plot mean energy vs sector
hsectors_norm1 = ROOT.TH1D(file_run2010.Get("analyzer/hRecHit_sector"))
hsectors_norm1.SetLineColor(1)
hsectors_norm1.SetLineWidth(2)
hsectors_norm1.Scale(100./hsectors_norm1.Integral())
hsectors_norm1.GetYaxis().SetTitle("Fraction [%]")
hsectors_norm1.GetXaxis().SetTitle("sector")
hsectors_norm1.GetYaxis().SetRangeUser(0.5,12.5)
hsectors_norm1.SetMarkerStyle(20)
hsectors_norm1.SetFillColor(ROOT.kYellow)
for ibin in range(1,hsectors_norm1.GetNbinsX()+1):
    hsectors_norm1.SetBinError(ibin,hsectors_norm1.GetBinContent(ibin)*0.15) # set 15% uncertainty

hsectors_norm1.Draw("E2")

hsectors_norm2 = ROOT.TH1D(file_pythia84C.Get("analyzer/hRecHit_sector"))
hsectors_norm2.SetLineColor(2)
hsectors_norm2.SetLineWidth(2)
hsectors_norm2.Scale(100./hsectors_norm2.Integral())
hsectors_norm2.Draw("same")

# add legend for 2 entries
lsectors_norm = makeLegend(3)
lsectors_norm.AddEntry(hsectors_norm1,"Run2010B")
lsectors_norm.AddEntry(hsectors_norm2,"Pythia8 4C")
lsectors_norm.Draw()

csectors_norm.Print("csectors_norm_"+"Run2010B.pdf")

c5Msectors = makeCMSCanvas()
c5Msectors.SetName("5Msectors")

# plot mean energy vs sector
h5Msectors1 = ROOT.TH1D(file_run2010.Get("analyzer/hRecHit_5Msector"))
h5Msectors1.SetLineColor(1)
h5Msectors1.SetLineWidth(2)
h5Msectors1.Scale(1./Nevents_run2010)
h5Msectors1.GetYaxis().SetTitle("<E> [GeV]")
h5Msectors1.GetXaxis().SetTitle("sector")
h5Msectors1.GetYaxis().SetRangeUser(4,49)
h5Msectors1.SetMarkerStyle(20)
h5Msectors1.SetFillColor(ROOT.kYellow)
for ibin in range(1,h5Msectors1.GetNbinsX()+1):
    h5Msectors1.SetBinError(ibin,h5Msectors1.GetBinContent(ibin)*0.15) # set 15% uncertainty

h5Msectors1.Draw("E2")

h5Msectors2 = ROOT.TH1D(file_pythia84C.Get("analyzer/hRecHit_5Msector"))
h5Msectors2.SetLineColor(2)
h5Msectors2.SetLineWidth(2)
h5Msectors2.Scale(1./Nevents_pythia84C)
h5Msectors2.Draw("same")

# add legend for 2 entries
l5Msectors = makeLegend(3)
l5Msectors.AddEntry(h5Msectors1,"Run2010B")
l5Msectors.AddEntry(h5Msectors2,"Pythia8 4C")
l5Msectors.Draw()

c5Msectors.Print("c5Msectors_"+"Run2010B.pdf")

c5Msectors_norm = makeCMSCanvas()
c5Msectors_norm.SetName("5Msectors_norm")

# plot mean energy vs sector
h5Msectors_norm1 = ROOT.TH1D(file_run2010.Get("analyzer/hRecHit_5Msector"))
h5Msectors_norm1.SetLineColor(1)
h5Msectors_norm1.SetLineWidth(2)
h5Msectors_norm1.Scale(100./h5Msectors_norm1.Integral())
h5Msectors_norm1.GetYaxis().SetTitle("Fraction [%]")
h5Msectors_norm1.GetXaxis().SetTitle("sector")
h5Msectors_norm1.GetYaxis().SetRangeUser(0.5,12.5)
h5Msectors_norm1.SetMarkerStyle(20)
h5Msectors_norm1.SetFillColor(ROOT.kYellow)
for ibin in range(1,h5Msectors_norm1.GetNbinsX()+1):
    h5Msectors_norm1.SetBinError(ibin,h5Msectors_norm1.GetBinContent(ibin)*0.15) # set 15% uncertainty

h5Msectors_norm1.Draw("E2")

h5Msectors_norm2 = ROOT.TH1D(file_pythia84C.Get("analyzer/hRecHit_5Msector"))
h5Msectors_norm2.SetLineColor(2)
h5Msectors_norm2.SetLineWidth(2)
h5Msectors_norm2.Scale(100./h5Msectors_norm2.Integral())
h5Msectors_norm2.Draw("same")

# add legend for 2 entries
l5Msectors_norm = makeLegend(3)
l5Msectors_norm.AddEntry(h5Msectors_norm1,"Run2010B")
l5Msectors_norm.AddEntry(h5Msectors_norm2,"Pythia8 4C")
l5Msectors_norm.Draw()

c5Msectors_norm.Print("c5Msectors_norm_"+"Run2010B.pdf")


# towers
cLTower_energy = makeCMSCanvas()
cLTower_energy.SetName("LTower_energy")
cLTower_energy.cd().SetLogy()

# plot energy
hLTower_energy1 = ROOT.TH1D(file_run2010.Get("analyzer/hLTower_energy"))
hLTower_energy1.SetLineColor(1)
hLTower_energy1.SetLineWidth(2)
hLTower_energy1.Scale(1./hLTower_energy1.Integral())
hLTower_energy1.GetYaxis().SetTitle("Fraction")
hLTower_energy1.GetXaxis().SetTitle("leading tower energy")
hLTower_energy1.GetYaxis().SetRangeUser(0.0001,0.1)
hLTower_energy1.SetMarkerStyle(20)
hLTower_energy1.Draw()

hLTower_energy2 = ROOT.TH1D(file_pythia84C.Get("analyzer/hLTower_energy"))
hLTower_energy2.SetLineColor(2)
hLTower_energy2.SetLineWidth(2)
hLTower_energy2.Scale(1./hLTower_energy2.Integral())
hLTower_energy2.Draw("same")

# add legend for 2 entries
lLTower_energy = makeLegend(3)
lLTower_energy.AddEntry(hLTower_energy1,"Run2010B")
lLTower_energy.AddEntry(hLTower_energy2,"Pythia8 4C")
lLTower_energy.Draw()

cLTower_energy.Print("cLTower_energy_"+"Run2010B.pdf")

cTower_multi = makeCMSCanvas()
cTower_multi.SetName("Tower_multi")
cTower_multi.cd().SetLogy()

# plot multiplicity
hTower_multi1 = ROOT.TH1D(file_run2010.Get("analyzer/hTower_multi"))
hTower_multi1.SetLineColor(1)
hTower_multi1.SetLineWidth(2)
hTower_multi1.Scale(1./hTower_multi1.Integral())
hTower_multi1.GetYaxis().SetTitle("Fraction")
hTower_multi1.GetXaxis().SetTitle("tower multiplicity")
hTower_multi1.GetYaxis().SetRangeUser(0.01,5)
hTower_multi1.SetMarkerStyle(20)
hTower_multi1.Draw()

hTower_multi2 = ROOT.TH1D(file_pythia84C.Get("analyzer/hTower_multi"))
hTower_multi2.SetLineColor(2)
hTower_multi2.SetLineWidth(2)
hTower_multi2.Scale(1./hTower_multi2.Integral())
hTower_multi2.Draw("same")

# add legend for 2 entries
lTower_multi = makeLegend(3)
lTower_multi.AddEntry(hTower_multi1,"Run2010B")
lTower_multi.AddEntry(hTower_multi2,"Pythia8 4C")
lTower_multi.Draw()

cTower_multi.Print("cTower_multi_"+"Run2010B.pdf")





# jets
cjet_energy = makeCMSCanvas("jet_energy","jet_energy",737,700)
cjet_energy.cd()
cjet_energy_upad = TPad("jet_energy_up","jet_energy_up",0,0.305,1,1)
cjet_energy_lpad = TPad("jet_energy_down","jet_energy_down",0,0,1,0.305)
cjet_energy_upad.SetLeftMargin(0.12)
cjet_energy_upad.SetRightMargin(0.04)
cjet_energy_upad.SetTopMargin(0.08*600/528)
cjet_energy_upad.SetBottomMargin(0)
cjet_energy_lpad.SetLeftMargin(0.12)
cjet_energy_lpad.SetRightMargin(0.04)
cjet_energy_lpad.SetTopMargin(0)
cjet_energy_lpad.SetBottomMargin(0.12*600/232)
cjet_energy_lpad.SetTickx(1)
cjet_energy_upad.Draw()
cjet_energy_lpad.Draw()
cjet_energy_upad.cd()
cjet_energy_upad.SetLogy()

# plot energy
hjet_energy1 = ROOT.TH1D(file_run2010.Get("analyzer/hJet_energy"))
hjet_energy1.SetLineColor(1)
hjet_energy1.SetLineWidth(2)
for ibin in range(1,hjet_energy1.GetNbinsX()+1):
    hjet_energy1.SetBinContent(ibin,hjet_energy1.GetBinContent(ibin)/hjet_energy1.GetXaxis().GetBinWidth(ibin))
    hjet_energy1.SetBinError(ibin,hjet_energy1.GetBinError(ibin)/hjet_energy1.GetXaxis().GetBinWidth(ibin))

hjet_energy1.Scale(Nevents_pythia84C/Nevents_run2010) # scale data to number of events in MC
hjet_energy1.GetYaxis().SetTitle("Fraction")
hjet_energy1.GetXaxis().SetTitle("jet energy")
hjet_energy1.GetXaxis().SetRangeUser(0,3000)
hjet_energy1.SetMarkerStyle(20)
hjet_energy1.Draw()

hjet_energy2 = ROOT.TH1D(file_pythia84C.Get("analyzer/hJet_energy"))
hjet_energy2.SetLineColor(2)
hjet_energy2.SetLineWidth(2)
for ibin in range(1,hjet_energy2.GetNbinsX()+1):
    hjet_energy2.SetBinContent(ibin,hjet_energy2.GetBinContent(ibin)/hjet_energy2.GetXaxis().GetBinWidth(ibin))
    hjet_energy2.SetBinError(ibin,hjet_energy2.GetBinError(ibin)/hjet_energy2.GetXaxis().GetBinWidth(ibin))

hjet_energy2.Draw("same")

# add legend for 2 entries
ljet_energy = makeLegend(3)
ljet_energy.AddEntry(hjet_energy1,"Run2010B")
ljet_energy.AddEntry(hjet_energy2,"Pythia8 4C")
ljet_energy.Draw()

cjet_energy_lpad.cd()
cjet_energy_lpad.SetGridy()
hjet_energy2_ratio = hjet_energy2.Clone()
hjet_energy2_ratio.Divide(hjet_energy1)
hjet_energy2_ratio.GetYaxis().SetRangeUser(0,2.49)
hjet_energy2_ratio.GetYaxis().SetTitle("MC/Data")
hjet_energy2_ratio.GetYaxis().SetTitleSize(0.06*1.8)
hjet_energy2_ratio.GetYaxis().SetTitleOffset(0.4)
hjet_energy2_ratio.GetYaxis().SetTickLength(0.04)
hjet_energy2_ratio.GetYaxis().SetLabelSize(0.05*1.8)
#hjet_energy2_ratio.GetYaxis().SetLabelOffset(0.007*232/600)
hjet_energy2_ratio.GetYaxis().SetNdivisions(505)
hjet_energy2_ratio.GetXaxis().SetTitleSize(0.06*1.8)
hjet_energy2_ratio.GetXaxis().SetTitleOffset(0.85)
hjet_energy2_ratio.GetXaxis().SetTickLength(0.03*1.8)
hjet_energy2_ratio.GetXaxis().SetLabelSize(0.05*1.8)
hjet_energy2_ratio.GetXaxis().SetLabelOffset(0.007*1.8)
hjet_energy2_ratio.Draw()

cjet_energy.Print("cjet_energy_"+"Run2010B.pdf")


# calibrated energy canvas

cjet_calenergy = makeCMSCanvas("jet_calenergy","jet_calenergy",737,700)
cjet_calenergy.cd()
cjet_calenergy_upad = TPad("jet_calenergy_up","jet_calenergy_up",0,0.305,1,1)
cjet_calenergy_lpad = TPad("jet_calenergy_down","jet_calenergy_down",0,0,1,0.305)
cjet_calenergy_upad.SetLeftMargin(0.12)
cjet_calenergy_upad.SetRightMargin(0.04)
cjet_calenergy_upad.SetTopMargin(0.08*600/528)
cjet_calenergy_upad.SetBottomMargin(0)
cjet_calenergy_lpad.SetLeftMargin(0.12)
cjet_calenergy_lpad.SetRightMargin(0.04)
cjet_calenergy_lpad.SetTopMargin(0)
cjet_calenergy_lpad.SetBottomMargin(0.12*600/232)
cjet_calenergy_lpad.SetTickx(1)
cjet_calenergy_upad.Draw()
cjet_calenergy_lpad.Draw()
cjet_calenergy_upad.cd()
cjet_calenergy_upad.SetLogy()

# plot calenergy
hjet_calenergy1 = ROOT.TH1D(file_run2010.Get("analyzer/hJet_calenergy"))
hjet_calenergy1.SetLineColor(1)
hjet_calenergy1.SetLineWidth(2)
for ibin in range(1,hjet_calenergy1.GetNbinsX()+1):
    hjet_calenergy1.SetBinContent(ibin,hjet_calenergy1.GetBinContent(ibin)/hjet_calenergy1.GetXaxis().GetBinWidth(ibin))
    hjet_calenergy1.SetBinError(ibin,hjet_calenergy1.GetBinError(ibin)/hjet_calenergy1.GetXaxis().GetBinWidth(ibin))
    
hjet_calenergy1.Scale(Nevents_pythia84C/Nevents_run2010) # scale data to number of events in MC
hjet_calenergy1.GetYaxis().SetTitle("Fraction")
hjet_calenergy1.GetXaxis().SetTitle("Calibrated jet energy")
hjet_calenergy1.GetXaxis().SetRangeUser(300,1600)
hjet_calenergy1.SetMarkerStyle(20)
hjet_calenergy1.Draw()

hjet_calenergy2 = ROOT.TH1D(file_pythia84C.Get("analyzer/hJet_calenergy"))
hjet_calenergy2.SetLineColor(2)
hjet_calenergy2.SetLineWidth(2)
for ibin in range(1,hjet_calenergy2.GetNbinsX()+1):
    hjet_calenergy2.SetBinContent(ibin,hjet_calenergy2.GetBinContent(ibin)/hjet_calenergy2.GetXaxis().GetBinWidth(ibin))
    hjet_calenergy2.SetBinError(ibin,hjet_calenergy2.GetBinError(ibin)/hjet_calenergy2.GetXaxis().GetBinWidth(ibin))

hjet_calenergy2.Draw("same")

# add legend for 2 entries
ljet_calenergy = makeLegend(2)
ljet_calenergy.AddEntry(hjet_calenergy1,"Run2010B")
ljet_calenergy.AddEntry(hjet_calenergy2,"Pythia8 4C")
ljet_calenergy.Draw()

cjet_calenergy_lpad.cd()
cjet_calenergy_lpad.SetGridy()
hjet_calenergy2_ratio = hjet_calenergy2.Clone()
hjet_calenergy2_ratio.Divide(hjet_calenergy1)
hjet_calenergy2_ratio.GetYaxis().SetRangeUser(0,2.49)
hjet_calenergy2_ratio.GetXaxis().SetRangeUser(300,1600)
hjet_calenergy2_ratio.GetYaxis().SetTitle("MC/Data")
hjet_calenergy2_ratio.GetYaxis().SetTitleSize(0.06*1.8)
hjet_calenergy2_ratio.GetYaxis().SetTitleOffset(0.4)
hjet_calenergy2_ratio.GetYaxis().SetTickLength(0.04)
hjet_calenergy2_ratio.GetYaxis().SetLabelSize(0.05*1.8)
#hjet_calenergy2_ratio.GetYaxis().SetLabelOffset(0.007*232/600)
hjet_calenergy2_ratio.GetYaxis().SetNdivisions(505)
hjet_calenergy2_ratio.GetXaxis().SetTitleSize(0.06*1.8)
hjet_calenergy2_ratio.GetXaxis().SetTitleOffset(0.85)
hjet_calenergy2_ratio.GetXaxis().SetTickLength(0.03*1.8)
hjet_calenergy2_ratio.GetXaxis().SetLabelSize(0.05*1.8)
hjet_calenergy2_ratio.GetXaxis().SetLabelOffset(0.007*1.8)
hjet_calenergy2_ratio.Draw()

cjet_calenergy.Print("cjet_calenergy_"+"Run2010B_v1.pdf")



# prevent python from exiting and closing the canvas
preventExit()


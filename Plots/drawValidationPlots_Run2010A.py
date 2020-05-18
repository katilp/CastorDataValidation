#!/usr/bin/env python
##################################################################
# This is the default stuff, and should not be changed

# import general system and ROOT functions
import ROOT
from ROOT import *
from array import array
import os,re,sys,math

# import CFF specific functions
from CommonFSQFramework.Core.Util import *
from CommonFSQFramework.Core.DrawUtil import *
import CommonFSQFramework.Core.Style

# set the CFF style
style = CommonFSQFramework.Core.Style.setStyle()
style.SetPalette(1)
style.SetPaintTextFormat("4.1f")

##################################################################

# user specific code
# manually draw your stuff from different files/histograms

# read in all files
file_comm10 = ROOT.TFile("CASTOR-Analysis-Commissioning10-7TeV-18062019/merged/CASTOR-Analysis-Commissioning10-7TeV-18062019_merged.root")

file_run2010 = ROOT.TFile("CASTOR-Analysis-Run2010A-7TeV-DemoVal-08082019/merged/CASTOR-Analysis-Run2010A-7TeV-DemoVal-08082019_merged.root")
file_pythia84C = ROOT.TFile("CASTOR-Analysis-Run2010A-Pythia84C-7TeV-DemoVal-08082019/merged/CASTOR-Analysis-Run2010A-Pythia84C-7TeV-DemoVal-08082019_merged.root")
file_pythia84C_sensor = ROOT.TFile("CASTOR-Analysis-Run2010A-Pythia84C-7TeV-FSSensor2010-DemoVal-08082019/merged/CASTOR-Analysis-Run2010A-Pythia84C-7TeV-FSSensor2010-DemoVal-08082019_merged.root")

# legends
Comm10name = "Commissioning10"

Run2010name = "Run2010A"

Pythia8 = "Pythia8 4C"
#Pythia8 = "Pythia8 4C FSsensor2010"

# get common histograms
hevents_run2010 = ROOT.TH1D(file_run2010.Get("demo/hEventSelection"))
Nevents_run2010 = hevents_run2010.GetBinContent(4) # all events that passed full event selection
print "events in Run2010A data used for normalisation:", Nevents_run2010

hevents_pythia84C = ROOT.TH1D(file_pythia84C.Get("demo/hEventSelection"))
Nevents_pythia84C = hevents_pythia84C.GetBinContent(4) # all events that passed full event selection
Ntot_pythia84C = hevents_pythia84C.GetBinContent(1) # all events in the sample for lumi calculation
print "events in Pythia8 4C used for normalisation:", Nevents_pythia84C

hevents_pythia84C_sensor = ROOT.TH1D(file_pythia84C_sensor.Get("demo/hEventSelection"))
Nevents_pythia84C_sensor = hevents_pythia84C_sensor.GetBinContent(4) # all events that passed full event selection
Ntot_pythia84C_sensor = hevents_pythia84C_sensor.GetBinContent(1) # all events in the sample for lumi calculation
print "events in Pythia8 4C FSsensor2010 used for normalisation:", Nevents_pythia84C_sensor

hevents_comm10 = ROOT.TH1D(file_comm10.Get("demo/hEventSelection"))
Nevents_comm10 = hevents_comm10.GetBinContent(5) # all events that passed full event selection
print "events in "+Comm10name+" data used for normalisation:", Nevents_comm10

cRHmap1 = makeCMSCanvas()
cRHmap1.SetName("RHmap1")

# plot rechit map
hRHmap1 = ROOT.TH2D(file_run2010.Get("demo/hRecHit_map"))
hRHmap1.Scale(1./Nevents_run2010)
hRHmap1.GetYaxis().SetTitle("module")
hRHmap1.GetXaxis().SetTitle("sector Run2010A data")
hRHmap1.Draw("COLZ")

cRHmap1.Print("cRHmap1_Run2010A.pdf")

cRHmap2 = makeCMSCanvas()
cRHmap2.SetName("RHmap2")

# plot rechit map
hRHmap2 = ROOT.TH2D(file_pythia84C.Get("demo/hRecHit_map"))
hRHmap2.Scale(1./Nevents_pythia84C)
hRHmap2.GetYaxis().SetTitle("module")
hRHmap2.GetXaxis().SetTitle("sector Pythia8 4C")
hRHmap2.Draw("COLZ")

cRHmap2.Print("cRHmap2_Pythia84C_Run2010A.pdf")


# plot rechit occupancy
cRHoccupancy1 = makeCMSCanvas()
cRHoccupancy1.SetName("RHoccupancy1")
hRHoccupancy1 = ROOT.TH2D(file_run2010.Get("demo/hRecHit_occupancy"))
hRHoccupancy1.Scale(1./Nevents_run2010)
hRHoccupancy1.GetYaxis().SetTitle("occupancy, module")
hRHoccupancy1.GetXaxis().SetTitle("sector Run2010A data")
hRHoccupancy1.Draw("COLZ TEXT")

cRHoccupancy1.Print("cRHoccupancy1_Run2010A.pdf")


ceflow = makeCMSCanvas()
ceflow.SetName("eflow")
#ceflow.cd().SetLogy()

# plot total energies
heflow1 = ROOT.TH1D(file_run2010.Get("demo/hCASTOR_totalE_80rechits"))
heflow1.SetLineColor(1)
heflow1.SetLineWidth(2)
heflow1.Scale(1./heflow1.Integral())
heflow1.GetYaxis().SetTitle("(1/N)dN/dE")
heflow1.GetXaxis().SetTitle("energy [GeV] (80 rechits)")
heflow1.GetYaxis().SetRangeUser(0.0,0.045)
heflow1.GetXaxis().SetRangeUser(0,1400)
heflow1.SetMarkerStyle(20)
heflow1.Draw()
print "eflow 80 rechits Run2010A data = ", heflow1.GetMean()

heflow1_pythia84C = ROOT.TH1D(file_pythia84C.Get("demo/hCASTOR_totalE_80rechits"))
heflow1_pythia84C.SetLineColor(2)
heflow1_pythia84C.SetLineWidth(2)
heflow1_pythia84C.Scale(1./heflow1_pythia84C.Integral())
heflow1_pythia84C.Draw("same")
print "eflow 80 rechits Pythia8 4C = ", heflow1_pythia84C.GetMean()

heflow1_pythia84C_sensor = ROOT.TH1D(file_pythia84C_sensor.Get("demo/hCASTOR_totalE_80rechits"))
heflow1_pythia84C_sensor.SetLineColor(4)
heflow1_pythia84C_sensor.SetLineWidth(2)
heflow1_pythia84C_sensor.Scale(1./heflow1_pythia84C_sensor.Integral())
#heflow1_pythia84C_sensor.Draw("same")
print "eflow 80 rechits Pythia8 4C FSsensor2010 = ", heflow1_pythia84C_sensor.GetMean()


# add legend for 2 entries
leflow = makeLegend(3)
leflow.AddEntry(heflow1,"Run2010A")
leflow.AddEntry(heflow1_pythia84C,"Pythia8 4C")
#leflow.AddEntry(heflow1_pythia84C_sensor,"Pythia8 4C FSsensor2010")
leflow.Draw()

ceflow.Print("ceflow_"+"Run2010A.pdf")

cmodules = makeCMSCanvas()
cmodules.SetName("modules")

# plot mean energy vs module
hmodules1 = ROOT.TH1D(file_run2010.Get("demo/hRecHit_module"))
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

hmodules2 = ROOT.TH1D(file_pythia84C.Get("demo/hRecHit_module"))
hmodules2.SetLineColor(2)
hmodules2.SetLineWidth(2)
hmodules2.Scale(1./Nevents_pythia84C)
hmodules2.Draw("same")

hmodules2_sensor = ROOT.TH1D(file_pythia84C_sensor.Get("demo/hRecHit_module"))
hmodules2_sensor.SetLineColor(4)
hmodules2_sensor.SetLineWidth(2)
hmodules2_sensor.Scale(1./Nevents_pythia84C_sensor)
#hmodules2_sensor.Draw("same")

# add legend for 2 entries
lmodules = makeLegend(3)
lmodules.AddEntry(hmodules1,"Run2010A")
lmodules.AddEntry(hmodules2,"Pythia8 4C")
#lmodules.AddEntry(hmodules2_sensor,"Pythia8 4C FSsensor2010")
lmodules.Draw()

cmodules.Print("cmodules_"+"Run2010A.pdf")

cmodules_norm = makeCMSCanvas()
cmodules_norm.SetName("modules_norm")

# plot mean energy vs module
hmodules_norm1 = ROOT.TH1D(file_run2010.Get("demo/hRecHit_module"))
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

hmodules_norm2 = ROOT.TH1D(file_pythia84C.Get("demo/hRecHit_module"))
hmodules_norm2.SetLineColor(2)
hmodules_norm2.SetLineWidth(2)
hmodules_norm2.GetXaxis().SetRangeUser(0,5)
hmodules_norm2.Scale(100./hmodules_norm2.Integral())
hmodules_norm2.Draw("same")

hmodules_norm2_sensor = ROOT.TH1D(file_pythia84C_sensor.Get("demo/hRecHit_module"))
hmodules_norm2_sensor.SetLineColor(4)
hmodules_norm2_sensor.SetLineWidth(2)
hmodules_norm2_sensor.GetXaxis().SetRangeUser(0,5)
hmodules_norm2_sensor.Scale(100./hmodules_norm2_sensor.Integral())
#hmodules_norm2_sensor.Draw("same")

# add legend for 2 entries
lmodules_norm = makeLegend(3)
lmodules_norm.AddEntry(hmodules_norm1,"Run2010A")
lmodules_norm.AddEntry(hmodules_norm2,"Pythia8 4C")
#lmodules_norm.AddEntry(hmodules_norm2_sensor,"Pythia8 4C FSsensor2010")
lmodules_norm.Draw()

cmodules_norm.Print("cmodules_norm_"+"Run2010A.pdf")

csectors = makeCMSCanvas()
csectors.SetName("sectors")

# plot mean energy vs sector
hsectors1 = ROOT.TH1D(file_run2010.Get("demo/hRecHit_sector"))
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

hsectors2 = ROOT.TH1D(file_pythia84C.Get("demo/hRecHit_sector"))
hsectors2.SetLineColor(2)
hsectors2.SetLineWidth(2)
hsectors2.Scale(1./Nevents_pythia84C)
hsectors2.Draw("same")

hsectors2_sensor = ROOT.TH1D(file_pythia84C_sensor.Get("demo/hRecHit_sector"))
hsectors2_sensor.SetLineColor(4)
hsectors2_sensor.SetLineWidth(2)
hsectors2_sensor.Scale(1./Nevents_pythia84C_sensor)
#hsectors2_sensor.Draw("same")

# add legend for 2 entries
lsectors = makeLegend(3)
lsectors.AddEntry(hsectors1,"Run2010A")
lsectors.AddEntry(hsectors2,"Pythia8 4C")
#lsectors.AddEntry(hsectors2_sensor,"Pythia8 4C FSsensor2010")
lsectors.Draw()

csectors.Print("csectors_"+"Run2010A.pdf")

csectors_norm = makeCMSCanvas()
csectors_norm.SetName("sectors_norm")

# plot mean energy vs sector
hsectors_norm1 = ROOT.TH1D(file_run2010.Get("demo/hRecHit_sector"))
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

hsectors_norm2 = ROOT.TH1D(file_pythia84C.Get("demo/hRecHit_sector"))
hsectors_norm2.SetLineColor(2)
hsectors_norm2.SetLineWidth(2)
hsectors_norm2.Scale(100./hsectors_norm2.Integral())
hsectors_norm2.Draw("same")

hsectors_norm2_sensor = ROOT.TH1D(file_pythia84C_sensor.Get("demo/hRecHit_sector"))
hsectors_norm2_sensor.SetLineColor(4)
hsectors_norm2_sensor.SetLineWidth(2)
hsectors_norm2_sensor.Scale(100./hsectors_norm2_sensor.Integral())
#hsectors_norm2_sensor.Draw("same")

# add legend for 2 entries
lsectors_norm = makeLegend(3)
lsectors_norm.AddEntry(hsectors_norm1,"Run2010A")
lsectors_norm.AddEntry(hsectors_norm2,"Pythia8 4C")
#lsectors_norm.AddEntry(hsectors_norm2_sensor,"Pythia8 4C FSsensor2010")
lsectors_norm.Draw()

csectors_norm.Print("csectors_norm_"+"Run2010A.pdf")

c5Msectors = makeCMSCanvas()
c5Msectors.SetName("5Msectors")

# plot mean energy vs sector
h5Msectors1 = ROOT.TH1D(file_run2010.Get("demo/hRecHit_5Msector"))
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

h5Msectors2 = ROOT.TH1D(file_pythia84C.Get("demo/hRecHit_5Msector"))
h5Msectors2.SetLineColor(2)
h5Msectors2.SetLineWidth(2)
h5Msectors2.Scale(1./Nevents_pythia84C)
h5Msectors2.Draw("same")

h5Msectors2_sensor = ROOT.TH1D(file_pythia84C_sensor.Get("demo/hRecHit_5Msector"))
h5Msectors2_sensor.SetLineColor(4)
h5Msectors2_sensor.SetLineWidth(2)
h5Msectors2_sensor.Scale(1./Nevents_pythia84C_sensor)
#h5Msectors2_sensor.Draw("same")

# add legend for 2 entries
l5Msectors = makeLegend(3)
l5Msectors.AddEntry(h5Msectors1,"Run2010A")
l5Msectors.AddEntry(h5Msectors2,"Pythia8 4C")
#l5Msectors.AddEntry(h5Msectors2_sensor,"Pythia8 4C FSsensor2010")
l5Msectors.Draw()

c5Msectors.Print("c5Msectors_"+"Run2010A.pdf")

c5Msectors_norm = makeCMSCanvas()
c5Msectors_norm.SetName("5Msectors_norm")

# plot mean energy vs sector
h5Msectors_norm1 = ROOT.TH1D(file_run2010.Get("demo/hRecHit_5Msector"))
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

h5Msectors_norm2 = ROOT.TH1D(file_pythia84C.Get("demo/hRecHit_5Msector"))
h5Msectors_norm2.SetLineColor(2)
h5Msectors_norm2.SetLineWidth(2)
h5Msectors_norm2.Scale(100./h5Msectors_norm2.Integral())
h5Msectors_norm2.Draw("same")

h5Msectors_norm2_sensor = ROOT.TH1D(file_pythia84C_sensor.Get("demo/hRecHit_5Msector"))
h5Msectors_norm2_sensor.SetLineColor(4)
h5Msectors_norm2_sensor.SetLineWidth(2)
h5Msectors_norm2_sensor.Scale(100./h5Msectors_norm2_sensor.Integral())
#h5Msectors_norm2_sensor.Draw("same")

# add legend for 2 entries
l5Msectors_norm = makeLegend(3)
l5Msectors_norm.AddEntry(h5Msectors_norm1,"Run2010A")
l5Msectors_norm.AddEntry(h5Msectors_norm2,"Pythia8 4C")
#l5Msectors_norm.AddEntry(h5Msectors_norm2_sensor,"Pythia8 4C FSsensor2010")
l5Msectors_norm.Draw()

c5Msectors_norm.Print("c5Msectors_norm_"+"Run2010A.pdf")


# towers
cLTower_energy = makeCMSCanvas()
cLTower_energy.SetName("LTower_energy")
cLTower_energy.cd().SetLogy()

# plot energy
hLTower_energy1 = ROOT.TH1D(file_run2010.Get("demo/hLTower_energy"))
hLTower_energy1.SetLineColor(1)
hLTower_energy1.SetLineWidth(2)
hLTower_energy1.Scale(1./hLTower_energy1.Integral())
hLTower_energy1.GetYaxis().SetTitle("Fraction")
hLTower_energy1.GetXaxis().SetTitle("leading tower energy")
hLTower_energy1.GetYaxis().SetRangeUser(0.0001,0.1)
hLTower_energy1.SetMarkerStyle(20)
hLTower_energy1.Draw()

hLTower_energy2 = ROOT.TH1D(file_pythia84C.Get("demo/hLTower_energy"))
hLTower_energy2.SetLineColor(2)
hLTower_energy2.SetLineWidth(2)
hLTower_energy2.Scale(1./hLTower_energy2.Integral())
hLTower_energy2.Draw("same")

hLTower_energy2_sensor = ROOT.TH1D(file_pythia84C_sensor.Get("demo/hLTower_energy"))
hLTower_energy2_sensor.SetLineColor(4)
hLTower_energy2_sensor.SetLineWidth(2)
hLTower_energy2_sensor.Scale(1./hLTower_energy2_sensor.Integral())
hLTower_energy2_sensor.Draw("same")

# add legend for 2 entries
lLTower_energy = makeLegend(3)
lLTower_energy.AddEntry(hLTower_energy1,"Run2010A")
lLTower_energy.AddEntry(hLTower_energy2,"Pythia8 4C")
lLTower_energy.AddEntry(hLTower_energy2_sensor,"Pythia8 4C FSsensor2010")
lLTower_energy.Draw()

cLTower_energy.Print("cLTower_energy_"+"Run2010A.pdf")

cTower_multi = makeCMSCanvas()
cTower_multi.SetName("Tower_multi")
cTower_multi.cd().SetLogy()

# plot multiplicity
hTower_multi1 = ROOT.TH1D(file_run2010.Get("demo/hTower_multi"))
hTower_multi1.SetLineColor(1)
hTower_multi1.SetLineWidth(2)
hTower_multi1.Scale(1./hTower_multi1.Integral())
hTower_multi1.GetYaxis().SetTitle("Fraction")
hTower_multi1.GetXaxis().SetTitle("tower multiplicity")
hTower_multi1.GetYaxis().SetRangeUser(0.01,5)
hTower_multi1.SetMarkerStyle(20)
hTower_multi1.Draw()

hTower_multi2 = ROOT.TH1D(file_pythia84C.Get("demo/hTower_multi"))
hTower_multi2.SetLineColor(2)
hTower_multi2.SetLineWidth(2)
hTower_multi2.Scale(1./hTower_multi2.Integral())
hTower_multi2.Draw("same")

hTower_multi2_sensor = ROOT.TH1D(file_pythia84C_sensor.Get("demo/hTower_multi"))
hTower_multi2_sensor.SetLineColor(4)
hTower_multi2_sensor.SetLineWidth(2)
hTower_multi2_sensor.Scale(1./hTower_multi2_sensor.Integral())
hTower_multi2_sensor.Draw("same")

# add legend for 2 entries
lTower_multi = makeLegend(3)
lTower_multi.AddEntry(hTower_multi1,"Run2010A")
lTower_multi.AddEntry(hTower_multi2,"Pythia8 4C")
lTower_multi.AddEntry(hTower_multi2_sensor,"Pythia8 4C FSsensor2010")
lTower_multi.Draw()

cTower_multi.Print("cTower_multi_"+"Run2010A.pdf")





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
hjet_energy1 = ROOT.TH1D(file_run2010.Get("demo/hJet_energy"))
hjet_energy1.SetLineColor(1)
hjet_energy1.SetLineWidth(2)
for ibin in range(1,hjet_energy1.GetNbinsX()+1):
    hjet_energy1.SetBinContent(ibin,hjet_energy1.GetBinContent(ibin)/hjet_energy1.GetXaxis().GetBinWidth(ibin))
    hjet_energy1.SetBinError(ibin,hjet_energy1.GetBinError(ibin)/hjet_energy1.GetXaxis().GetBinWidth(ibin))

hjet_energy1.Scale(Nevents_pythia84C_sensor/Nevents_run2010) # scale data to number of events in MC
hjet_energy1.GetYaxis().SetTitle("Fraction")
hjet_energy1.GetXaxis().SetTitle("jet energy")
hjet_energy1.GetXaxis().SetRangeUser(0,3000)
hjet_energy1.SetMarkerStyle(20)
hjet_energy1.Draw()

hjet_energy2 = ROOT.TH1D(file_pythia84C.Get("demo/hJet_energy"))
hjet_energy2.SetLineColor(2)
hjet_energy2.SetLineWidth(2)
for ibin in range(1,hjet_energy2.GetNbinsX()+1):
    hjet_energy2.SetBinContent(ibin,hjet_energy2.GetBinContent(ibin)/hjet_energy2.GetXaxis().GetBinWidth(ibin))
    hjet_energy2.SetBinError(ibin,hjet_energy2.GetBinError(ibin)/hjet_energy2.GetXaxis().GetBinWidth(ibin))

hjet_energy2.Scale(Nevents_pythia84C_sensor/Nevents_pythia84C) # scale data to number of events in MC
hjet_energy2.Draw("same")

hjet_energy2_sensor = ROOT.TH1D(file_pythia84C_sensor.Get("demo/hJet_energy"))
hjet_energy2_sensor.SetLineColor(4)
hjet_energy2_sensor.SetLineWidth(2)
for ibin in range(1,hjet_energy2_sensor.GetNbinsX()+1):
    hjet_energy2_sensor.SetBinContent(ibin,hjet_energy2_sensor.GetBinContent(ibin)/hjet_energy2_sensor.GetXaxis().GetBinWidth(ibin))
    hjet_energy2_sensor.SetBinError(ibin,hjet_energy2_sensor.GetBinError(ibin)/hjet_energy2_sensor.GetXaxis().GetBinWidth(ibin))

hjet_energy2_sensor.Draw("same")

# add legend for 2 entries
ljet_energy = makeLegend(3)
ljet_energy.AddEntry(hjet_energy1,"Run2010A")
ljet_energy.AddEntry(hjet_energy2,"Pythia8 4C")
ljet_energy.AddEntry(hjet_energy2_sensor,"Pythia8 4C FSsensor2010")
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

hjet_energy2_ratio_sensor = hjet_energy2_sensor.Clone()
hjet_energy2_ratio_sensor.Divide(hjet_energy1)
hjet_energy2_ratio_sensor.Draw("same")

cjet_energy.Print("cjet_energy_"+"Run2010A.pdf")


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
hjet_calenergy1 = ROOT.TH1D(file_run2010.Get("demo/hJet_calenergy"))
hjet_calenergy1.SetLineColor(1)
hjet_calenergy1.SetLineWidth(2)
for ibin in range(1,hjet_calenergy1.GetNbinsX()+1):
    hjet_calenergy1.SetBinContent(ibin,hjet_calenergy1.GetBinContent(ibin)/hjet_calenergy1.GetXaxis().GetBinWidth(ibin))
    hjet_calenergy1.SetBinError(ibin,hjet_calenergy1.GetBinError(ibin)/hjet_calenergy1.GetXaxis().GetBinWidth(ibin))
    
hjet_calenergy1.Scale(Nevents_pythia84C_sensor/Nevents_run2010) # scale data to number of events in MC
hjet_calenergy1.GetYaxis().SetTitle("Fraction")
hjet_calenergy1.GetXaxis().SetTitle("Calibrated jet energy")
hjet_calenergy1.GetXaxis().SetRangeUser(300,1600)
hjet_calenergy1.SetMarkerStyle(20)
hjet_calenergy1.Draw()

hjet_calenergy2 = ROOT.TH1D(file_pythia84C.Get("demo/hJet_calenergy"))
hjet_calenergy2.SetLineColor(2)
hjet_calenergy2.SetLineWidth(2)
for ibin in range(1,hjet_calenergy2.GetNbinsX()+1):
    hjet_calenergy2.SetBinContent(ibin,hjet_calenergy2.GetBinContent(ibin)/hjet_calenergy2.GetXaxis().GetBinWidth(ibin))
    hjet_calenergy2.SetBinError(ibin,hjet_calenergy2.GetBinError(ibin)/hjet_calenergy2.GetXaxis().GetBinWidth(ibin))

hjet_calenergy2.Scale(Nevents_pythia84C_sensor/Nevents_pythia84C) # scale data to number of events in MC
hjet_calenergy2.Draw("same")

hjet_calenergy2_sensor = ROOT.TH1D(file_pythia84C_sensor.Get("demo/hJet_calenergy"))
hjet_calenergy2_sensor.SetLineColor(4)
hjet_calenergy2_sensor.SetLineWidth(2)
for ibin in range(1,hjet_calenergy2_sensor.GetNbinsX()+1):
    hjet_calenergy2_sensor.SetBinContent(ibin,hjet_calenergy2_sensor.GetBinContent(ibin)/hjet_calenergy2_sensor.GetXaxis().GetBinWidth(ibin))
    hjet_calenergy2_sensor.SetBinError(ibin,hjet_calenergy2_sensor.GetBinError(ibin)/hjet_calenergy2_sensor.GetXaxis().GetBinWidth(ibin))

hjet_calenergy2_sensor.Draw("same")

# add legend for 2 entries
ljet_calenergy = makeLegend(2)
ljet_calenergy.AddEntry(hjet_calenergy1,"Run2010A")
ljet_calenergy.AddEntry(hjet_calenergy2,"Pythia8 4C")
ljet_calenergy.AddEntry(hjet_calenergy2_sensor,"Pythia8 4C FSsensor2010")
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

hjet_calenergy2_ratio_sensor = hjet_calenergy2_sensor.Clone()
hjet_calenergy2_ratio_sensor.Divide(hjet_calenergy1)
hjet_calenergy2_ratio_sensor.Draw("same")

cjet_calenergy.Print("cjet_calenergy_"+"Run2010A_v1.pdf")


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

jetbins = [150, 190, 230, 290, 360, 455, 575, 710, 890, 1120, 1400, 1750]

# plot calenergy
hjet_calenergy1_up = ROOT.TH1D(file_comm10.Get("demo/hJet_calenergy_jes_up"))
# remove high E bins
hjet_calenergy1_up_red = ROOT.TH1D("hjet_calenergy1_up_red", "hjet_calenergy1_up_red", 11, array('d',jetbins))
for ibin in range(1,12):
	hjet_calenergy1_up_red.SetBinContent(ibin,hjet_calenergy1_up.GetBinContent(ibin))
	hjet_calenergy1_up_red.SetBinError(ibin,hjet_calenergy1_up.GetBinError(ibin))
	
hjet_calenergy1_up = hjet_calenergy1_up_red.Clone()

hjet_calenergy1_up.SetLineColor(1)
hjet_calenergy1_up.SetLineWidth(2)
hjet_calenergy1_up.SetLineStyle(2)
#hjet_calenergy1_up.Scale(1./hjet_calenergy1_up.Integral())
for ibin in range(1,hjet_calenergy1_up.GetNbinsX()+1):
    hjet_calenergy1_up.SetBinContent(ibin,hjet_calenergy1_up.GetBinContent(ibin)/hjet_calenergy1_up.GetXaxis().GetBinWidth(ibin))
    hjet_calenergy1_up.SetBinError(ibin,hjet_calenergy1_up.GetBinError(ibin)/hjet_calenergy1_up.GetXaxis().GetBinWidth(ibin))
    
hjet_calenergy1_up.GetYaxis().SetTitle("dN/dE (1/GeV)")
hjet_calenergy1_up.GetXaxis().SetTitle("Calibrated jet energy")
hjet_calenergy1_up.GetXaxis().SetRangeUser(300,1600)
hjet_calenergy1_up.GetYaxis().SetRangeUser(5,60000)
hjet_calenergy1_up.DrawCopy()

hjet_calenergy1_down = ROOT.TH1D(file_comm10.Get("demo/hJet_calenergy_jes_down"))
# remove high E bins
hjet_calenergy1_down_red = ROOT.TH1D("hjet_calenergy1_down_red", "hjet_calenergy1_down_red", 11, array('d',jetbins))
for ibin in range(1,12):
	hjet_calenergy1_down_red.SetBinContent(ibin,hjet_calenergy1_down.GetBinContent(ibin))
	hjet_calenergy1_down_red.SetBinError(ibin,hjet_calenergy1_down.GetBinError(ibin))
	
hjet_calenergy1_down = hjet_calenergy1_down_red.Clone()

hjet_calenergy1_down.SetLineColor(1)
hjet_calenergy1_down.SetLineWidth(2)
hjet_calenergy1_down.SetLineStyle(2)
for ibin in range(1,hjet_calenergy1_down.GetNbinsX()+1):
    hjet_calenergy1_down.SetBinContent(ibin,hjet_calenergy1_down.GetBinContent(ibin)/hjet_calenergy1_down.GetXaxis().GetBinWidth(ibin))
    hjet_calenergy1_down.SetBinError(ibin,hjet_calenergy1_down.GetBinError(ibin)/hjet_calenergy1_down.GetXaxis().GetBinWidth(ibin))
    
hjet_calenergy1_down.DrawCopy("same")

hjet_calenergy1 = ROOT.TH1D(file_comm10.Get("demo/hJet_calenergy"))
# remove high E bins
hjet_calenergy1_red = ROOT.TH1D("hjet_calenergy1_red", "hjet_calenergy1_red", 11, array('d',jetbins))
for ibin in range(1,12):
	hjet_calenergy1_red.SetBinContent(ibin,hjet_calenergy1.GetBinContent(ibin))
	hjet_calenergy1_red.SetBinError(ibin,hjet_calenergy1.GetBinError(ibin))
	
hjet_calenergy1 = hjet_calenergy1_red.Clone()

hjet_calenergy1.SetLineColor(1)
hjet_calenergy1.SetLineWidth(2)
for ibin in range(1,hjet_calenergy1.GetNbinsX()+1):
    hjet_calenergy1.SetBinContent(ibin,hjet_calenergy1.GetBinContent(ibin)/hjet_calenergy1.GetXaxis().GetBinWidth(ibin))
    hjet_calenergy1.SetBinError(ibin,hjet_calenergy1.GetBinError(ibin)/hjet_calenergy1.GetXaxis().GetBinWidth(ibin))
    
hjet_calenergy1.SetMarkerStyle(20)
hjet_calenergy1.Draw("same")

hjet_calenergy2 = ROOT.TH1D(file_pythia84C.Get("demo/hJet_calenergy"))
hjet_calenergy2.SetLineColor(2)
hjet_calenergy2.SetLineWidth(2)
for ibin in range(1,hjet_calenergy2.GetNbinsX()+1):
    hjet_calenergy2.SetBinContent(ibin,hjet_calenergy2.GetBinContent(ibin)/hjet_calenergy2.GetXaxis().GetBinWidth(ibin))
    hjet_calenergy2.SetBinError(ibin,hjet_calenergy2.GetBinError(ibin)/hjet_calenergy2.GetXaxis().GetBinWidth(ibin))

hjet_calenergy2.Scale(Nevents_comm10/Nevents_pythia84C) # scale MC to number of events in data
hjet_calenergy2.Draw("same")

hjet_calenergy4 = ROOT.TH1D(file_pythia84C_sensor.Get("demo/hJet_calenergy"))
hjet_calenergy4.SetLineColor(4)
hjet_calenergy4.SetLineWidth(2)
for ibin in range(1,hjet_calenergy4.GetNbinsX()+1):
    hjet_calenergy4.SetBinContent(ibin,hjet_calenergy4.GetBinContent(ibin)/hjet_calenergy4.GetXaxis().GetBinWidth(ibin))
    hjet_calenergy4.SetBinError(ibin,hjet_calenergy4.GetBinError(ibin)/hjet_calenergy4.GetXaxis().GetBinWidth(ibin))

hjet_calenergy4.Scale(Nevents_comm10/Nevents_pythia84C_sensor) # scale MC to number of events in data
hjet_calenergy4.Draw("same")

hjet_calenergy3 = ROOT.TH1D(file_run2010.Get("demo/hJet_calenergy"))
hjet_calenergy3.SetLineColor(ROOT.kGreen+2)
hjet_calenergy3.SetLineWidth(2)
for ibin in range(1,hjet_calenergy3.GetNbinsX()+1):
    hjet_calenergy3.SetBinContent(ibin,hjet_calenergy3.GetBinContent(ibin)/hjet_calenergy3.GetXaxis().GetBinWidth(ibin))
    hjet_calenergy3.SetBinError(ibin,hjet_calenergy3.GetBinError(ibin)/hjet_calenergy3.GetXaxis().GetBinWidth(ibin))

hjet_calenergy3.Scale(Nevents_comm10/Nevents_run2010) # scale Run2010 data to Comm10 data
hjet_calenergy3.Draw("same")

# add legend for 2 entries
ljet_calenergy = makeLegend(3)
ljet_calenergy.AddEntry(hjet_calenergy1,Comm10name)
ljet_calenergy.AddEntry(hjet_calenergy1_up,"JES up & down (15%)")
ljet_calenergy.AddEntry(hjet_calenergy2,Pythia8)
ljet_calenergy.AddEntry(hjet_calenergy4,Pythia8+" FSsensor2010")
ljet_calenergy.AddEntry(hjet_calenergy3,Run2010name)
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

hjet_calenergy1_down_ratio = hjet_calenergy1_down.Clone()
hjet_calenergy1_down_ratio.Divide(hjet_calenergy1)
hjet_calenergy1_down_ratio.Draw("same")

hjet_calenergy1_up_ratio = hjet_calenergy1_up.Clone()
hjet_calenergy1_up_ratio.Divide(hjet_calenergy1)
hjet_calenergy1_up_ratio.Draw("same")

hjet_calenergy3_ratio = hjet_calenergy3.Clone()
hjet_calenergy3_ratio.Divide(hjet_calenergy1)
hjet_calenergy3_ratio.Draw("same")

hjet_calenergy4_ratio = hjet_calenergy4.Clone()
hjet_calenergy4_ratio.Divide(hjet_calenergy1)
hjet_calenergy4_ratio.Draw("same")

cjet_calenergy.Print("cjet_calenergy_"+"Run2010A_v2.pdf")



# prevent python from exiting and closing the canvas
preventExit()


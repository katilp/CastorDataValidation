# CastorDataValidation

## Description

This repository contains code that needs to be used to properly read out CASTOR OpenData of Commissioning10, Run2010A, and Run2010B datasets. It includes two EDAnalyzer plugins that are created to correctly read the reconstructed CASTOR data objects and make validation plots. The needed python configuration files are also included, as well as a plotting script + ROOT files to check the output histograms.

## Requirements

The analysis needs to be run within a [CMS VM 2010](http://opendata.cern.ch/docs/cms-virtual-machine-2010) and the CMSSW_4_2_8_lowpupatch1 release.

## Installation

After installing the CERN OpenData VM for 2010 data (version CMS-OpenData-1.1.2) you need to start up your VM and open the 'CMS shell'.
Then install the correct version of CMSSW and activate it:

    cmsrel CMSSW_4_2_8_lowpupatch1
    cd CMSSW_4_2_8_lowpupatch1/src
    cmsenv

Then add additional needed packages by downloading them as follows:

    wget --no-check-certificate https://twiki.cern.ch/twiki/pub/CMS/CASTOROpenDataRun2010AB/Run2010AB_additional_packages.tar
    tar -xvf Run2010AB_additional_packages.tar

Note that following directories should appear in the CMSSW_4_2_8_lowpupatch1/src directory: RecoLocalCalo, RecoJets, data. If this is not the case then something went wrong when downloading/extracting the packages.

Finally, add this repository and compile everything:

    git clone https://github.com/cms-legacydata-validation/CastorDataValidation.git
    scram b

Now you should be ready to start analysing data.

## Commissioning10 data validation

### Run analyzer 

text

### Create validation plots

## Run2010AB data validation

### Run analyzer

text

### Create validation plots

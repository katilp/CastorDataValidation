# CastorDataValidation

## Description

This repository contains code that needs to be used to properly read out CASTOR OpenData of Commissioning10, Run2010A, and Run2010B datasets. It includes two EDAnalyzer plugins that are created to correctly read the reconstructed CASTOR data objects and make validation plots. The needed python configuration files are also included, as well as a plotting script + ROOT files to check the output histograms.

## Requirements

The analysis needs to be run within a [CMS VM 2010](http://opendata.cern.ch/docs/cms-virtual-machine-2010) and the CMSSW_4_2_8_lowpupatch1 release.

## Installation

After installing the CERN OpenData VM for 2010 data (version CMS-OpenData-1.1.2) you need to start up your VM and open the 'CMS shell'.
First install the correct version of CMSSW and activate it:

    cmsrel CMSSW_4_2_8_lowpupatch1
    cd CMSSW_4_2_8_lowpupatch1/src
    cmsenv

Second, download this repository:

    git clone git://github.com/cms-legacydata-validation/CastorDataValidation.git


Then move and unpack the needed additional packages by doing the following:

    mv CastorDataValidation/CMSSW_additional_packages.tar .
    tar -xvf CMSSW_additional_packages.tar

Note that following extra directories should appear in the CMSSW_4_2_8_lowpupatch1/src directory: RecoLocalCalo, RecoJets, data. If this is not the case then something went wrong when extracting the packages.

Finally, make sure you compile everything:

    scram b

Now you should be ready to start analysing data.

## Commissioning10 data validation

### Run analyzer 

To run the analysis code on Commissioning10 data and MC samples go to following directory:

    cd CastorDataValidation/Commissioning10Analyzer/
    
First, set up the Global Tag environment by doing following (these instructions can be found back [here](http://opendata.cern.ch/docs/cms-guide-for-condition-database) ):

    ln -sf /cvmfs/cms-opendata-conddb.cern.ch/FT_R_42_V10A FT_R_42_V10A
    ln -sf /cvmfs/cms-opendata-conddb.cern.ch/FT_R_42_V10A.db FT_R_42_V10A.db
    ln -sf /cvmfs/cms-opendata-conddb.cern.ch/START42_V17B START42_V17B
    ln -sf /cvmfs/cms-opendata-conddb.cern.ch/START42_V17B.db START42_V17B.db

Then for data execute:

    cmsRun analyzer_cfg_Commissioning10.py
    
And for MC do:

    cmsRun analyzer_cfg_Comm10MC.py
    
Note: when running for the first time to check if everything works, reduce the number of events in the python file to run over, e.g. change this line:

    process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100000) )
    
to only run on 10000 events instead of 100000. This will take much less time.

If everything worked as expected you should see two new ROOT files in the current directory:

    CASTOR_test_Comm10MC.root
    CASTOR_test_Commissioning10.root
    

### Create validation plots

Go to the directory containing the plotting tools:

    cd ../Plots/
    
and there execute the following python script:

    python drawValidationPlots_Commissioning10.py
    
This will create PDF files containing the plots with Commissioning10 data and MC points. Once you run over a sufficient amount of statistics you can compare your obtained plots with those presented [here](https://twiki.cern.ch/twiki/pub/CMSPublic/CASTOROpenData2010/OpenData_CASTORValidationplots_Commissioning10_v1.pdf).
They should be very similar, having the same behaviour, etc. If that is the case, your code is working properly and you are ready to analyse CASTOR data.

## Run2010AB data validation

### Run analyzer

To run the analysis code on Run2010A or Run2010B data and MC samples go to following directory:

    cd CastorDataValidation/Run2010ABAnalyzer/
    
First, set up the Global Tag environment by doing following (these instructions can be found back [here](http://opendata.cern.ch/docs/cms-guide-for-condition-database) ):

    ln -sf /cvmfs/cms-opendata-conddb.cern.ch/FT_R_42_V10A FT_R_42_V10A
    ln -sf /cvmfs/cms-opendata-conddb.cern.ch/FT_R_42_V10A.db FT_R_42_V10A.db
    ln -sf /cvmfs/cms-opendata-conddb.cern.ch/START42_V17B START42_V17B
    ln -sf /cvmfs/cms-opendata-conddb.cern.ch/START42_V17B.db START42_V17B.db

Then for Run2010A data execute:

    cmsRun analyzer_cfg_Run2010A.py
    
For Run2010B data execute:

    cmsRun analyzer_cfg_Run2010B.py
    
And for MC do:

    cmsRun analyzer_cfg_Run2010AMC.py
   
Although the configuration file is called Run2010AMC, it produces MC results that can also be used with Run2010B data.
    
Note: when running for the first time to check if everything works, reduce the number of events in the python file to run over, e.g. change this line:

    process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(500000) )
    
to only run on 10000 events instead of 100000. This will take much less time.

If everything worked as expected you should see three new ROOT files in the current directory:

    CASTOR_test_Run2010AMC.root
    CASTOR_test_Run2010A.root
    CASTOR_test_Run2010B.root
    
### Create validation plots

Go to the directory containing the plotting tools:

    cd ../Plots/
    
and there execute the following python script to compare Run2010A data with the MC sample:

    python drawValidationPlots_Run2010A.py
    
And to compare Run2010B data with the MC sample do:

    python drawValidationPlots_Run2010B.py
    
In both cases this will create PDF files containing the plots with Run2010A or Run2010B data and MC points. Once you run over a sufficient amount of statistics you can compare your obtained plots with those presented [here](https://twiki.cern.ch/twiki/pub/CMS/CASTOROpenDataRun2010AB/OpenData_CASTORValidationplots_Run2010A_v1.pdf) for Run2010A data and [here](https://twiki.cern.ch/twiki/pub/CMS/CASTOROpenDataRun2010AB/OpenData_CASTORValidationplots_Run2010B_v1.pdf) for Run2010B data.
They should be very similar, having the same behaviour, etc. If that is the case, your code is working properly and you are ready to analyse CASTOR data.

## More information

For more information and background on how to properly use CASTOR detector data, please visit the following pages:

[Commissioning10 data twiki page](https://twiki.cern.ch/twiki/bin/view/CMSPublic/CASTOROpenData2010#Commissioning10_data_period)

[Run2010A and Run2010B data twiki page](https://twiki.cern.ch/twiki/bin/view/CMS/CASTOROpenDataRun2010AB)

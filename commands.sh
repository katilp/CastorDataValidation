#!/bin/sh -l

git clone git://github.com/katilp/CastorDataValidation.git

mv CastorDataValidation/CMSSW_additional_packages.tar .
tar -xvf CMSSW_additional_packages.tar

scram b

cd CastorDataValidation/Commissioning10Analyzer/

cmsRun analyzer_cfg_Commissioning10.py
cmsRun analyzer_cfg_Comm10MC.py

ls -l

cd ../Plots/

python drawValidationPlots_Commissioning10.py
ls -l *.pdf

sudo chown -R cmsusr /mountedvolume
chmod 755 /mountedvolume
mkdir /mountedvolume/outputs
cp *.pdf /mountedvolume/outputs
ls -l /mountedvolume/outputs
cd /mountedvolume/outputs
pwd

#!/bin/sh -l

git clone git://github.com/katilp/CastorDataValidation.git

mv CastorDataValidation/CMSSW_additional_packages.tar .
tar -xvf CMSSW_additional_packages.tar

scram b

cd CastorDataValidation/Commissioning10Analyzer/

#change number of events to 10000 if not input or to input value if give
if [ -z "$1" ]
  then
    nev=10000
  else 
    nev=$1
fi
dataeventline=$(grep maxEvents analyzer_cfg_Commissioning10.py)
sed -i "s/$dataeventline/process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32($nev) )/g" analyzer_cfg_Commissioning10.py
mceventline=$(grep maxEvents analyzer_cfg_Comm10MC.py)
sed -i "s/$mceventline/process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32($nev) )/g" analyzer_cfg_Comm10MC.py

#comment the connection to the condition database on cvmfs, the condition data is read differently in the container
sed "/process.GlobalTag.connect/d" analyzer_cfg_Comm10MC.py
sed "/process.GlobalTag.connect/d" analyzer_cfg_Comm10MC.py

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

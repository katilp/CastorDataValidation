#!/bin/sh -l

cd /home/cmsusr

set  -e

echo "Setting up CMSSSW_4_2_8"
source /opt/cms/cmsset_default.sh
scramv1 project CMSSW CMSSW_4_2_8
cd CMSSW_4_2_8/src
eval `scramv1 runtime -sh`
echo "CMSSW_4_2_8 is at your service."


git clone git://github.com/cms-legacydata-validation/CastorDataValidation.git
ls -l
#scram b

#edmProvDump --sort $1 > dump.txt
#sudo chown -R cmsusr /github/workspace
#chmod 755 /github/workspace
#cp dump.txt /github/workspace


echo "::set-output name=another_output::dump.txt"

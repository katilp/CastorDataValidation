import FWCore.ParameterSet.Config as cms
from RecoMuon.TrackingTools.MuonServiceProxy_cff import *
import PhysicsTools.PythonAnalysis.LumiList as LumiList
import FWCore.ParameterSet.Types as CfgTypes
#import FWCore.PythonUtilities.LumiList as LumiList
process = cms.Process("Demo")


# intialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
# **********************************************************************
# set the maximum number of events to be processed                     *
#    this number (argument of int32) is to be modified by the user     *
#    according to need and wish                                        *
#    default is preset to 10000 events                                 *
# **********************************************************************
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )

# set the number of events to be skipped (if any) at end of file below

# define JSON file
goodJSON = '/home/cms-opendata/CMSSW_4_2_8_lowpupatch1/src/Demo/DemoAnalyzer/datasets/Commissioning10-May19ReReco_7TeV.json'

myLumis = LumiList.LumiList(filename = goodJSON).getCMSSWString().split(',')

# ****************************************************************************
# define the input data set here by inserting the appropriate .txt file list *
# ****************************************************************************
import FWCore.Utilities.FileUtils as FileUtils
#
# ****************************************************************
# load the data set                                              * 
# To run over all data subsets, replace '0000' by '0001' etc.    *
# consecutively (make sure you save the output before rerunning) *
# and add up the histograms using root tools.                    *
# ****************************************************************
#
Comm2010data = FileUtils.loadListFromFile('/home/cms-opendata/CMSSW_4_2_8_lowpupatch1/src/Demo/DemoAnalyzer/datasets/CMS_Commissioning10_7TeV_Run135523_file_index.txt')
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    *Comm2010data
    #"root://eospublic.cern.ch//eos/opendata/cms/Run2010B/MinimumBias/AOD/Apr21ReReco-v1/0000/008A07E5-1771-E011-AC8F-001A92971B62.root"
    #"root://xrootd.ba.infn.it//store/data/Commissioning10/MinimumBias/RECO/May19ReReco-v1/0001/FC24D593-1F83-E011-AA02-003048670BF8.root"
    )
)

# apply JSON file
#   (needs to be placed *after* the process.source input file definition!)
process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
process.source.lumisToProcess.extend(myLumis)

# *************************************************
# number of events to be skipped (0 by default)   *
# *************************************************
process.source.skipEvents = cms.untracked.uint32(0)

# ************************************
# CASTOR analysis specific additions *
# ************************************

# require physics declared
process.physDecl = cms.EDFilter("PhysDecl",applyfilter = cms.untracked.bool(True),HLTriggerResults = cms.InputTag("TriggerResults"))

# selection on the rate of high purity tracks (scraping events rejection) 
process.noscraping = cms.EDFilter("FilterOutScraping",
   applyfilter = cms.untracked.bool(True),
   debugOn = cms.untracked.bool(False),
   numtrack = cms.untracked.uint32(10),
   thresh = cms.untracked.double(0.25)
)

# L1 trigger selection - works
process.load('HLTrigger.HLTfilters.hltLevel1GTSeed_cfi')
process.hltLevel1GTSeed.L1TechTriggerSeeding = cms.bool(True)
process.hltLevel1GTSeed.L1SeedsLogicalExpression = cms.string('0 AND (40 OR 41) AND (NOT 36 AND NOT 37 AND NOT 38 AND NOT 39)')
process.load("L1TriggerConfig.L1GtConfigProducers.L1GtTriggerMaskTechTrigConfig_cff")
process.es_prefer_l1GtTriggerMaskTechTrig = cms.ESPrefer("L1GtTriggerMaskTechTrigTrivialProducer","l1GtTriggerMaskTechTrig")

# communicate with the DB
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#### does not work outside CERN, but use with CRAB
process.GlobalTag.globaltag = 'FT_R_42_V10A::All'
#### use for local running 
#process.GlobalTag.connect = cms.string('sqlite_file:/cvmfs/cms-opendata-conddb.cern.ch/FT_R_42_V10A.db')
#process.GlobalTag.globaltag = 'FT_R_42_V10A::All'

# load latest ChannelQuality conditions to remove the bad channels
process.es_ascii = cms.ESSource("CastorTextCalibrations",
    input = cms.VPSet(
                cms.PSet(
                    object = cms.string('ChannelQuality'),
                    file = cms.FileInPath('./data/castor_db2013/DumpCastorCondChannelQuality_Run135059.txt')
                ),
    )
)
process.es_prefer_castor = cms.ESPrefer('CastorTextCalibrations','es_ascii')

# import correct treatment of CASTOR objects
process.load('RecoLocalCalo.Castor.ReReco_data_cff')

# filter bad data
process.castorInvalidDataFilter = cms.EDFilter("CastorInvalidDataFilter")

process.demo = cms.EDAnalyzer('DemoAnalyzer'
)
# ***********************************************************
# output file name                                          *
# default is Mu.root                                        *
# change this according to your wish                        *
# ***********************************************************
process.TFileService = cms.Service("TFileService",
       fileName = cms.string('CASTOR_test_Commissioning10.root')
                                   )                                   
process.recopath = cms.Path(process.hltLevel1GTSeed*process.physDecl*process.noscraping*process.castorInvalidDataFilter*process.CastorReReco*process.demo)

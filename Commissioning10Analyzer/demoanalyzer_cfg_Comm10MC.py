import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.Types as CfgTypes
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
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(25000) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    "root://xrootd.ba.infn.it//store/user/hvanhaev/MinBias_Tune4C_7TeV_pythia8_cff_py_GEN_SIM_START311_V2_Dec11_v1/MinBias_Tune4C_7TeV_pythia8_cff_py_Step3_START42_V11_Dec11_v1/86bcdbe9c73956c342e477ba771c41c7/STEP2_RAW2DIGI_L1Reco_RECO_7TeV_9_1_DE0.root"
    )
)

# *************************************************
# number of events to be skipped (0 by default)   *
# *************************************************
process.source.skipEvents = cms.untracked.uint32(0)

# ************************************
# CASTOR analysis specific additions *
# ************************************

# communicate with the DB
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#### does not work outside CERN, but use with CRAB
process.GlobalTag.globaltag = 'START42_V11::All'
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
process.load('RecoLocalCalo.Castor.ReReco_MC_cff')

process.demo = cms.EDAnalyzer('DemoAnalyzer'
)
# ***********************************************************
# output file name                                          *
# default is Mu.root                                        *
# change this according to your wish                        *
# ***********************************************************
process.TFileService = cms.Service("TFileService",
       fileName = cms.string('CASTOR_test_Comm10MC.root')
                                   )                                   
process.recopath = cms.Path(process.CastorReReco*process.demo)

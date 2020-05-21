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
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )

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
Comm2010MC = FileUtils.loadListFromFile('datasets/CMS_MonteCarloCASTOR_MinBias_Tune4C_7TeV_pythia8_cff_py_Step3_START42_V11_Dec11_v1_86bcdbe9c73956c342e477ba771c41c7_file_index.txt')
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    *Comm2010MC
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
#### use for local running 
process.GlobalTag.connect = cms.string('sqlite_file:/cvmfs/cms-opendata-conddb.cern.ch/START42_V17B.db')
process.GlobalTag.globaltag = 'START42_V17B::All'

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

process.analyzer = cms.EDAnalyzer('Commissioning10Analyzer'
)
# ***********************************************************
# output file name                                          *
# default is Mu.root                                        *
# change this according to your wish                        *
# ***********************************************************
process.TFileService = cms.Service("TFileService",
       fileName = cms.string('CASTOR_test_Comm10MC.root')
                                   )                                   
process.recopath = cms.Path(process.CastorReReco*process.analyzer)

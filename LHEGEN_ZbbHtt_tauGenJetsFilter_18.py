# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: Configuration/GenProduction/python/ZttHbb_fragment.py --nThreads=8 --python_filename B2G-RunIIFall18wmLHEGS-01094_1_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE --fileout file:EGM-RunIISummer20UL18wmLHEGEN-00001.root --conditions 106X_mc2017_realistic_v6 --beamspot Realistic25ns13TeVEarly2017Collision --customise_commands process.source.numberEventsInLuminosityBlock=cms.untracked.uint32(270);process.MessageLogger.cerr.FwkReport.reportEvery=100 --step LHE,GEN --geometry DB:Extended --era Run2_2017 --mc --no_exec --python_filename Step_0_cfg.py -n 100 --nThreads=1 --fileout file:Step_0_Ntuple_2.root
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run2_2018_cff import Run2_2018

process = cms.Process('GEN',Run2_2018)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic25ns13TeVEarly2018Collision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('Configuration/GenProduction/python/ZttHbb_fragment.py nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        #SelectEvents = cms.vstring('generation_step')
		SelectEvents = cms.vstring('tauTauFilterPath', 'tauTauBoostedFilterPath', 'muTauFilterPath', 'eTauFilterPath')
        
    ),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(1),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(20971520),
    fileName = cms.untracked.string('file:Step_0_Ntuple_2.root'),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

process.LHEoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('LHE'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:Step_0_Ntuple_2_inLHE.root'),
    outputCommands = process.LHEEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_upgrade2018_realistic_v4', '')



# this filters at least 2 b quarks at LHE. Requiring 2  avoids including additional jet that are b jets (not from Z decay)
process.LHEBBFilter = cms.EDFilter("LHEGenericFilter",
   src = cms.InputTag("externalLHEProducer"),
   NumRequired = cms.int32(1),
    ParticleID = cms.vint32(5), # it matches both particle & antiparticle
    AcceptLogic = cms.string("GT") # LT meaning < NumRequired, GT >, EQ =, NE !=
)



process.generator = cms.EDFilter("Pythia8ConcurrentHadronizerFilter",
    PythiaParameters = cms.PSet(
        parameterSets = cms.vstring(
            'pythia8CommonSettings', 
            'pythia8CP5Settings', 
            'pythia8PowhegEmissionVetoSettings', 
            'pythia8PSweightsSettings', 
            'processParameters'
        ),
        processParameters = cms.vstring(
            'POWHEG:nFinal = 3', 
            '25:onMode = off', # turn OFF all H decays
            '25:onIfMatch = 15 -15', # turn ON H->tautau      
            '25:m0 = 125.0'
        ),
        pythia8CP5Settings = cms.vstring(
            'Tune:pp 14', 
            'Tune:ee 7', 
            'MultipartonInteractions:ecmPow=0.03344', 
            'MultipartonInteractions:bProfile=2', 
            'MultipartonInteractions:pT0Ref=1.41', 
            'MultipartonInteractions:coreRadius=0.7634', 
            'MultipartonInteractions:coreFraction=0.63', 
            'ColourReconnection:range=5.176', 
            'SigmaTotal:zeroAXB=off', 
            'SpaceShower:alphaSorder=2', 
            'SpaceShower:alphaSvalue=0.118', 
            'SigmaProcess:alphaSvalue=0.118', 
            'SigmaProcess:alphaSorder=2', 
            'MultipartonInteractions:alphaSvalue=0.118', 
            'MultipartonInteractions:alphaSorder=2', 
            'TimeShower:alphaSorder=2', 
            'TimeShower:alphaSvalue=0.118', 
            'SigmaTotal:mode = 0', 
            'SigmaTotal:sigmaEl = 21.89', 
            'SigmaTotal:sigmaTot = 100.309', 
            'PDF:pSet=LHAPDF6:NNPDF31_nnlo_as_0118'
        ),
        pythia8CommonSettings = cms.vstring(
            'Tune:preferLHAPDF = 2', 
            'Main:timesAllowErrors = 10000', 
            'Check:epTolErr = 0.01', 
            'Beams:setProductionScalesFromLHEF = off', 
            'SLHA:keepSM = on', 
            'SLHA:minMassSM = 1000.', 
            'ParticleDecays:limitTau0 = on', 
            'ParticleDecays:tau0Max = 10', 
            'ParticleDecays:allowPhotonRadiation = on'
        ),
        pythia8PSweightsSettings = cms.vstring(
            'UncertaintyBands:doVariations = on', 
            'UncertaintyBands:List = {isrRedHi isr:muRfac=0.707,fsrRedHi fsr:muRfac=0.707,isrRedLo isr:muRfac=1.414,fsrRedLo fsr:muRfac=1.414,isrDefHi isr:muRfac=0.5,fsrDefHi fsr:muRfac=0.5,isrDefLo isr:muRfac=2.0,fsrDefLo fsr:muRfac=2.0,isrConHi isr:muRfac=0.25,fsrConHi fsr:muRfac=0.25,isrConLo isr:muRfac=4.0,fsrConLo fsr:muRfac=4.0,fsr_G2GG_muR_dn fsr:G2GG:muRfac=0.5,fsr_G2GG_muR_up fsr:G2GG:muRfac=2.0,fsr_G2QQ_muR_dn fsr:G2QQ:muRfac=0.5,fsr_G2QQ_muR_up fsr:G2QQ:muRfac=2.0,fsr_Q2QG_muR_dn fsr:Q2QG:muRfac=0.5,fsr_Q2QG_muR_up fsr:Q2QG:muRfac=2.0,fsr_X2XG_muR_dn fsr:X2XG:muRfac=0.5,fsr_X2XG_muR_up fsr:X2XG:muRfac=2.0,fsr_G2GG_cNS_dn fsr:G2GG:cNS=-2.0,fsr_G2GG_cNS_up fsr:G2GG:cNS=2.0,fsr_G2QQ_cNS_dn fsr:G2QQ:cNS=-2.0,fsr_G2QQ_cNS_up fsr:G2QQ:cNS=2.0,fsr_Q2QG_cNS_dn fsr:Q2QG:cNS=-2.0,fsr_Q2QG_cNS_up fsr:Q2QG:cNS=2.0,fsr_X2XG_cNS_dn fsr:X2XG:cNS=-2.0,fsr_X2XG_cNS_up fsr:X2XG:cNS=2.0,isr_G2GG_muR_dn isr:G2GG:muRfac=0.5,isr_G2GG_muR_up isr:G2GG:muRfac=2.0,isr_G2QQ_muR_dn isr:G2QQ:muRfac=0.5,isr_G2QQ_muR_up isr:G2QQ:muRfac=2.0,isr_Q2QG_muR_dn isr:Q2QG:muRfac=0.5,isr_Q2QG_muR_up isr:Q2QG:muRfac=2.0,isr_X2XG_muR_dn isr:X2XG:muRfac=0.5,isr_X2XG_muR_up isr:X2XG:muRfac=2.0,isr_G2GG_cNS_dn isr:G2GG:cNS=-2.0,isr_G2GG_cNS_up isr:G2GG:cNS=2.0,isr_G2QQ_cNS_dn isr:G2QQ:cNS=-2.0,isr_G2QQ_cNS_up isr:G2QQ:cNS=2.0,isr_Q2QG_cNS_dn isr:Q2QG:cNS=-2.0,isr_Q2QG_cNS_up isr:Q2QG:cNS=2.0,isr_X2XG_cNS_dn isr:X2XG:cNS=-2.0,isr_X2XG_cNS_up isr:X2XG:cNS=2.0}', 
            'UncertaintyBands:nFlavQ = 4', 
            'UncertaintyBands:MPIshowers = on', 
            'UncertaintyBands:overSampleFSR = 10.0', 
            'UncertaintyBands:overSampleISR = 10.0', 
            'UncertaintyBands:FSRpTmin2Fac = 20', 
            'UncertaintyBands:ISRpTmin2Fac = 1'
        ),
        pythia8PowhegEmissionVetoSettings = cms.vstring(
            'POWHEG:veto = 1', 
            'POWHEG:pTdef = 1', 
            'POWHEG:emitted = 0', 
            'POWHEG:pTemt = 0', 
            'POWHEG:pThard = 0', 
            'POWHEG:vetoCount = 100', 
            'SpaceShower:pTmaxMatch = 2', 
            'TimeShower:pTmaxMatch = 2'
        )
    ),
    comEnergy = cms.double(13000.0),
    filterEfficiency = cms.untracked.double(1.0),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    pythiaPylistVerbosity = cms.untracked.int32(0)
)


# not possible as H->tautau is done vai Pythia
# process.LHEPtTauFilter = cms.EDFilter("LHEPtFilter",
#     ptMax = cms.double(-1.0),
#     ptMin = cms.double(25),
#     selectedPdgIds = cms.vint32(15),
#     src = cms.InputTag("externalLHEProducer")
# )


process.externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/HZJ_HanythingJ_NNPDF31_13TeV_M125_noWeights.tgz'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    generateConcurrently = cms.untracked.bool(True)
)



process.ProductionFilterSequence = cms.Sequence(process.LHEBBFilter+process.generator)


# tauGenJets : 
# - finds all status==2 taus and collect all non-neutrino descendents in a GeNJet
# - GenJet status is set to the tau decay mode (from PFTau::k... enum, with special values for electron, muon, etc)

# tauGenJetsSelectorAllHadrons : EDFilter that extracts from TauGenJets the hadronic ones only


# process.load("CommonTools.UtilAlgos.BoolOrFilter_cfi")

# first make a list of TauGenJets
# selecting
# - if decayMode == muon -> pt genJet > 15
# - if decayMode == electron -> pt genJet > 20 GeV
# - if decayMode == hadronic -> pt genJet > 15 (unless tautau in which case > 30 GeV each)

# filter decayMode of genJets : with StatusSelector


process.load('PhysicsTools.JetMCAlgos.TauGenJets_cfi')# import tauGenJets
process.load("PhysicsTools.JetMCAlgos.TauGenJetsDecayModeSelectorAllHadrons_cfi") # import tauGenJetsSelectorAllHadrons
process.tauGenJetsSelectorElectrons = cms.EDFilter("TauGenJetDecayModeSelector",
     src = cms.InputTag("tauGenJets"),
     select = cms.vstring('electron'),
     filter = cms.bool(False)
)
process.tauGenJetsSelectorMuons = cms.EDFilter("TauGenJetDecayModeSelector",
     src = cms.InputTag("tauGenJets"),
     select = cms.vstring('muon'),
     filter = cms.bool(False)
)
process.tauGenJetsSequence = cms.Sequence(process.tauGenJets + process.tauGenJetsSelectorAllHadrons + process.tauGenJetsSelectorElectrons+process.tauGenJetsSelectorMuons)

####### filtering for tautau
process.tauTauGenJetFilter = cms.EDFilter("GenJetSelector",
    src = cms.InputTag("tauGenJetsSelectorAllHadrons"),
	cut = cms.string('pt > 37 && abs(eta) < 2.2'), # ditau trigger requirements
	minNumber = cms.uint32(2),
	filter = cms.bool(True),
	)
process.tauTauFilterPath = cms.Path(process.pgen + process.tauGenJetsSequence + process.tauTauGenJetFilter) # add pgen as that was used as SelectEvents in default configuration for RAWSIMoutput

####### filtering for tautau (boostedTau)
# first filter on Z pT (would be better to filter on deltaR(tau,tau) but that is a bit complicated to do)
# could use ObjectPairFilter but that was removed from CMSSW....
process.LHEVptFilter = cms.EDFilter("LHEIntermediateParticlePtFilter", # will match the Z (matches LHE status == 2)
    src = cms.InputTag("externalLHEProducer"),
    ptMin = cms.double(150), # this is very loose (could be 200 GeV)
    ptMax = cms.double(1e10),
   selectedPdgIds = cms.vint32(23),
)
process.tauTauBoostedGenJetFilter = cms.EDFilter("GenJetSelector",
    src = cms.InputTag("tauGenJetsSelectorAllHadrons"),
	cut = cms.string('pt > 35 && abs(eta) < 2.4'), # in boostedTaus tautau we require only eta<2.3 (HPS is <2.1 because of trigger)
	minNumber = cms.uint32(2),
	filter = cms.bool(True),
)
process.tauTauBoostedFilterPath = cms.Path(process.pgen + process.tauGenJetsSequence + process.LHEVptFilter + process.tauTauBoostedGenJetFilter) # add pgen as that was used as SelectEvents in default configuration for RAWSIMoutput


########## filtering for etau
process.emuTauTauhFilter = cms.EDFilter("GenJetSelector",
    src = cms.InputTag("tauGenJetsSelectorAllHadrons"),
	cut = cms.string('pt > 15 && abs(eta) < 2.5'),
	minNumber = cms.uint32(1),
	filter = cms.bool(True)
	)
process.eTauElectronFilter = cms.EDFilter("GenJetSelector",
    src = cms.InputTag("tauGenJetsSelectorElectrons"),
	cut = cms.string('pt > 20 && abs(eta) < 2.6'), # offline selection : pt>25, eta<2.5
	minNumber = cms.uint32(1),
	filter = cms.bool(True)
	)
process.eTauFilterPath = cms.Path(process.pgen + process.tauGenJetsSequence + process.emuTauTauhFilter + process.eTauElectronFilter) # take the AND of both filters

############# mutau
process.muTauMuonFilter = cms.EDFilter("GenJetSelector",
    src = cms.InputTag("tauGenJetsSelectorMuons"),
	cut = cms.string('pt > 18 && abs(eta) < 2.5'), # offline selection :pt>20 (boostedTaus), eta<2.4
	minNumber = cms.uint32(1),
	filter = cms.bool(True)
	)
process.muTauFilterPath = cms.Path(process.pgen + process.tauGenJetsSequence + process.emuTauTauhFilter + process.muTauMuonFilter) # take the AND of both filters


# Path and EndPath definitions
process.lhe_step = cms.Path(process.externalLHEProducer)
process.generation_step = cms.Path(process.pgen)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)
process.LHEoutput_step = cms.EndPath(process.LHEoutput)




# Schedule definition
process.schedule = cms.Schedule(process.lhe_step,process.generation_step,process.tauTauFilterPath,process.tauTauBoostedFilterPath,process.eTauFilterPath,process.muTauFilterPath, process.genfiltersummary_step,process.endjob_step,process.RAWSIMoutput_step,process.LHEoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)
# filter all path with the production filter sequence
for path in process.paths:
	if path in ['lhe_step']: continue
	getattr(process,path).insert(0, process.ProductionFilterSequence)

# customisation of the process.

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions

# Customisation from command line

process.source.numberEventsInLuminosityBlock=cms.untracked.uint32(270);process.MessageLogger.cerr.FwkReport.reportEvery=100
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper
randSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)
randSvc.populate()



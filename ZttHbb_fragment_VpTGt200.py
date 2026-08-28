import FWCore.ParameterSet.Config as cms

# link to cards:
# https://github.com/cms-sw/genproductions/blob/abd5e620174f05eada6dac35f9e366f3019fd6ef/bin/Powheg/production/2017/13TeV/Higgs/HZJ_HanythingJ_NNPDF31_13TeV/HZJ_HanythingJ_NNPDF31_13TeV_M125_Vleptonic.input

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    # the central gridpack produces tens of thousands of PDF replicas which we don't use
    # so hacked the gridpack to not compute PDF weights from replicas (edited pwg-rwl.dat and removed the weights except a few central ones)
    #args = cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/powheg/V2/HZJ_slc7_amd64_gcc700_CMSSW_10_6_27_ZH_HToBB_ZToLL_M125_13TeV_powheg/v1/HZJ_slc7_amd64_gcc700_CMSSW_10_6_27_ZH_HToBB_ZToLL_M125_13TeV_powheg.tgz'),
    args = cms.vstring('/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/HZJ_slc7_amd64_gcc700_CMSSW_10_6_27_ZH_HToBB_ZToLL_M125_13TeV_powheg_noWeights.tgz'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    generateConcurrently = cms.untracked.bool(True)
)

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.Pythia8PowhegEmissionVetoSettings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *


generator = cms.EDFilter("Pythia8ConcurrentHadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PowhegEmissionVetoSettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(
            'POWHEG:nFinal = 3',   ## Number of final state particles
                                   ## (BEFORE THE DECAYS) in the LHE
                                   ## other than emitted extra parton
            '25:m0 = 125.0',
            '25:onMode = off',
            '25:onIfMatch = 5 -5',
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PowhegEmissionVetoSettings',
                                    'pythia8PSweightsSettings',
                                    'processParameters'
                                    )
        )
                         )

#ProductionFilterSequence = cms.Sequence(generator)
LHETauTauFilter = cms.EDFilter("LHEGenericFilter",
   src = cms.InputTag("externalLHEProducer"),
   NumRequired = cms.int32(1),
    ParticleID = cms.vint32(15), # it matches both particle & antiparticle
    AcceptLogic = cms.string("GT") # LT meaning < NumRequired, GT >, EQ =, NE !=
)

LHEPtZFilter = cms.EDFilter("LHEVpTFilter", # will match the Z (matches lepton pair with LHE status == 1). Could be increased to 250
    src = cms.InputTag("externalLHEProducer"),
    VpTMin = cms.double(200),
    VpTMax = cms.double(1e10),
)

# matches the Higgs (status==1)
LHEPtHiggsFilter = cms.EDFilter("LHEPtFilter",
    src = cms.InputTag("externalLHEProducer"),
    selectedPdgIds = cms.vint32(25),
    ptMin = cms.double(200),
    ptMax = cms.double(-1.)
)

ProductionFilterSequence = cms.Sequence(LHETauTauFilter*LHEPtZFilter*LHEPtHiggsFilter*generator)

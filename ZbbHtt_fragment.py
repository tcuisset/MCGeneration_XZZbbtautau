import FWCore.ParameterSet.Config as cms

# link to cards:
#https://github.com/cms-sw/genproductions/blob/ed4fe8f16facb54accec64bfc72246690a166ae3/bin/Powheg/production/2017/13TeV/Higgs/HZJ_HanythingJ_NNPDF31_13TeV/HZJ_HanythingJ_NNPDF31_13TeV_M125_Vinc.input

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    # the central gridpack produces tens of thousands of PDF replicas which we don't use
    # so hacked the gridpack to not compute PDF weights from replicas (edited pwg-rwl.dat and removed the weights except a few central ones)
    #args = cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/HZJ_HanythingJ_NNPDF31_13TeV_M125/v1/HZJ_HanythingJ_NNPDF31_13TeV_M125.tgz'),
    args = cms.vstring('/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/HZJ_HanythingJ_NNPDF31_13TeV_M125_noWeights.tgz'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    generateConcurrently = cms.untracked.bool(True)
)
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
            'POWHEG:nFinal = 3',
            '25:onMode = off', # turn OFF all H decays
            '25:onIfMatch = 15 -15', # turn ON H->tautau      
            '25:m0 = 125.0'
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PowhegEmissionVetoSettings',
                                    'pythia8PSweightsSettings',
                                    'processParameters'
                                    )
        )
                         )

# Gridpack is Z->anything + H
# Pythia force decay H->tautau

# So we need to filter Z->bb
# we can c

#ProductionFilterSequence = cms.Sequence(generator)

# this filters at least 2 b quarks at LHE. Requiring 2  avoids including additional jet that are b jets (not from Z decay)
LHEBBFilter = cms.EDFilter("LHEGenericFilter",
   src = cms.InputTag("externalLHEProducer"),
   NumRequired = cms.int32(1),
    ParticleID = cms.vint32(5), # it matches both particle & antiparticle
    AcceptLogic = cms.string("GT") # LT meaning < NumRequired, GT >, EQ =, NE !=
)

# filter on taus : tau pt >20


# should not be used (filters too much)
# LHEPtZFilter = cms.EDFilter("LHEIntermediateParticlePtFilter", # will match the Z (matches LHE status == 2)
#     src = cms.InputTag("externalLHEProducer"),
#     selectedPdgIds = cms.vint32(23),
#     ptMin = cms.double(30),
#     ptMax = cms.double(-1.)
# )
# LHEPtHiggsFilter = cms.EDFilter("LHEPtFilter",
#     src = cms.InputTag("externalLHEProducer"),
#     selectedPdgIds = cms.vint32(25),
#     ptMin = cms.double(30),
#     ptMax = cms.double(-1.)
# )

# Z boson will be included at LHE with status==2

ProductionFilterSequence = cms.Sequence(LHEBBFilter*generator)

import FWCore.ParameterSet.Config as cms


externalLHEProducer = cms.EDProducer(
    "ExternalLHEProducer",
    args=cms.vstring(
        "/grid_mnt/vol_home/llr/cms/cuisset/bbtautau/ZZbbtautau/MCGeneration/"
        "XToYYTo2B2Tau/genproductions_local/"
        "XToYYTo2B2Tau_MX1000_MY200_13TeV_Run2UL_"
        "slc7_amd64_gcc700_CMSSW_10_6_47_tarball.tar.xz"
    ),
    nEvents=cms.untracked.uint32(100),
    numberOfParameters=cms.uint32(1),
    outputFile=cms.string("cmsgrid_final.lhe"),
    scriptName=cms.FileInPath(
        "GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh"
    ),
    generateConcurrently=cms.untracked.bool(True),
)


from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *


# The hard process is an LO, zero-additional-parton sample.  No MLM/FxFx or
# POWHEG matching block is appropriate; Pythia performs the shower,
# hadronization, and tau decays with the Run-2 CP5 tune.  Tau decay
# polarization is taken from the LHE SPINUP entries written by MadGraph.
generator = cms.EDFilter(
    "Pythia8ConcurrentHadronizerFilter",
    maxEventsToPrint=cms.untracked.int32(0),
    pythiaPylistVerbosity=cms.untracked.int32(0),
    filterEfficiency=cms.untracked.double(1.0),
    pythiaHepMCVerbosity=cms.untracked.bool(False),
    comEnergy=cms.double(13000.0),
    PythiaParameters=cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters=cms.vstring(
            "TauDecays:mode = 5",
            "TauDecays:externalMode = 0",
        ),
        parameterSets=cms.vstring(
            "pythia8CommonSettings",
            "pythia8CP5Settings",
            "pythia8PSweightsSettings",
            "processParameters",
        ),
    ),
)


ProductionFilterSequence = cms.Sequence(generator)

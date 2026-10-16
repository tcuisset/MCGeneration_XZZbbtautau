import os, glob, sys
from datetime import datetime
from optparse import OptionParser
import copy

""" Config dictionnary. Key is name to be passed as command line argument. Value is array of processing steps in order.
Can sepecify either "cfg" : cmssw python config to be run using cmsRun, or "cmsDriver" : string of commands to be passed to cmsDriver.py
"""
multi_conf_dict = {
"gg_X_ZZbbtautau" : [
    {
      "release": "CMSSW_10_6_18",
      "cfg": "gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_0_cfg.py",
      "KeepOutput": False,
    },
    {
      "release": "CMSSW_10_6_17_patch1",
      "cfg": "gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_1_cfg.py",
      "KeepOutput": False,
    },
    {
      "release": "CMSSW_10_2_16_UL",
      "cfg": "gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_2_cfg.py",
      "KeepOutput": False,
    },
    {
      "release": "CMSSW_10_6_17_patch1",
      "cfg": "gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_3_cfg.py",
      "KeepOutput": True,
    },
    {
      "release": "CMSSW_10_6_19_patch2",
      "cfg": "gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_4_cfg.py",
      "KeepOutput": True,
    }
],
"gg_Zprime_ZHtautaubb_v1" : [ # first version of ZtautauHbb config, uses MiniAODv1 which causes problems for nanoAOD production later on
    {
      "release": "CMSSW_10_2_13_patch1",
      "cfg": "gg_Zprime_ZHtautaubb_0_cfg.py",
      "KeepOutput": False,
    },
    {
      "release": "CMSSW_10_2_5",
      "cfg": "gg_Zprime_ZHtautaubb_1_cfg.py",
      "KeepOutput": False,
    },
    {
      "release": "CMSSW_10_2_5",
      "cfg": "gg_Zprime_ZHtautaubb_2_cfg.py",
      "KeepOutput": False,
    },
    {
      "release": "CMSSW_10_2_5",
      "cfg": "gg_Zprime_ZHtautaubb_3_cfg.py",
      "KeepOutput": True,
    },
    {
      "release": "CMSSW_10_2_22",
      "cfg": "gg_Zprime_ZHtautaubb_4_cfg.py",
      "KeepOutput": True,
    },
],
"Zprime_Zh_Zbbhtautau_v2" : [ # second version of Zprime_Zh_Zbbhtautau, based on MiniAODv2 and nanoAODv9 (copied from DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8 production for RunIISummer20UL18)
    { # LHE,GEN
      "release": "CMSSW_10_6_19_patch3", 
      "cmsDriver": 'cmsDriver.py Configuration/GenProduction/python/Zprime_ZH_fragment_template.py --python_filename B2G-RunIIFall18wmLHEGS-01094_1_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE --fileout file:EGM-RunIISummer20UL18wmLHEGEN-00001.root --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(270)" --step LHE,GEN --geometry DB:Extended --era Run2_2018 --mc',
      "KeepOutput": False,
    },
    { # SIM,
      "release": "CMSSW_10_6_17_patch1",
      "cmsDriver": "cmsDriver.py --python_filename EGM-RunIISummer20UL18SIM-00002_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:EGM-RunIISummer20UL18SIM-00002.root --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step SIM --geometry DB:Extended --filein file:EGM-RunIISummer20UL18wmLHEGEN-00001.root --era Run2_2018 --runUnscheduled  --mc",
      "KeepOutput": False,
    },
    { # DIGI,DATAMIX,L1,DIGI2RAW
      "release": "CMSSW_10_6_17_patch1",
      "cmsDriver": 'cmsDriver.py --python_filename EGM-RunIISummer20UL18DIGIPremix-00002_1_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-DIGI --fileout file:EGM-RunIISummer20UL18DIGIPremix-00002.root --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX" --conditions 106X_upgrade2018_realistic_v11_L1v1 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --geometry DB:Extended --filein file:EGM-RunIISummer20UL18SIM-00002.root --datamix PreMix --era Run2_2018 --runUnscheduled  --mc',
      "KeepOutput": False,
    },
    { # HLT
      "release": "CMSSW_10_2_16_UL",
      "cmsDriver": 'cmsDriver.py  --python_filename EGM-RunIISummer20UL18HLT-00002_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:EGM-RunIISummer20UL18HLT-00002.root --conditions 102X_upgrade2018_realistic_v15 --customise_commands \'process.source.bypassVersionCheck = cms.untracked.bool(True)\' --step HLT:2018v32 --geometry DB:Extended --filein file:EGM-RunIISummer20UL18DIGIPremix-00002.root --era Run2_2018 --mc',
      "KeepOutput": False,
    },
    { # RECO
      "release": "CMSSW_10_6_17_patch1",
      "cmsDriver": 'cmsDriver.py --python_filename EGM-RunIISummer20UL18RECO-00002_1_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:EGM-RunIISummer20UL18RECO-00002.root --conditions 106X_upgrade2018_realistic_v11_L1v1 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --geometry DB:Extended --filein file:EGM-RunIISummer20UL18HLT-00002.root --era Run2_2018 --runUnscheduled  --mc',
      "KeepOutput": False,
    },
    {  # MINIAOD
      "release": "CMSSW_10_6_20",
      "cmsDriver": 'cmsDriver.py --python_filename EGM-RunIISummer20UL18MiniAODv2-00004_1_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:EGM-RunIISummer20UL18MiniAODv2-00004.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step PAT --procModifiers run2_miniAOD_UL --geometry DB:Extended --filein "file:EGM-RunIISummer20UL18RECO-00002.root" --era Run2_2018 --runUnscheduled  --mc',
      "KeepOutput": True,
    },
    { # NANO
      "release": "CMSSW_10_6_27", # nanoaod twiki says CMSSW_10_6_27, DY prod used CMSSW_10_6_26 + changed NANOEDMAODSIM to NANOAODSIM
      "cmsDriver": 'cmsDriver.py --python_filename EGM-RunIISummer20UL18NanoAODv9-00005_1_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:EGM-RunIISummer20UL18NanoAODv9-00005.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --customise_commands "process.add_(cms.Service(\'InitRootHandlers\', EnableIMT = cms.untracked.bool(False))) \\n from PhysicsTools.NanoAOD.custom_jme_cff import PrepJMECustomNanoAOD_MC; PrepJMECustomNanoAOD_MC(process)" --step NANO --filein "dbs:/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" --era Run2_2018,run2_nanoAOD_106Xv2  --mc',
      "KeepOutput": True,
    },
],
"ZZbbtt_v1" : [ # ZZ->bbtautau from madgraph. Custom NanoV12 with boostedTaus. 2018UL !!
    { # LHE,GEN
      "release": "CMSSW_10_6_47", 
      "cmsDriver": 'cmsDriver.py Configuration/GenProduction/python/ZZbbtt_fragment.py --nThreads=8 --python_filename B2G-RunIIFall18wmLHEGS-01094_1_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE --fileout file:EGM-RunIISummer20UL18wmLHEGEN-00001.root --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(270)"\\;process.MessageLogger.cerr.FwkReport.reportEvery=100 --step LHE,GEN --geometry DB:Extended --era Run2_2018 --mc',
      "KeepOutput": False,
    },
    { # SIM,
      "release": "CMSSW_10_6_17_patch1",
      "cmsDriver": "cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18SIM-00002_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:EGM-RunIISummer20UL18SIM-00002.root --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step SIM --geometry DB:Extended --filein file:EGM-RunIISummer20UL18wmLHEGEN-00001.root --era Run2_2018 --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100",
      "KeepOutput": False,
    },
    { # DIGI,DATAMIX,L1,DIGI2RAW
      "release": "CMSSW_10_6_17_patch1",
      # --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX"
      # using DAS sopmetimes gte unreadable files. Using manual file list made with : dasgoclient -query 'file dataset=/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX site=T2_FR_GRIF' >PU_LLR.txt
      # so we use only files available at GRIF T2
      # this would need to be rerun after a while as the files may move sites
      # --pileup_input filelist:/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1/PU_LLR.txt 
      "cmsDriver": 'cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18DIGIPremix-00002_1_cfg.py --pileup_input filelist:/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1/PU_LLR.txt --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-DIGI --fileout file:EGM-RunIISummer20UL18DIGIPremix-00002.root  --conditions 106X_upgrade2018_realistic_v11_L1v1 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --geometry DB:Extended --filein file:EGM-RunIISummer20UL18SIM-00002.root --datamix PreMix --era Run2_2018 --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100',
      "KeepOutput": False,
    },
    { # HLT
      "release": "CMSSW_10_2_16_UL",
      "cmsDriver": 'cmsDriver.py --nThreads=8  --python_filename EGM-RunIISummer20UL18HLT-00002_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:EGM-RunIISummer20UL18HLT-00002.root --conditions 102X_upgrade2018_realistic_v15 --customise_commands \'process.source.bypassVersionCheck = cms.untracked.bool(True); process.MessageLogger.cerr.FwkReport.reportEvery=100\' --step HLT:2018v32 --geometry DB:Extended --filein file:EGM-RunIISummer20UL18DIGIPremix-00002.root --era Run2_2018 --mc',
      "KeepOutput": False,
    },
    { # RECO
      "release": "CMSSW_10_6_17_patch1",
      "cmsDriver": 'cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18RECO-00002_1_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:EGM-RunIISummer20UL18RECO-00002.root --conditions 106X_upgrade2018_realistic_v11_L1v1 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --geometry DB:Extended --filein file:EGM-RunIISummer20UL18HLT-00002.root --era Run2_2018 --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100',
      "KeepOutput": False,
    },
    {  # MINIAOD
      "release": "CMSSW_10_6_20",
      "cmsDriver": 'cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18MiniAODv2-00004_1_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:EGM-RunIISummer20UL18MiniAODv2-00004.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step PAT --procModifiers run2_miniAOD_UL --geometry DB:Extended --filein "file:EGM-RunIISummer20UL18RECO-00002.root" --era Run2_2018 --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100',
      "KeepOutput": True,
    },
    { # NANOv12 with boostedTaus
      "release": "CMSSW_13_0_23", 
      # NANO -s NANO --mc --conditions auto:phase1_2018_realistic --era Run2_2018,run2_nanoAOD_106Xv2 --eventcontent NANOAODSIM --datatier NANOAODSIM --customise_commands=process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000 -n -1 --no_exec --filein /store/mc/RunIISummer20UL18MiniAODv2/GluGluToXToZZTo2B2Tau_M-5000_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2830000/0AF2F12C-C0C0-6647-94DF-FB7424298BC7.root
      "cmsDriver": 'cmsDriver.py --nThreads=5 --python_filename EGM-RunIISummer20UL18NanoAODv9-00005_1_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:EGM-RunIISummer20UL18NanoAODv9-00005.root --conditions auto:phase1_2018_realistic --step NANO --filein "file:TOBEREPLACED" --era Run2_2018,run2_nanoAOD_106Xv2  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100',
      "KeepOutput": True,
    },
    # { # NANOv9
    #   "release": "CMSSW_10_6_27", # nanoaod twiki says CMSSW_10_6_27, DY prod used CMSSW_10_6_26 + changed NANOEDMAODSIM to NANOAODSIM
    #   "cmsDriver": 'cmsDriver.py --python_filename EGM-RunIISummer20UL18NanoAODv9-00005_1_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:EGM-RunIISummer20UL18NanoAODv9-00005.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --customise_commands "process.add_(cms.Service(\'InitRootHandlers\', EnableIMT = cms.untracked.bool(False))) \\n from PhysicsTools.NanoAOD.custom_jme_cff import PrepJMECustomNanoAOD_MC; PrepJMECustomNanoAOD_MC(process)" --step NANO --filein "dbs:/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" --era Run2_2018,run2_nanoAOD_106Xv2  --mc',
    #   "KeepOutput": True,
    # },
],
"ZZbbtt_17_v1" : [ # ZZ->bbtautau from madgraph. Custom NanoV12 with boostedTaus
    { # LHE,GEN
      "release": "CMSSW_10_6_47", # probably this should be newer (_38 or _39)
      "cmsDriver": 'cmsDriver.py Configuration/GenProduction/python/ZZbbtt_fragment.py --nThreads=8 --python_filename B2G-RunIIFall18wmLHEGS-01094_1_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE --fileout file:EGM-RunIISummer20UL18wmLHEGEN-00001.root --conditions 106X_mc2017_realistic_v6 --beamspot Realistic25ns13TeVEarly2017Collision --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(270)"\\;process.MessageLogger.cerr.FwkReport.reportEvery=100 --step LHE,GEN --geometry DB:Extended --era Run2_2017 --mc',
      "KeepOutput": False,
    },
    { # SIM,
      "release": "CMSSW_10_6_17_patch1",
      "cmsDriver": "cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18SIM-00002_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:EGM-RunIISummer20UL18SIM-00002.root --conditions 106X_mc2017_realistic_v6 --beamspot Realistic25ns13TeVEarly2017Collision --step SIM --geometry DB:Extended --filein file:EGM-RunIISummer20UL18wmLHEGEN-00001.root --era Run2_2017 --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100",
      "KeepOutput": False,
    },
    { # DIGI,DATAMIX,L1,DIGI2RAW
      "release": "CMSSW_10_6_17_patch1",
      # --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL17_106X_mc2017_realistic_v6-v3/PREMIX"
      # was not available at LLR so selected CERN only (avoid FNAL)
      # using DAS sopmetimes gte unreadable files. Using manual file list made with : dasgoclient -query 'file dataset=/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL17_106X_mc2017_realistic_v6-v3/PREMIX site=T2_CH_CERN' >PU_LLR_17.txt
      # so we use only files available at GRIF T2
      # this would need to be rerun after a while as the files may move sites
      # --pileup_input filelist:/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1/PU_LLR.txt 
      "cmsDriver": 'cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18DIGIPremix-00002_1_cfg.py --pileup_input filelist:/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1/PU_LLR_17.txt --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-DIGI --fileout file:EGM-RunIISummer20UL18DIGIPremix-00002.root  --conditions 106X_mc2017_realistic_v6 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --geometry DB:Extended --filein file:EGM-RunIISummer20UL18SIM-00002.root --datamix PreMix --era Run2_2017 --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100',
      "KeepOutput": False,
    },
    { # HLT
      "release": "CMSSW_9_4_14_UL_patch1", # release depends on year !
      "cmsDriver": 'cmsDriver.py --nThreads=8  --python_filename EGM-RunIISummer20UL18HLT-00002_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:EGM-RunIISummer20UL18HLT-00002.root --conditions 94X_mc2017_realistic_v15 --customise_commands \'process.source.bypassVersionCheck = cms.untracked.bool(True); process.MessageLogger.cerr.FwkReport.reportEvery=100\' --step HLT:2e34v40 --geometry DB:Extended --filein file:EGM-RunIISummer20UL18DIGIPremix-00002.root --era Run2_2017 --mc',
      "KeepOutput": False,
    },
    { # RECO
      "release": "CMSSW_10_6_17_patch1",
      "cmsDriver": 'cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18RECO-00002_1_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:EGM-RunIISummer20UL18RECO-00002.root --conditions 106X_mc2017_realistic_v6 --step RAW2DIGI,L1Reco,RECO,RECOSIM --geometry DB:Extended --filein file:EGM-RunIISummer20UL18HLT-00002.root --era Run2_2017 --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100',
      "KeepOutput": False,
    },
    {  # MINIAOD
      "release": "CMSSW_10_6_20",
      "cmsDriver": 'cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18MiniAODv2-00004_1_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:EGM-RunIISummer20UL18MiniAODv2-00004.root --conditions 106X_mc2017_realistic_v9 --step PAT --procModifiers run2_miniAOD_UL --geometry DB:Extended --filein "file:EGM-RunIISummer20UL18RECO-00002.root" --era Run2_2017 --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100',
      "KeepOutput": True,
    },
    { # NANOv12 with boostedTaus
      "release": "CMSSW_13_0_23", 
      # NANO -s NANO --mc --conditions auto:phase1_2018_realistic --era Run2_2018,run2_nanoAOD_106Xv2 --eventcontent NANOAODSIM --datatier NANOAODSIM --customise_commands=process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000 -n -1 --no_exec --filein /store/mc/RunIISummer20UL18MiniAODv2/GluGluToXToZZTo2B2Tau_M-5000_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2830000/0AF2F12C-C0C0-6647-94DF-FB7424298BC7.root
      "cmsDriver": 'cmsDriver.py --nThreads=5 --python_filename EGM-RunIISummer20UL18NanoAODv9-00005_1_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:EGM-RunIISummer20UL18NanoAODv9-00005.root --conditions auto:phase1_2017_realistic --step NANO --filein "file:TOBEREPLACED" --era Run2_2017,run2_nanoAOD_106Xv2  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100',
      "KeepOutput": True,
    },
],
"ZZbbtt_16_v1" : [ # ZZ->bbtautau from madgraph. Custom NanoV12 with boostedTaus
    { # LHE,GEN
      "release": "CMSSW_10_6_47", # probably this should be newer (_38 or _39)
      "cmsDriver": 'cmsDriver.py Configuration/GenProduction/python/ZZbbtt_fragment.py --nThreads=8 --python_filename B2G-RunIIFall18wmLHEGS-01094_1_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE --fileout file:EGM-RunIISummer20UL18wmLHEGEN-00001.root --conditions 106X_mcRun2_asymptotic_v13 --beamspot Realistic25ns13TeV2016Collision --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(270)"\\;process.MessageLogger.cerr.FwkReport.reportEvery=100 --step LHE,GEN --geometry DB:Extended --era Run2_2016 --mc',
      "KeepOutput": False,
    },
    { # SIM,
      "release": "CMSSW_10_6_17_patch1",
      "cmsDriver": "cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18SIM-00002_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:EGM-RunIISummer20UL18SIM-00002.root --conditions 106X_mcRun2_asymptotic_v13 --beamspot Realistic25ns13TeV2016Collision --step SIM --geometry DB:Extended --filein file:EGM-RunIISummer20UL18wmLHEGEN-00001.root --era Run2_2016 --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100",
      "KeepOutput": False,
    },
    { # DIGI,DATAMIX,L1,DIGI2RAW
      "release": "CMSSW_10_6_17_patch1",
      #--pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL16_106X_mcRun2_asymptotic_v13-v1/PREMIX" 
      #  dasgoclient -query 'file dataset=/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL16_106X_mcRun2_asymptotic_v13-v1/PREMIX site=T1_FR_CCIN2P3_Disk' >PU_LLR_16.txt
      "cmsDriver": 'cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18DIGIPremix-00002_1_cfg.py --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL16_106X_mcRun2_asymptotic_v13-v1/PREMIX" --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-DIGI --fileout file:EGM-RunIISummer20UL18DIGIPremix-00002.root  --conditions 106X_mcRun2_asymptotic_v13 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --geometry DB:Extended --filein file:EGM-RunIISummer20UL18SIM-00002.root --datamix PreMix --era Run2_2016 --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100',
      "KeepOutput": False,
    },
    { # HLT
      "release": "CMSSW_8_0_36_UL_patch2", # release depends on year !
      "cmsDriver": 'cmsDriver.py --nThreads=8  --python_filename EGM-RunIISummer20UL18HLT-00002_1_cfg.py --eventcontent RAWSIM --outputCommand "keep *_mix_*_*,keep *_genPUProtons_*_*"  --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:EGM-RunIISummer20UL18HLT-00002.root  --inputCommands "keep *","drop *_*_BMTF_*","drop *PixelFEDChannel*_*_*_*" --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --customise_commands \'process.source.bypassVersionCheck = cms.untracked.bool(True); process.MessageLogger.cerr.FwkReport.reportEvery=100\' --step HLT:25ns15e33_v4 --geometry DB:Extended --filein file:EGM-RunIISummer20UL18DIGIPremix-00002.root --era Run2_2016 --mc',
      "KeepOutput": False,
    },
    { # RECO
      "release": "CMSSW_10_6_17_patch1",
      "cmsDriver": 'cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18RECO-00002_1_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:EGM-RunIISummer20UL18RECO-00002.root --conditions 106X_mcRun2_asymptotic_v13 --step RAW2DIGI,L1Reco,RECO,RECOSIM --geometry DB:Extended --filein file:EGM-RunIISummer20UL18HLT-00002.root --era Run2_2016 --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100',
      "KeepOutput": False,
    },
    {  # MINIAOD
      "release": "CMSSW_10_6_25", 
      "cmsDriver": 'cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18MiniAODv2-00004_1_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:EGM-RunIISummer20UL18MiniAODv2-00004.root --conditions 106X_mcRun2_asymptotic_v17 --step PAT --procModifiers run2_miniAOD_UL --geometry DB:Extended --filein "file:EGM-RunIISummer20UL18RECO-00002.root" --era Run2_2016 --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100',
      "KeepOutput": True,
    },
    { # NANOv12 with boostedTaus
      "release": "CMSSW_13_0_23", 
      # NANO -s NANO --mc --conditions auto:phase1_2018_realistic --era Run2_2018,run2_nanoAOD_106Xv2 --eventcontent NANOAODSIM --datatier NANOAODSIM --customise_commands=process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000 -n -1 --no_exec --filein /store/mc/RunIISummer20UL18MiniAODv2/GluGluToXToZZTo2B2Tau_M-5000_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2830000/0AF2F12C-C0C0-6647-94DF-FB7424298BC7.root
      "cmsDriver": 'cmsDriver.py --nThreads=5 --python_filename EGM-RunIISummer20UL18NanoAODv9-00005_1_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:EGM-RunIISummer20UL18NanoAODv9-00005.root --conditions auto:run2_mc --step NANO --filein "file:TOBEREPLACED" --era Run2_2016,run2_nanoAOD_106Xv2  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100',
      "KeepOutput": True,
    },
    # { # NANOv9
    #   "release": "CMSSW_10_6_27", # nanoaod twiki says CMSSW_10_6_27, DY prod used CMSSW_10_6_26 + changed NANOEDMAODSIM to NANOAODSIM
    #   "cmsDriver": 'cmsDriver.py --python_filename EGM-RunIISummer20UL18NanoAODv9-00005_1_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:EGM-RunIISummer20UL18NanoAODv9-00005.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --customise_commands "process.add_(cms.Service(\'InitRootHandlers\', EnableIMT = cms.untracked.bool(False))) \\n from PhysicsTools.NanoAOD.custom_jme_cff import PrepJMECustomNanoAOD_MC; PrepJMECustomNanoAOD_MC(process)" --step NANO --filein "dbs:/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" --era Run2_2018,run2_nanoAOD_106Xv2  --mc',
    #   "KeepOutput": True,
    # },
],
"ZZbbtt_16_HIPM_v1" : [ # ZZ->bbtautau from madgraph. Custom NanoV12 with boostedTaus
    { # LHE,GEN
      "release": "CMSSW_10_6_47", # latest 10_6_X release
      "cmsDriver": 'cmsDriver.py Configuration/GenProduction/python/ZZbbtt_fragment.py --nThreads=8 --python_filename B2G-RunIIFall18wmLHEGS-01094_1_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE --fileout file:EGM-RunIISummer20UL18wmLHEGEN-00001.root --conditions 106X_mcRun2_asymptotic_preVFP_v8 --beamspot Realistic25ns13TeV2016Collision --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(270)"\\;process.MessageLogger.cerr.FwkReport.reportEvery=100 --step LHE,GEN --geometry DB:Extended --era Run2_2016_HIPM --mc',
      "KeepOutput": False,
    },
    { # SIM,
      "release": "CMSSW_10_6_17_patch1",
      "cmsDriver": "cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18SIM-00002_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:EGM-RunIISummer20UL18SIM-00002.root --conditions 106X_mcRun2_asymptotic_preVFP_v8 --beamspot Realistic25ns13TeV2016Collision --step SIM --geometry DB:Extended --filein file:EGM-RunIISummer20UL18wmLHEGEN-00001.root --era Run2_2016_HIPM --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100",
      "KeepOutput": False,
    },
    { # DIGI,DATAMIX,L1,DIGI2RAW
      "release": "CMSSW_10_6_17_patch1",
      # --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL16_106X_mcRun2_asymptotic_v13-v1/PREMIX"
      # supposed to be partially available at CCIN2P3 but seems buggy. Available at T2 CERN 
      "cmsDriver": 'cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18DIGIPremix-00002_1_cfg.py --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL16_106X_mcRun2_asymptotic_v13-v1/PREMIX" --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-DIGI --fileout file:EGM-RunIISummer20UL18DIGIPremix-00002.root  --conditions 106X_mcRun2_asymptotic_preVFP_v8 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --geometry DB:Extended --filein file:EGM-RunIISummer20UL18SIM-00002.root --datamix PreMix --era Run2_2016_HIPM --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100',
      "KeepOutput": False,
    },
    { # HLT
      "release": "CMSSW_8_0_36_UL_patch2", # release depends on year !
      "cmsDriver": 'cmsDriver.py --nThreads=8  --python_filename EGM-RunIISummer20UL18HLT-00002_1_cfg.py --eventcontent RAWSIM --outputCommand "keep *_mix_*_*,keep *_genPUProtons_*_*"  --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:EGM-RunIISummer20UL18HLT-00002.root  --inputCommands "keep *","drop *_*_BMTF_*","drop *PixelFEDChannel*_*_*_*" --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --customise_commands \'process.source.bypassVersionCheck = cms.untracked.bool(True); process.MessageLogger.cerr.FwkReport.reportEvery=100\' --step HLT:25ns15e33_v4 --geometry DB:Extended --filein file:EGM-RunIISummer20UL18DIGIPremix-00002.root --era Run2_2016 --mc',
      "KeepOutput": False,
    },
    { # RECO
      "release": "CMSSW_10_6_17_patch1",
      "cmsDriver": 'cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18RECO-00002_1_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:EGM-RunIISummer20UL18RECO-00002.root --conditions 106X_mcRun2_asymptotic_preVFP_v8 --step RAW2DIGI,L1Reco,RECO,RECOSIM --geometry DB:Extended --filein file:EGM-RunIISummer20UL18HLT-00002.root --era Run2_2016_HIPM --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100',
      "KeepOutput": False,
    },
    {  # MINIAOD
      "release": "CMSSW_10_6_25", 
      "cmsDriver": 'cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18MiniAODv2-00004_1_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:EGM-RunIISummer20UL18MiniAODv2-00004.root --conditions 106X_mcRun2_asymptotic_preVFP_v11 --step PAT --procModifiers run2_miniAOD_UL --geometry DB:Extended --filein "file:EGM-RunIISummer20UL18RECO-00002.root" --era Run2_2016_HIPM --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100',
      "KeepOutput": True,
    },
    { # NANOv12 with boostedTaus
      "release": "CMSSW_13_0_23", 
      # NANO -s NANO --mc --conditions auto:phase1_2018_realistic --era Run2_2018,run2_nanoAOD_106Xv2 --eventcontent NANOAODSIM --datatier NANOAODSIM --customise_commands=process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000 -n -1 --no_exec --filein /store/mc/RunIISummer20UL18MiniAODv2/GluGluToXToZZTo2B2Tau_M-5000_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2830000/0AF2F12C-C0C0-6647-94DF-FB7424298BC7.root
      "cmsDriver": 'cmsDriver.py --nThreads=5 --python_filename EGM-RunIISummer20UL18NanoAODv9-00005_1_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:EGM-RunIISummer20UL18NanoAODv9-00005.root --conditions auto:run2_mc_pre_vfp --step NANO --filein "file:TOBEREPLACED" --era Run2_2016_HIPM,run2_nanoAOD_106Xv2  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100',
      "KeepOutput": True,
    },
],
}
# runs LHE filter after shower : quite slow
multi_conf_dict["ZZbbtt_v1_LHEFilter"] = copy.deepcopy(multi_conf_dict["ZZbbtt_v1"])
multi_conf_dict["ZZbbtt_v1_LHEFilter"][0]["cmsDriver"] = multi_conf_dict["ZZbbtt_v1_LHEFilter"][0]["cmsDriver"].replace("ZZbbtt_fragment.py", "ZZbbtt_fragment_LHEFilter.py")
assert ("ZZbbtt_fragment_LHEFilter.py" in multi_conf_dict["ZZbbtt_v1_LHEFilter"][0]["cmsDriver"])

# better version
multi_conf_dict["ZZbbtt_v1_LHEFilter_before_shower"] = copy.deepcopy(multi_conf_dict["ZZbbtt_v1"])
multi_conf_dict["ZZbbtt_v1_LHEFilter_before_shower"][0]["cmsDriver"] = multi_conf_dict["ZZbbtt_v1_LHEFilter_before_shower"][0]["cmsDriver"].replace("ZZbbtt_fragment.py", "ZZbbtt_fragment_LHEFilter_before_shower.py")
multi_conf_dict["ZZbbtt_v1_LHEFilter_before_shower"][0]["allowFailure"] = True # CMSSW retruns exception in this case but actually works

for year in ["17", "16_HIPM", "16"]:
  multi_conf_dict[f"ZZbbtt_{year}_v1_LHEFilter_before_shower"] = copy.deepcopy(multi_conf_dict[f"ZZbbtt_{year}_v1"])
  multi_conf_dict[f"ZZbbtt_{year}_v1_LHEFilter_before_shower"][0]["cmsDriver"] = multi_conf_dict[f"ZZbbtt_{year}_v1_LHEFilter_before_shower"][0]["cmsDriver"].replace("ZZbbtt_fragment.py", "ZZbbtt_fragment_LHEFilter_before_shower.py")
  multi_conf_dict[f"ZZbbtt_{year}_v1_LHEFilter_before_shower"][0]["allowFailure"] = True # CMSSW retruns exception in this case but actually works


multi_conf_dict["ZttHbb_v1"] = copy.deepcopy(multi_conf_dict["ZZbbtt_v1"])
multi_conf_dict["ZttHbb_v1"][0]["cmsDriver"] = multi_conf_dict["ZttHbb_v1"][0]["cmsDriver"].replace("ZZbbtt_fragment.py", "ZttHbb_fragment.py")
multi_conf_dict[f"ZttHbb_v1"][0]["allowFailure"] = True # CMSSW retruns exception in this case but actually works
assert ("ZttHbb_fragment.py" in multi_conf_dict["ZttHbb_v1"][0]["cmsDriver"])
for year in ["17", "16_HIPM", "16"]:
  multi_conf_dict[f"ZttHbb_{year}_v1"] = copy.deepcopy(multi_conf_dict[f"ZZbbtt_{year}_v1"])
  multi_conf_dict[f"ZttHbb_{year}_v1"][0]["cmsDriver"] = multi_conf_dict[f"ZttHbb_{year}_v1"][0]["cmsDriver"].replace("ZZbbtt_fragment.py", "ZttHbb_fragment.py")
  multi_conf_dict[f"ZttHbb_{year}_v1"][0]["allowFailure"] = True # CMSSW retruns exception in this case but actually works

multi_conf_dict["ZttHbb_VpTGt200_v1"] = copy.deepcopy(multi_conf_dict["ZZbbtt_v1"])
multi_conf_dict["ZttHbb_VpTGt200_v1"][0]["cmsDriver"] = multi_conf_dict["ZttHbb_VpTGt200_v1"][0]["cmsDriver"].replace("ZZbbtt_fragment.py", "ZttHbb_fragment_VpTGt200.py")
multi_conf_dict[f"ZttHbb_VpTGt200_v1"][0]["allowFailure"] = True # CMSSW retruns exception in this case but actually works
assert ("ZttHbb_fragment_VpTGt200.py" in multi_conf_dict["ZttHbb_VpTGt200_v1"][0]["cmsDriver"])
for year in ["17", "16_HIPM", "16"]:
  multi_conf_dict[f"ZttHbb_VpTGt200_{year}_v1"] = copy.deepcopy(multi_conf_dict[f"ZZbbtt_{year}_v1"])
  multi_conf_dict[f"ZttHbb_VpTGt200_{year}_v1"][0]["cmsDriver"] = multi_conf_dict[f"ZttHbb_VpTGt200_{year}_v1"][0]["cmsDriver"].replace("ZZbbtt_fragment.py", "ZttHbb_fragment_VpTGt200.py")
  multi_conf_dict[f"ZttHbb_VpTGt200_{year}_v1"][0]["allowFailure"] = True # CMSSW retruns exception in this case but actually works

# ZttHbb with LHE&MCFilters
multi_conf_dict["ZttHbb_18_v2"] = copy.deepcopy(multi_conf_dict["ZttHbb_v1"])
del multi_conf_dict["ZttHbb_18_v2"][0]["cmsDriver"]
multi_conf_dict["ZttHbb_18_v2"][0]["cfg"] = "LHEGEN_ZttHbb_tauGenJetsFilter_18.py"

multi_conf_dict["ZttHbb_17_v2"] = copy.deepcopy(multi_conf_dict["ZttHbb_17_v1"])
del multi_conf_dict["ZttHbb_17_v2"][0]["cmsDriver"]
multi_conf_dict["ZttHbb_17_v2"][0]["cfg"] = "LHEGEN_ZttHbb_tauGenJetsFilter_17.py"

multi_conf_dict["ZttHbb_16_v2"] = copy.deepcopy(multi_conf_dict["ZttHbb_16_v1"])
del multi_conf_dict["ZttHbb_16_v2"][0]["cmsDriver"]
multi_conf_dict["ZttHbb_16_v2"][0]["cfg"] = "LHEGEN_ZttHbb_tauGenJetsFilter_16.py"

multi_conf_dict["ZttHbb_16_HIPM_v2"] = copy.deepcopy(multi_conf_dict["ZttHbb_v1"])
del multi_conf_dict["ZttHbb_16_HIPM_v2"][0]["cmsDriver"]
multi_conf_dict["ZttHbb_16_HIPM_v2"][0]["cfg"] = "LHEGEN_ZttHbb_tauGenJetsFilter_16_HIPM.py"


multi_conf_dict["ZbbHtt_v1"] = copy.deepcopy(multi_conf_dict["ZZbbtt_v1"])
multi_conf_dict["ZbbHtt_v1"][0]["cmsDriver"] = multi_conf_dict["ZbbHtt_v1"][0]["cmsDriver"].replace("ZZbbtt_fragment.py", "ZbbHtt_fragment.py")
multi_conf_dict["ZbbHtt_v1"][0]["allowFailure"] = True # CMSSW retruns exception in this case but actually works
assert ("ZbbHtt_fragment.py" in multi_conf_dict["ZbbHtt_v1"][0]["cmsDriver"])
for year in ["17", "16_HIPM", "16"]:
  multi_conf_dict[f"ZbbHtt_{year}_v1"] = copy.deepcopy(multi_conf_dict[f"ZZbbtt_{year}_v1"])
  multi_conf_dict[f"ZbbHtt_{year}_v1"][0]["cmsDriver"] = multi_conf_dict[f"ZbbHtt_{year}_v1"][0]["cmsDriver"].replace("ZZbbtt_fragment.py", "ZbbHtt_fragment.py")
  multi_conf_dict[f"ZbbHtt_{year}_v1"][0]["allowFailure"] = True # CMSSW retruns exception in this case but actually works

multi_conf_dict["ZbbHtt_VpTGt200_v1"] = copy.deepcopy(multi_conf_dict["ZZbbtt_v1"])
multi_conf_dict["ZbbHtt_VpTGt200_v1"][0]["cmsDriver"] = multi_conf_dict["ZbbHtt_VpTGt200_v1"][0]["cmsDriver"].replace("ZZbbtt_fragment.py", "ZbbHtt_fragment_VpTGt200.py")
multi_conf_dict["ZbbHtt_VpTGt200_v1"][0]["allowFailure"] = True # CMSSW retruns exception in this case but actually works
assert ("ZbbHtt_fragment_VpTGt200.py" in multi_conf_dict["ZbbHtt_VpTGt200_v1"][0]["cmsDriver"])
for year in ["17", "16_HIPM", "16"]:
  multi_conf_dict[f"ZbbHtt_VpTGt200_{year}_v1"] = copy.deepcopy(multi_conf_dict[f"ZZbbtt_{year}_v1"])
  multi_conf_dict[f"ZbbHtt_VpTGt200_{year}_v1"][0]["cmsDriver"] = multi_conf_dict[f"ZbbHtt_VpTGt200_{year}_v1"][0]["cmsDriver"].replace("ZZbbtt_fragment.py", "ZbbHtt_fragment_VpTGt200.py")
  multi_conf_dict[f"ZbbHtt_VpTGt200_{year}_v1"][0]["allowFailure"] = True # CMSSW retruns exception in this case but actually works


# ZttHbb with LHE&MCFilters
multi_conf_dict["ZbbHtt_18_v2"] = copy.deepcopy(multi_conf_dict["ZbbHtt_v1"])
del multi_conf_dict["ZbbHtt_18_v2"][0]["cmsDriver"]
multi_conf_dict["ZbbHtt_18_v2"][0]["cfg"] = "LHEGEN_ZbbHtt_tauGenJetsFilter_18.py"

# X -> YY -> bbtautau Run-2 UL18 production.  Reuse the detector-simulation
# chain validated for ZZ -> bbtautau, changing only the LHE/GEN fragment.
multi_conf_dict["XToYYTo2B2Tau_18_v1"] = copy.deepcopy(multi_conf_dict["ZZbbtt_v1"])
multi_conf_dict["XToYYTo2B2Tau_18_v1"][0]["cmsDriver"] = (
    multi_conf_dict["XToYYTo2B2Tau_18_v1"][0]["cmsDriver"].replace(
        "ZZbbtt_fragment.py",
        "XToYYTo2B2Tau_MX1000_MY200_13TeV_Run2UL18_cfi.py",
    )
)
assert "XToYYTo2B2Tau_MX1000_MY200_13TeV_Run2UL18_cfi.py" in (
    multi_conf_dict["XToYYTo2B2Tau_18_v1"][0]["cmsDriver"]
)

multi_conf_dict["ZbbHtt_17_v2"] = copy.deepcopy(multi_conf_dict["ZbbHtt_17_v1"])
del multi_conf_dict["ZbbHtt_17_v2"][0]["cmsDriver"]
multi_conf_dict["ZbbHtt_17_v2"][0]["cfg"] = "LHEGEN_ZbbHtt_tauGenJetsFilter_17.py"

multi_conf_dict["ZbbHtt_16_v2"] = copy.deepcopy(multi_conf_dict["ZbbHtt_16_v1"])
del multi_conf_dict["ZbbHtt_16_v2"][0]["cmsDriver"]
multi_conf_dict["ZbbHtt_16_v2"][0]["cfg"] = "LHEGEN_ZbbHtt_tauGenJetsFilter_16.py"

multi_conf_dict["ZbbHtt_16_HIPM_v2"] = copy.deepcopy(multi_conf_dict["ZbbHtt_16_HIPM_v1"])
del multi_conf_dict["ZbbHtt_16_HIPM_v2"][0]["cmsDriver"]
multi_conf_dict["ZbbHtt_16_HIPM_v2"][0]["cfg"] = "LHEGEN_ZbbHtt_tauGenJetsFilter_16_HIPM.py"

additional_cmsDriver_commands = "" # --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100

def findCmsswRelease(releaseName:str) -> str:
    """ Finds CMSSW release location (created with cmsrel). Returns path to src folder, ie  /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_2_22/src/ """
    bases = [#"/grid_mnt/data__data.polcms/cms/vernazza/MCProduction/2023_11_14",
             "/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases",
             "/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd"]
    for base in bases:
        pathToSrc = os.path.join(base, releaseName, "src")
        if os.path.isdir(pathToSrc):
            return pathToSrc
    raise RuntimeError("Could not find CMSSW release version " + releaseName)

# Script to submit MC production

if __name__ == "__main__" :

    parser = OptionParser()    
    parser.add_option("--base",      dest="base",      type=str,            default=None,                            help="Base output folder name")
    parser.add_option("--grid",      dest="grid",      type=str,            default=None,                            help="Gridpack location for step 0")
    parser.add_option("--process",   dest="process",   type=str,            default=None,                            help="Name of process ["+', '.join(multi_conf_dict.keys())+"]")
    parser.add_option("--maxEvents", dest="maxEvents", type=int,            default=50,                              help="Number of events per job")
    parser.add_option("--nThreads",  dest="nThreads", type=int,            default=8,                              help="Number of threads (default:8) can only be 1 or 8 on LLR T3")
    parser.add_option("--nJobs",     dest="nJobs",     type=int,            default=1,                               help="Number of jobs")
    parser.add_option("--start_from",dest="start_from",type=int,            default=0,                               help="Start random seed from")
    parser.add_option("--queue",     dest="queue",     type=str,            default='reserv',                        help="long or short queue")
    parser.add_option("--deterministic_seed",  dest="deterministic_seed",  action='store_true', default=False, help="Don't randomize start seed, rather use deterministic according to job number")
    parser.add_option("--no_exec",   dest="no_exec",   action='store_true', default=False)
    parser.add_option("--resubmit",  dest="resubmit",  action='store_true', default=False)
    parser.add_option("--max-materialize", type=int, default=0, help="Set max_materialize in condor sub file (sets max nb of concurrent jobs)")
    (options, args) = parser.parse_args()

    try:
        conf_dict = multi_conf_dict[options.process]
    except KeyError as e:
        print("Invalid process specified (" + str(e) + ")", file=sys.stderr)
        print("Possible options : " + ', '.join(multi_conf_dict.keys()))
        sys.exit(-5)
    
    outdir = options.base
    print(" ### INFO: Saving output in", outdir)
    os.system('mkdir -p '+outdir)

    if options.grid == None:
        print(" ### WARNING: not specified gridpack location. Gridpack should be hardcoded in frgament")
    else:
        print(" ### INFO: Gridpack location is", options.grid)

    if options.max_materialize>0:
        max_materialize = "max_materialize = " + str(options.max_materialize)
    else: max_materialize = ""

    transfer_input_files = []

    starting_index = int(options.start_from)
    ending_index = starting_index + int(options.nJobs)
    print(" ### INFO: Index range", starting_index, ending_index)
    os.system('mkdir -p '+outdir+'/jobs')

    status = {i: -1 for i in range(starting_index, ending_index)}

    for idx in range(starting_index, ending_index):
        
        resubmit = False

        os.system('mkdir -p '+outdir+'/jobs/' + str(idx))
        outJobName  = outdir + '/jobs/' + str(idx) + '/job_' + str(idx) + '.sh'
        # if options.resubmit: outJobName = outdir + '/jobs/' + str(idx) + '/job_' + str(idx) + '_re.sh'

        # random seed for MC production should every time we submit a new generation
        # it's obtained by summing current Y+M+D+H+M+S+job_number
        # now = datetime.now()
        # randseed = int(now.year) + int(now.month) + int(now.day) + int(now.hour) + int(now.minute) + int(now.second) + idx
        randseed = idx*10+1 # to be reproducible (plus we multiply by more than nb of threads)

        cmsRuns = []

        for step in range(len(conf_dict)):
            
            cur_dir = outdir + '/Step_' + str(step)
            os.system('mkdir -p '+cur_dir)
            outFileName = 'Step_' + str(step) + '_Ntuple_' + str(idx) + '.root' # filename in case of keeping the output on worker node
            outRootName = cur_dir + '/Ntuple_' + str(idx) + '.root'
            if step > 0:
                prev_dir = outdir + '/Step_' + str(step-1)
                inFileName = 'Step_' + str(step-1) +'_Ntuple_' + str(idx) + '.root' # filename in case input was kept on worker node
                inRootName = prev_dir + '/' + 'Ntuple_' + str(idx) + '.root'
            outLogName  = outdir + '/jobs/' + str(idx) + '/log_' + str(step) + '_' + str(idx) + '.txt'

            if options.resubmit:
                if not resubmit:
                  if os.path.isfile(outLogName):
                      if len(os.popen('tail '+outLogName+' | grep dropped').read()) > 0:
                          status[idx] = step
                          continue
                      elif len(os.popen('grep "Fatal" '+outLogName).read()) > 0 or len(os.popen('grep "fatal" '+outLogName).read()) > 0:
                          resubmit = True
                          if not "Error" in str(status[idx]):
                            status[idx] = "Error Step%s" %(str(step))
                  else:
                      continue # not started yet

            cfg = conf_dict[step].get('cfg', None)
            cmsDriverCommand = conf_dict[step].get('cmsDriver', None)
            assert (cfg is None) ^ (cmsDriverCommand is None), "In config, either cfg or cmsDriver must be set (not both)"
            release = conf_dict[step]['release']
            keep_previousStep = True if int(step) == 0 else conf_dict[int(step-1)]['KeepOutput']
            keep_currentStep = conf_dict[int(step)]['KeepOutput']

            scriptRun = 'cd "' + findCmsswRelease(release) + '"\n'
            scriptRun += 'cmsenv\n'
            scriptRun += 'eval `scram r -sh`\n'
            #scriptRun += 'cd %s\n' %(outdir + '/jobs/' + str(idx))
            scriptRun += 'cd -\n' # go back to job directory on node
            if cfg is not None: # cmsRun mode
              assert step == 0
              # new mode without VarParsing
              if not cfg in transfer_input_files:
                 transfer_input_files.append(cfg)
              
              scriptRun += f"echo '\nprocess.RAWSIMoutput.fileName = \"file:{(outRootName if keep_currentStep else outFileName)}\"' >> {os.path.basename(cfg)}\n"
              #scriptRun += f"echo '\nprocess.LHEoutput.fileName = \"file:{(outRootName if keep_currentStep else outFileName)}\"' >> {os.path.basename(cfg)}\n"
              if step == 0:
                scriptRun += f"echo 'process.externalLHEProducer.nEvents = cms.untracked.uint32({options.maxEvents})' >> {os.path.basename(cfg)}\n"
              # mode with VarParsing :
              #scriptRun += "cmsRun " + os.getcwd() + "/" + cfg + " outputFile=file:"+ (outRootName if keep_currentStep else outFileName) + \
              #    " maxEvents="+str(options.maxEvents)+" randseed="+str(randseed)
              #if step == 0: scriptRun = scriptRun+" inputFiles="+options.grid
              #if int(step) > 0: 
              #    scriptRun = scriptRun+" inputFiles=file:"+ (inRootName if keep_previousStep else inFileName)

              if conf_dict[step].get("allowFailure", False):
                  scriptRun += "set +e\n"
              scriptRun += f"cmsRun -n {options.nThreads} {os.path.basename(cfg)} >& "+outLogName + '\n'
              if conf_dict[step].get("allowFailure", False):
                scriptRun += "set -e\n"
              

            else: # cmsDriver mode
                scriptRun += cmsDriverCommand + f" --no_exec --python_filename Step_{step}_cfg.py -n {str(options.maxEvents)} --nThreads={options.nThreads} {additional_cmsDriver_commands}"
                if int(step) > 0:
                  scriptRun += f"--filein 'file:{(inRootName if keep_previousStep else inFileName)}' "
                scriptRun += f"--fileout 'file:{(outRootName if keep_currentStep else outFileName)}' "
                
                scriptRun += "\n"
                if options.deterministic_seed:
                  scriptRun += f"echo '\nprocess.RandomNumberGeneratorService.generator.initialSeed = {str(randseed)}' >> Step_{step}_cfg.py\n"
                  if step == 0:
                    scriptRun += f"echo 'process.RandomNumberGeneratorService.externalLHEProducer.initialSeed = {str(randseed)}' >> Step_{step}_cfg.py\n"
                else:
                  scriptRun += f"echo '\nfrom IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper\nrandSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)\nrandSvc.populate()\n' >> Step_{step}_cfg.py\n"
                
                if step == 0:
                  if options.grid is not None:
                    scriptRun += f"echo 'process.externalLHEProducer.args = cms.vstring(\"{options.grid}\")' >> Step_{step}_cfg.py\n"
                  scriptRun += f"echo 'process.externalLHEProducer.nEvents = cms.untracked.uint32({options.maxEvents})' >> Step_{step}_cfg.py\n"
                if conf_dict[step].get("allowFailure", False):
                  scriptRun += "set +e\n"
                scriptRun += f"cmsRun Step_{step}_cfg.py  >&{outLogName}\n"
                if conf_dict[step].get("allowFailure", False):
                  scriptRun += "set -e\n"

            
            if int(step) > 0 and not keep_previousStep:
                scriptRun += "rm "+inFileName + '\n'
                if int(step) == 1: # remove LHE file as well (otherwise it gets shipped back at the end of the job)
                    scriptRun += f"set +e; rm Step_0_Ntuple_{str(idx)}_inLHE.root; set -e;\n"
            cmsRuns.append(scriptRun)

        if not options.resubmit:
            skimjob = open (outJobName, 'w')
            skimjob.write ('#!/bin/bash\n')
            skimjob.write ('set -e\n') # abort script at first error
            skimjob.write ('export X509_USER_PROXY=' + os.path.expanduser('~/.t3/proxy.cert') + '\n')
            skimjob.write ('source /cvmfs/cms.cern.ch/cmsset_default.sh\n')
            for cmsRun in cmsRuns:
                skimjob.write(cmsRun)
            skimjob.close ()

            os.system ('chmod u+rwx ' + outJobName)
        
        if options.resubmit:
            if not resubmit: continue
            if not options.no_exec: os.system ('rm ' + outdir + '/jobs/' + str(idx) + '/log_*')

    submit_file_path = outdir + '/jobs.sub'
    with open(submit_file_path, "w") as submit_file:
        submit_file.write(f"""
executable = {outdir}/jobs/$(JobIdx)/job_$(JobIdx).sh
universe = vanilla
output = {outdir}/jobs/$(JobIdx)/job_$(JobIdx).o
error = {outdir}/jobs/$(JobIdx)/job_$(JobIdx).e
transfer_input_files = {','.join(transfer_input_files)}
transfer_output_files = ""
when_to_transfer_output = ON_EXIT_OR_EVICT
{max_materialize}
batch_name = {options.process}

request_memory = {'15G' if options.nThreads == 8 else '2.5G' if options.nThreads == 1 else (str(2.5*options.nThreads)+"G")} 
# can only be 1 or 8 on LLR T3
request_cpus = {options.nThreads}

# avoid VMs as they cause issues with TensorFlow
#requirements = regexp("llrgrwnvm[0-9]+.in2p3.fr", Machine) == FALSE
T3Queue = {options.queue}
WNTag = el9
+SingularityCmd = "/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/framework/el7_container"
include : /opt/exp_soft/cms/t3/t3queue |

queue JobIdx from seq {starting_index} {ending_index-1} |
""")
        

    # command = ('/home/llr/cms/evernazza/t3submit -'+options.queue+' \'' + outJobName +"\'")
    #command = ('/opt/exp_soft/cms/t3/t3submit -8c -'+options.queue+' \'' + outJobName +"\'")
    command = "condor_submit " + submit_file_path
    if not options.no_exec: os.system (command)


    if options.resubmit:
        done = [i for i in status.keys() if status[i] == 4]
        if len(done) == int(options.nJobs):
            print(" ### CONGRATULATION! EVERYTHING IS DONE! :)\n")
        else:
            error = [i for i in status.keys() if "Error" in str(status[i])]
            print(" ### JOBS RESUBMITTED: {}\n".format(error))
            running_0 = [i for i in status.keys() if status[i] == -1]
            running_1 = [i for i in status.keys() if status[i] == 0]
            running_2 = [i for i in status.keys() if status[i] == 1]
            running_3 = [i for i in status.keys() if status[i] == 2]
            running_4 = [i for i in status.keys() if status[i] == 3]
            print(" ### INFO: Running Step 0", running_0)
            print(" ### INFO: Running Step 1", running_1)
            print(" ### INFO: Running Step 2", running_2)
            print(" ### INFO: Running Step 3", running_3)
            print(" ### INFO: Running Step 4", running_4)
            print(" ### INFO: Done", done)

#!/usr/bin/env bash
set -euo pipefail

: "${_CONDOR_SCRATCH_DIR:?HTCondor scratch directory is unavailable}"
: "${CLUSTER_ID:?HTCondor cluster ID is unavailable}"
: "${PROC_ID:?HTCondor process ID is unavailable}"

campaign=/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/XToYYTo2B2Tau_fullsim_UL18_100evt
mini_local=Step_5_Ntuple_0.root
nano_local=Step_6_Ntuple_0.root
mini_final="$campaign/Step_5/Ntuple_0.root"
nano_final="$campaign/Step_6/Ntuple_0.root"

[[ ! -e $mini_final ]] || { echo "refusing to overwrite $mini_final" >&2; exit 73; }
[[ ! -e $nano_final ]] || { echo "refusing to overwrite $nano_final" >&2; exit 73; }

publish_output() {
  local source=$1
  local destination=$2
  local partial="${destination}.partial.${CLUSTER_ID}.${PROC_ID}"
  [[ -s $source ]] || { echo "missing local output: $source" >&2; exit 74; }
  cp -- "$source" "$partial"
  [[ -s $partial ]] || { echo "failed stage-out: $partial" >&2; exit 74; }
  ln -- "$partial" "$destination"
  rm -f -- "$partial"
}

export X509_USER_PROXY=/grid_mnt/vol_home/llr/cms/cuisset/.t3/proxy.cert
openssl x509 -in "$X509_USER_PROXY" -noout -checkend 3600
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd "$_CONDOR_SCRATCH_DIR"
(
cd "/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_6_47/src"
eval "$(scram runtime -sh)"
cd "$_CONDOR_SCRATCH_DIR"
cmsDriver.py Configuration/GenProduction/python/XToYYTo2B2Tau_MX1000_MY200_13TeV_Run2UL18_cfi.py --nThreads=8 --python_filename B2G-RunIIFall18wmLHEGS-01094_1_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE --fileout file:EGM-RunIISummer20UL18wmLHEGEN-00001.root --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(270)"\;process.MessageLogger.cerr.FwkReport.reportEvery=100 --step LHE,GEN --geometry DB:Extended --era Run2_2018 --mc --no_exec --python_filename Step_0_cfg.py -n 100 --nThreads=8 --fileout 'file:Step_0_Ntuple_0.root' 
echo '
from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper
randSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)
randSvc.populate()' >> Step_0_cfg.py
echo '
process.RandomNumberGeneratorService.generator.initialSeed = 1' >> Step_0_cfg.py
echo 'process.RandomNumberGeneratorService.externalLHEProducer.initialSeed = 2' >> Step_0_cfg.py
echo 'process.source.firstLuminosityBlock = cms.untracked.uint32(1)' >> Step_0_cfg.py
echo 'process.source.numberEventsInLuminosityBlock = cms.untracked.uint32(100)' >> Step_0_cfg.py
echo 'process.externalLHEProducer.args = cms.vstring("/grid_mnt/vol_home/llr/cms/cuisset/bbtautau/ZZbbtautau/MCGeneration/XToYYTo2B2Tau/genproductions_local/XToYYTo2B2Tau_MX1000_MY200_13TeV_Run2UL_slc7_amd64_gcc700_CMSSW_10_6_47_tarball.tar.xz")' >> Step_0_cfg.py
echo 'process.externalLHEProducer.nEvents = cms.untracked.uint32(100)' >> Step_0_cfg.py
cmsRun Step_0_cfg.py  >&/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/XToYYTo2B2Tau_fullsim_UL18_100evt/jobs/retry1/log_0_0.txt
)
(
cd "/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_6_17_patch1/src"
eval "$(scram runtime -sh)"
cd "$_CONDOR_SCRATCH_DIR"
cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18SIM-00002_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:EGM-RunIISummer20UL18SIM-00002.root --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step SIM --geometry DB:Extended --filein file:EGM-RunIISummer20UL18wmLHEGEN-00001.root --era Run2_2018 --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100 --no_exec --python_filename Step_1_cfg.py -n 100 --nThreads=8 --filein 'file:Step_0_Ntuple_0.root' --fileout 'file:Step_1_Ntuple_0.root' 
echo '
process.RandomNumberGeneratorService.generator.initialSeed = 1' >> Step_1_cfg.py
cmsRun Step_1_cfg.py  >&/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/XToYYTo2B2Tau_fullsim_UL18_100evt/jobs/retry1/log_1_0.txt
)
rm Step_0_Ntuple_0.root
set +e; rm Step_0_Ntuple_0_inLHE.root; set -e;
(
cd "/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_6_17_patch1/src"
eval "$(scram runtime -sh)"
cd "$_CONDOR_SCRATCH_DIR"
cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18DIGIPremix-00002_1_cfg.py --pileup_input filelist:/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1/PU_LLR.txt --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-DIGI --fileout file:EGM-RunIISummer20UL18DIGIPremix-00002.root  --conditions 106X_upgrade2018_realistic_v11_L1v1 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --geometry DB:Extended --filein file:EGM-RunIISummer20UL18SIM-00002.root --datamix PreMix --era Run2_2018 --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100 --no_exec --python_filename Step_2_cfg.py -n 100 --nThreads=8 --filein 'file:Step_1_Ntuple_0.root' --fileout 'file:Step_2_Ntuple_0.root' 
echo '
process.RandomNumberGeneratorService.generator.initialSeed = 1' >> Step_2_cfg.py
cmsRun Step_2_cfg.py  >&/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/XToYYTo2B2Tau_fullsim_UL18_100evt/jobs/retry1/log_2_0.txt
)
rm Step_1_Ntuple_0.root
(
cd "/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_2_16_UL/src"
eval "$(scram runtime -sh)"
cd "$_CONDOR_SCRATCH_DIR"
cmsDriver.py --nThreads=8  --python_filename EGM-RunIISummer20UL18HLT-00002_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:EGM-RunIISummer20UL18HLT-00002.root --conditions 102X_upgrade2018_realistic_v15 --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True); process.MessageLogger.cerr.FwkReport.reportEvery=100' --step HLT:2018v32 --geometry DB:Extended --filein file:EGM-RunIISummer20UL18DIGIPremix-00002.root --era Run2_2018 --mc --no_exec --python_filename Step_3_cfg.py -n 100 --nThreads=8 --filein 'file:Step_2_Ntuple_0.root' --fileout 'file:Step_3_Ntuple_0.root' 
echo '
process.RandomNumberGeneratorService.generator.initialSeed = 1' >> Step_3_cfg.py
cmsRun Step_3_cfg.py  >&/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/XToYYTo2B2Tau_fullsim_UL18_100evt/jobs/retry1/log_3_0.txt
)
rm Step_2_Ntuple_0.root
(
cd "/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_6_17_patch1/src"
eval "$(scram runtime -sh)"
cd "$_CONDOR_SCRATCH_DIR"
cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18RECO-00002_1_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:EGM-RunIISummer20UL18RECO-00002.root --conditions 106X_upgrade2018_realistic_v11_L1v1 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --geometry DB:Extended --filein file:EGM-RunIISummer20UL18HLT-00002.root --era Run2_2018 --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100 --no_exec --python_filename Step_4_cfg.py -n 100 --nThreads=8 --filein 'file:Step_3_Ntuple_0.root' --fileout 'file:Step_4_Ntuple_0.root' 
echo '
process.RandomNumberGeneratorService.generator.initialSeed = 1' >> Step_4_cfg.py
cmsRun Step_4_cfg.py  >&/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/XToYYTo2B2Tau_fullsim_UL18_100evt/jobs/retry1/log_4_0.txt
)
rm Step_3_Ntuple_0.root
(
cd "/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_6_20/src"
eval "$(scram runtime -sh)"
cd "$_CONDOR_SCRATCH_DIR"
cmsDriver.py --nThreads=8 --python_filename EGM-RunIISummer20UL18MiniAODv2-00004_1_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:EGM-RunIISummer20UL18MiniAODv2-00004.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step PAT --procModifiers run2_miniAOD_UL --geometry DB:Extended --filein "file:EGM-RunIISummer20UL18RECO-00002.root" --era Run2_2018 --runUnscheduled  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100 --no_exec --python_filename Step_5_cfg.py -n 100 --nThreads=8 --filein 'file:Step_4_Ntuple_0.root' --fileout "file:$mini_local" 
echo '
process.RandomNumberGeneratorService.generator.initialSeed = 1' >> Step_5_cfg.py
cmsRun Step_5_cfg.py  >&/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/XToYYTo2B2Tau_fullsim_UL18_100evt/jobs/retry1/log_5_0.txt
edmFileUtil -j "file:$mini_local" > "$campaign/jobs/retry1/edmFileUtil_MINIAOD.json"
)
rm Step_4_Ntuple_0.root
publish_output "$mini_local" "$mini_final"
echo "published $mini_final"
(
cd "/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/CMSSW_13_0_23/src"
eval "$(scram runtime -sh)"
cd "$_CONDOR_SCRATCH_DIR"
cmsDriver.py --nThreads=5 --python_filename EGM-RunIISummer20UL18NanoAODv9-00005_1_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:EGM-RunIISummer20UL18NanoAODv9-00005.root --conditions auto:phase1_2018_realistic --step NANO --filein "file:TOBEREPLACED" --era Run2_2018,run2_nanoAOD_106Xv2  --mc --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100 --no_exec --python_filename Step_6_cfg.py -n 100 --nThreads=8 --filein "file:$mini_local" --fileout "file:$nano_local" 
echo '
process.RandomNumberGeneratorService.generator.initialSeed = 1' >> Step_6_cfg.py
cmsRun Step_6_cfg.py  >&/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/XToYYTo2B2Tau_fullsim_UL18_100evt/jobs/retry1/log_6_0.txt
edmFileUtil -j "file:$nano_local" > "$campaign/jobs/retry1/edmFileUtil_NANOAOD.json"
)

publish_output "$nano_local" "$nano_final"
echo "published $nano_final"

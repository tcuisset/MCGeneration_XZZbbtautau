#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 6 ]]; then
  echo "usage: $0 POINT JOB_INDEX FIRST_LUMI SEED_BASE FRAGMENT GRIDPACK" >&2
  exit 64
fi

point=$1
job_index=$2
first_lumi=$3
seed_base=$4
fragment=$5
gridpack=$6

[[ $point =~ ^MX[0-9]+_MY[0-9]+$ ]] || { echo "invalid point: $point" >&2; exit 64; }
[[ $job_index =~ ^[0-9]+$ ]] || { echo "invalid job index: $job_index" >&2; exit 64; }
[[ $first_lumi =~ ^[1-9][0-9]*$ ]] || { echo "invalid first lumi: $first_lumi" >&2; exit 64; }
[[ $seed_base =~ ^[1-9][0-9]*$ ]] || { echo "invalid seed base: $seed_base" >&2; exit 64; }
: "${_CONDOR_SCRATCH_DIR:?HTCondor scratch directory is unavailable}"
: "${CLUSTER_ID:?HTCondor cluster ID is unavailable}"
: "${PROC_ID:?HTCondor process ID is unavailable}"

events=100
threads=8
# The custom DeepTau inference used in this CMSSW_13_0_23 overlay is run with
# one stream.  Full simulation remains eight-threaded; this avoids sporadic
# non-finite TensorFlow predictions observed in the MX600_MY200 pilot.
nano_threads=1
campaign=/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/XToYYTo2B2Tau_fullsim_UL18_10k
point_dir="$campaign/$point"
log_dir="$point_dir/jobs/$job_index"
mini_local="Step_5_Ntuple_${job_index}.root"
nano_local="Step_6_Ntuple_${job_index}.root"
mini_final="$point_dir/Step_5/Ntuple_${job_index}.root"
nano_final="$point_dir/Step_6/Ntuple_${job_index}.root"

[[ -d $log_dir && -d $point_dir/Step_5 && -d $point_dir/Step_6 ]] || {
  echo "campaign directories were not pre-created for $point job $job_index" >&2
  exit 72
}
[[ -s $gridpack ]] || { echo "missing gridpack: $gridpack" >&2; exit 74; }
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

append_rng_configuration() {
  local cfg=$1
  local step=$2
  local step_seed_base=$((seed_base + step * 1000))
  {
    printf '\nfrom IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper\n'
    printf '_rng_helper = RandomNumberServiceHelper(process.RandomNumberGeneratorService)\n'
    printf '_rng_helper.populate()\n'
    printf '_rng_base = %d\n' "$step_seed_base"
    printf 'for _rng_offset, _rng_name in enumerate(sorted(process.RandomNumberGeneratorService.parameterNames_())):\n'
    printf '    _rng_pset = getattr(process.RandomNumberGeneratorService, _rng_name)\n'
    printf '    if hasattr(_rng_pset, "initialSeed"):\n'
    printf '        _rng_pset.initialSeed.setValue(_rng_base + _rng_offset + 1)\n'
  } >> "$cfg"
}

export X509_USER_PROXY=/grid_mnt/vol_home/llr/cms/cuisset/.t3/proxy.cert
openssl x509 -in "$X509_USER_PROXY" -noout -checkend 21600
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd "$_CONDOR_SCRATCH_DIR"

if [[ -s $mini_final ]]; then
  echo "resuming from validated MiniAOD $mini_final"
  cp -- "$mini_final" "$mini_local"
else
  (
    cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_6_47/src
    eval "$(scram runtime -sh)"
    cd "$_CONDOR_SCRATCH_DIR"
    cmsDriver.py "Configuration/GenProduction/python/$fragment" \
      --eventcontent RAWSIM,LHE \
      --customise Configuration/DataProcessing/Utils.addMonitoring \
      --datatier GEN,LHE \
      --conditions 106X_upgrade2018_realistic_v4 \
      --beamspot Realistic25ns13TeVEarly2018Collision \
      --step LHE,GEN \
      --geometry DB:Extended \
      --era Run2_2018 \
      --mc --no_exec --python_filename Step_0_cfg.py \
      -n "$events" --nThreads="$threads" \
      --fileout "file:Step_0_Ntuple_${job_index}.root"
    append_rng_configuration Step_0_cfg.py 0
    printf 'process.source.firstLuminosityBlock = cms.untracked.uint32(%d)\n' "$first_lumi" >> Step_0_cfg.py
    printf 'process.source.numberEventsInLuminosityBlock = cms.untracked.uint32(%d)\n' "$events" >> Step_0_cfg.py
    printf 'process.externalLHEProducer.args = cms.vstring("%s")\n' "$gridpack" >> Step_0_cfg.py
    printf 'process.externalLHEProducer.nEvents = cms.untracked.uint32(%d)\n' "$events" >> Step_0_cfg.py
    cmsRun Step_0_cfg.py >& "$log_dir/log_0_${job_index}.txt"
  )

  (
    cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_6_17_patch1/src
    eval "$(scram runtime -sh)"
    cd "$_CONDOR_SCRATCH_DIR"
    cmsDriver.py --eventcontent RAWSIM \
      --customise Configuration/DataProcessing/Utils.addMonitoring \
      --datatier GEN-SIM --conditions 106X_upgrade2018_realistic_v11_L1v1 \
      --beamspot Realistic25ns13TeVEarly2018Collision --step SIM \
      --geometry DB:Extended --era Run2_2018 --runUnscheduled --mc \
      --no_exec --python_filename Step_1_cfg.py -n "$events" --nThreads="$threads" \
      --filein "file:Step_0_Ntuple_${job_index}.root" \
      --fileout "file:Step_1_Ntuple_${job_index}.root"
    append_rng_configuration Step_1_cfg.py 1
    cmsRun Step_1_cfg.py >& "$log_dir/log_1_${job_index}.txt"
  )
  rm -f -- "Step_0_Ntuple_${job_index}.root" "Step_0_Ntuple_${job_index}_inLHE.root"

  (
    cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_6_17_patch1/src
    eval "$(scram runtime -sh)"
    cd "$_CONDOR_SCRATCH_DIR"
    cmsDriver.py --pileup_input filelist:/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1/PU_LLR.txt \
      --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring \
      --datatier GEN-SIM-DIGI --conditions 106X_upgrade2018_realistic_v11_L1v1 \
      --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 \
      --geometry DB:Extended --datamix PreMix --era Run2_2018 --runUnscheduled --mc \
      --no_exec --python_filename Step_2_cfg.py -n "$events" --nThreads="$threads" \
      --filein "file:Step_1_Ntuple_${job_index}.root" \
      --fileout "file:Step_2_Ntuple_${job_index}.root"
    append_rng_configuration Step_2_cfg.py 2
    cmsRun Step_2_cfg.py >& "$log_dir/log_2_${job_index}.txt"
  )
  rm -f -- "Step_1_Ntuple_${job_index}.root"

  (
    cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_2_16_UL/src
    eval "$(scram runtime -sh)"
    cd "$_CONDOR_SCRATCH_DIR"
    cmsDriver.py --eventcontent RAWSIM \
      --customise Configuration/DataProcessing/Utils.addMonitoring \
      --datatier GEN-SIM-RAW --conditions 102X_upgrade2018_realistic_v15 \
      --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' \
      --step HLT:2018v32 --geometry DB:Extended --era Run2_2018 --mc \
      --no_exec --python_filename Step_3_cfg.py -n "$events" --nThreads="$threads" \
      --filein "file:Step_2_Ntuple_${job_index}.root" \
      --fileout "file:Step_3_Ntuple_${job_index}.root"
    append_rng_configuration Step_3_cfg.py 3
    cmsRun Step_3_cfg.py >& "$log_dir/log_3_${job_index}.txt"
  )
  rm -f -- "Step_2_Ntuple_${job_index}.root"

  (
    cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_6_17_patch1/src
    eval "$(scram runtime -sh)"
    cd "$_CONDOR_SCRATCH_DIR"
    cmsDriver.py --eventcontent AODSIM \
      --customise Configuration/DataProcessing/Utils.addMonitoring \
      --datatier AODSIM --conditions 106X_upgrade2018_realistic_v11_L1v1 \
      --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --geometry DB:Extended \
      --era Run2_2018 --runUnscheduled --mc \
      --no_exec --python_filename Step_4_cfg.py -n "$events" --nThreads="$threads" \
      --filein "file:Step_3_Ntuple_${job_index}.root" \
      --fileout "file:Step_4_Ntuple_${job_index}.root"
    append_rng_configuration Step_4_cfg.py 4
    cmsRun Step_4_cfg.py >& "$log_dir/log_4_${job_index}.txt"
  )
  rm -f -- "Step_3_Ntuple_${job_index}.root"

  (
    cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_6_20/src
    eval "$(scram runtime -sh)"
    cd "$_CONDOR_SCRATCH_DIR"
    cmsDriver.py --eventcontent MINIAODSIM \
      --customise Configuration/DataProcessing/Utils.addMonitoring \
      --datatier MINIAODSIM --conditions 106X_upgrade2018_realistic_v16_L1v1 \
      --step PAT --procModifiers run2_miniAOD_UL --geometry DB:Extended \
      --era Run2_2018 --runUnscheduled --mc \
      --no_exec --python_filename Step_5_cfg.py -n "$events" --nThreads="$threads" \
      --filein "file:Step_4_Ntuple_${job_index}.root" \
      --fileout "file:$mini_local"
    append_rng_configuration Step_5_cfg.py 5
    cmsRun Step_5_cfg.py >& "$log_dir/log_5_${job_index}.txt"
    edmFileUtil -j "file:$mini_local" > "$log_dir/edmFileUtil_MINIAOD.json"
  )
  rm -f -- "Step_4_Ntuple_${job_index}.root"
  publish_output "$mini_local" "$mini_final"
  echo "published $mini_final"
fi

(
  python_base=/cvmfs/cms.cern.ch/slc7_amd64_gcc11/external/python3/3.9.14-76a14295dd5255228210eb596893b98c
  export PATH="$python_base/bin:$PATH"
  export LD_LIBRARY_PATH="$python_base/lib:${LD_LIBRARY_PATH:-}"
  export SCRAMRT_SET=1
  cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/CMSSW_13_0_23/src
  eval "$(scram runtime -sh)"
  cd "$_CONDOR_SCRATCH_DIR"
  cmsDriver.py --eventcontent NANOAODSIM \
    --customise Configuration/DataProcessing/Utils.addMonitoring \
    --datatier NANOAODSIM --conditions auto:phase1_2018_realistic \
    --step NANO --era Run2_2018,run2_nanoAOD_106Xv2 --mc \
    --no_exec --python_filename Step_6_cfg.py -n "$events" --nThreads="$nano_threads" \
    --filein "file:$mini_local" --fileout "file:$nano_local"
  append_rng_configuration Step_6_cfg.py 6
  cmsRun Step_6_cfg.py >& "$log_dir/log_6_${job_index}.${CLUSTER_ID}.${PROC_ID}.txt"
  edmFileUtil -j "file:$nano_local" > "$log_dir/edmFileUtil_NANOAOD.${CLUSTER_ID}.${PROC_ID}.json"
)
publish_output "$nano_local" "$nano_final"
echo "published $nano_final"

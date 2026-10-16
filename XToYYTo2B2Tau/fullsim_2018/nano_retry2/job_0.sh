#!/usr/bin/env bash
set -euo pipefail

: "${_CONDOR_SCRATCH_DIR:?HTCondor scratch directory is unavailable}"
: "${CLUSTER_ID:?HTCondor cluster ID is unavailable}"
: "${PROC_ID:?HTCondor process ID is unavailable}"

campaign=/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/XToYYTo2B2Tau_fullsim_UL18_100evt
mini_source="$campaign/Step_5/Ntuple_0.root"
mini_local=Step_5_Ntuple_0.root
nano_local=Step_6_Ntuple_0.root
nano_final="$campaign/Step_6/Ntuple_0.root"
log_dir="$campaign/jobs/nano_retry2"

[[ -s $mini_source ]] || { echo "missing validated MiniAOD: $mini_source" >&2; exit 74; }
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

python_base=/cvmfs/cms.cern.ch/slc7_amd64_gcc11/external/python3/3.9.14-76a14295dd5255228210eb596893b98c
export PATH="$python_base/bin:$PATH"
export LD_LIBRARY_PATH="$python_base/lib:${LD_LIBRARY_PATH:-}"
export SCRAMRT_SET=1
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/CMSSW_13_0_23/src
eval "$(scram runtime -sh)"

cd "$_CONDOR_SCRATCH_DIR"
cp -- "$mini_source" "$mini_local"
cmsDriver.py --python_filename EGM-RunIISummer20UL18NanoAODv9-00005_1_cfg.py \
  --eventcontent NANOAODSIM \
  --customise Configuration/DataProcessing/Utils.addMonitoring \
  --datatier NANOAODSIM \
  --conditions auto:phase1_2018_realistic \
  --step NANO \
  --era Run2_2018,run2_nanoAOD_106Xv2 \
  --mc \
  --customise_commands=process.MessageLogger.cerr.FwkReport.reportEvery=100 \
  --no_exec \
  -n 100 \
  --nThreads=8 \
  --filein "file:$mini_local" \
  --fileout "file:$nano_local"
echo '
process.RandomNumberGeneratorService.generator.initialSeed = 1' >> EGM-RunIISummer20UL18NanoAODv9-00005_1_cfg.py
cmsRun EGM-RunIISummer20UL18NanoAODv9-00005_1_cfg.py >& "$log_dir/log_6_0.txt"
edmFileUtil -j "file:$nano_local" > "$log_dir/edmFileUtil_NANOAOD.json"
publish_output "$nano_local" "$nano_final"
echo "published $nano_final"

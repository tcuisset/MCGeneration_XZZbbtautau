#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 MX<mass>_MY91" >&2
  exit 64
fi

point=$1
case "$point" in
  MX800_MY91|MX1500_MY91) ;;
  *) echo "unsupported mass point: $point" >&2; exit 64 ;;
esac

campaign=/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/XToYYTo2B2Tau_fullsim_UL18_10k_mZ
merged_base=/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/XToYYTo2B2Tau_fullsim_UL18_mergedNano
tool=/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py
cmssw=/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/CMSSW_13_0_23
input_dir="$campaign/$point/Step_6"
output_dir="$merged_base/$point"
work_dir=$(mktemp -d "/scratch/cuisset/tmp/XToYYTo2B2Tau_${point}_merge.XXXXXX")
report="$merged_base/report-${point}.json"

cleanup() {
  rm -rf -- "$work_dir"
}
trap cleanup EXIT

export X509_USER_PROXY=/grid_mnt/vol_home/llr/cms/cuisset/.t3/proxy.cert
openssl x509 -in "$X509_USER_PROXY" -noout -checkend 7200
source /cvmfs/cms.cern.ch/cmsset_default.sh
python_base=/cvmfs/cms.cern.ch/slc7_amd64_gcc11/external/python3/3.9.14-76a14295dd5255228210eb596893b98c
export PATH="$python_base/bin:$PATH"
export LD_LIBRARY_PATH="$python_base/lib:${LD_LIBRARY_PATH:-}"
export SCRAMRT_SET=1
cd "$cmssw/src"
eval "$(scram runtime -sh)"

mkdir -p "$output_dir"
python3 -u "$tool" \
  --output-dir "$output_dir" \
  --output-name "XToYYTo2B2Tau_${point}_NanoAOD.root" \
  --work-dir "$work_dir" \
  --target-size 800 \
  --remote-io \
  --n-retries 2 \
  --merge-report "$report" \
  "$input_dir"

echo "merge complete: $point"
echo "report: $report"

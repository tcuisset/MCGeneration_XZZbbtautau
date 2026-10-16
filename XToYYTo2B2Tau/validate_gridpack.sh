#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: $0 MX MY" >&2
  exit 64
fi
mx=$1
my=$2
expected_my=$my
if [[ $my == 91 ]]; then
  expected_my=91.1876
fi
point="MX${mx}_MY${my}"
base=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
gridpack="$base/genproductions_local/XToYYTo2B2Tau_${point}_13TeV_Run2UL_slc7_amd64_gcc700_CMSSW_10_6_47_tarball.tar.xz"
work=$(mktemp -d "/tmp/cuisset/x2y_${point}.XXXXXX")
trap 'rm -rf -- "$work"' EXIT

tar -C "$work" -xaf "$gridpack"
/cvmfs/cms.cern.ch/common/cmssw-el7 -B /grid_mnt/vol_home -B /grid_mnt/data__data.polcms --command-to-run \
  "cd $work && ./runcmsgrid.sh 8 ${mx}${my} 4"
python3 "$base/validate_lhe.py" "$work/cmsgrid_final.lhe" "$mx" "$expected_my"

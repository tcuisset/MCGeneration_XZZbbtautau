#!/bin/bash
set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
build_cores=${NB_CORE:-4}
mx=${1:-1000}
my=${2:-200}
sample=XToYYTo2B2Tau_MX${mx}_MY${my}_13TeV_Run2UL
container=/cvmfs/cms.cern.ch/common/cmssw-el7

if (( mx <= 2 * my )); then
  echo "invalid on-shell point: mX=$mx must be greater than 2*mY=$((2 * my))" >&2
  exit 2
fi

# Keep the build checkout's real cards directory synchronized with the
# authoritative cards kept next to this script.
for suffix in proc_card.dat customizecards.dat run_card.dat extramodels.dat; do
  cp "$script_dir/cards/${sample}_${suffix}" \
    "$script_dir/genproductions_local/cards/${sample}_${suffix}"
done

"$container" -B /data_CMS -B /grid_mnt/vol_home --command-to-run \
  "cd $script_dir/genproductions_local && unset PRODHOME && MG5_PYTHON=python2 NB_CORE=$build_cores ./gridpack_generation_localmodels.sh $sample cards local ALL slc7_amd64_gcc700 CMSSW_10_6_47"

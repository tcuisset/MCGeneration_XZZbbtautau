#!/usr/bin/env bash
set -euo pipefail

source /cvmfs/cms.cern.ch/cmsset_default.sh
python_base=/cvmfs/cms.cern.ch/slc7_amd64_gcc11/external/python3/3.9.14-76a14295dd5255228210eb596893b98c
export PATH="$python_base/bin:$PATH"
export LD_LIBRARY_PATH="$python_base/lib:${LD_LIBRARY_PATH:-}"
export SCRAMRT_SET=1
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/CMSSW_13_0_23/src
eval "$(scram runtime -sh)"

python3 /grid_mnt/vol_home/llr/cms/cuisset/bbtautau/ZZbbtautau/MCGeneration/XToYYTo2B2Tau/campaign_10k_lowMY/validate_merged.py

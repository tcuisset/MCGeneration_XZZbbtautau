#!/usr/bin/env bash
set -euo pipefail

bind_paths=()
for path in /etc/grid-security /etc/vomses /cvmfs /opt/exp_soft /data_CMS /data_CMS2 /data_CMS_upgrade /grid_mnt /scratch; do
  if [[ -e $path ]]; then
    bind_paths+=("$path")
  fi
done

export APPTAINER_BINDPATH
APPTAINER_BINDPATH=$(IFS=,; echo "${bind_paths[*]}")
exec apptainer -s exec /opt/exp_soft/vo.gridcl.fr/singularity/ui_el7.snb "$@"

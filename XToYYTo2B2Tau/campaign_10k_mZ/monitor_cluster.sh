#!/usr/bin/env bash
set -euo pipefail

cluster=${1:?cluster id required}
expected=${2:?expected job count required}
campaign=/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/XToYYTo2B2Tau_fullsim_UL18_10k_mZ
event_log="$campaign/cluster.${cluster}.log"

while true; do
  started=$(rg -c "^001 \(${cluster}\." "$event_log" || true)
  terminated=$(rg -c "^005 \(${cluster}\." "$event_log" || true)
  held=$(rg -c "^012 \(${cluster}\." "$event_log" || true)
  minis=$(find "$campaign" -path '*/Step_5/Ntuple_*.root' -type f | wc -l)
  nanos=$(find "$campaign" -path '*/Step_6/Ntuple_*.root' -type f | wc -l)
  partials=$(find "$campaign" -name '*.partial.*' -type f | wc -l)
  printf '%(%F %T)T starts=%s terminated=%s held=%s mini=%s nano=%s partial=%s\n' \
    -1 "${started:-0}" "${terminated:-0}" "${held:-0}" "$minis" "$nanos" "$partials"
  if (( ${terminated:-0} + ${held:-0} >= expected )); then
    break
  fi
  sleep 50
done

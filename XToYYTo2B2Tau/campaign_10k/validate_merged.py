#!/usr/bin/env python3
from pathlib import Path

import ROOT


campaign = Path(
    "/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/"
    "XToYYTo2B2Tau_fullsim_UL18_10k"
)
expected_events = {
    "MX600_MY200": 9900,
    "MX1000_MY200": 10000,
    "MX1500_MY400": 9700,
}

for point, expected in expected_events.items():
    path = campaign / "merged_NanoAOD" / point / f"XToYYTo2B2Tau_{point}_NanoAOD_0.root"
    root_file = ROOT.TFile.Open(str(path), "READ")
    if not root_file or root_file.IsZombie():
        raise RuntimeError(f"cannot open {path}")
    events = root_file.Get("Events")
    if not events:
        raise RuntimeError(f"Events tree is absent in {path}")
    entries = events.GetEntries()
    print(f"VALID {point} events={entries} bytes={path.stat().st_size}", flush=True)
    if entries != expected:
        raise RuntimeError(f"{point}: expected {expected} events, found {entries}")
    root_file.Close()

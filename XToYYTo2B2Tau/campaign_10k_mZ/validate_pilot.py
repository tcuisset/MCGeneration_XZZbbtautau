#!/usr/bin/env python3
from pathlib import Path

import ROOT


campaign = Path(
    "/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/"
    "XToYYTo2B2Tau_fullsim_UL18_10k_mZ"
)
points = {
    "MX800_MY91": (800.0, 91.1876, 20001),
    "MX1500_MY91": (1500.0, 91.1876, 21001),
}

all_event_ids = set()
for point, (expected_mx, expected_my, expected_lumi) in points.items():
    path = campaign / point / "Step_6" / "Ntuple_0.root"
    root_file = ROOT.TFile.Open(str(path), "READ")
    if not root_file or root_file.IsZombie():
        raise RuntimeError(f"cannot open {path}")
    events = root_file.Get("Events")
    if not events or events.GetEntries() != 100:
        raise RuntimeError(f"{point}: expected 100 NanoAOD events")

    point_ids = set()
    x_masses = []
    y_masses = []
    bad_resonance_counts = 0
    for event in events:
        event_id = (int(event.run), int(event.luminosityBlock), int(event.event))
        point_ids.add(event_id)
        last_x = []
        last_y = []
        for index in range(int(event.nGenPart)):
            pdg_id = int(event.GenPart_pdgId[index])
            is_last_copy = bool(int(event.GenPart_statusFlags[index]) & (1 << 13))
            if not is_last_copy:
                continue
            if pdg_id == 35:
                last_x.append(float(event.GenPart_mass[index]))
            elif pdg_id == 1023:
                last_y.append(float(event.GenPart_mass[index]))
        if len(last_x) != 1 or len(last_y) != 2:
            bad_resonance_counts += 1
        x_masses.extend(last_x)
        y_masses.extend(last_y)

    if len(point_ids) != 100:
        raise RuntimeError(f"{point}: duplicate event identity within pilot")
    if {event_id[0] for event_id in point_ids} != {1}:
        raise RuntimeError(f"{point}: unexpected run number")
    if {event_id[1] for event_id in point_ids} != {expected_lumi}:
        raise RuntimeError(f"{point}: unexpected luminosity block")
    if {event_id[2] for event_id in point_ids} != set(range(1, 101)):
        raise RuntimeError(f"{point}: unexpected event-number range")
    if all_event_ids.intersection(point_ids):
        raise RuntimeError(f"{point}: event identity overlaps another point")
    all_event_ids.update(point_ids)
    if bad_resonance_counts:
        raise RuntimeError(
            f"{point}: {bad_resonance_counts}/100 events have incorrect last-copy X/Y counts"
        )

    mean_x = sum(x_masses) / len(x_masses)
    mean_y = sum(y_masses) / len(y_masses)
    if abs(mean_x - expected_mx) > 0.01 * expected_mx:
        raise RuntimeError(f"{point}: mean mX {mean_x} is inconsistent")
    if abs(mean_y - expected_my) > 0.01 * expected_my:
        raise RuntimeError(f"{point}: mean mY {mean_y} is inconsistent")
    print(
        f"VALID {point} events=100 lumi={expected_lumi} "
        f"mean_mX={mean_x:.3f} mean_mY={mean_y:.3f} bytes={path.stat().st_size}",
        flush=True,
    )
    root_file.Close()

print(f"VALID combined unique event identities={len(all_event_ids)}", flush=True)

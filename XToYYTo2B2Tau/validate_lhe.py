#!/usr/bin/env python3
import math
import sys
from pathlib import Path


if len(sys.argv) != 4:
    raise SystemExit("usage: validate_lhe.py FILE MX MY")

path = Path(sys.argv[1])
expected_mx = float(sys.argv[2])
expected_my = float(sys.argv[3])
events = []
inside = False
particles = []
for raw_line in path.read_text().splitlines():
    line = raw_line.strip()
    if line == "<event>":
        inside = True
        particles = []
        continue
    if line == "</event>":
        events.append(particles)
        inside = False
        continue
    if not inside or not line or line.startswith("#"):
        continue
    fields = line.split()
    if len(fields) < 13:
        continue
    try:
        pdg_id = int(fields[0])
        status = int(fields[1])
        momentum = tuple(float(fields[index]) for index in range(6, 11))
    except ValueError:
        continue
    particles.append((pdg_id, status, momentum))

bad = 0
x_masses = []
y_masses = []
for particles in events:
    ids = [particle[0] for particle in particles]
    if ids.count(35) != 1 or ids.count(1023) != 2 or sum(abs(i) == 5 for i in ids) != 2 or sum(abs(i) == 15 for i in ids) != 2:
        bad += 1
    for pdg_id, _status, (_px, _py, _pz, _energy, mass) in particles:
        if pdg_id == 35:
            x_masses.append(mass)
        elif pdg_id == 1023:
            y_masses.append(mass)

if not events:
    raise RuntimeError(f"no events in {path}")
if bad:
    raise RuntimeError(f"{bad}/{len(events)} events fail the 1X+2Y+2b+2tau topology")
if len(x_masses) != len(events) or len(y_masses) != 2 * len(events):
    raise RuntimeError("resonance mass entries are incomplete")

mean_x = sum(x_masses) / len(x_masses)
mean_y = sum(y_masses) / len(y_masses)
if abs(mean_x - expected_mx) > max(1.0, 0.01 * expected_mx):
    raise RuntimeError(f"mean X mass {mean_x} is inconsistent with {expected_mx}")
if abs(mean_y - expected_my) > max(1.0, 0.01 * expected_my):
    raise RuntimeError(f"mean Y mass {mean_y} is inconsistent with {expected_my}")

print(
    f"events={len(events)} bad_topology={bad} "
    f"mean_mX={mean_x:.3f} mean_mY={mean_y:.3f}"
)

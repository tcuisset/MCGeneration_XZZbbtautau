#!/usr/bin/env python
from __future__ import print_function

import sys

import ROOT


input_path = sys.argv[1]
input_file = ROOT.TFile.Open(input_path)
if not input_file or input_file.IsZombie():
    raise RuntimeError("Could not open {0}".format(input_path))

events = input_file.Get("Events")
if not events:
    raise RuntimeError("The input has no Events tree")

bad_events = []
for entry, event in enumerate(events):
    pdg_ids = [int(value) for value in event.GenPart_pdgId]
    mothers = [int(value) for value in event.GenPart_genPartIdxMother]
    status_flags = [int(value) for value in event.GenPart_statusFlags]

    def mother_id(index):
        mother = mothers[index]
        return pdg_ids[mother] if mother >= 0 else 0

    topology = (
        # Pythia keeps several shower-history copies of the resonance.  NanoAOD
        # statusFlags bit 12 selects the unique first copy.
        sum(pdg_id == 35 and bool(status_flags[i] & (1 << 12))
            for i, pdg_id in enumerate(pdg_ids)),
        sum(pdg_id == 1023 and mother_id(i) == 35
            for i, pdg_id in enumerate(pdg_ids)),
        sum(abs(pdg_id) == 5 and mother_id(i) == 1023
            for i, pdg_id in enumerate(pdg_ids)),
        sum(abs(pdg_id) == 15 and mother_id(i) == 1023
            for i, pdg_id in enumerate(pdg_ids)),
    )
    if topology != (1, 2, 2, 2):
        bad_events.append((entry, topology))

print("events={0}".format(events.GetEntries()))
print("expected topology per event: X=1, Y_from_X=2, b_from_Y=2, tau_from_Y=2")
print("events failing topology check={0}".format(len(bad_events)))
for entry, topology in bad_events[:10]:
    print("entry={0} topology={1}".format(entry, topology))

input_file.Close()
sys.exit(1 if bad_events else 0)

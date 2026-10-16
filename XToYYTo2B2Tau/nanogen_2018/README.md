# Run-2 UL 2018 NanoGEN test

This directory contains a 20-event `LHE,GEN,NANOGEN` test for
`gg -> X(35) -> Y(1023)Y(1023) -> bbtautau` at `mX = 1000 GeV` and
`mY = 200 GeV`.

The configuration was generated with CMSSW `10_6_47` using:

- 13 TeV beams;
- `106X_upgrade2018_realistic_v4`;
- `Realistic25ns13TeVEarly2018Collision`;
- `DB:Extended` geometry and the `Run2_2018` era;
- Pythia8 CP5 and PS weights;
- Pythia8 `TauDecays:mode = 5` and `TauDecays:externalMode = 0`, requesting
  longitudinal tau polarization from the MadGraph LHE `SPINUP` entries;
- no POWHEG, MLM, or FxFx matching, because this is an LO zero-extra-parton
  matrix element.

Files:

- `XToYYTo2B2Tau_MX1000_MY200_Run2UL18_SPINUP_LHEGEN_NANOGEN_cfg.py`:
  generated `cmsDriver.py` configuration with the SPINUP settings;
- `XToYYTo2B2Tau_MX1000_MY200_Run2UL18_SPINUP_NANOGEN.root`: 20-event
  SPINUP test output;
- `cmsRun_XToYYTo2B2Tau_MX1000_MY200_Run2UL18_SPINUP.log`: full SPINUP job
  log;
- the corresponding files without `SPINUP` are retained as the original
  Pythia source-inference fallback test;
- `validate_nanogen.py`: checks the hard-process ancestry in the NanoGEN
  `GenPart` branches.

The MadGraph cross section is determined by the arbitrary small HAHM coupling
choices and is not the intended signal normalization. Analysis samples should
be normalized to the quoted `pp -> X -> YY -> bbtautau` cross section.

The MadGraph LHE output was independently audited with 100 events. All 200
physical tau entries had valid `SPINUP = +/-1`, and both helicity combinations
occurred. The settings are also printed as active by each Pythia instance.

Important limitation: Pythia 8.240 in CMSSW 10_6_47 still occasionally emits
`unknown uncorrelated tau production, assuming unpolarized` after showering,
even though the corresponding input LHE tau helicities are valid. A
single-thread 10-event control reproduced one fallback, and disabling lepton
QED showering did not remove it. Therefore this is a diagnostic implementation
of the requested method, not yet a production-approved fully polarized sample.
Before a large campaign, either resolve the Pythia 8.240 metadata-loss path or
validate a Tauola-based LHE-SPINUP afterburner. Also note that independent
longitudinal `SPINUP` values do not encode the full transverse two-tau spin
density matrix.

For this initial kinematic sample the gridpack contains the central Run-2
NNPDF3.1 set (`lhaid = 306000`) and deliberately omits the checkout's Run-3
PDF/scale reweighting list. A full production should add the agreed Run-2 UL
systematic-weight prescription before submission.

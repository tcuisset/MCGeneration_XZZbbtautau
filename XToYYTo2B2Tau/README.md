# XToYYTo2B2Tau signal gridpack

Pilot benchmark:

- `mX = 1000 GeV`, `mY = 200 GeV`
- `X = h2` (the MG5-converted name of HAHM `hs`, PDG 35)
- `Y = zp` (PDG 1023)
- `GammaX/mX = GammaY/mY = 0.1%`
- exact matrix-element decay chain `gg -> X -> YY -> bb tautau`
- Run-3 five-flavor PDF selection through an explicit 5F proton definition

The HAHM production rate and branching fractions are not physics predictions for
this topology sample. Normalize to the requested final-state cross section
`sigma(pp -> X -> YY -> bb tautau)`.

The local build wrapper accepts a full URL in `extramodels.dat`. Before official
CMS production, copy the exact UFO archive to `cms-project-generators`, replace
the URL by its hosted basename, and retain the archive checksum in the request.

UFO SHA-256 used for the pilot build:

`54fd17ed8e5b4f5cafc5d962ed54888d9e54aa6b37ac4c0f4d6e69b3041b3ab9`

Build from this directory with:

```bash
./build_gridpack.sh
```

The build uses MG5_aMC 2.9.18, `el9_amd64_gcc11`, and CMSSW 13_2_9 from
the supplied CMS genproductions installation. Set `NB_CORE` to override the
default of four local build cores.

Validated pilot artifact:

`genproductions_local/XToYYTo2B2Tau_MX1000_MY200_el9_amd64_gcc11_CMSSW_13_2_9_tarball.tar.xz`

Gridpack SHA-256:

`16f90662c3fc77ea1a289541a7410e489ba8a2539cc84ddd504fac657f48cde0`

Validation summary: 100 events requested and produced; zero events failed the
`1 h2 + 2 zp + 2 b + 2 tau` topology check; mean generated masses were
`m(h2) = 1000.085 GeV` and `m(zp) = 200.025 GeV`; the Run-3 systematics step
used NNPDF31 set 325300, produced 926 weights per event, and found no NaNs.


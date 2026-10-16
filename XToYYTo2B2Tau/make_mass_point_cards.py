#!/usr/bin/env python3
from pathlib import Path


base = Path(__file__).resolve().parent
cards = base / "cards"
fragments = base / "fragments"
template_sample = "XToYYTo2B2Tau_MX600_MY200_13TeV_Run2UL"
template_fragment = fragments / "XToYYTo2B2Tau_MX600_MY200_13TeV_Run2UL18_cfi.py"
# (mX label/value, mY label, physical mY value, kinetic mixing).  The MY91
# samples use the measured SM Z-boson mass while retaining an integer-only
# production label.  Near exact Z--Y degeneracy, this UFO requires a much
# smaller kinetic mixing to keep its analytically derived masses real.
points = (
    (200, "80", 80.0, 1.0e-3),
    (800, "80", 80.0, 1.0e-3),
    (400, "100", 100.0, 1.0e-3),
    (800, "100", 100.0, 1.0e-3),
    (1500, "100", 100.0, 1.0e-3),
    (800, "91", 91.1876, 1.0e-8),
    (1500, "91", 91.1876, 1.0e-8),
)

run_card = (cards / f"{template_sample}_run_card.dat").read_text()
extra_models = (cards / f"{template_sample}_extramodels.dat").read_text()
proc_template = (cards / f"{template_sample}_proc_card.dat").read_text()
fragment_template = template_fragment.read_text()

for mx, my_label, my, epsilon in points:
    if mx <= 2 * my:
        raise ValueError(f"off-shell point: mX={mx}, mY={my}")
    sample = f"XToYYTo2B2Tau_MX{mx}_MY{my_label}_13TeV_Run2UL"
    (cards / f"{sample}_run_card.dat").write_text(run_card)
    (cards / f"{sample}_extramodels.dat").write_text(extra_models)
    (cards / f"{sample}_proc_card.dat").write_text(
        proc_template.replace(template_sample, sample)
    )
    (cards / f"{sample}_customizecards.dat").write_text(
        "# HAHM physical input masses\n"
        f"set param_card hidden 1 {my:.6e}\n"
        f"set param_card hidden 2 {mx:.6e}\n\n"
        "# Non-zero mixings activate gg->h2, h2->zp zp, and zp->ff vertices.\n"
        "# Rates and native branching fractions are not used for normalization.\n"
        f"set param_card hidden 3 {epsilon:.6e}\n"
        "set param_card hidden 4 1.000000e-02\n"
        "set param_card hidden 5 1.279000e+02\n\n"
        "# Keep explicit MASS entries synchronized with the HIDDEN physical inputs.\n"
        f"set param_card mass 35 {mx:.6e}\n"
        f"set param_card mass 1023 {my:.6e}\n\n"
        "# Narrow-width topology benchmark: Gamma/m = 0.1% for both resonances.\n"
        f"set param_card DECAY 35 {0.001 * mx:.6e}\n"
        f"set param_card DECAY 1023 {0.001 * my:.6e}\n"
    )
    fragment_name = f"XToYYTo2B2Tau_MX{mx}_MY{my_label}_13TeV_Run2UL18_cfi.py"
    (fragments / fragment_name).write_text(
        fragment_template.replace("MX600_MY200", f"MX{mx}_MY{my_label}")
    )

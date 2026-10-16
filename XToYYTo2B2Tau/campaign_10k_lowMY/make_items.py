#!/usr/bin/env python3
import hashlib
from pathlib import Path


campaign = Path(
    "/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/"
    "XToYYTo2B2Tau_fullsim_UL18_10k_lowMY"
)
points = (
    ("MX200_MY80", "XToYYTo2B2Tau_MX200_MY80_13TeV_Run2UL18_cfi.py"),
    ("MX800_MY80", "XToYYTo2B2Tau_MX800_MY80_13TeV_Run2UL18_cfi.py"),
    ("MX400_MY100", "XToYYTo2B2Tau_MX400_MY100_13TeV_Run2UL18_cfi.py"),
    ("MX800_MY100", "XToYYTo2B2Tau_MX800_MY100_13TeV_Run2UL18_cfi.py"),
    ("MX1500_MY100", "XToYYTo2B2Tau_MX1500_MY100_13TeV_Run2UL18_cfi.py"),
)

rows = []
pilot_rows = []
production_rows = []
manifest_rows = []
wrapper_hash = hashlib.sha256(
    Path(__file__).with_name("run_fullsim.sh").read_bytes()
).hexdigest()
for point_number, (point, fragment) in enumerate(points):
    gridpack = campaign / "gridpacks" / (
        f"XToYYTo2B2Tau_{point}_13TeV_Run2UL_"
        "slc7_amd64_gcc700_CMSSW_10_6_47_tarball.tar.xz"
    )
    for job_index in range(100):
        global_point_number = point_number + 10
        first_lumi = global_point_number * 1000 + job_index + 1
        seed_base = 1_000_000 + global_point_number * 10_000_000 + job_index * 10_000
        row = f"{point} {job_index} {first_lumi} {seed_base} {fragment} {gridpack}"
        rows.append(row)
        (pilot_rows if job_index == 0 else production_rows).append(row)
        manifest_rows.append(
            "\t".join(
                (
                    point,
                    str(job_index),
                    str(first_lumi),
                    "100",
                    str(seed_base),
                    fragment,
                    str(gridpack),
                    str(campaign / point / "Step_5" / f"Ntuple_{job_index}.root"),
                    str(campaign / point / "Step_6" / f"Ntuple_{job_index}.root"),
                    wrapper_hash,
                )
            )
        )

(campaign / "items.txt").write_text("\n".join(rows) + "\n")
(campaign / "pilot_items.txt").write_text("\n".join(pilot_rows) + "\n")
(campaign / "production_items.txt").write_text("\n".join(production_rows) + "\n")
(campaign / "manifest.tsv").write_text(
    "point\tjob_index\tfirst_lumi\tevents\tseed_base\tfragment\tgridpack\t"
    "miniaod_output\tnanoaod_output\twrapper_sha256\n"
    + "\n".join(manifest_rows)
    + "\n"
)

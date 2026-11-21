"""Application scenarios: convert clock ADEV into application metrics. Run: .venv/bin/python scenarios.py
Outputs go to out/ (CSV tables, PNG plots, summary.json). Tags as in clock_noise.py.
"""
from __future__ import annotations
import csv, json, math, copy
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from clock_noise import CLOCKS, validate
from coherence import ENVS, Env, holdover_rms, coherence_time, rel_adev, C

OUT = "out"
S = {}
deg = math.pi / 180


def fmt_t(T):
    if T is None:
        return "<0.1 s"
    return f"{T:.3g} s" if T < 120 else (f"{T/60:.3g} min" if T < 7200 else f"{T/3600:.3g} h")


def table(path, header, rows):
    with open(path, "w", newline="") as f:      # csv module: labels may contain commas
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow([str(v) for v in r])


# ------------------------------------------------------------- 0. validation
validate(f"{OUT}/validation_adev.csv")

# ------------------------------------------------------------- A. baseline: sub-THz ISL coherent
A = []
for f in (140e9, 300e9):
    lam = C / f
    for cname in ("SA65 CSAC", "Space USO", "Challenge chip"):
        c = CLOCKS[cname]
        for envn in ("ideal", "leo"):
            Tc = coherence_time(c, c, ENVS[envn], f, 0.1)
            A.append((f"{f/1e9:.0f} GHz", cname, envn, fmt_t(Tc), Tc))
    # non-clock: line-of-sight baseline knowledge for 0.1 rad
    S[f"A_pos_req_um_{f/1e9:.0f}GHz"] = 0.1 * lam / (2 * math.pi) * 1e6
table(f"{OUT}/A_baseline_isl.csv", ["carrier", "clock", "env", "coherence_time", "T_s"], A)
S["A"] = A

# ------------------------------------------------------------- B. untethered sub-THz channel sounding
B = []
phi_B = 10 * deg   # [ASM] virtual-array phase-coherence tolerance
for f in (140e9, 300e9):
    for cname in ("Rb lab ref", "Rakon HSO (OCXO)", "SA65 CSAC", "Challenge chip"):
        c = CLOCKS[cname]
        Tc = coherence_time(c, c, ENVS["lab"], f, phi_B)
        ph600 = 2 * math.pi * f * holdover_rms(c, c, ENVS["lab"], 600.0) / deg
        B.append((f"{f/1e9:.0f} GHz", cname, fmt_t(Tc), f"{ph600:.3g}", Tc))
table(f"{OUT}/B_sounding.csv", ["carrier", "clock", "coherence_time_10deg", "phase_rms_deg_after_600s", "T_s"], B)
S["B"] = B
# non-clock: positioner 10 um rms [ASM] at 300 GHz
S["B_positioner_deg_300GHz_10um"] = 2 * math.pi * 10e-6 / (C / 300e9) / deg

# ------------------------------------------------------------- C. one-way Doppler (spacecraft clock vs ground maser)
Cr = []
maser = CLOCKS["H-maser (ground)"]
for cname in ("SA65 CSAC", "Space USO", "Rakon HSO (OCXO)", "Challenge chip"):
    sy = rel_adev(CLOCKS[cname], maser, ENVS["deep"], 60.0)
    Cr.append((cname, f"{sy:.2e}", f"{C*sy*1e3:.3g}"))
table(f"{OUT}/C_oneway_doppler.csv", ["spacecraft_clock", "rel_adev_60s", "range_rate_err_mm_s"], Cr)
S["C"] = Cr
S["C_req_adev_for_two_way_parity"] = 0.1e-3 / C   # two-way 0.1 mm/s [SRC:iris_navi]

# ------------------------------------------------------------- D. distributed SAR interferometry
D = []
for f, band in ((5.405e9, "C (Harmony)"), (9.65e9, "X (TanDEM-X)"), (35.75e9, "Ka")):
    gnss_deg = 2 * math.pi * f * 515e-15 / deg       # GNSS sync 515 fs measured [SRC:dlr_tgrs2025]
    for cname in ("Space USO", "Challenge chip"):
        c = CLOCKS[cname]
        Tc = coherence_time(c, c, ENVS["leo"], f, 1 * deg)
        D.append((band, cname, fmt_t(Tc), f"{gnss_deg:.2g}", Tc))
table(f"{OUT}/D_sar_sync.csv", ["band", "clock", "free_run_time_within_1deg", "gnss_sync_deg", "T_s"], D)
S["D"] = D

# ------------------------------------------------------------- E. sensitivity of the chip
E = []
base = CLOCKS["Challenge chip"]
cases = [("baseline (floor 7e-16)", {}, {}),
         ("flicker floor 3e-15", {"floor": 3e-15}, {}),
         ("flicker floor 1e-14", {"floor": 1e-14}, {}),
         ("no temp. compensation (kappa_T=0)", {}, {"kappa_T": 0.0}),
         ("kappa_T=0.999", {}, {"kappa_T": 0.999}),
         ("aging not estimated (eps_D=1)", {}, {"eps_D": 1.0}),
         ("LEO: magnetic shielding 1e2", {}, {"kappa_B": 0.99}),
         ("LEO: magnetic shielding 1e5", {}, {"kappa_B": 0.99999})]
for label, cmod, emod in cases:
    c = copy.deepcopy(base)
    for k, v in cmod.items():
        setattr(c, k, v)
    for envn, f, phi in (("lab", 300e9, phi_B), ("leo", 300e9, 0.1), ("leo", 35.75e9, 1 * deg)):
        if label.startswith("LEO") and envn == "lab":
            continue
        e = copy.deepcopy(ENVS[envn])
        for k, v in emod.items():
            setattr(e, k, v)
        Tc = coherence_time(c, c, e, f, phi)
        E.append((label, envn, f"{f/1e9:.4g} GHz", f"{phi/deg:.3g} deg", fmt_t(Tc), Tc))
table(f"{OUT}/E_sensitivity_chip.csv", ["case", "env", "carrier", "tolerance", "coherence_time", "T_s"], E)
S["E"] = E

# lab magnetic shielding sweep (300 GHz sounding, 10 deg)
for kB in (0.0, 0.99, 0.9999):
    e = copy.deepcopy(ENVS["lab"]); e.kappa_B = kB
    Tc = coherence_time(base, base, e, 300e9, phi_B)
    E.append((f"lab magnetic shielding factor {1/(1-kB):.0f}", "lab", "300 GHz", "10 deg", fmt_t(Tc), Tc))
table(f"{OUT}/E_sensitivity_chip.csv", ["case", "env", "carrier", "tolerance", "coherence_time", "T_s"], E)

# ------------------------------------------------------------- H. minimum clock each application needs
def min_floor(f, T, phi, env):
    """Largest ADEV level (white = floor = L/sqrt2 -> ADEV(1s) = L) that still meets phi over T."""
    lo, hi = 1e-17, 1e-10
    for _ in range(22):
        mid = math.sqrt(lo * hi)
        c = copy.deepcopy(base); c.a_wfm = mid / math.sqrt(2); c.floor = mid / math.sqrt(2)
        if 2 * math.pi * f * holdover_rms(c, c, env, T, reps=24) <= phi:
            lo = mid
        else:
            hi = mid
    return lo

H = []
apps = [("A sub-THz ISL coherent, 300 GHz, sync every 10 s, 0.1 rad", 300e9, 10, 0.1, "leo"),
        ("A sub-THz ISL coherent, 140 GHz, sync every 10 s, 0.1 rad", 140e9, 10, 0.1, "leo"),
        ("B sub-THz sounding 300 GHz, re-reference every 60 s, 10 deg", 300e9, 60, phi_B, "lab"),
        ("B sub-THz sounding 140 GHz, re-reference every 60 s, 10 deg", 140e9, 60, phi_B, "lab"),
        ("D Ka-band distributed InSAR, 60 s data take, 1 deg", 35.75e9, 60, 1 * deg, "leo"),
        ("D C-band (Harmony-class) InSAR, 120 s data take, 1 deg", 5.405e9, 120, 1 * deg, "leo")]
for label, f, T, phi, envn in apps:
    e = copy.deepcopy(ENVS[envn]); e.dB_amp = 0.0; e.dT_amp = 0.0; e.eps_D = 0.0   # clock-only requirement
    L = min_floor(f, T, phi, e)
    H.append((label, f"{L:.1e}", "YES" if L < 6e-14 else "no (HSO/USO-class suffices)"))
H.append(("C one-way Doppler parity with two-way (0.1 mm/s @60 s)", f"{S['C_req_adev_for_two_way_parity']:.1e}", "no (USO-class suffices)"))
table(f"{OUT}/H_min_clock.csv", ["application", "max_allowed_adev_1s_equiv", "needs_better_than_best_quartz_6e-14"], H)
S["H"] = H

# ------------------------------------------------------------- F. f x T map: required ADEV vs clocks
fig, ax = plt.subplots(figsize=(8, 5.2))
T = np.logspace(-1, 4, 200)
for f, lab in ((10e9, "10 GHz"), (35.75e9, "35.75 GHz Ka"), (140e9, "140 GHz"), (300e9, "300 GHz")):
    ax.loglog(T, 0.1 / (2 * math.pi * f * T), lw=1.6, label=f"needed for 0.1 rad @ {lab}")
for cname, ls in (("SA65 CSAC", ":"), ("Rb lab ref", "-."), ("Rakon HSO (OCXO)", "--"), ("Challenge chip", "-")):
    ax.loglog(T, CLOCKS[cname].adev_model(T), "k", ls=ls, lw=1.2, label=f"clock: {cname}")
ax.set_xlabel("coherence window T [s]")
ax.set_ylabel("Allan deviation  /  required sigma_y")
ax.set_title("Where 1e-15 is needed: required stability ~ phi / (2 pi f T)\n(approximation, random noise only)")
ax.set_ylim(1e-17, 1e-9)
ax.grid(True, which="both", alpha=0.3)
ax.legend(fontsize=7, loc="upper right")
fig.tight_layout()
fig.savefig(f"{OUT}/F_fT_map.png", dpi=150)

# coherence-time vs carrier plot (simulated), lab vs LEO
fig, ax = plt.subplots(figsize=(8, 5))
fs = np.array([1e9, 5.4e9, 10e9, 35.75e9, 94e9, 140e9, 300e9, 1e12])
for cname, envn, ls in (("Challenge chip", "ideal", "-"), ("Challenge chip", "lab", "--"),
                        ("Challenge chip", "leo", ":"), ("Rakon HSO (OCXO)", "lab", "-."),
                        ("Space USO", "leo", "-"), ("SA65 CSAC", "lab", "-")):
    vals = [coherence_time(CLOCKS[cname], CLOCKS[cname], ENVS[envn], f, 0.1, reps=20) or 0.1 for f in fs]
    ax.loglog(fs / 1e9, vals, ls=ls, marker="o", ms=3, label=f"{cname} / {envn}")
ax.set_xlabel("carrier frequency [GHz]")
ax.set_ylabel("free-running coherence time, 0.1 rad rms [s]")
ax.set_title("Simulated holdover coherence between two independent clocks\n(floor of plot = 0.1 s = model validity limit)")
ax.grid(True, which="both", alpha=0.3)
ax.legend(fontsize=7)
fig.tight_layout()
fig.savefig(f"{OUT}/G_coherence_vs_carrier.png", dpi=150)

with open(f"{OUT}/summary.json", "w") as f:
    json.dump(S, f, indent=1, default=str)

for k in ("A", "B", "C", "D", "E", "H"):
    print(f"\n== {k}")
    for r in S[k]:
        print("  ", r[:-1] if k in "ABDE" else r)
for k, v in S.items():
    if not isinstance(v, list):
        print(k, v)

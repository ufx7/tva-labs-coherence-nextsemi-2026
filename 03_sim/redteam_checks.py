"""Red-team checks requested by the jury review. Run: .venv/bin/python redteam_checks.py
R1  P1 beachhead with uncertainty bands (P10/P50/P90 over 200 Monte Carlo runs) instead of point values.
R2  Non-clock phase budget for a 300 GHz / 60 s virtual aperture: when is the clock NOT the limit?
R3  Bottom-up revenue model per phase (all inputs [ASM], swept) -> is a EUR 1B outcome plausible?
"""
import math, json
import numpy as np
from clock_noise import CLOCKS
from coherence import ENVS, holdover_rms, C
from poc_phases import residual_series, image_metrics

OUT = "out"
rng = np.random.default_rng(7)
deg = math.pi / 180
res = {}

# ---------------------------------------------------------------- R1 uncertainty bands
R1 = []
for cname in ("Rakon HSO (OCXO)", "Challenge chip"):
    for T in (60, 300):
        pl = []
        for _ in range(200):
            r = residual_series(CLOCKS[cname], CLOCKS[cname], ENVS["lab"], T, n=512, rng=rng)
            pl.append(image_metrics(2 * math.pi * 300e9 * r)[0])
        p10, p50, p90 = np.percentile(pl, [10, 50, 90])
        R1.append((cname, T, round(p90, 2), round(p50, 2), round(p10, 2)))
res["R1_peak_loss_dB_300GHz_P90_P50_P10"] = R1

# ---------------------------------------------------------------- R2 non-clock budget
f = 300e9; lam = C / f
clock_deg = 2 * math.pi * f * holdover_rms(CLOCKS["Challenge chip"], CLOCKS["Challenge chip"], ENVS["lab"], 60.0, reps=60) / deg
hso_deg = 2 * math.pi * f * holdover_rms(CLOCKS["Rakon HSO (OCXO)"], CLOCKS["Rakon HSO (OCXO)"], ENVS["lab"], 60.0, reps=60) / deg
budget = {
    "clock: challenge chip, 2 independent refs, 60 s [SIM]": clock_deg,
    "clock: Rakon HSO, 60 s [SIM]": hso_deg,
    "positioner / antenna position 10 um rms (one-way) [ASM]": 360 * 10e-6 / lam,
    "positioner 50 um rms [ASM]": 360 * 50e-6 / lam,
    "freq. extender + cable thermal drift, 1 deg/K x 0.1 K in 60 s [ASM]": 0.1,
    "freq. extender + cable thermal drift, 10 deg/K x 0.5 K in 60 s [ASM]": 5.0,
    "indoor air path 10 m, 0.1 K / 1 hPa change (n-1 ~ 3e-7 per unit) [ASM]": 360 * 10 * 3e-7 / lam,
}
res["R2_phase_budget_deg_300GHz_60s"] = {k: round(v, 2) for k, v in budget.items()}

# ---------------------------------------------------------------- R3 bottom-up revenue model
years = list(range(2027, 2036))
def model(lab_units, nodes, node_price0, price_decline, licence, anchors, anchor_price, api_per_anchor):
    rev, installed = [], 0
    for i, y in enumerate(years):
        hw_lab = lab_units[i] * 25_000
        price = node_price0 * (1 - price_decline) ** max(0, i - 2)
        hw_node = nodes[i] * price
        installed += nodes[i]
        sw = installed * licence
        vis = anchors[i] * anchor_price + sum(anchors[:i + 1]) * api_per_anchor
        rev.append(hw_lab + hw_node + sw + vis)
    return rev
#            2027 2028 2029 2030  2031  2032   2033    2034    2035
lab      =  [4,   15,  30,  40,   40,   40,    40,     40,     40]
nodes_b  =  [0,   0,   60,  300,  900,  2000,  3500,   5000,   6500]
nodes_lo =  [0,   0,   30,  120,  350,  700,   1200,   1700,   2200]
anch_b   =  [0,   0,   0,   0,    2e3,  2e4,   1e5,    3e5,    6e5]
anch_0   =  [0] * 9
cases = {
    "base: scale + vision": model(lab, nodes_b, 12_000, 0.08, 1_500, anch_b, 120, 15),
    "scale only (no vision)": model(lab, nodes_b, 12_000, 0.08, 1_500, anch_0, 0, 0),
    "slow scale, no vision": model(lab, nodes_lo, 12_000, 0.08, 1_500, anch_0, 0, 0),
}
res["R3_revenue_EURm"] = {k: [round(v / 1e6, 1) for v in r] for k, r in cases.items()}
res["R3_years"] = years
res["R3_note"] = ("Valuation at 2033 revenue x 5-10x (hardware/infra multiple; SiTime 22x is peak-cycle): "
                  + "; ".join(f"{k}: EUR {cases[k][6]/1e6*5:.0f}-{cases[k][6]/1e6*10:.0f}M" for k in cases))
# share of the European counter-UAS market implied by node hardware in 2030 (EUR ~3.8B ~ $4.16B) [MR]
res["R3_node_hw_2030_share_of_EU_cUAS_2030"] = f"{nodes_b[3]*12_000*(0.92**1)/3.8e9*100:.2f} %"

with open(f"{OUT}/R_redteam_checks.json", "w") as fh:
    json.dump(res, fh, indent=1)
for k, v in res.items():
    print(k, ":", v if not isinstance(v, dict) else "")
    if isinstance(v, dict):
        for kk, vv in v.items():
            print("   ", kk, vv)

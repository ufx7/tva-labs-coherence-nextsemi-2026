"""Self-check: compares headline numbers in out/ with the values quoted in README.md.
Coherence times live on a ~1.47x log grid, so 'grid' checks allow one step either way;
other checks allow the stated relative tolerance. Exit code 1 if anything is off."""
import csv, json, sys

def rows(name):
    return list(csv.DictReader(open(f"out/{name}")))

def pick(name, **kw):
    for r in rows(name):
        if all(r[k] == v for k, v in kw.items()):
            return r
    raise KeyError((name, kw))

checks = []   # (label, value, expected, mode, tol)
def add(label, value, expected, mode="rel", tol=0.10):
    checks.append((label, value, expected, mode, tol))

# generator validation
ratios = [float(r["adev_generated"]) / float(r["adev_model"]) for r in rows("validation_adev.csv")]
add("generator/model ADEV ratio, min", min(ratios), 0.93, "abs", 0.02)
add("generator/model ADEV ratio, max", max(ratios), 1.07, "abs", 0.02)
# B: coherence time at 300 GHz, 10 deg (grid)
for clk, exp in (("Challenge chip", 31.6), ("Rakon HSO (OCXO)", 1.0)):
    add(f"B coherence time 300 GHz [{clk}] (s)", float(pick("B_sounding.csv", carrier="300 GHz", clock=clk)["T_s"]), exp, "grid")
# H: minimum clock
add("H min ADEV, 300 GHz sounding 60 s", float(pick("H_min_clock.csv", application="B sub-THz sounding 300 GHz, re-reference every 60 s, 10 deg")["max_allowed_adev_1s_equiv"]), 2.1e-15)
add("H min ADEV, Ka InSAR 60 s", float(pick("H_min_clock.csv", application="D Ka-band distributed InSAR, 60 s data take, 1 deg")["max_allowed_adev_1s_equiv"]), 1.8e-15)
add("H min ADEV, one-way Doppler parity", float(pick("H_min_clock.csv", application="C one-way Doppler parity with two-way (0.1 mm/s @60 s)")["max_allowed_adev_1s_equiv"]), 3.3e-13)
# C: external validation vs JPL
add("C SA65 one-way Doppler error (mm/s) [JPL measured 11]", float(pick("C_oneway_doppler.csv", spacecraft_clock="SA65 CSAC")["range_rate_err_mm_s"]), 11.5)
# P1 image loss, 300 GHz, 60 s (dB)
for clk, exp, tol in (("Challenge chip", -0.01, 0.5), ("Rakon HSO (OCXO)", -4.3, 0.5), ("Rb lab ref", -18.2, 0.5)):
    add(f"P1 peak loss 300 GHz 60 s [{clk}] (dB)", float(pick("P1_beachhead_image_blur.csv", carrier="300 GHz", aperture_time_s="60", clock=clk)["peak_loss_dB_median"]), exp, "abs", tol)
# P2 outage (grid)
for band, clk, exp in (("X-band 10 GHz", "Challenge chip", 100), ("X-band 10 GHz", "Rakon HSO (OCXO)", 30), ("W-band 94 GHz", "Challenge chip", 30), ("W-band 94 GHz", "Rakon HSO (OCXO)", 3)):
    add(f"P2 max sync outage {band} [{clk}] (s)", float(pick("P2_scale_outage.csv", band=band, clock=clk)["max_sync_outage_s_with_gain>=0.9"]), exp, "grid")
# J floor envelope
add("J V1 (random-walk FM) coherence 300 GHz (s)", float(pick("J_floor_envelope.csv", variant="V1 + random-walk FM worst case (ADEV 1e-15 @1s, ~sqrt(tau) rise)")["coh_time_300GHz_10deg_s"]), 21.5, "grid")
# red-team
r = json.load(open("out/R_redteam_checks.json"))
add("R2 chip clock phase 300 GHz 60 s (deg)", r["R2_phase_budget_deg_300GHz_60s"]["clock: challenge chip, 2 independent refs, 60 s [SIM]"], 19.6)
add("R3 base revenue 2033 (EUR M) [assumption-driven]", r["R3_revenue_EURm"]["base: scale + vision"][6], 55.1)

bad = 0
for label, v, e, mode, tol in checks:
    if mode == "rel":   ok = abs(v - e) <= tol * abs(e)
    elif mode == "abs": ok = abs(v - e) <= tol
    else:               ok = e / 1.5 / 1.01 <= v <= e * 1.5 * 1.01     # one grid step
    bad += not ok
    print(f"{'OK  ' if ok else 'FAIL'} {label}: got {v:.4g}, expected ~{e:.4g} ({mode} tol {tol if mode != 'grid' else '1 step'})")
print(f"\n{len(checks)-bad}/{len(checks)} checks passed")
sys.exit(1 if bad else 0)

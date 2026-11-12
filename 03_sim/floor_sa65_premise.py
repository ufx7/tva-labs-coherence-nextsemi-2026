"""Premise taken literally: 'the flicker floor is not as low as expected but follows the SA65 specs'.
Three readings, all run through the three phases (same machinery as floor_envelope.py):
  P1  flat flicker floor at CSAC-class level 1e-12 (literal 'floor = SA65'); contradicts the 1 s spec 1000x
  P2  ADEV 1e-15 at 1 s but rising ~tau (drift-like, NOT estimable) to SA65-class 1e-12 at 1000 s
      -> drift 1.2e-10/day (4x SA65 aging), eps_D = 1
  P3  same shape reaching the SA65 *table* value 1e-11 at 1000 s -> drift 1.2e-9/day (40x SA65 aging), eps_D = 1
  P2e/P3e  the same drifts but ESTIMABLE (a stable drift rate removed to 1 % by firmware) -> what engineering recovers
Run: .venv/bin/python floor_sa65_premise.py -> out/K_sa65_premise.csv
"""
import math, copy
import numpy as np
from clock_noise import Clock, CLOCKS
from coherence import ENVS, Env, coherence_time
import floor_envelope as fe

deg = math.pi / 180
e = 1e-15 / math.sqrt(2)
V = {
 "base (floor 7e-16)":                              (Clock("B",  7e-16, 7e-16, 0.0, 3e-11,   5e-12, "", {"alpha_B": 9e-11}), dict()),
 "P1 flat floor 1e-12 (literal; breaks the 1 s spec 1000x)": (Clock("P1", 7e-16, 1e-12, 0.0, 3e-11, 5e-12, "", {"alpha_B": 9e-11}), dict()),
 "P2 SA65-shape: 1e-15@1s -> 1e-12@1000s, drift not estimable": (Clock("P2", e, e, 0.0, 1.2e-10, 5e-12, "", {"alpha_B": 9e-11}), dict(eps_D=1.0)),
 "P2e same drift, estimated to 1% by firmware":    (Clock("P2e", e, e, 0.0, 1.2e-10, 5e-12, "", {"alpha_B": 9e-11}), dict(eps_D=0.01)),
 "P3 SA65-table: 1e-15@1s -> 1e-11@1000s, drift not estimable": (Clock("P3", e, e, 0.0, 1.2e-9, 5e-12, "", {"alpha_B": 9e-11}), dict(eps_D=1.0)),
 "P3e same drift, estimated to 1% by firmware":    (Clock("P3e", e, e, 0.0, 1.2e-9, 5e-12, "", {"alpha_B": 9e-11}), dict(eps_D=0.01)),
 "HSO best quartz (reference)":                    (CLOCKS["Rakon HSO (OCXO)"], dict()),
}
rows = []
for name, (c, ek) in V.items():
    lab = fe.env_with("lab", **ek); field = fe.env_with(fe.FIELD, **ek); indoor = fe.env_with(fe.INDOOR, **ek)
    # ADEV incl. uncompensated drift term D*tau/sqrt(2) when eps_D = 1
    D = c.aging_per_day / 86400 * ek.get("eps_D", 0.01)
    adev = [math.sqrt(c.a_wfm**2 / t + c.floor**2 + (D * t / math.sqrt(2))**2) for t in (1, 10, 100, 1000)]
    t300 = coherence_time(c, c, lab, 300e9, 10 * deg, reps=24)
    il300_10 = fe.image_loss(c, lab, 300e9, 10)
    il300_60 = fe.image_loss(c, lab, 300e9, 60)
    ox = fe.outage(c, field, 10e9)
    rs = fe.resync_interval(c, indoor)
    rows.append((name, *[f"{a:.1e}" for a in adev], t300, round(il300_10, 2), round(il300_60, 2), ox, rs))
    print(f"{name[:62]:62s} ADEV@1/10/100/1000s={rows[-1][1:5]} | 300GHz coh {t300} s | img 10s/60s {il300_10:.2f}/{il300_60:.2f} dB | X-band outage {ox} s | anchor resync {rs} s")
with open("out/K_sa65_premise.csv", "w") as fh:
    fh.write("reading,adev_1s,adev_10s,adev_100s,adev_1000s,coh_300GHz_10deg_s,image_300GHz_10s_dB,image_300GHz_60s_dB,xband_outage_s,anchor_resync_100ps_s\n")
    for r in rows:
        fh.write(",".join(str(v) for v in r) + "\n")

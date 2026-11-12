"""Hypothesis test: GNSS carrier-phase sync (515 fs 1-sigma per 0.5 s sample, white [SRC:dlr_tgrs2025])
smoothed with a stable clock as flywheel. Estimate = moving average of GNSS samples over W seconds
centred on t (non-causal smoothing, as in SAR post-processing). Error = true relative clock phase - estimate.
Assumes white GNSS noise; multipath/hardware drift would set a floor (not modelled) [ASM]."""
import math, numpy as np
from clock_noise import CLOCKS
from coherence import ENVS, rel_y
from clock_noise import phase_from_y
deg = math.pi/180; f = 35.75e9; dt = 0.5; n = 4800      # 40 min record
rng = np.random.default_rng(3)
print("Ka-band 35.75 GHz, rms sync phase error [deg] vs smoothing window W")
print("clock            " + "  ".join(f"W={W:>4}s" for W in (0.5, 10, 30, 60, 120, 300)))
for cname in ("Space USO", "Challenge chip"):
    c = CLOCKS[cname]; res = {W: [] for W in (0.5, 10, 30, 60, 120, 300)}
    for _ in range(20):
        x = phase_from_y(rel_y(c, c, ENVS["leo"], n, dt, rng), dt)
        g = x + 515e-15 * rng.standard_normal(n)
        for W in res:
            k = max(1, int(W / dt)); est = np.convolve(g, np.ones(k) / k, mode="same")
            e = (x - est)[k:-k] if k > 1 else x - est
            res[W].append(np.sqrt(np.mean(e**2)))
    print(f"{cname:16s} " + "  ".join(f"{2*math.pi*f*np.mean(v)/deg:7.2f}" for v in res.values()))

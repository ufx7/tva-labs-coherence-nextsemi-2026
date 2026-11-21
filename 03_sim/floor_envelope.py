"""Flicker-floor / noise-above-1-s envelope. Run: .venv/bin/python floor_envelope.py -> out/J_floor_envelope.csv
Physics: a flicker-FM floor is flat in tau, so ADEV(1 s) <= 1e-15 bounds the flicker floor at <= 1e-15 [CHAL].
Unbounded by the spec: random-walk FM (~sqrt(tau)), linear drift (~tau; SA65 aging 3e-11/day frozen) and
environmental sensitivity (SA65 temperature 5e-12/K, magnetic 9e-11/G frozen). Variants V1-V3 are the worst
spec-consistent cases; V4-V5 violate the 1 s spec (a sceptic who treats 1e-15 as a best-case lab number).
"""
import csv, math, copy
import numpy as np
from clock_noise import Clock, CLOCKS, gen_y, oadev, phase_from_y
from coherence import ENVS, Env, holdover_rms, coherence_time, rel_y
from poc_phases import image_metrics

deg = math.pi / 180
rng = np.random.default_rng(5)
IDEAL = CLOCKS["ideal ref"]
e = 1e-15 / math.sqrt(3)       # three equal components -> total 1e-15 at 1 s

V = {
 "V0 current (white+flicker 7e-16, drift est., kappa_T 0.99)": (Clock("V0", 7e-16, 7e-16, 0.0, 3e-11, 5e-12, "", {"alpha_B": 9e-11}), dict()),
 "V1 + random-walk FM worst case (ADEV 1e-15 @1s, ~sqrt(tau) rise)": (Clock("V1", e, e, e, 3e-11, 5e-12, "", {"alpha_B": 9e-11}), dict()),
 "V2 = V1 + SA65 drift NOT estimated": (Clock("V2", e, e, e, 3e-11, 5e-12, "", {"alpha_B": 9e-11}), dict(eps_D=1.0)),
 "V3 = V2 + poor thermal compensation (kappa_T 0.9)": (Clock("V3", e, e, e, 3e-11, 5e-12, "", {"alpha_B": 9e-11}), dict(eps_D=1.0, kappa_T=0.9)),
 "V4 sceptic: flicker floor 1e-14 (violates spec 10x)": (Clock("V4", 7e-16, 1e-14, 0.0, 3e-11, 5e-12, "", {"alpha_B": 9e-11}), dict()),
 "V5 SA65-physics floor 1e-13 (violates spec 100x)": (Clock("V5", 7e-16, 1e-13, 0.0, 3e-11, 5e-12, "", {"alpha_B": 9e-11}), dict()),
 "HSO best quartz (reference)": (CLOCKS["Rakon HSO (OCXO)"], dict()),
}

# generator check for random-walk FM (not covered by validate()): sigma_y = b*sqrt(tau)
rw = Clock("rw", 0.0, 0.0, 1e-15, 0.0, 0.0)
chk = [(tau, float(np.mean([oadev(gen_y(rw, 4096, tau / 16, rng, include_aging=False), tau / 16, 16) for _ in range(20)])) / (1e-15 * math.sqrt(tau))) for tau in (1, 10, 100)]
print("RW-FM generator check (generated/model):", [f"tau={t}: {r:.2f}" for t, r in chk])


def env_with(name, **kw):
    env = copy.deepcopy(ENVS[name] if isinstance(name, str) else name)
    for k, v in kw.items():
        setattr(env, k, v)
    return env


FIELD = Env("field", 2.0, 3600, 0.005, 1800, kappa_T=0.99, kappa_B=0.99)
INDOOR = Env("indoor", 1.0, 3600, 0.002, 600, kappa_T=0.99, kappa_B=0.99)


def residual(c, env, T, n=512):
    dt = T / n
    y = rel_y(c, c, env, 2 * n, dt, rng)
    x = phase_from_y(y, dt)
    y_est = (x[n] - x[0]) / T
    return x[n:] - x[n] - y_est * np.arange(n) * dt


def image_loss(c, env, f, T, reps=40):
    return float(np.median([image_metrics(2 * math.pi * f * residual(c, env, T))[0] for _ in range(reps)]))


def outage(c, env, f, N=16, reps=8):
    best = None
    for T in (1, 3, 10, 30, 100, 300, 1000):
        g = []
        for _ in range(reps):
            ph = np.array([2 * math.pi * f * residual_vs_ideal(c, env, T)[-1] for _ in range(N)])
            g.append(abs(np.exp(1j * ph).sum()) ** 2 / N**2)
        if np.mean(g) >= 0.9:
            best = T
        else:
            break
    return best


def residual_vs_ideal(c, env, T, n=256):
    dt = T / n
    y = rel_y(c, IDEAL, env, 2 * n, dt, rng)
    x = phase_from_y(y, dt)
    y_est = (x[n] - x[0]) / T
    return x[n:] - x[n] - y_est * np.arange(n) * dt


def resync_interval(c, env, budget=100e-12):
    best = None
    for T in (1, 3, 10, 30, 60, 120, 300, 600, 1800, 3600, 7200):
        if holdover_rms(c, IDEAL, env, T, n_half=512, reps=12) < budget:
            best = T
        else:
            break
    return best


rows = []
for name, (c, ek) in V.items():
    lab = env_with("lab", **ek); field = env_with(FIELD, **ek); indoor = env_with(INDOOR, **ek)
    adev = [float(np.sqrt(c.a_wfm**2 / t + c.floor**2 + c.b_rwfm**2 * t)) for t in (1, 10, 100, 1000)]
    t300 = coherence_time(c, c, lab, 300e9, 10 * deg, reps=24)
    t150 = coherence_time(c, c, lab, 150e9, 10 * deg, reps=24)
    il300 = image_loss(c, lab, 300e9, 60)
    il150 = image_loss(c, lab, 150e9, 60)
    ox = outage(c, field, 10e9)
    rs = resync_interval(c, indoor)
    rows.append((name, *[f"{a:.1e}" for a in adev], t300, t150, round(il300, 2), round(il150, 2), ox, rs))
    print(f"{name[:58]:58s} ADEV(1,10,100,1000s)={rows[-1][1:5]} | 300GHz {t300} s | 150GHz {t150} s | img60s 300/150GHz {il300:.2f}/{il150:.2f} dB | X-band outage {ox} s | anchor resync {rs} s")

with open("out/J_floor_envelope.csv", "w") as fh:
    fh.write("variant,adev_1s,adev_10s,adev_100s,adev_1000s,coh_time_300GHz_10deg_s,coh_time_150GHz_10deg_s,image_loss_300GHz_60s_dB,image_loss_150GHz_60s_dB,xband_16node_outage_s,indoor_anchor_resync_100ps_s\n")
    for r in rows:
        csv.writer(fh, lineterminator="\n").writerow([str(v) for v in r])   # variant names contain commas

"""Proof-of-concept simulations for the three venture phases. Run: .venv/bin/python poc_phases.py
P1 BEACHHEAD  - multi-module / bistatic virtual-aperture imaging at 150/300 GHz: image blur vs clock
               (Fraunhofer Leistungszentrum Terahertzsensorik pain: "phase drift -> blurred image,
               minute range, the longer the better" [INT TVA notes]).
P2 SCALE      - fibre-free distributed coherent radar network: coherent gain of N nodes during a
               sync-link outage (jamming / link loss) + economics vs fibre per node.
P3 VISION     - "coherent layer": (a) indoor TDOA positioning error vs anchor sync error,
               (b) how long each oscillator class holds the anchors inside the sync budget,
               (c) relay/spoofing attack detection threshold vs timing precision.
Tags: [SRC] sourced, [INT] interview, [ASM] assumption, [SIM] output. Model limits: see README.
"""
from __future__ import annotations
import math, copy, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from clock_noise import CLOCKS, phase_from_y
from coherence import ENVS, Env, rel_y, holdover_rms, C

OUT = "out"
R = {}
rng = np.random.default_rng(42)
IDEAL = CLOCKS["ideal ref"]


def residual_series(cA, cB, env, T, n=1024, rng=rng):
    """Residual time error r(t) over a window T after sync; frequency estimated from prior window."""
    dt = T / n
    y = rel_y(cA, cB, env, 2 * n, dt, rng)
    x = phase_from_y(y, dt)
    y_est = (x[n] - x[0]) / T
    return x[n:] - x[n] - y_est * np.arange(n) * dt


def image_metrics(phi, pad=16):
    s = np.exp(1j * phi)
    K = len(s)
    img = np.abs(np.fft.fftshift(np.fft.fft(s, K * pad))) ** 2
    ideal = np.abs(np.fft.fftshift(np.fft.fft(np.ones(K), K * pad))) ** 2
    peak_loss_db = 10 * np.log10(img.max() / ideal.max())
    # ISLR: energy outside the ideal mainlobe (+-1 resolution cell) / energy inside
    c = np.argmax(ideal); w = pad
    main = img[c - w:c + w + 1].sum()
    islr_db = 10 * np.log10((img.sum() - main) / main)
    return peak_loss_db, islr_db, img / ideal.max()



def _main():
    P1 = []
    cuts = {}
    envP1 = ENVS["lab"]
    for f in (150e9, 300e9):
        for T in (10, 60, 300):
            for cname in ("Rb lab ref", "Rakon HSO (OCXO)", "Challenge chip"):
                c = CLOCKS[cname]
                pl, isl = [], []
                for k in range(20):
                    r = residual_series(c, c, envP1, T, n=512)
                    phi = 2 * math.pi * f * r
                    a, b, img = image_metrics(phi)
                    pl.append(a); isl.append(b)
                    if k == 0 and f == 300e9 and T == 60:
                        cuts[cname] = img
                P1.append((f"{f/1e9:.0f} GHz", T, cname, round(float(np.median(pl)), 2), round(float(np.median(isl)), 1)))
    with open(f"{OUT}/P1_beachhead_image_blur.csv", "w") as fh:
        fh.write("carrier,aperture_time_s,clock,peak_loss_dB_median,ISLR_dB_median\n")
        for r_ in P1:
            fh.write(",".join(map(str, r_)) + "\n")
    R["P1"] = P1

    fig, ax = plt.subplots(figsize=(8, 4.2))
    x = np.linspace(-1, 1, len(next(iter(cuts.values()))))
    ideal = np.abs(np.fft.fftshift(np.fft.fft(np.ones(512), 512 * 16))) ** 2
    ax.plot(x, 10 * np.log10(ideal / ideal.max() + 1e-12), "k", lw=2, label="ideal (cable / common reference)")
    for cname, img in cuts.items():
        ax.plot(x, 10 * np.log10(img + 1e-12), lw=1.2, label=cname)
    ax.set_xlim(-0.05, 0.05); ax.set_ylim(-40, 3)
    ax.set_xlabel("normalised azimuth"); ax.set_ylabel("dB")
    ax.set_title("P1 Beachhead: point-target image, 300 GHz, 60 s virtual aperture,\nseparate TX/RX references (no cable), one sync at start [SIM]")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(f"{OUT}/P1_beachhead_image_blur.png", dpi=150)

    # =============================================================== P2 scale
    # Field environment for outdoor radar nodes: enclosure-controlled 2 K/1 h, 5 mG, shielding x100 [ASM]
    FIELD = Env("field", 2.0, 3600, 0.005, 1800, kappa_T=0.99, kappa_B=0.99)


    def network_gain(cname, f, T_out, N, reps=12):
        """Mean coherent combining gain |sum exp(j phi_i)|^2 / N^2 at the END of a sync outage T_out."""
        c = CLOCKS[cname]
        g = []
        for _ in range(reps):
            ph = np.array([2 * math.pi * f * residual_series(c, IDEAL, FIELD, T_out, n=256)[-1] for _ in range(N)])
            g.append(abs(np.exp(1j * ph).sum()) ** 2 / N**2)
        return float(np.mean(g))


    P2 = []
    grid = [0.1, 0.3, 1, 3, 10, 30, 100, 300, 1000, 3000]
    curves = {}
    for f, lab in ((10e9, "X-band 10 GHz"), (94e9, "W-band 94 GHz")):
        for cname in ("Rb lab ref", "Rakon HSO (OCXO)", "Challenge chip"):
            gs = [network_gain(cname, f, T, 16) for T in grid]
            curves[(lab, cname)] = gs
            ok = [T for T, gv in zip(grid, gs) if gv >= 0.9]
            P2.append((lab, cname, 16, max(ok) if ok else "<0.1"))
    with open(f"{OUT}/P2_scale_outage.csv", "w") as fh:
        fh.write("band,clock,N_nodes,max_sync_outage_s_with_gain>=0.9\n")
        for r_ in P2:
            fh.write(",".join(map(str, r_)) + "\n")
    R["P2_outage"] = P2

    fig, axs = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    for ax, lab in zip(axs, ("X-band 10 GHz", "W-band 94 GHz")):
        for cname in ("Rb lab ref", "Rakon HSO (OCXO)", "Challenge chip"):
            ax.semilogx(grid, curves[(lab, cname)], marker="o", ms=3, label=cname)
        ax.axhline(0.9, color="grey", ls="--", lw=1)
        ax.set_title(f"{lab}, 16 nodes"); ax.set_xlabel("sync-link outage [s]"); ax.grid(alpha=0.3)
    axs[0].set_ylabel("coherent gain / ideal (N^2)")
    axs[0].legend(fontsize=8)
    fig.suptitle("P2 Scale: distributed radar keeps coherence through a sync outage (jamming/link loss) [SIM]")
    fig.tight_layout(); fig.savefig(f"{OUT}/P2_scale_outage.png", dpi=150)

    # economics: fibre per node vs coherence module [ASM inputs, swept]
    P2e = []
    for spacing_km in (0.5, 1, 3, 5):
        for eur_per_m in (20, 60, 150):           # rural plough .. urban trench [ASM, verify]
            fibre = spacing_km * 1000 * eur_per_m
            for module in (8000, 15000):          # target module price at scale [ASM]
                P2e.append((spacing_km, eur_per_m, fibre, module, round(fibre / module, 1)))
    with open(f"{OUT}/P2_scale_economics.csv", "w") as fh:
        fh.write("node_spacing_km,fibre_eur_per_m,fibre_cost_per_node_eur,module_price_eur,fibre_to_module_ratio\n")
        for r_ in P2e:
            fh.write(",".join(map(str, r_)) + "\n")
    R["P2_econ_examples"] = [r_ for r_ in P2e if r_[1] == 60 and r_[3] == 15000]

    # =============================================================== P3 vision
    # (a) TDOA positioning, 50 m x 50 m building, 8 anchors on the perimeter, 2-D, Gauss-Newton
    anchors = np.array([[0, 0], [25, 0], [50, 0], [50, 25], [50, 50], [25, 50], [0, 50], [0, 25]], float)


    def tdoa_solve(meas, p0):
        p = p0.copy()
        for _ in range(15):
            d = np.linalg.norm(anchors - p, axis=1)
            h = d[1:] - d[0]
            u = (p - anchors) / d[:, None]
            J = u[1:] - u[0]
            dp = np.linalg.lstsq(J, meas - h, rcond=None)[0]
            p += dp
            if np.linalg.norm(dp) < 1e-6:
                break
        return p


    def tdoa_error(sync_s, meas_m, trials=1500):
        errs = []
        for _ in range(trials):
            p = rng.uniform(5, 45, 2)
            d = np.linalg.norm(anchors - p, axis=1)
            bias = C * sync_s * rng.standard_normal(len(anchors))        # anchor clock errors
            noisy = d + bias + meas_m * rng.standard_normal(len(anchors))
            est = tdoa_solve(noisy[1:] - noisy[0], np.array([25.0, 25.0]))
            errs.append(np.linalg.norm(est - p))
        e = np.array(errs)
        return float(np.median(e)), float(np.percentile(e, 90))


    P3a = []
    for meas_m, mlab in ((0.30, "100 MHz-class ranging (30 cm)"), (0.03, "1 GHz-class ranging (3 cm)")):
        for sync, slab in ((50e-9, "50 ns (GNSS/PTP-class network)"), (5e-9, "5 ns"), (1e-9, "1 ns"),
                           (100e-12, "100 ps"), (10e-12, "10 ps (coherent layer)")):
            med, p90 = tdoa_error(sync, meas_m)
            P3a.append((mlab, slab, round(med, 3), round(p90, 3)))
    with open(f"{OUT}/P3a_vision_positioning.csv", "w") as fh:
        fh.write("ranging_noise,anchor_sync_error,median_error_m,p90_error_m\n")
        for r_ in P3a:
            fh.write(",".join(map(str, r_)) + "\n")
    R["P3a"] = P3a

    # (b) anchor holdover: rms time error vs a perfect reference after a sync interval (indoor env)
    INDOOR = Env("indoor", 1.0, 3600, 0.002, 600, kappa_T=0.99, kappa_B=0.99)
    P3b = []
    for cname in ("TCXO", "OCXO (std)", "Rakon HSO (OCXO)", "Challenge chip"):
        row = [cname]
        for T in (1, 60, 3600):
            row.append(f"{holdover_rms(CLOCKS[cname], IDEAL, INDOOR, T, n_half=512, reps=20)*1e12:.3g}")
        P3b.append(tuple(row))
    with open(f"{OUT}/P3b_vision_anchor_holdover_ps.csv", "w") as fh:
        fh.write("anchor_oscillator,rms_ps_after_1s,rms_ps_after_60s,rms_ps_after_1h\n")
        for r_ in P3b:
            fh.write(",".join(r_) + "\n")
    R["P3b"] = P3b

    # (c) relay / spoofing detection: smallest extra path a relay can add without detection (3 sigma)
    P3c = []
    for sig, lab in ((50e-9, "50 ns"), (1e-9, "1 ns"), (100e-12, "100 ps"), (10e-12, "10 ps")):
        P3c.append((lab, round(3 * math.sqrt(2) * sig * C, 4)))
    with open(f"{OUT}/P3c_vision_relay_detection.csv", "w") as fh:
        fh.write("timing_precision_1sigma,min_detectable_relay_extra_path_m\n")
        for r_ in P3c:
            fh.write(",".join(map(str, r_)) + "\n")
    R["P3c"] = P3c

    with open(f"{OUT}/poc_summary.json", "w") as fh:
        json.dump(R, fh, indent=1, default=str)
    for k, v in R.items():
        print("==", k)
        for r_ in v:
            print("  ", r_)


if __name__ == "__main__":
    _main()

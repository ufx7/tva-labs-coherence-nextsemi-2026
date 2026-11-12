"""Clock noise model: power-law fractional-frequency noise + deterministic aging + temperature.

Every clock is described by:
  a_wfm   ADEV at tau = 1 s of the white-FM part (sigma_y ~ a_wfm / sqrt(tau))
  floor   flicker-FM floor (sigma_y = floor, flat in tau)
  b_rwfm  random-walk-FM part, sigma_y = b_rwfm * sqrt(tau)
  aging   linear frequency drift per day (deterministic)
  alpha_T temperature coefficient per kelvin; kappa = fraction removed by compensation

Tags: [SRC:x] sourced, [ASM] engineering assumption, [CHAL] challenge assumption.
Time-domain generation; amplitudes are calibrated by measuring ADEV of the generated
noise (see validate()), so the model is checked rather than trusted.
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass, field

DAY = 86400.0


@dataclass
class Clock:
    name: str
    a_wfm: float
    floor: float
    b_rwfm: float = 0.0
    aging_per_day: float = 0.0
    alpha_T: float = 0.0          # 1/K
    sources: str = ""
    extra: dict = field(default_factory=dict)

    def adev_model(self, tau):
        tau = np.asarray(tau, float)
        return np.sqrt((self.a_wfm**2) / tau + self.floor**2 + (self.b_rwfm**2) * tau)


# ---------------------------------------------------------------- catalogue
CLOCKS = {
    # Datasheet points 3e-10@1s, 1e-10@10s, 3e-11@100s, 1e-11@1000s -> white FM 3e-10/sqrt(tau)
    # [SRC:sa65_ds]; floor below datasheet range [ASM]; aging 9e-10/month = 3e-11/day [SRC:sa65_ds]
    "SA65 CSAC": Clock("SA65 CSAC", 3e-10, 3e-12, 0.0, 3e-11, 5e-12,
                       "SA65 sell sheet (ADEV table, aging); floor ASM",
                       extra={"alpha_B": 9e-11}),          # +-9e-11/Gauss [SRC:sa65_ds]
    # Lab rubidium, as used in sub-THz channel sounders [SRC:nyu_sounder uses Rb];
    # 2e-11 @1s, floor 1e-13 typical of PRS10-class units [ASM, verify datasheet]
    "Rb lab ref": Clock("Rb lab ref", 2e-11, 1e-13, 0.0, 1e-11 / 30, 1e-12,
                        "Rb used in NYU/AAU sounders; numbers ASM (PRS10-class)"),
    # Rakon HSO: 6e-14 @ 1 s, 50 ppt/day aging [SRC:rakon_interview]; flat floor [ASM]
    "Rakon HSO (OCXO)": Clock("Rakon HSO (OCXO)", 1e-14, 6e-14, 0.0, 5e-11, 1e-12,
                              "Rakon booth interview: 6e-14@1s, 50 ppt/day; rack-size"),
    # Space USO, flat ~1e-13 for 1-1000 s [ASM, typical deep-space USO class]
    "Space USO": Clock("Space USO", 3e-14, 1e-13, 0.0, 1e-11, 1e-13,
                       "USO class ASM (deep-space radio science heritage)"),
    # Challenge chip: 1e-15 @1s [CHAL]; flicker floor 1e-15 [ASM, swept in sensitivity];
    # all else frozen at SA65 [CHAL]: aging 3e-11/day, alpha_T 5e-12/K (from +-3e-10/120K)
    # white 7e-16 and floor 7e-16 -> total 1.0e-15 at 1 s (meets the challenge spec)
    "Challenge chip": Clock("Challenge chip", 7e-16, 7e-16, 0.0, 3e-11, 5e-12,
                            "imec challenge: ADEV<1e-15@1s; SA65 for rest; floor ASM",
                            extra={"alpha_B": 9e-11}),
    # Ground hydrogen maser (DSN-class reference): ~1e-13@1s, ~1e-15@1000s [ASM, typical];
    # one-way Doppler ground side ~1e-15@1000s per Galileo-era JPL report [SRC:jpl_tda]
    "H-maser (ground)": Clock("H-maser (ground)", 1e-13, 7e-16, 0.0, 0.0, 0.0,
                              "typical active H-maser; JPL TDA report"),
    # Typical infrastructure oscillators for the vision scenario [ASM, typical datasheet class]
    "TCXO": Clock("TCXO", 1e-10, 1e-10, 0.0, 1e-9, 1e-8, "typical TCXO class ASM"),
    "OCXO (std)": Clock("OCXO (std)", 3e-13, 1e-12, 0.0, 5e-10, 1e-11, "typical telecom OCXO class ASM"),
    "ideal ref": Clock("ideal ref", 0.0, 0.0, 0.0, 0.0, 0.0, "perfect reference"),
}


# ---------------------------------------------------------------- noise generation
_rng = np.random.default_rng(20261112)
_FLICKER_CAL = {}     # calibration constant per record length n (the raw generator's amplitude scales ~1/n)


def _flicker_unit(n, rng):
    """Flicker-FM y-samples with PSD ~ 1/f, generated 8x longer then cropped (less wrap)."""
    m = 8 * n
    w = rng.standard_normal(m // 2 + 1) + 1j * rng.standard_normal(m // 2 + 1)
    k = np.arange(m // 2 + 1)
    w[0] = 0.0
    w[1:] /= np.sqrt(k[1:])
    y = np.fft.irfft(w, m)
    s = rng.integers(0, m - n)
    return y[s:s + n]


def oadev(y, dt, m):
    """Overlapping Allan deviation from fractional-frequency samples y at averaging m*dt."""
    x = np.concatenate([[0.0], np.cumsum(y) * dt])
    tau = m * dt
    d = x[2 * m:] - 2 * x[m:-m] + x[:-2 * m]
    return np.sqrt(np.mean(d**2) / (2 * tau**2))


def _flicker_cal(n, reps=60):
    """ADEV of the raw flicker generator for record length n (cached). Must be called with the
    same n that gen_y uses, because the raw amplitude depends on n (bug found 12 Nov 2026 04:20:
    earlier runs calibrated at n=4096 only, so records of 512..2048 samples had 2-8x too much flicker)."""
    if n not in _FLICKER_CAL:
        rng = np.random.default_rng(1)
        ms = [m for m in (8, 16, 32, 64, 128) if m <= n // 8] or [max(2, n // 8)]
        vals = []
        for _ in range(reps):
            y = _flicker_unit(n, rng)
            vals += [oadev(y, 1.0, m) for m in ms]
        _FLICKER_CAL[n] = float(np.mean(vals))
    return _FLICKER_CAL[n]


def gen_y(clock: Clock, n: int, dt: float, rng=_rng, temp_profile=None, kappa=0.0,
          include_aging=True):
    """Fractional frequency y(t) of one clock, n samples at spacing dt (random + deterministic)."""
    y = clock.a_wfm / np.sqrt(dt) * rng.standard_normal(n)                     # white FM
    y += clock.floor / _flicker_cal(n) * _flicker_unit(n, rng)                   # flicker FM
    if clock.b_rwfm:
        y += np.cumsum(clock.b_rwfm * np.sqrt(3 * dt) * rng.standard_normal(n))  # RW FM
    t = np.arange(n) * dt
    if include_aging:
        y += clock.aging_per_day / DAY * t
    if temp_profile is not None:
        y += clock.alpha_T * (1 - kappa) * temp_profile(t)
    return y


def phase_from_y(y, dt):
    return np.concatenate([[0.0], np.cumsum(y)[:-1]]) * dt     # time error x(t) in s


def validate(out_csv=None):
    """Generated ADEV vs model ADEV for every clock -> proves the generator honours the inputs."""
    rows = []
    for c in CLOCKS.values():
        if c.floor == 0 and c.a_wfm == 0:
            continue
        for tau in (1, 10, 100, 1000):
            dt = tau / 16
            n = 4096
            ests = [oadev(gen_y(c, n, dt, include_aging=False), dt, 16) for _ in range(30)]
            rows.append((c.name, tau, n, float(c.adev_model(tau)), float(np.mean(ests))))
    # record-length sweep on a flicker-dominated clock: the generator must not depend on n
    c = CLOCKS["Rakon HSO (OCXO)"]
    for n in (256, 512, 1024, 2048, 8192):
        ests = [oadev(gen_y(c, n, 1.0, include_aging=False), 1.0, 16) for _ in range(40)]
        rows.append((c.name + " [n-sweep]", 16, n, float(c.adev_model(16)), float(np.mean(ests))))
    if out_csv:
        with open(out_csv, "w") as f:
            f.write("clock,tau_s,n_samples,adev_model,adev_generated\n")
            for r in rows:
                f.write(f"{r[0]},{r[1]},{r[2]},{r[3]:.3e},{r[4]:.3e}\n")
    return rows


if __name__ == "__main__":
    for r in validate():
        print(f"{r[0]:28s} tau={r[1]:5d}s n={r[2]:5d} model={r[3]:.2e}  generated={r[4]:.2e}  ratio={r[4]/r[3]:.2f}")

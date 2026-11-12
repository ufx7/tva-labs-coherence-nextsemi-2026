"""Relative phase coherence between two INDEPENDENT clocks after a sync event.

Model (predict / holdover mode):
  * At t = 0 the two nodes are synchronised in phase (sync error added separately).
  * Their relative frequency is estimated from the preceding window of equal length T
    (phase difference over that window / T) - a realistic, causal estimator.
  * During the next window the residual time error r(t) = x(t) - y_est * t accumulates.
  * Deterministic terms (aging, temperature, magnetic field) are included as RESIDUALS
    after compensation: aging * eps_D, alpha_T * (1-kappa_T) * dT(t), alpha_B * (1-kappa_B) * dB(t).
  * Output: rms phase error at carrier f, 2*pi*f*rms(r), Monte Carlo mean over realisations.

Limits: valid for T >= 0.1 s (below that the CSAC output is set by its internal VCXO,
which this model does not contain); no vibration/acceleration sensitivity; environment
profiles are sinusoids with assumed amplitudes [ASM].
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from clock_noise import Clock, gen_y, phase_from_y, oadev

C = 299_792_458.0


@dataclass
class Env:
    name: str
    dT_amp: float = 0.0      # K, amplitude of temperature swing seen by the clock
    dT_period: float = 3600  # s
    dB_amp: float = 0.0      # gauss
    dB_period: float = 5700  # s
    kappa_T: float = 0.99    # fraction of temperature effect compensated
    kappa_B: float = 0.999   # magnetic shielding/compensation fraction
    eps_D: float = 0.01      # residual fraction of aging drift after estimation


ENVS = {
    # Lab/field measurement: HVAC cycle 0.5 K / 30 min, ~1 mG fluctuation [ASM]
    # magnetic shielding factor 100 (simple mu-metal can) is part of the product [ASM]
    "lab": Env("lab", 0.5, 1800, 0.001, 600, kappa_T=0.99, kappa_B=0.99),
    # LEO spacecraft: 1 K orbital thermal swing after S/C thermal control, |B| ~0.2-0.5 G
    # over a 95 min orbit -> 0.15 G amplitude [ASM]; magnetic shielding factor 1e3 [ASM]
    "leo": Env("leo", 1.0, 5700, 0.15, 5700, kappa_T=0.99, kappa_B=0.999),
    # Cislunar / deep space: slow thermal, negligible field change [ASM]
    "deep": Env("deep", 0.5, 20000, 1e-5, 20000, kappa_T=0.99, kappa_B=0.99),
    "ideal": Env("ideal", 0, 3600, 0, 3600, eps_D=0.0),
}


def _env_y(clock: Clock, env: Env, t, phase0):
    y = np.zeros_like(t)
    if env.dT_amp:
        y += clock.alpha_T * (1 - env.kappa_T) * env.dT_amp * np.sin(2 * np.pi * t / env.dT_period + phase0[0])
    aB = clock.extra.get("alpha_B", 0.0)
    if env.dB_amp and aB:
        y += aB * (1 - env.kappa_B) * env.dB_amp * np.sin(2 * np.pi * t / env.dB_period + phase0[1])
    return y


def rel_y(cA: Clock, cB: Clock, env: Env, n, dt, rng):
    t = np.arange(n) * dt
    y = gen_y(cA, n, dt, rng, include_aging=False) - gen_y(cB, n, dt, rng, include_aging=False)
    # independent aging of the two units; residual after drift estimation = eps_D
    y += np.hypot(cA.aging_per_day, cB.aging_per_day) / 86400 * env.eps_D * t
    y += _env_y(cA, env, t, rng.uniform(0, 2 * np.pi, 2)) - _env_y(cB, env, t, rng.uniform(0, 2 * np.pi, 2))
    return y


def holdover_rms(cA, cB, env, T, n_half=1024, reps=40, seed=0):
    """rms residual time error [s] over a window T after sync, frequency estimated over prior T."""
    rng = np.random.default_rng(seed)
    dt = T / n_half
    out = []
    for _ in range(reps):
        y = rel_y(cA, cB, env, 2 * n_half, dt, rng)
        x = phase_from_y(y, dt)
        y_est = (x[n_half] - x[0]) / T
        tt = np.arange(n_half) * dt
        r = x[n_half:] - x[n_half] - y_est * tt
        out.append(np.sqrt(np.mean(r**2)))
    return float(np.sqrt(np.mean(np.square(out))))


def coherence_time(cA, cB, env, f, phi_max, T_grid=None, **kw):
    """Largest T on the grid for which rms phase error at carrier f stays below phi_max [rad]."""
    if T_grid is None:
        T_grid = np.logspace(-1, 4.5, 34)
    best = None
    for T in T_grid:
        ph = 2 * np.pi * f * holdover_rms(cA, cB, env, T, **kw)
        if ph <= phi_max:
            best = T
        else:
            break
    return best


def rel_adev(cA, cB, env, tau, reps=20, seed=0):
    rng = np.random.default_rng(seed)
    dt = tau / 16
    vals = [oadev(rel_y(cA, cB, env, 4096, dt, rng), dt, 16) for _ in range(reps)]
    return float(np.mean(vals))

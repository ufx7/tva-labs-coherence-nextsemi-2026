# Handover for Emmanuele: verify the simulations, publish the repo
Target: repo public (or jury-accessible) and link pasted into the deck and the submission by 11:30.

## A. Fresh-environment run (15 min)
```
cd TVA_submission/03_sim
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python clock_noise.py        # generator validation (expect ratios 0.93–1.07 everywhere)
.venv/bin/python scenarios.py          # A–H tables, F/G plots (~20 s)
.venv/bin/python poc_phases.py         # P1/P2/P3 (~5 s)
.venv/bin/python hybrid_gnss.py        # Ka-band GNSS + chip flywheel
.venv/bin/python redteam_checks.py     # R1–R3 (bands, non-clock budget, revenue model)
.venv/bin/python floor_envelope.py     # J: noise-above-1-s envelope
.venv/bin/python navigator.py          # market opportunity scores
```
Python 3.11+ works; developed on 3.14 with numpy 2.5 and matplotlib 3.11.

## B. Numbers that must come out (tolerance: coherence times are on a 1.5x grid, so one grid step either way is fine; image losses ±0.5 dB; everything else ±10 %)
| Script | Check | Expected |
|---|---|---|
| clock_noise | n-sweep ratios for the HSO, n = 256…8192 | 0.93–1.07 |
| scenarios B | 300 GHz lab 10°: chip / HSO / Rb | 31.6 s / ~1 s / <0.1 s |
| scenarios H | 300 GHz 60 s needs; one-way Doppler needs | 2.1e-15; 3.3e-13 |
| scenarios C | SA65 one-way Doppler range-rate error | 11.5 mm/s (JPL measured 11) |
| scenarios E | κ_T = 0; floor 1e-14 | 3.2 s; 6.8 s |
| poc P1 | 300 GHz 60 s: chip / HSO / Rb peak loss | −0.01 / −4.3 / −18 dB |
| poc P2 | X-band outage chip / HSO; W-band | 100 / 30 s; 30 / 3 s |
| poc P3b | resync-relevant: chip 1 h drift | ~35 ps |
| hybrid_gnss | chip, W = 60 s | 0.6–0.9° |
| redteam R2 | chip clock term at 300 GHz / 60 s | ~20° |
| redteam R3 | base revenue 2033 / 2035 | 55 / 163 €M |
| floor_envelope | V1 300 GHz; V5 300 GHz | ~22 s; ~0.7 s |

If anything is off by more than the tolerance, do not "fix" the document: tell Claus and Sascha first; the numbers in `02_tech/VC_story.md` and the deck must match the repo.

## C. Independent sanity check (5 min, write the result into README under "Independent checks")
Analytic estimate for a flicker-dominated clock: rms time error over T ≈ σ_y × T (order of magnitude). For the HSO at 300 GHz, 60 s: 6e-14 × 60 s × √2 (two clocks) = 5.1 ps → phase = 2π × 3e11 × 5.1e-12 = 9.6 rad. The sim reports ~490° = 8.5 rad for the same case (`R_redteam_checks.json`, R2). Same order; good. Do the same for the chip (7e-16 × 60 × √2 = 59 fs → 0.11 rad = 6.4°; sim ~20° because the lab temperature term dominates: state that).

## D. Things to read before the jury asks
- `clock_noise.py` → `_flicker_cal(n)`: the bug fix. The raw 1/f generator's amplitude scales ~1/n; we calibrate per record length. Validation sweeps n = 256…8192.
- `coherence.py` → `holdover_rms`: causal frequency estimate from the previous window, residual over the next. Tolerances: 0.1 rad (beam combining), 10° (virtual array), 1° (InSAR). Model valid from 0.1 s upward (no VCXO / multiplier phase-noise model).
- `poc_phases.py` → `image_metrics`: FFT of exp(jφ) over the aperture; peak loss and ISLR (energy outside ±1 resolution cell / inside).
- Environments (`coherence.ENVS`, `poc_phases` FIELD/INDOOR): sinusoidal temperature and magnetic profiles with assumed amplitudes; all [ASM].

## E. Repo hygiene (10 min)
1. From the package root run `grep -rn -i -f private/names_to_scrub.txt --exclude-dir=private --exclude-dir=.git .`; it must return nothing. The pattern file lives in `private/` (gitignored) so the names never enter the repo. Never commit `private/`.
2. `git status` must not show `.venv/` or `__pycache__/`.
3. The README at the package root is the jury's entry point; the sim README is the method. Both must say the same numbers.
4. Keep `out/` committed: the jury should see results without running anything.

## F. Publish (10 min)
```
cd TVA_submission
git init -b main
git add -A
git commit -m "TVA Labs: coherence where sync is denied or impossible (NextSEMI 2026 submission)"
gh repo create tva-labs-coherence-nextsemi-2026 --public --source=. --push     # or private + invite the jury
```
Then paste the URL into: deck slide "Validation" (S13) and the last slide; the submission form/email; `README.md` top line. Tag the submitted state: `git tag submission-2026-11-12 && git push --tags`.
If a local commit already exists (Claus may have initialised the repo), just set the remote and push.

## G. If a juror wants to see a case live (13:00 workspace review)
Have the venv activated and `scenarios.py` already run. Fast demos: change `phi_B` or a carrier in `scenarios.py` (B block only, ~5 s), or run `floor_envelope.py` (~5 s) and point at the HSO vs chip lines.

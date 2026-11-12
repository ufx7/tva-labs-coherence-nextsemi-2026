# Coherence simulation: does 1e-15 @ 1 s matter, and where?

Reproduce (about 20 s on a laptop):
```
cd sim && python3 -m venv .venv && .venv/bin/pip install numpy matplotlib
.venv/bin/python clock_noise.py      # generator validation vs ADEV targets
.venv/bin/python scenarios.py        # A-H scenario tables + plots -> out/
.venv/bin/python hybrid_gnss.py      # GNSS + chip flywheel at Ka-band
.venv/bin/python poc_phases.py       # P1 beachhead / P2 scale / P3 vision PoCs
.venv/bin/python navigator.py        # Market Opportunity Navigator scoring -> out/navigator.csv
```

## Model
1. **Clock noise (`clock_noise.py`):** time-domain fractional-frequency noise: white FM + flicker FM + optional random-walk FM, plus aging, temperature and magnetic terms. Amplitudes are calibrated by **measuring** the overlapping ADEV of the generated noise. `out/validation_adev.csv` shows generated vs target within ±7 % for every clock, tau = 1 to 1000 s, and record lengths 256 to 8192 samples.
2. **Coherence (`coherence.py`):** two **independent** clocks are synchronised at t = 0. Their relative frequency is estimated causally from the previous window, and the residual phase drift is accumulated over the next window T. The metric is rms phase error at carrier f, Monte Carlo over 24 to 40 realisations. The coherence time is the longest T with rms phase below a tolerance.
3. **Scenarios (`scenarios.py`):**
   - A: baseline sub-THz inter-satellite links
   - B: untethered sub-THz channel sounding
   - C: one-way deep-space Doppler
   - D: distributed SAR
   - E: chip sensitivity
   - F, G: plots
   - H: minimum clock each application actually needs

## Inputs: sourced [SRC], challenge [CHAL], assumed [ASM]
| Input | Value | Tag |
|---|---|---|
| Challenge chip ADEV @1 s | 1e-15 (white 7e-16 + flicker floor 7e-16) | CHAL; split and floor ASM, swept in E |
| Chip aging, temperature, magnetic | 3e-11/day; 5e-12/K (from ±3e-10 over 120 K); 9e-11/G | CHAL = SA65 sell sheet |
| SA65 ADEV | 3e-10/√τ (1 to 1000 s) | SRC: SA65 sell sheet |
| Rakon HSO | 6e-14 @1 s, 50 ppt/day | SRC: Rakon booth interview |
| Lab Rb (sounders) | 2e-11 @1 s | ASM (PRS10 class), verify |
| Space USO | ~1e-13 flat | ASM (typical deep-space USO) |
| Ground H-maser | 1e-13/√τ, floor 7e-16 | ASM; JPL TDA: about 1e-15 @1000 s |
| Two-way Doppler reference | 0.1 mm/s @60 s | SRC: Iris/CSAC paper (NAVIGATION 71(1)) |
| GNSS-based SAR phase sync | 515 fs (1σ) = 1° @5.4 GHz | SRC: DLR, IEEE TGRS 2025 |
| Lab environment | 0.5 K / 30 min, 1 mG, κ_T = 0.99, magnetic shield ×100 | ASM |
| LEO environment | 1 K / orbit, 0.15 G / orbit, κ_T = 0.99, shield ×1000 | ASM |
| Tolerances | 0.1 rad (beam combining), 10° (virtual array), 1° (InSAR) | ASM (InSAR: TanDEM-X "few degrees") |

## Main outputs (`out/`)
- `H_min_clock.csv`: the minimum ADEV each application needs. **Sub-THz links, untethered sub-THz sounding and Ka-band InSAR need 2e-15 to 7e-15.** One-way Doppler needs only 3.3e-13.
- `B_sounding.csv`: at 300 GHz the chip stays within 10° for 31.6 s. The best quartz (HSO) manages about 1 s and lab Rb less than 0.1 s.
- `C_oneway_doppler.csv`: the model gives 11.5 mm/s with an SA65, against 11 mm/s measured by JPL with Iris and an SA.45s. This is an **external validation** of the model.
- `I_hybrid_gnss_ka.txt` (`hybrid_gnss.py`): GNSS sync (515 fs) plus the chip as a flywheel gives 0.6–0.9° at Ka-band; GNSS alone gives 6.6°, and with a space USO the best is 3.5°. Assumes white GNSS noise.
- `J_floor_envelope.csv` (`floor_envelope.py`): noise-above-1-s envelope. Flicker floor is bounded at ≤1e-15 by the 1 s spec (flat in τ). Worst spec-consistent case (random-walk FM): 300 GHz coherence 32 → 22 s, 60 s image −0.02 dB, X-band outage 100 s, anchor resync 1 h. Drift not estimated or κ_T = 0.9 removes the scale/vision advantage (engineering, not physics). Floor 1e-14 (spec ×10): 7 s at 300 GHz, rest intact. Floor 1e-13: nothing survives.
- `E_sensitivity_chip.csv`: no thermal compensation cuts coherence 10x. No magnetic shielding in the lab cuts it 3x. A flicker floor of 1e-14 instead of 7e-16 cuts it about 5x.

## Phase PoCs (`poc_phases.py`)
- `P1_beachhead_image_blur.*`: 300 GHz, 60 s virtual aperture with separate references. Chip −0.01 dB peak loss; HSO −4.3 dB (blurred); Rb −18 dB. At 150 GHz over 60 s the HSO loses only 1.3 dB.
- `P2_scale_outage.*`: 16-node coherent radar. Sync-link outage tolerated at 90% gain: chip 100 s at X-band and 30 s at W-band; HSO 30 s and 3 s. `P2_scale_economics.csv` compares fibre to module per node (ASM inputs).
- `P3a/b/c_*`: indoor TDOA positioning error vs anchor sync; anchor holdover in ps per oscillator class; relay-detection threshold vs timing precision.

## Bug log
- **12 Nov 04:20:** the flicker-noise generator's amplitude scaled with record length (about 1/n) and was calibrated at n = 4096 only, which was also the only length validated. Scenarios using 512 to 2048 samples had 2 to 8x too much flicker. Fixed by calibrating per record length; validation now sweeps n = 256 to 8192. Effect: chip results nearly unchanged (environment-limited); quartz comparisons softened (HSO at 300 GHz 0.46 s → 1 s; X-band outage 3 s → 30 s; OCXO anchor drift 170 ps → 44 ps per minute). The one-way Doppler validation (n = 4096) was unaffected.

## Limitations
- Not valid below 0.1 s. The CSAC's internal VCXO and the multiplier-chain phase noise (+20·log N) are not modelled; at 300 GHz the multiplier adds about +89.5 dB.
- The coherence-time grid is coarse (steps of about 1.5x).
- Environment profiles are sinusoids with assumed amplitudes.
- No vibration or acceleration sensitivity, relativistic or orbit-determination errors, or multipath.
- The flicker floor of the chip is unknown and is the most sensitive input (sweep E).
- The navigator scores are judgement calls; the evidence for each is in `navigator.py`.

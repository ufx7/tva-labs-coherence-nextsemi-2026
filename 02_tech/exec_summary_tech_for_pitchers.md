# The technology from the ground up: for Sascha and Claus
Read this once end-to-end (20 minutes). Then you can answer any technical question the jury can ask, and you will know which questions you should hand to Emmanuele.

## 1. What a clock is, and what "stability" means
A clock is an oscillator (something that ticks) plus a counter. A chip-scale atomic clock (CSAC) is a quartz oscillator that is continuously corrected by atoms: caesium vapour in a tiny cell is probed with light and microwaves, and the atoms' resonance tells the quartz when it has drifted. The atoms set the long-term behaviour; the quartz sets the very short-term behaviour (below about a second).

Stability is described by the **Allan deviation (ADEV)**, written σ_y(τ): the typical fractional frequency change between two adjacent measurements of length τ. "1e-15 at 1 s" means that over one second the clock's rate wanders by one part in 10¹⁵, i.e. about one femtosecond of time per second. For comparison:

| Reference | ADEV at 1 s | Picture |
|---|---|---|
| Phone TCXO | 1e-10 | 100 ps per second |
| Microchip SA65 CSAC (our baseline) | 3e-10 | 300 ps per second |
| Lab rubidium | 2e-11 | 20 ps per second |
| Best quartz (Rakon HSO, rack-sized) | 6e-14 | 60 fs per second |
| Hydrogen maser (room-sized) | 1e-13 | 100 fs per second |
| **Our chip** | **1e-15** | **1 fs per second** |

So the challenge clock is 300,000x more stable than the SA65 at 1 s, and 60x more than the best quartz ever sold. Do not say "300,000x better" on stage: over a day the chip is no better than an SA65, because the challenge freezes aging and temperature at SA65 level.

## 2. The ADEV curve: four kinds of noise
Plot ADEV against τ and you get a curve with four regions:
- **White FM** (falls as 1/√τ): the atoms' detection noise averages out. Dominant in CSACs from 1 s to 1000 s.
- **Flicker floor** (flat): the clock stops improving with averaging. A property of the physics (light shift, cell temperature). **Key fact: because it is flat, a flicker floor can never be above the 1 s value. The spec "≤1e-15 at 1 s" therefore bounds the flicker floor at ≤1e-15. That is not our assumption; it is arithmetic.**
- **Random-walk FM** (rises as √τ) and **drift / aging** (rises as τ): the clock wanders. Aging is deterministic (a constant rate, 3e-11 per day for the SA65) and can be estimated and subtracted. Temperature and magnetic field changes also move the frequency: SA65 5e-12 per kelvin, 9e-11 per gauss.

What the spec leaves open is the rise above 1 s. We simulated the worst case consistent with the spec (random-walk FM reaching 1.8e-14 at 1000 s) and the venture survives it (§7).

## 3. The one law: φ / (2π · f · T)
When two devices with separate clocks must stay **phase-coherent** (act as one antenna, one radar, one instrument), the phase error between them is 2π × carrier frequency × time error. Time error ≈ ADEV × window. So the stability you need is

**σ_y needed ≈ φ_tolerance / (2π · f · T)**

Worked examples (tolerance 0.1 rad ≈ 6°):
- 10 GHz radar, 10 s: 1.6e-13 → best quartz is fine.
- 10 GHz, 100 s: 1.6e-14 → quartz fails, our chip works.
- 300 GHz, 60 s: 9e-16 → only our chip (and in the model, with real environments, 2.1e-15).
- 1.3 GHz (L-band space-surveillance radar), 100 s: 1.2e-13 → quartz is fine. **That is why we no longer claim the L-band radar as a clock-limited customer.**

Two corollaries you will be asked about:
- **Frequency multiplication preserves fractional stability but multiplies phase.** A 10 MHz reference multiplied to 300 GHz keeps its 1e-15, but every femtosecond of time error becomes 2π × 3e11 × 1e-15 = 0.002 rad of phase. That is why high frequency is where the chip matters.
- **Phase noise also multiplies by 20·log(N) dB.** From 10 MHz to 300 GHz that is +89.5 dB. The chip's output must therefore be cleaned by a low-noise "flywheel" oscillator locked to it. Our model is valid from 0.1 s upward and says so.

## 4. Sync versus clock: the question that decides everything
A clock only matters **between synchronisations**. If two nodes can exchange a sync signal continuously (a cable, a fibre, a direct radio path, GNSS), the clock is almost irrelevant: an OCXO resyncing every minute meets a 100 ps budget. Our clock matters when sync is **slow, expensive, power-hungry, impossible (no wire, out of range) or denied (jammed, spoofed)**. Hence our thesis: *coherence where sync is denied or impossible.*

Numbers to remember (all from the model, corrected 12 Nov):
- Free-running coherence at 300 GHz, 10° tolerance: chip ~32 s, best quartz ~1 s, rubidium <0.1 s.
- 16-node X-band radar, sync link cut: chip keeps 90 % coherent gain for 100 s (300 s with 0.1 % residual thermal sensitivity), best quartz 30 s. W-band: 30 s vs 3 s.
- Anchor holding 100 ps without resync: standard OCXO 1 min, best quartz 30 min, chip 2 h.

## 5. What the chip does to an image (the slide the jury will remember)
A radar builds a sharp image by adding echoes coherently over an aperture time. If the transmitter and receiver clocks drift apart during that time, the echoes add with wrong phases: the peak drops and energy leaks into sidelobes, i.e. **blur**. Our simulation (300 GHz, 60 s aperture, separate references, one sync at the start): chip −0.01 dB (indistinguishable from a cabled system), best quartz −4.3 dB (blurred), rubidium −18 dB (incoherent). At 150 GHz over 60 s quartz loses only 1.3 dB, so we claim 300 GHz × 1 min, not "minutes" in general. At 300 s our residual frequency error *shifts* the target by 2–4 resolution cells rather than blurring it; the calibration firmware removes that.

## 6. The product is not the chip
Four things set the field advantage, and they are engineering, not physics:
1. **Thermal control** to 99 % compensation (residual ≤5e-14/K). Without it coherence falls 10x; with 99.9 % the X-band outage tolerance triples.
2. **Magnetic shield** ×100 in the lab, ×1000 on vehicles. One milligauss uncompensated costs 3x.
3. **Drift estimation** to 1 %. Without it an anchor drifts 2.3 ns per hour instead of 35 ps.
4. **Flywheel oscillator** for phase noise above the atomic loop bandwidth.
If we fail at 1 or 3, the chip is no better than a compensated quartz for phases 2 and 3. Say this before the jury does; it is our second moat after the licence.

## 7. The noise envelope (if asked "what if the floor is worse?")
| Case | 300 GHz coherence | 60 s image | X-band outage | Anchor resync |
|---|---|---|---|---|
| Base | 32 s | −0.01 dB | 100 s | 2 h |
| Worst spec-consistent (random walk) | 22 s | −0.02 dB | 100 s | 1 h |
| Sceptic's floor 1e-14 (violates spec 10x) | 7 s | −0.16 dB | 100 s | 1 h |
| Floor 1e-13 (violates spec 100x) | 0.7 s | −5.8 dB | 30 s | 10 min |
| Best quartz | ~1 s | −3.8 dB | 30 s | 30 min |

One sentence for the stage: "The flicker floor is bounded by the spec itself; what is open is the noise above one second, and we survive its worst case. Milestone one of the seed is the measured curve."

## 8. The model, in two sentences
We generate clock noise in the time domain (white, flicker, random walk, drift, temperature, magnetic), calibrate it by measuring its ADEV, synchronise two clocks, estimate their relative frequency causally from the previous window, and accumulate the residual phase at the carrier over the next window, Monte Carlo over 24–200 runs. It reproduces JPL's measured one-way Doppler error with a CSAC (11.5 vs 11 mm/s), carries P10–P90 bands, and has a bug log: we found and fixed a record-length bug in the flicker generator on the last night and corrected every number.

## 9. Words and numbers
Say: coherence, sync-denied, wire-free, 300 GHz × 1 minute, 100 s at X-band, 2 hours at 100 ps, "the licence is the moat", "proof phase, not revenue".
Avoid: "300,000x better", "minutes" (say 60 s at 300 GHz), "holdover" (we do not sell it), "every device" (say infrastructure first), "GPS replacement" (say complement), ISLR / flicker / Allan on stage unless asked.

## 10. Hand to Emmanuele
Anything about the generator, calibration constants, Monte Carlo counts, the CRLB geometry in the drone critique, or re-running a case live.

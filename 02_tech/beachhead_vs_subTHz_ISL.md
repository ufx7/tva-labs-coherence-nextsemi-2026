# Beachhead check: sub-THz inter-satellite links (baseline) vs. alternatives
Status: 12 Nov 2026, early morning. Model: `sim/` (reproducible, about 20 s). Tags: [SIM] own simulation, [SRC] sourced, [INT] our booth interviews, [ASM] assumption.

## 1. Bottom line
- **Better beachhead than the baseline: a "Coherence Module" for untethered, phase-coherent sub-THz and mm-wave measurement.** Users are 6G channel-sounding labs and bistatic sensing (ISAC) testbeds. They are sold directly and through test-equipment makers such as Rohde & Schwarz (R&S) and Keysight.
  - It is one of three applications where **1e-15 is mission-critical** [SIM H].
  - It needs **no space qualification**.
  - It has the only **interview-backed willingness to pay** we have [INT Rakon, Microchip].
- **Sub-THz inter-satellite links stay as the end point of the expansion path:** lab → field → orbit. They are not the first market.
  - The links do need the clock [SIM H: 7.3e-15].
  - But no buyer budgets for them yet. The first in-space demonstrations are planned for 2027 [SRC].
  - Line-of-sight position knowledge of about 16 µm at 300 GHz, not the clock, is the limit unless the system calibrates itself [SIM A].
- **Honest size caveat:** the beachhead is small, an estimated $10–50 M serviceable [ASM]. 3GPP's first 6G release (Rel-21, 2027–28) focuses on 7–24 GHz and sensing (ISAC); sub-THz remains research-driven [SRC]. The venture case therefore depends on the expansion steps.

## 2. Where 1e-15 is actually needed [SIM]
The required stability scales as φ/(2π·f·T): carrier frequency × coherence window decides it (`sim/out/F_fT_map.png`).
The minimum clock each application needs, from the noise-only search (`sim/out/H_min_clock.csv`):

| Application | Needed ADEV (1 s equiv.) | Best quartz 6e-14 enough? |
|---|---|---|
| Sub-THz sounding, 300 GHz, re-reference every 60 s, 10° | **2.1e-15** | no → only the chip |
| Sub-THz sounding, 140 GHz, 60 s, 10° | 4.5e-15 | no |
| Sub-THz inter-satellite link coherent, 300 GHz, sync every 10 s, 0.1 rad (baseline) | 7.3e-15 | no |
| Ka-band distributed InSAR, 60 s data take, 1° | 1.8e-15 | no |
| C-band Harmony-class InSAR, 120 s, 1° | 5.7e-15 | no, but GNSS sync already gives 1° [SRC DLR] → competitor good enough |
| One-way deep-space Doppler matching two-way (0.1 mm/s @60 s) | 3.3e-13 | **yes → 1e-15 not needed**, value would be SWaP only |

Free-running coherence at 300 GHz, lab, 10° [SIM B]:

| Clock | Coherence time |
|---|---|
| Challenge chip | **31.6 s** |
| Rakon HSO (best quartz, rack size) | about 1 s |
| Lab rubidium (today's sounders) | < 0.1 s |
| SA65 CSAC | < 0.1 s |

**Model validation:** the model gives 11.5 mm/s one-way Doppler with an SA65. JPL measured 11 mm/s with the Iris radio and an SA.45s CSAC [SRC].

**What the product must contain** (otherwise the spec is lost) [SIM E]:
- **Thermal compensation:** without it (κ_T = 0), coherence drops 10x, to 3 s.
- **Magnetic shield:** the challenge holds the SA65 sensitivity of 9e-11/G. Without a shield, 1 mG of lab fluctuation costs 3x; in low Earth orbit (about 0.15 G per orbit) a shield of at least ×1000 is mandatory.
- **Aging-rate estimation.**
- **The flicker floor is the key unknown:** if it is 1e-14 instead of 7e-16, coherence falls about 5x, to 7 s. That makes it imec's number-one validation item.

## 3. Navigator ranking (`sim/navigator.py`; scores 1–5 with evidence)
| Rank | Opportunity | Total /35 | GTM (access + cycle + qualification) /15 | Spec mission-critical |
|---|---|---|---|---|
| 1 | **Untethered phase-coherent sub-THz measurement** | **28** | **14** | 5 |
| 2 | Drone TDOA / anti-spoofing (current TVA deck) | 22 | 9 | 2 |
| 3 | Distributed / companion SAR interferometry | 18 | 4 | 4 |
| 4 | One-way tracking, lunar and deep-space smallsats | 16 | 7 | 1 |
| 5 | Sub-THz inter-satellite links (baseline) | 15 | 3 | 3 |

## 4. Beachhead: customer problem and evidence
- **Problem:** phase-coherent measurements at 140–300 GHz need the transmitter and receiver locked in phase.
- **Today's workarounds:**
  - **Cables or VNA:** short range.
  - **Phase-compensated radio-over-fibre:** this is the Aalborg (AAU) approach, about 300 m, sensitive to bending and temperature [SRC].
  - **Rubidium plus PTP resync every second plus drift-correction algorithms (NYU).** This gives timing only, not phase. Untethered drift causes "ghost multipath" [SRC].
  - The bistatic sensing literature calls clock asynchronism "a key obstacle" [SRC IEEE SPM 2024].
- **Users vs. economic buyer:** users are channel-sounding and testbed engineers. The economic buyer is the principal investigator's grant budget (EU SNS JU / 6G Flagship / NSF), or the T&M OEM's product manager for an instrument option.
- **Willingness to pay:**
  - Rakon: lab and science buyers of ultra-stable references "don't care much about price"; the quoted figure was "15,000 or whatever" (currency not stated), with no large competition [INT].
  - Microchip, unprompted, named lab and measurement equipment (R&S) as the best fit for this spec [INT].
  - A sub-THz chain already costs $35–130k in components [SRC, low confidence] → a €20–30k module is a fraction of it [ASM].
- **Buying trigger:** a measurement campaign beyond fibre reach (more than 300 m, outdoor, vehicle- or drone-borne), or bistatic ISAC experiments.
- **Complete product:**
  - chip clock,
  - magnetic shield and thermal control,
  - low-noise LO distribution for multiplier chains,
  - two-way calibration and drift-estimation software,
  - a phase-health monitor.
  
  It is sold as a module (high margin), with an OEM option variant for R&S and Keysight.

## 5. Expansion path: same core, rising qualification
1. **Lab, 2027–28:** sub-THz and mm-wave measurement modules; first revenue and field data on the flicker floor.
2. **Field, 2028–30:** bistatic and multistatic mm-wave sensing (ISAC pilots, counter-UAS W-band multistatic radar). Ruggedised version, MIL-STD-810 like the SA65.
3. **Orbit, 2030+:** Ka-band SAR interferometry formations (multistatic constellations such as Umbra's 32-satellite licence; DARPA DRIFT), then **sub-THz inter-satellite coherent links (baseline)**. Uses the SA65 space-option heritage and magnetic shielding.
   - **GNSS sync plus the chip as a flywheel [SIM `sim/hybrid_gnss.py`, `out/I_hybrid_gnss_ka.txt`]:** with GNSS carrier-phase sync alone (515 fs per 0.5 s sample), Ka-band (35.75 GHz) sync error is 6.6°. Smoothing over 30–120 s with the chip brings it to **0.6–0.9° (<1°)**. With a space USO the best result is 3.5°, at 10 s, and longer smoothing makes it worse. The model assumes white GNSS noise; multipath or hardware drift would set a floor (not modelled). This turns the existing nominal sync method (Harmony) into a Ka-band-capable one: an upgrade, not a replacement.

## 6. Funding sketch [ASM, to be refined]
- **Seed, about €3–4 M, 18 months:**
  - 2 lab design partners (for example AAU, Fraunhofer HHI) and 1 T&M OEM evaluation.
  - Measured flicker floor and coherence at 140 and 300 GHz versus the simulation.
  - 10 paid units.
- **Series A, about €12–15 M:**
  - ruggedised field version and 1 defence or ISAC pilot,
  - space engineering model with ESA co-funding,
  - OEM option agreement.

## 7. What kills this (test before the pitch if possible)
- **The noise above 1 s is worse than assumed.** The flicker floor itself is bounded at ≤1e-15 by the 1 s spec (flicker is flat in τ); random-walk FM and drift are not. Worst spec-consistent case: 300 GHz coherence 22 s, 60 s image still lossless [SIM J]. A floor of 1e-14 (violates the spec): 7 s.
- **Labs are happy with fibre and cables:** ask AAU and HHI whether more than 300 m untethered matters.
- **Sub-THz research funding fades** as 6G settles on 7–24 GHz. At 7–24 GHz the best quartz holds coherence for about 10 s, so the chip only matters for windows of minutes.
- **Two booth questions for R&S and Keysight before 12:00:** "How do your customers keep TX/RX phase-coherent above 100 GHz without a cable today, and what would they pay for a 120 mW reference that holds 10° at 300 GHz for 30 s?"

## Sources
- SA65 sell sheet; imec challenge PDF; Rakon and Microchip booth transcripts (Kontext/)
- [Iris radio + CSAC one-way tracking, NAVIGATION 71(1)](https://navi.ion.org/content/71/1/navi.633)
- [DLR: GNSS-based phase sync for bistatic/multistatic SAR, IEEE TGRS 2025](https://elib.dlr.de/214099/)
- [TU Delft: data-driven phase sync of Harmony ocean topography](https://repository.tudelft.nl/record/uuid:b944aacc-d91e-4178-8c74-a0c948d5c0ce)
- [OHB €280 M Harmony contract](https://defence-industry.eu/ohb-signs-eur-280-million-contract-with-esa-for-two-earth-observation-satellites/), [Thales Alenia Space Harmony radar](https://www.thalesgroup.com/en/news-centre/press-releases/thales-alenia-space-signs-contract-ohb-develop-two-radar-instruments)
- [Umbra DARPA DRIFT Phase II](https://umbra.space/blog/umbra-advances-to-phase-ii-of-the-darpa-drift-program/), [Via Satellite on DRIFT](https://satellitetoday.com/government-military/2024/05/03/darpa-selects-northrop-grumman-umbra-for-phase-ii-of-drift-program)
- [NYU 142 GHz sounder: PTP-synced Rb clocks](https://arxiv.org/pdf/2309.01006), [158/300 GHz sounder with Rb](https://arxiv.org/pdf/2203.04404), [HHI 300 GHz sounder](https://arxiv.org/pdf/2001.06703), [140/220 GHz sounder](https://arxiv.org/pdf/2311.11546)
- [AAU phase-compensated radio-over-fibre sub-THz sounding](https://core.ac.uk/download/518024236.pdf), [AAU dataset](https://zenodo.org/records/15475728), [300 GHz virtual array](https://www.6gflagship.com/publications/virtual-antenna-array-based-channel-sounding-at-300-ghz-implementation-and-field-measurements/)
- [IEEE SPM 2024: clock asynchronism in bistatic ISAC](https://signalprocessingsociety.org/publications-resources/ieee-signal-processing-magazine/2024/09/sensing-bistatic-isac-systems-clock-asynchronism-signal-processing-perspective)
- [TeraLink sub-THz in-space demo preprint](https://arxiv.org/html/2606.15410v1), [THIS-SAT](https://www.nanosats.eu/sat/this-sat)
- [Ericsson: 6G standardisation milestones](https://www.ericsson.com/en/blog/2026/6/6g-standardization-key-milestones-and-ran-decisions), [RCR: FR3 explained](https://www.rcrwireless.com/20260102/fundamentals/fr3-explained)
- [Sub-THz testbed component costs (vendor FAQ, low confidence)](https://rfessentials.com/rf-knowledge-base/how-do-i-design-a-testbed-for-evaluating-sub-terahertz-communication-links/), [6G testing equipment market (low confidence)](https://www.emergenresearch.com/industry-report/6g-testing-equipment-market)

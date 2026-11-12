# TVA Labs: Coherence where sync is denied or impossible
**VC story v2**, 12 Nov 2026, about 05:30. Rewritten after the VC critique (`VC_story/vc_critique.md`) and the model fix (`sim/README.md`, bug log). Working name from the team deck.
Team: Emmanuele, Sascha, Sagar, Claus [FILL: roles, CV highlights, who goes full-time and when].

Evidence tags: [SIM] auditable simulation in `sim/` (one command, about 30 s; every number below comes from the corrected model) · [INT] our interviews, anonymised except where the organisation gave permission · [SRC] published source (see `research_market_vc.md`, `beachhead_vs_subTHz_ISL.md`) · [ASM] explicit assumption, with the experiment that validates it · [MR] syndicated market research, low confidence.

**What changed from v1:** a noise-generator bug was found and fixed (every quartz comparison softened 2–8x); the wedge is stated narrowly; one thesis in three volumes replaces three stapled businesses; IP, incumbents, unit economics, three revenue cases, the noise envelope and anonymised interviews were added; the L-band space-surveillance radar is no longer claimed as a clock-limited account; "no offensive products" became "protective systems".

---

## 0. One minute
A radar engineer at a Fraunhofer THz centre builds a large aperture from separate modules. Within a minute the modules' references drift apart and the image blurs. Today's fixes are a cable, a fibre with active phase compensation, or a shorter aperture. A multistatic air-defence radar has the same problem at kilometre spacing, and when its GNSS or sync link is jammed it loses coherence within 30 s. A positioning anchor without a wire loses its time within a minute.

Our product is **coherence without a wire**. A chip-scale atomic clock with 1e-15 stability at 1 s (17 cc, 120 mW), packaged with thermal control, magnetic shielding, drift estimation and a low-noise flywheel, keeps separate devices phase-coherent for seconds to minutes at up to 300 GHz, and keeps time to 100 ps for two hours without a sync. The best quartz manages about 1 s at 300 GHz, 30 s of sync outage at X-band, and one minute of 100 ps holdover [SIM].

We **prove** it where the spec is mission-critical (sub-THz measurement, 2027–28), **deploy** it where sync is denied (multistatic sensing under jamming, 2028–31), and make it a **platform** for wireless infrastructure that has no wire to sync over (2031+). Base case: €55 M revenue in 2033, €163 M in 2035. The platform phase is what makes this a €1 B company, and we show the cases without it.

## 1. Technology: what is given, what physics bounds, what we must build
**Given [CHAL]:** ADEV < 1e-15 at 1 s. Everything else at SA65 level: aging 3e-11/day, temperature ±3e-10 over −40 to +80 °C (5e-12/K), magnetic 9e-11/G, 17 cc, 120 mW, MIL-STD-810G vibration.

**One law.** The stability a coherent system needs is **φ / (2π · f · T)**: phase tolerance over carrier frequency × coherence window [SIM `F_fT_map.png`]. Low frequency or short window: quartz is enough. High frequency × long window, or any window with no sync: only this clock. Minimum clock per application [SIM H]:

| Application | Needs (ADEV, 1 s equivalent) | Best quartz (6e-14) enough? |
|---|---|---|
| 300 GHz virtual aperture, 60 s, 10° | 2.1e-15 | no |
| 140 GHz virtual aperture, 60 s | 4.5e-15 | no |
| Ka-band distributed InSAR, 60 s, 1° | 1.8e-15 | no |
| X-band multistatic radar, 100 s sync outage | ~1.6e-14 | no (quartz holds 30 s) |
| L-band radar (space-surveillance class), 100 s | 1.2e-13 | **yes** |
| One-way deep-space Doppler | 3.3e-13 | **yes** |

**What the physics settles.** A flicker-FM floor is flat in averaging time, so the 1 s spec bounds the flicker floor at ≤ 1e-15. That is not our assumption; it is the spec.
**What it leaves open.** Noise that rises above 1 s (random-walk FM, drift, environment); the frozen SA65 numbers say that part is CSAC-class. Worst spec-consistent envelope [SIM J, `floor_envelope.py`]:

| Case | 300 GHz coherence (10°) | 60 s image at 300 GHz | X-band sync outage | Anchor resync for 100 ps |
|---|---|---|---|---|
| Base (floor 7e-16) | 32 s | −0.01 dB | 100 s | 2 h |
| Worst spec-consistent (random-walk FM; 1.8e-14 at 1000 s) | 22 s | −0.02 dB | 100 s | 1 h |
| Sceptic's floor 1e-14 (violates the spec 10x) | 7 s | −0.16 dB | 100 s | 1 h |
| Floor 1e-13 (SA65-class physics; violates the spec 100x) | 0.7 s | −5.8 dB | 30 s | 10 min |
| Best quartz | ~1 s | −3.8 dB | 30 s | 30 min |

The venture survives the worst spec-consistent noise and even a tenfold sceptic. At 1e-13 there is no venture, and no challenge.

**What we must build. The spec alone is not a product; these four items decide the field advantage:**
- **Thermal control to ≤ 5e-14/K residual (99 % compensation).** Without it coherence falls 10x [SIM E]; with 99.9 % the X-band outage tolerance triples (100 → 300 s) [SIM].
- **Magnetic shield** ×100 (lab) to ×1000 (vehicle, orbit): 1 mG uncompensated costs 3x [SIM E].
- **Drift estimation to ≤ 1 %.** Without it the hourly anchor drift is 2.3 ns instead of 35 ps [SIM J]; with drift unestimated or 90 % thermal compensation the chip is no better than a compensated quartz for phases 2 and 3.
- **A low-noise flywheel oscillator.** ADEV 1e-15 at 1 s implies close-in phase noise near −150 dBc/Hz at 1 Hz on 10 MHz, which is inconsistent with the frozen SA65 sheet (−44 dBc/Hz). We take the time-domain spec as given, assume close-in phase noise consistent with it, and add the flywheel for offsets above the atomic loop bandwidth. The model is valid from 0.1 s upward and says so.

**Model validation:** generated noise matches target ADEV within ±7 % across record lengths of 256–8192 samples; the model reproduces JPL's measured one-way Doppler error with a CSAC (11.5 vs 11 mm/s) [SRC, SIM C]; headline results carry P10–P90 bands.

## 2. Where the clock is mission-critical, and where it is not (questions 1, 4, 5)
| Mission-critical: only possible with this clock [SIM] | Good enough with quartz, GNSS or a wire: not our market |
|---|---|
| Separate-module or bistatic apertures at 300 GHz over ≥ 1 min (150 GHz over ≥ 5 min) | Monostatic radar: one clock, no drift problem [INT] |
| Multistatic sensing whose sync is denied longer than quartz tolerates: > 30 s at X-band, > 3 s at W-band | L-band space-surveillance radar: quartz plus GNSS suffices |
| Anchors that cannot resync for > 30 min (35 ps after 1 h; quartz 175 ps) | Wired anchors: an OCXO resyncing each minute meets 100 ps |
| Ka-band GNSS-aided satellite phase sync < 1° (GNSS + chip flywheel: 6.6° → 0.6–0.9°) | Telecom and data-centre holdover: needs aging, frozen at SA65 |
| | Drone TDOA with a good resync link (gain 1.3–16x only); one-way deep-space Doppler |

Market Opportunity Navigator (`sim/navigator.py`, each score with its evidence): sub-THz coherent measurement 28/35 (GTM 14/15); drone anti-spoofing 22; distributed SAR 18; lunar one-way tracking 16; sub-THz inter-satellite links 15. Satellite constellations are explicitly not our route.

## 3. Phase 1, PROVE (2027–2028): sub-THz coherent measurement
**Why here.** It is the only place the spec is mission-critical today, buyers already pay for ultra-stable references, there is no qualification gate, and it produces the measurement that decides everything else: the ADEV curve from 1 to 10⁴ s on a real device.

**Customer and pain.** Fraunhofer Leistungszentrum Terahertzsensorik (named with permission): "Problem with phase drift: with a virtual large aperture, the image gets blurred. Minute range, the longer the better. PLL used to compensate." The same conversation also said that a single-clock system has no drift problem, so the pain is specific to separate-module and multi-site apertures [INT]. They offered a digital LOI and a manager contact. Until a price is on it, the LOI is a signal of interest, not of willingness to pay [FILL: LOI status today].
Published pain [SRC]: a 142 GHz channel sounder resyncs its rubidium clocks every second over PTP and still corrects drift ("ghost multipath"); a Danish group built phase-compensated radio-over-fibre (about 300 m) because fibre phase drifts with bending and temperature; a 2024 IEEE review calls clock asynchronism "a key obstacle" for bistatic sensing.

**Proof [SIM P1, `P1_beachhead_image_blur.png`].** Point target, 300 GHz, 60 s virtual aperture, separate TX/RX references, one sync at the start:

| Reference | Peak loss (median; P90–P10) | Image |
|---|---|---|
| This clock | −0.01 dB (0.00 to −0.02) | identical to the cabled ideal; target shift ≤ 0.2 cell |
| Best quartz (6e-14, rack size) | −4.3 dB (−2.4 to −5.7) | blurred, ISLR +5.7 dB |
| Lab rubidium | −18 dB | incoherent |

Honest limits: at 150 GHz over 60 s the best quartz loses only 1.3 dB; at 300 s our residual frequency error shifts the target 2–4 resolution cells, which the calibration firmware must remove. We claim 60 s at 300 GHz, not "minutes". Non-clock error budget at 300 GHz over 60 s: antenna position 10–50 µm = 3.6–18°, extender thermal drift 0.1–5°, indoor air 1° [SIM R2]. With this clock the system is no longer clock-limited; with quartz the clock dominates by 25x.

**Who pays and what it is worth.** User: the radar or sounding engineer. Economic buyer: the institute's project budget (EU, BMBF, DLR, defence research) or a T&M OEM product manager for an instrument option. A top-3 precision-oscillator maker told us buyers of ultra-stable lab references "don't care much about price", pay around 15,000 for a 6e-14 reference, and that only 4–5 of 10 units pass calibration [INT]. A major timing-IC and atomic-clock vendor pointed us, unprompted, to T&M OEMs as the fit [INT]. A sub-THz chain costs $35–130 k in components [SRC, low confidence]. Price: €25 k per module [ASM]. The customer cost to put in euros today, with Fraunhofer: hours of campaign time lost per blurred aperture, and campaigns that cannot be run untethered at all [FILL].

**Size, stated plainly.** Perhaps 60 organisations worldwide (30–40 sub-THz sounding groups, about 20 THz radar groups, 3 T&M OEMs), one or two units each: €3–4 M lifetime; €0.1 M (2027) to €1.6 M (2029) in our model. **This phase buys proof, data and a reference customer, not revenue.**

**Complete product (question 6), the Coherence Module:** clock; thermal control (≥ 99 %); magnetic shield; flywheel oscillator and low-noise 10/100 MHz distribution for multiplier chains; two-way calibration and drift-estimation firmware; phase-health monitor and API.

**Milestones:** signed LOI → imec engineering samples → measured ADEV 1–10⁴ s and 300 GHz coherence versus the model → 2 paid pilots (Fraunhofer THz plus one 6G sounding lab) → 10 units → 1 T&M OEM evaluation.

## 4. Phase 2, DEPLOY (2028–2031): sync-denied coherent sensing
The same module, ruggedised, inside production multistatic systems whose sync link can be jammed, lost or never installed: deployable and mobile counter-UAS radar at X-band and above, mm-wave multistatic sensing, ISAC pilots.

**Why now.** GNSS spoofing +193 % and jamming +67 % (2025 vs 2023), 59 GPS-loss events per 1,000 flights [SRC, IATA via trade press]. European defence and resilience startups raised a record $8.7 B in 2025; anti-drone startups $1.2 B in 2026 [SRC]. The EIC opened to dual-use in June 2026 [SRC].

**Proof [SIM P2, `P2_scale_outage.png`].** 16 radar nodes combined coherently; longest sync-link outage with ≥ 90 % of ideal gain:

| Reference | X-band | W-band |
|---|---|---|
| This clock, 99 % thermal compensation | 100 s | 30 s |
| This clock, 99.9 % | 300 s | — |
| Best quartz | 30 s | 3 s |
| Rubidium | < 0.1 s | < 0.1 s |

The advantage is 3x at X-band and 10x at W-band, and it is set by the module's thermal engineering. We do not claim it for L-band space-surveillance radar: GESTRA-class systems are quartz-sufficient by our own law. Fraunhofer FHR/GESTRA and its commercial version at Hensoldt are a relationship and a channel, not a clock-limited account.

**Economics.** Fibre at €60/m and 1–5 km node spacing costs €60–300 k per node, 4–20x a €15 k node [SIM, ASM €/m]. Mobile and temporary sites cannot be cabled at all.

**Target accounts (targets, not customers):** counter-UAS and airspace protection (Hensoldt, Rheinmetall, Thales, Saab, Leonardo); critical infrastructure and airports; T&M OEMs (R&S, Keysight, Anritsu); 6G sensing pilots (Nokia, Ericsson; Ericsson has committed $100 M to ISAC, and AT&T/Ericsson demonstrated multistatic drone detection with synchronised sites in July 2026 [SRC]).

**Business model.** Node subsystem (€12 k, falling 8 %/yr) plus a per-node coherence software licence (€1.5 k/yr: sync, calibration, health monitoring). Lock-in through calibration data and integration into the radar processing chain.

## 5. Phase 3, PLATFORM (2031+): coherent wireless infrastructure
**"Where there is no wire, there is still coherence."** Not a CSAC in every device. Infrastructure nodes that have no wire to sync over (mm-wave small cells with wireless backhaul, IAB nodes, deployable networks, vehicles, mesh access points) become one coherent instrument; devices are clients of coherence, not carriers of a vapour cell. Services: positioning, physical-layer authenticity, trusted time.

**Proof [SIM P3].**
- Indoor positioning (50 × 50 m, 8 anchors, line of sight): median error 11.7 m at 50 ns anchor sync, 0.23 m at 1 ns, 3.2 cm at 100 ps, 2.3 cm at 10 ps. Below 100 ps the sync stops being the limit; accuracy is then set by bandwidth and multipath.
- Resync interval to hold 100 ps: TCXO never, standard OCXO 1 min, best quartz 30 min, this clock 2 h. Wired anchors do not need us; wireless, power-limited or deniable anchors do.
- Relay and spoofing detection: at 10 ps any relay adding more than 1.3 cm of path is detected; at 50 ns it must add 64 m. 3GPP-class sync (±50 ns) gives about 15 m of ranging error; O-RAN's ~65 ns cannot deliver sub-metre positioning [SRC]. In the UK, 93 % of recovered stolen cars were taken without keys in 2025 [SRC].
- Trusted time: coherence-derived timestamps signed with post-quantum signatures. Roughtime is now RFC 10049; a post-quantum security vendor we met has no trusted-time product, which is a partnership gap [SRC, INT].

**Plausibility chain.** Infrastructure first: nodes tolerate €300–500 and 120 mW. The US DoD's < $300 CSAC target is an open solicitation, not a result, so the cost-down is a Series B/C milestone tied to imec's wafer-level roadmap, not a promise. 3GPP studies ISAC and positioning; UWB 802.15.4z and Wi-Fi 802.11az already ship secure ranging without a coherent reference.
Markets [MR, low]: RTLS $6.7 B → $15.7 B; UWB $8.5 B → $17.6 B; assured PNT $0.65 B → $2.6 B by 2030.

**Values.** Resilience and sovereignty (a European reference that works when GNSS does not). Privacy by physics (position computed on the device). Open API and protocol. Protective systems (airspace, space safety, critical infrastructure), which keeps us eligible for European dual-use funders.

## 6. Competition and incumbents
| Who | What they have | Why they lose in our wedge | What they could do to us |
|---|---|---|---|
| Microchip | The SA65/SA.45s CSAC line; channels into every defence prime | No 1e-15 physics; a CSAC holds < 0.1 s at 300 GHz | License the imec clock and ship a "coherent CSAC": **the licence is the moat** |
| Safran (Orolia), Rakon, Adtran/Oscilloquartz | Military timing; 6e-14 HSO; ePRTC | Quartz holds 1 s at 300 GHz and 30 s at X-band; rack size; they sell aging, not ADEV [INT] | Bundle with GNSS and White Rabbit; compete on price |
| SiTime | Volume MEMS timing (acquired Renesas timing) | No atomic physics; 1e-10 class | Own the device end of the platform if it ever needs a cheap part |
| Infleqtion, IonQ/Vector Atomic, Mesa Quantum | Optical and next-generation CSACs; DARPA Evergreen about $460 k per clock including development; Mesa $11.8 M seed | Litres and watts, or holdover-focused: a different price class | Race us on the platform phase with better holdover |
| White Rabbit (Safran/Seven Solutions), Meinberg | Sub-ns sync over fibre | Needs fibre; no phase at mm-wave | Good enough wherever a wire exists; we do not compete there |
| Radar primes' in-house sync; GNSS common-view | Direct-path and dedicated-link sync | Fails exactly when the link is denied | Partners and channels, not competitors |

## 7. Business model, unit economics, defensibility (question 7)
| Phase | Offer | Price | COGS [ASM] | Gross margin |
|---|---|---|---|---|
| Prove | Module | €25 k | clock €2–4 k; shield, thermal, RF €1.5 k; test €0.5–1 k | about 75 % |
| Deploy | Node + licence | €12 k + €1.5 k/yr | same, at volume | 55–65 % hardware; about 90 % software |
| Platform | Infrastructure licence / API | per anchor, per call | — | software |

Production test of a 1e-15 clock needs a better reference and hours per unit; the plan is a shared hydrogen maser plus parallel test racks, costed in the COGS line.

**IP and ownership (proposal, to negotiate):** TVA Labs as the imec co-creation spin-off; exclusive field-of-use licence for coherent sensing and wireless infrastructure; wafer supply through the imec pilot line; imec ventures in the seed round. Without exclusivity we are a reseller.

**Moat, in order:** the licence; the thermal, magnetic and drift engineering that sets the field advantage; calibration data and radar-chain integration; per-node software; MIL-STD-810 qualification; later the API network effect.

## 8. Go-to-market (question 8)
1. **2027:** Fraunhofer THz (LOI → paid pilot), one 6G sounding lab, one T&M OEM evaluation. Institute budgets, direct sales, no qualification gate.
2. **2028–29:** field pilot with a deployable multistatic radar (mobile counter-UAS) and one mm-wave multistatic or ISAC testbed; MIL-STD-810 qualification on the SA65 heritage.
3. **2029–31:** primes and T&M OEMs as integrators; per-node software sold direct.
4. **2031+:** standards (3GPP ISAC and positioning, IETF trusted time) and infrastructure licences through RAN vendors.

Connections: imec (clock, roadmap); Fraunhofer THz → FHR → Hensoldt (channel); Infineon (track partner) and a PQC vendor for trusted time; Ericsson/AT&T ISAC; free-space-optical link vendors for fibre-free coherent backhaul; NATO DIANA (GNSS-denied PNT challenge 2026), NIF, EIC dual-use, ESA BIC.

## 9. Funding plan (question 9)
| Round | Amount | When | Use of funds | Proof that unlocks the next round |
|---|---|---|---|---|
| **Seed** | €4 M + €1.5–2 M non-dilutive (EXIST/BMBF, ESA BIC) | Q2 2027 | 8 FTE; module v1 on imec samples; 2 pilots | measured ADEV 1–10⁴ s at or below the random-walk envelope; 300 GHz ≥ 20 s demonstrated with Fraunhofer; 10 units / ≥ €0.5 M bookings; exclusive licence signed; 1 OEM evaluation |
| **Series A** | €15 M + up to €2.5 M EIC Accelerator | late 2029 / early 2030 | ruggedised node, qualification, 2 field pilots | ≥ 10 paying customers; €1.5–2 M revenue plus ≥ €5 M backlog; licence on > 50 % of nodes |
| **Series B** | €60 M | 2031 | volume manufacturing with imec/foundry; ISAC base-station pilot; API beta; PQC trusted time with a security partner | €20–40 M revenue; 1,000+ nodes; first infrastructure contract |

**Three revenue cases [SIM R3, ASM inputs], € M:**

| Case | 2029 | 2031 | 2033 | 2035 | Value at 5–10x 2035 revenue |
|---|---|---|---|---|---|
| Base: deploy + platform | 1.6 | 12.3 | 55 | 163 | €0.8–1.6 B |
| Deploy only | 1.6 | 12.0 | 41 | 76 | €0.4–0.8 B |
| Slow deploy | 1.2 | 5.3 | 15 | 27 | €0.1–0.3 B |

Multiples: SiTime trades at 22x revenue, a peak-cycle number for a profitable volume company; Infleqtion at 39x is a pre-profit SPAC; we underwrite 5–10x. Timing-component exits have historically been below $1 B (Symmetricom to Microsemi, $230 M, 2013; Orolia to Safran, 2022, price undisclosed; both from memory, verify), so only the platform phase earns a platform multiple, and we show the cases without it. Benchmarks: FMC's path (Series B $20 M led by M Ventures and imec.xpand; about €100 M Series C in 2025); Mesa Quantum $11.8 M seed; European medians: deep-tech deal €4.4 M, Series A > €14 M, Series B €29.6 M [SRC].

## 10. Team [FILL]
Emmanuele, Sascha, Sagar, Claus: roles, one CV line each, who goes full-time and when. Gaps an investor will look for: someone who has shipped a precision oscillator product; someone who has sold to a radar prime; an advisor from imec's clock group. First three hires: RF/timing lead, radar systems engineer, defence business development. Credential from this week: 18 organisations contacted in three days, about 10 substantive interviews, beachhead pivoted on the evidence.

## 11. Validation (the 2x criterion)
**Simulation.** `sim/` reproduces every number in this document in about 30 s. Inputs are tagged sourced, challenge or assumed; competing architectures are modelled (quartz, rubidium, GNSS sync, fibre); non-clock noise is included (temperature, magnetic, drift, link, positioner, air); sensitivity sweeps and a bug log are part of the record.

**Interviews (anonymised; stakeholder types: supplier, integrator, end user, security vendor, GNSS maker, T&M OEM):**

| # | Who (role) | What we learned | What changed |
|---|---|---|---|
| 1 | A major timing-IC and atomic-clock vendor | "Not really" on customer demand for better short-term stability; pointed to T&M OEMs | Dropped the component-upgrade framing; T&M channel |
| 2 | A top-3 precision-oscillator maker | 6e-14 at 1 s exists; demand for better is "very rare"; lab buyers price-insensitive; telecom buys aging | Dropped telecom holdover; set the quartz benchmark |
| 3 | Fraunhofer THz radar centre (named with permission) | Phase drift blurs multi-module apertures over minutes; LOI offered; GESTRA's modular expansion | Beachhead confirmed and narrowed to separate-module apertures |
| 4 | A GNSS module maker | "It has to be a universal system"; OCXO when the signal is lost | Platform complements GNSS |
| 5 | An RF front-end major | "If you dig deep enough, it's all about timing"; GPS loss forces reduced bandwidth | Resilience framing |
| 6 | A post-quantum security vendor | PQC secure elements; no trusted-time product | Trusted-time pillar |
| 7 | An optical-interconnect startup | 2–10 cm on-board links | Excluded |
| 8 | A drone-radar integrator and a radio-triangulation company | "Higher clock speed → better triangulation" (speed, not stability) | Treated as hearsay; drone TDOA demoted |
| 9 | A T&M OEM | Missiles, encryption, high-precision radio are small markets | Beachhead sized honestly |

**How the concept changed:** holdover → short-term coherence (1, 2); drone-TDOA beachhead → demoted after the link-noise critique; telecom → excluded except through positioning and ISAC; satellites → excluded (crowded); "better than quartz everywhere" → "mission-critical at 300 GHz × 1 min, or wherever sync is denied" after the model fix; "a CSAC in every device" → infrastructure first, devices as clients.

## 12. Risks and the experiment for each
| Risk | Experiment or requirement |
|---|---|
| Noise above 1 s worse than assumed (the flicker floor is bounded by the spec; random-walk FM, drift and environment are not) | Ask imec today what the ADEV does beyond 1 s; measure 1–10⁴ s on the first samples (seed milestone 1). The worst spec-consistent case costs the beachhead a third of its coherence time and nothing else [SIM J] |
| Drift estimation or thermal compensation fails (drift unestimated, 90 % compensation): the chip is then no better than a compensated quartz for phases 2 and 3 [SIM J] | Product requirements: drift estimated to ≤ 1 %; residual temperature sensitivity ≤ 5e-14/K; demonstrated in the module before Series A |
| Labs stay with cables | Priced LOI with Fraunhofer and two labs; the untethered use cases named by them |
| imec licenses non-exclusively | Exclusive field-of-use licence as a seed condition |
| Sub-THz 6G slips (3GPP Rel-21 focuses on 7–24 GHz) | Beachhead anchored in radar, 6G as the second segment |
| Platform needs a 10–30x cost-down | Infrastructure first at €300–500 per node; device-scale integration tied to imec's roadmap as a Series B/C milestone |
| Fraunhofer pain is softer than quoted (single-clock systems have no problem) | Claim only separate-module and multi-site apertures; get two numbers today (drift in °/min, hours lost per campaign) |
| Positioning claims ignore multipath | Claim only "sync stops being the limit below 100 ps"; accuracy from bandwidth and multipath |

## 13. Asks today
- **imec:** what does the ADEV curve do beyond 1 s, and does freezing aging and temperature mean the long-term is CSAC-class? Engineering samples; a licence term-sheet conversation.
- **Fraunhofer THz:** sign the digital LOI; two numbers: drift today in degrees per minute, and hours lost per campaign.
- **R&S and Keysight at their booths:** how do customers keep TX and RX phase-coherent above 100 GHz without a cable today, and what is a 120 mW reference that holds 10° at 300 GHz for 30 s worth?

## Sources
Simulation outputs in `sim/out/`, run instructions and bug log in `sim/README.md`. Published sources with URLs, dates and credibility ratings in `VC_story/research_market_vc.md` and `beachhead_vs_subTHz_ISL.md`. Interview notes in `Kontext/SEMICON Hackathon 2/` (internal; anonymised here).

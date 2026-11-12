# Red-team review of the VC story, through the jury's eyes
12 Nov 2026, about 04:00. Sources: `Kontext/…/NextSEMI-Hackathon-2026-Jury-Research-Challenge-Forecast.pdf`, plus web checks (links at the end), plus our own re-checks in `sim/redteam_checks.py` (`out/R_redteam_checks.json`).

## 0. Verdict in five lines
1. **Strongest asset:** validation. The simulations are auditable, and we have one external model validation (JPL Iris). This is the 2x criterion, and we are ahead of most teams.
2. **Biggest risk: "this is not a VC story yet."** Selling €25k modules to a few radar institutes is grant-funded and small, and the beachhead is not tied to the €1B outcome with numbers. Fixed partly now (bottom-up R3), but the slide must say so plainly.
3. **Most dangerous rookie mistakes:**
   - We never say **who owns the clock**: imec licence or spin-off. For imec ventures as challenge owner, that is the first question.
   - **Incumbents** (Microchip makes the SA65 and could build our module; White Rabbit for sub-ns sync) are missing.
   - **Our own metrics contradict each other** (10° coherence time vs. image loss), unless explained.
4. **Too technical for the final jury:** ISLR, flicker floor and ADEV belong in backup. One law, one image, one number.
5. **Fix in the next 3 hours** (§5): ownership slide, incumbent slide, revenue ladder, anonymise interviews, align the TVA deck (it still says drone anti-spoofing and "300,000x").

## 1. Who judges, and how they will test us
| Juror | Background (public, professional) | What they will check | How they will check |
|---|---|---|---|
| **Bruno Iafelice** (track) | Chair of the IEEE Hard Tech Venture Summits; TVLP Institute; Stanford instructor; hard-tech VC networker. His summits are vetted by "investors who understand engineering, capital requirements, system-level complexities". | Investability, capital intensity vs milestones, international ambition, pitch clarity | "How much capital to first revenue? To break-even?"; due-diligence checklist style |
| **Helen Kardan** (track) | Director Science & Technology, High Tech Industry, TNO; ex-ASML Senior Manager New Business Development; ex-Freescale marketing; NWO valorisation committee | Business-model sharpness, ecosystem fit (imec/TNO/ASML world), whether the beachhead is a real buying unit | "Who signs the PO? Which budget line? What did they say about price?" |
| **Thomas Schiml** (final) | 30+ years Intel/Infineon (Senior Director Foundry Enablement), CDL and ignite next mentor; RF processes, packaging | Manufacturability, supply chain, cost-down path for a 1e-15 clock, yield and **test cost** | "How do you test 1e-15 in production? You need a better reference and hours per unit." "Who fabs it?" |
| **Stefan F. Müller** (final, warm contact; approach professionally) | Co-founder and ex-CEO/CTO of FMC (TU Dresden spin-off, 14 years to market): $20M Series B led by **imec.xpand**, about **€100M Series C** in 2025 (€77M equity + €23M public); boOst semiconductor track | Realism of the timeline and rounds; the IP and licence relationship with imec; non-dilutive stacking | Compares our €4M / €15M / €60M with FMC's path and asks for the IP structure |
| **Betsy Lindsey** (final) | Co-founder and CFO of Aircision (free-space optics telecom, TNO venture portfolio, "quantum-secure coherent engine"); TU/e Quantum Delta business developer. **Probably the juror who suggested telecom and PQC.** | CFO lens: unit economics, gross margin, revenue ramp vs burn; telecom/backhaul logic | Asks for COGS, margin and a revenue table; will test our telecom rejection |
| **Cassandra Melvin** (final) | SEMI Europe Senior Director; EU Pact for Skills; Chips Diversity Alliance | European sovereignty, jobs and skills, team diversity, presentation | Listens for "Europe", "sovereign", "talent"; team slide |
| **Michael Machold** (final) | Operational Director, TUM Venture Labs Quantum/Semicon | Will the team actually found? Spin-off potential, coachability | "Who goes full-time when? What happens Monday?" |

## 2. What they would find: issues ranked by severity
| # | Severity | Finding | Who catches it | Fix |
|---|---|---|---|---|
| 0 | **Critical (found during the VC pass, 04:20)** | **Model bug.** The flicker generator's amplitude depended on record length; scenarios with short records had 2–8x too much flicker. Fixed, re-run, all documents corrected (`sim/README.md`, bug log). Chip results barely moved (they are environment-limited), but every quartz comparison softened: HSO 1 s not 0.46 s at 300 GHz; X-band outage 30 s not 3 s; OCXO anchor 44 ps not 170 ps per minute. The mission-critical band is narrower than first claimed. | A reproducing juror | Done. State the corrected numbers; never show the old ones. |
| 1 | **Critical** | **No ownership/IP model.** The challenge clock is imec's. If imec licenses it to Microchip, Safran or SiTime, we are a reseller. imec ventures' own model is "creation and co-creation" of spin-offs from imec IP (challenge transcript). | Müller, imec/track jury | Slide: "We are the imec co-creation spin-off. **Exclusive field-of-use licence: coherent sensing and networks**; imec ventures in the seed; wafer supply through imec pilot line." |
| 2 | **Critical** | **Incumbents missing:** Microchip (owns the CSAC line, could ship a "coherent CSAC"), Safran/Orolia, Rakon, SiTime (MEMS; bought Renesas timing), Adtran/Oscilloquartz; the radar primes' own synchronisation; **White Rabbit** (CERN, sub-ns over fibre); GNSS common-view | Schiml, Kardan | Competitor slide: our wedge is *wireless coherence at mm-wave for minutes*. White Rabbit needs fibre; Microchip lacks the 1e-15 physics; primes are partners, not competitors. |
| 3 | **High** | **Our own metrics contradict each other.** At 300 GHz over 60 s the chip has 20° rms phase error [R2], above the 10° tolerance (coherence 31.6 s), yet the image loses only −0.01 dB [P1]. Reason: most of the error is a linear ramp that **shifts** the target instead of blurring it. Simulated shift: 0.06 cells median, 0.19 cells P90 at 60 s; but **1.8 cells median, 3.8 cells P90 at 300 s** (200 runs). | Any technical juror, imec | Footnote: "Blur ≠ shift. At 60 s: blur −0.01 dB (0.00 to −0.02), shift ≤0.2 cell. At 300 s: sharp, but shifted 2–4 cells unless a reference target recalibrates it, which belongs in the calibration firmware." Claim **60 s**, not "minutes", as the headline. |
| 4 | **High** | **Revenue figures were inconsistent** (€70–100M in 2033 claimed vs €55M bottom-up). Now fixed: €55M (2033), €163M (2035), unicorn about 2035 *with* the vision [R3]. Scale-only is €0.4–0.8B. | Lindsey, Iafelice | Done in VC_story and slides; show the revenue ladder chart. |
| 5 | **High** | **The beachhead pain is softer than we claim.** Fraunhofer THz also said: "single clock: TX and RX in the same system, so no problem with drift", "clock speed: no idea", "PLL used to compensate". No price was discussed; the LOI is not signed. | Kardan, Machold | Say precisely: "pain appears with **separate modules / multi-site** apertures, which is where GESTRA is going". Get the digital LOI signed today and ask: "how many degrees of drift per minute today, and what would you pay to remove it?" |
| 6 | **High** | **Not anonymised.** The brief asks for anonymised interview summaries; we name companies (and one person, in the notes) alongside quotes. Only Fraunhofer gave permission to be named. | Organisers | Use roles: "a top-3 oscillator vendor", "a GNSS module maker", "an RF front-end major". |
| 7 | **High** | **The TVA deck is inconsistent with the new story.** It still says drone anti-spoofing beachhead, "300,000x better" (true only at τ = 1 s; about 10,000x at 1000 s and equal over days), Fraunhofer FHR as "space debris radar expansion". | Everyone | Rewrite S1–S4 of the deck to the coherence story; replace "300,000x" with "100x longer coherence at 300 GHz than the best quartz" [SIM B]. |
| 8 | **Medium** | **No COGS, gross margin or production test cost.** A 1e-15 clock needs a better reference and long test times; Rakon gets only 4–5 of 10 HSO units through calibration [INT]. | Schiml, Lindsey | Unit-economics box [ASM]: clock supply €2–4k, shield/thermal/RF €1.5k, test €0.5–1k → €12k node at ~55–65% gross margin; test with a shared H-maser plus parallel test racks. |
| 9 | **Medium** | **The vision has an unaddressed cost-down gap.** Anchors at €120 by 2032 (R3) need a 10–30x cost-down from CSAC prices (about $1.5–10k); the DoD LC-CSAC target is <$300. | Schiml | Say it: infrastructure first at €300–500 (base stations tolerate it); devices only with imec wafer-level integration. Treat it as a Series B/C milestone, not a promise. |
| 10 | **Medium** | **Vision positioning overclaims** (2.3 cm). It assumes line-of-sight, independent anchor errors and no multipath. Indoors, multipath and bandwidth dominate once sync is ≤100 ps. | Technical jurors | Claim "sync stops being the limit (≤100 ps); accuracy then set by bandwidth/multipath: cm with 1 GHz UWB-class". |
| 11 | **Medium** | **Values vs customers:** "no offensive targeting products" while naming Rheinmetall/Hensoldt. | Melvin, Iafelice | Rephrase: "We build *protective* systems: airspace, space safety, critical infrastructure". |
| 12 | **Medium** | **False precision.** "31.6 s", "−0.02 dB", "2.3 cm" come from a coarse grid (±1.5x) and 20–40 Monte Carlo runs. | Kardan (ASML-style rigour) | Ranges: chip at 60 s: 0.00 to −0.02 dB (P90–P10, 200 runs); at 300 s: −0.05 to −4.3 dB. Coherence time "≈ 20–45 s". |
| 13 | **Medium** | **Telecom rejection may annoy the juror who suggested it.** | Lindsey | Frame as respect: "We tested it: holdover is frozen at SA65 level by the challenge; telecom enters through positioning, ISAC and **fibre-free coherent backhaul** (free-space optics + coherence)." That last item ties to her Aircision background. |
| 14 | **Medium** | **PQC is only one bullet** although the track is "Quantum-Ready Semicon" with Infineon/FOCAL as sponsors. | Track jury | One vision line: "time is a security primitive: spoof-proof physical-layer authentication + PQC-signed timestamps (Infineon/SEALSQ secure elements)". |
| 15 | **Low** | Market sizes are syndicated (low confidence) and top-down; TAM ≠ PMF (a named guardrail). | Kardan | Lead with bottom-up node counts; market reports only as context. |
| 16 | **Low** | The beachhead was moved from 6G labs, while 3GPP Rel-21 focuses on 7–24 GHz. | Informed jurors | Anchor the beachhead on radar (Fraunhofer) and mention 6G only as a second segment. |

## 3. Is it a VC story? Ambition and numbers
- **VCs want:** a large outcome (≥10x fund return potential), a clear wedge to scale, capital efficiency per milestone, defensibility, and a team. We now have:

  | Case | Revenue | Valuation |
  |---|---|---|
  | Base, with vision | €163M (2035) | €1–1.6B |
  | Scale only | €76M (2035) | €0.4–0.8B |
  | Slow scale | €27M (2035) | small |

- **Weakness:** the unicorn depends on the most speculative phase. That is normal for deep tech, but say it and show the **leading indicators** that de-risk the vision early: an ISAC pilot with a RAN vendor by 2031, and an imec cost-down roadmap.
- **"Is selling to a few radar centres enough?"** No, and it isn't meant to be. Make the logic explicit: beachhead = proof and reference (€1–2M); scale = **thousands of nodes per year** (R3: 3,500 nodes in 2033, only 0.09% of the European counter-UAS market in 2030, so there is upside); vision = infrastructure licence.
- **Ambition statement for the final:** "Every radio becomes part of one coherent instrument. We start with the radars Europe needs to protect its skies and orbits."

## 4. Criteria scorecard (max 30) and strategic gaps
| Criterion (weight) | Now (estimate) | With the fixes | What moves it |
|---|---|---|---|
| Technical feasibility (1x) | 3.5/5 | 4.5 | Non-clock budget (R2: positioner 3.6–18°, thermal 0.1–5°, air about 1°, so the system is no longer clock-limited), test-cost answer, flicker floor as milestone 1 |
| Innovation (1x) | 4/5 | 4.5 | The f×T law + "coherence without cables" category; the GNSS + chip flywheel |
| Market potential (1x) | 3/5 | 4 | Bottom-up revenue ladder; scale and vision TAM via node counts; ambition statement |
| Business viability (1x) | 2.5/5 | 4 | **IP/licence with imec**, unit economics, incumbent slide, round logic |
| Validation (2x) | 4/5 → 8 | 4.5 → 9 | Signed LOI, anonymised interview table with "how we changed", uncertainty bands, external model validation (Iris) |
| **Total** | **≈ 21/30** | **≈ 26/30** | |

These estimates are judgement, not a measurement.

## 5. Fix list before 12:00, in priority order
1. **imec ownership slide** (co-creation spin-off, exclusive field-of-use licence, imec ventures in the seed). 15 min.
2. **Competitor/incumbent slide** (Microchip, Safran, Rakon, SiTime, White Rabbit, primes' synchronisation), with our wedge. 20 min.
3. **Get the Fraunhofer digital LOI signed**, plus two numbers: drift today (°/min) and what it is worth. Ask R&S or Keysight the price question. Booth time.
4. **Rewrite the TVA deck S1–S4:** drop "300,000x" and drone-first; use the f×T law, the image, the Fraunhofer quote. 45 min.
5. **Revenue ladder + unit economics** on one slide (R3 base / scale-only / slow; COGS box). 20 min.
6. **Anonymise interviews** (roles only, except Fraunhofer). 10 min.
7. **Footnotes:** blur vs shift; uncertainty ranges; positioning claim limited to "sync no longer limits". 10 min.
8. **Team slide** with founding commitment (who full-time, from when). Ask Claus for CVs.
9. Move ISLR, ADEV, flicker floor and the Monte Carlo details to the **backup/appendix**.

## Sources (jury)
- Jury research PDF in `Kontext/SEMICON Hackathon 2/`
- [IEEE ITeN: Lab to Market, Hard Tech Venture Summit](https://iten.ieee-ies.org/featured-news/2026/from-lab-to-market-why-the-hard-tech-venture-summit-matters-for-electronics-engineers/), [HTVS Silicon Valley](https://entrepreneurship.ieee.org/venturesummitsiliconvalley), [Iafelice: Want to launch a hard tech venture?](https://iten.ieee-ies.org/featured-news/2025/want-to-launch-a-hard-tech-venture-do-it-now)
- [FMC $20M Series B, led by M Ventures and imec.xpand](https://www.eenewseurope.com/en/ferroelectric-memory-startup-raises-funds/), [FMC ~€100M Series C](https://www.startbase.com/news/fmc-sichert-100-millionen-euro-fuer-neue-speicherchip-standards/), [Blocks & Files on FMC](https://www.blocksandfiles.com/ai-ml/2025/11/14/fmc-gets-feram-cash-to-kill-optanes-ghost/1704708)
- [Aircision at TNO ventures](https://ventures.tno.nl/portfolio/aircision/), [Aircision + EFFECT Photonics coherent FSO](https://www.photondelta.com/news/aircision-and-effect-photonics-to-jointly-develop-coherent-technology-for-free-space-optics/), [HighTechXL: Aircision](https://www.hightechxl.com/?p=5778)
- [CDL mentor profile: Thomas Schiml](https://creativedestructionlab.com/mentors/thomas-schiml/)

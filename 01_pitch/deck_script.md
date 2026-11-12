# Deck script: stage version (5 min), workspace extras, appendix
Format from the organisers: finalists pitch **5 minutes + 5 minutes Q&A** on the SEMICON stage; round 1 is a technical review at the workspace (13:00). So one deck, three sections: **Stage (S1–S10, 5:00)**, **Workspace extras (W1–W5)** shown at the desk, **Backup (B1–B17)** for questions (`backup_slides.md`). Figures in `figures/`. Every number is from the corrected model (`03_sim/`); keep the source footnote in 9 pt.

Speaker lines are verbatim and timed; C = Claus, S = Sascha. Total 300 s with a 15 s buffer.

---
## S1 · Title · 0:00–0:20 · C
**Visual:** black slide, one line, the matchbox-sized clock as a photo or outline (SA65 is 41 × 35 × 11 mm, 16 cc: a matchbox).
**On slide:** TVA Labs — *Coherence where sync is denied or impossible.*
**C:** "Sascha's watch and mine have drifted apart by about a millisecond since we walked up here. Nobody noticed. If our watches were two halves of a radar, we would have lost the target before I finished this sentence. We fix that, without a wire."

## S2 · Problem · 0:20–0:50 · C
**Visual:** the Fraunhofer quote large; three small proof points beneath.
**On slide:** "Phase drift: with a virtual large aperture, the image gets blurred. Minute range, the longer the better." — Fraunhofer Leistungszentrum Terahertzsensorik · A 142 GHz lab resyncs its atomic clocks every second and still sees ghost echoes · Fibre needs active phase compensation and stops at 300 m · IEEE 2024: clock asynchronism is "a key obstacle" for bistatic sensing.
**C:** "Whenever two radios must act as one instrument, their clocks drift apart. Today you run a cable, a fibre, or you accept blur. A Fraunhofer radar centre told us this on Tuesday in exactly these words. [FILL if the LOI is signed: 'This morning they confirmed it in writing.']"

## S3 · One law, and where we are useless · 0:50–1:20 · C
**Visual:** left: the formula big; right: two columns, "only our clock" / "quartz is fine". Footnote: `F_fT_map.png` in the appendix.
**On slide:** stability needed = φ / (2π · f · T). Only our clock: 300 GHz × 1 minute; sync denied > 30 s at X-band; anchors with no wire. Quartz is fine: monostatic radar, L-band radar, wired anchors, telecom holdover, deep space.
**C:** "One law decides where a better clock matters: carrier frequency times coherence window. We spent two days finding out where our clock is useless, and we put the list on the slide. Everywhere on the right, quartz and a sync link are good enough. Everywhere on the left, only this clock works."

## S4 · Proof: the image · 1:20–1:50 · C
**Visual:** `P1_beachhead_image_blur.png` full-bleed; a three-row table overlay.
**On slide:** 300 GHz, 60 s aperture, no cable. This clock −0.01 dB (cable-identical) · best quartz −4.3 dB (blurred) · rubidium incoherent. Footnote: median, P90–P10 bands; at 150 GHz quartz loses only 1.3 dB.
**C:** "Here is the radar image of a point target at 300 GHz over a one-minute aperture, transmitter and receiver on separate clocks, synced once at the start. Black is the cabled ideal. Green, our clock, sits on top of it. Orange is the best quartz oscillator money can buy, rack-sized: blurred. Blue is a lab rubidium: gone."

## S5 · Phase 1 · Prove (2027–28) · 1:50–2:20 · S
**Visual:** three icons (lab, module, LOI); a plain size statement.
**On slide:** Sub-THz coherent measurement · Buyers: institute budgets, T&M OEM option (R&S, Keysight) · Lab reference buyers are price-insensitive (top-3 oscillator maker) · Module €25 k · About 60 organisations, €3–4 M lifetime: **this phase buys proof, data and a reference customer, not revenue** · Traction: Fraunhofer THz, LOI [status].
**S:** "We start where only this clock works and where buyers already pay for references. It is a small market and we say so: sixty organisations worldwide. It buys us proof, a reference customer, and the one measurement that decides everything, the real noise curve of the chip."

## S6 · Phase 2 · Deploy (2028–31) · 2:20–2:55 · S
**Visual:** `P2_scale_outage.png` left; three bullets right.
**On slide:** Sync-denied coherent sensing · 16-node X-band radar keeps coherence through a 100 s sync outage (quartz 30 s); W-band 30 s vs 3 s · Fibre per node at km spacing: 4–20x the module; mobile sites cannot be cabled · Why now: GNSS spoofing +193 %, jamming +67 %; record $8.7 B for European defence and resilience startups · Targets: mobile counter-UAS primes, airports, T&M OEMs, 6G sensing pilots (Ericsson, $100 M) · Node €12 k + €1.5 k/yr licence.
**S:** "Then the same module goes into multistatic radars whose sync link can be jammed. Sixteen nodes, link cut: quartz holds thirty seconds, we hold a hundred, three hundred with better thermal control. That is coherence surviving the jammer. Node plus software licence; recurring revenue starts here."

## S7 · Phase 3 · Platform (2031+) · 2:55–3:30 · S
**Visual:** a city skyline with wire-free nodes glowing; a three-row table.
**On slide:** "Where there is no wire, there is still coherence." · Resync interval for 100 ps: standard OCXO 1 min, best quartz 30 min, this clock 2 h · Indoor positioning 11.7 m → 2.3 cm · Relay attacks adding > 1.3 cm of path are detected · Post-quantum-signed trusted time · Values: resilient, private by physics, open, protective.
**S:** "The platform: infrastructure that has no wire to sync over, mm-wave small cells, deployable networks, vehicles, becomes one coherent instrument. Devices are clients, not clock carriers. Centimetre positioning computed on your phone, not in the network. Relay attacks caught at one centimetre. Time you can trust, signed post-quantum."

## S8 · Why we win · 3:30–4:00 · S
**Visual:** incumbents in a row with one line each; the IP box.
**On slide:** Microchip owns the CSAC line, not the 1e-15 physics: **the licence is the moat** · Quartz: 1 s at 300 GHz · Optical clocks: $460 k and litres · White Rabbit: needs fibre · Product requirements that set the field advantage: thermal ≥ 99 %, drift ≤ 1 %, shield, flywheel · imec co-creation spin-off, exclusive field-of-use licence.
**S:** "Who stops us? Microchip, if they get the licence. So the licence is the moat, and imec ventures is in our seed round. After that it is engineering nobody has done: thermal and drift control that turns a lab spec into a field advantage. We know exactly which four things, because the model told us."

## S9 · The money · 4:00–4:30 · S
**Visual:** three rounds on a timeline; three revenue lines.
**On slide:** Seed Q2 2027 €4 M + €1.5–2 M non-dilutive · Series A late 2029 €15 M + EIC · Series B 2031 €60 M · Revenue 2035: base €163 M (platform) → €0.8–1.6 B at 5–10x; deploy only €76 M; slow €27 M · Comparables: SiTime 22x (peak), Mesa Quantum $11.8 M seed, FMC's imec.xpand-led path.
**S:** "Three rounds, each unlocked by a measurement, not a promise. Three revenue cases; we show you the one without the platform too, because timing-component companies have never been unicorns. Platforms have."

## S10 · Validation, team, ask · 4:30–5:00 · C
**Visual:** left: "how we changed our minds" as five strike-throughs; centre: team photos; right: the ask.
**On slide:** Killed: holdover, telecom, drone-TDOA, satellites, "better than quartz everywhere" · Model reproducible in 30 s, validated against a JPL measurement, bug log included · 10 anonymised interviews, 7 stakeholder types · Team [FILL] · Ask: imec samples and a licence conversation; Fraunhofer LOI; seed €4 M · repo: [URL]
**C:** "At four this morning we found a bug in our own model, fixed it, and corrected every number you have seen. That is what validation means to us. We killed five of our own ideas to find the one place only this clock works. We are Emmanuele, Sascha, Sagar and Claus. We would like imec's samples, Fraunhofer's signature, and four million euros. Thank you."

---
## Workspace extras (13:00 technical review; show at the desk after S1–S10)
**W1 · Technology honesty:** flicker floor bounded by the spec (flat in τ); the noise-above-1-s envelope table (base 32 s / worst spec-consistent 22 s / sceptic 7 s / quartz ~1 s at 300 GHz); milestone 1 = measured curve 1–10⁴ s.
**W2 · What we must build:** thermal 99 % (×10), shield ×100 (×3), drift ≤ 1 % (35 ps vs 2.3 ns per hour), flywheel (phase-noise statement).
**W3 · Where 1e-15 buys nothing:** the full two-column table from `VC_story.md` §2; navigator scores.
**W4 · Model:** architecture diagram (noise generator → two clocks → causal frequency estimate → residual phase at carrier → metric), validation (generator ±7 % across n; JPL 11.5 vs 11 mm/s), limitations, bug log.
**W5 · Interviews:** the anonymised table with "what changed" (from `04_validation/interviews_anonymised.md`).

Live demo at the desk: Emmanuele runs `floor_envelope.py` (5 s) and `scenarios.py` block B with a juror-chosen carrier.

## Appendix / backup
See `backup_slides.md` (B1–B17), each mapped to an expected question.

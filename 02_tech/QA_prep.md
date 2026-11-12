# Jury Q&A prep: hard questions, evidence-backed answers
Keep each answer to about 20 seconds: claim → number → source.

**1. "Monostatic radars don't have drift problems. Why do radar people need you?"**
Correct. A single-clock radar is fine; the Fraunhofer THz contact said the same [INT]. The pain appears when the aperture is built from **separate modules or separate TX/RX sites** over minutes, as in GESTRA-style modular arrays, bistatic/multistatic setups and untethered sounders. That is where they told us images blur [INT]. Our simulation shows the blur: 300 GHz, 60 s, HSO −4.3 dB, chip −0.01 dB [SIM P1].

**2. "Why not just run fibre?"**
- In the lab, at short range, fibre works.
- At kilometre spacing, fibre costs €60–300k per node, 4–20x our module [SIM P2, ASM €/m].
- Fibre phase drifts with bending and temperature; Aalborg needs active compensation [SRC].
- Mobile or temporary nodes can't be cabled.

**3. "Isn't a good OCXO enough?"**
Below about 10 GHz with second-scale windows, yes, and we say so on our "where 1e-15 buys nothing" slide. At 300 GHz the best quartz holds about 1 s, the chip 31.6 s [SIM B]. The minimum needed for 300 GHz over 60 s is 2.1e-15 [SIM H].

**4. "The challenge freezes aging and temperature at SA65 level. Does your claim survive that?"**
Yes. The model includes SA65 aging (3e-11/day), temperature (5e-12/K) and magnetic sensitivity (9e-11/G). They are deterministic and compensable, which is why the module contains thermal control, a magnetic shield and drift estimation. Without them coherence drops 3–10x [SIM E]. Over days, the chip is no better than an SA65: we don't sell holdover.

**5. "What if imec's flicker floor isn't 1e-15?"**
Two parts. **Physics:** a flicker-FM floor is flat in averaging time, so the challenge's own ADEV ≤1e-15 at 1 s bounds the flicker floor at ≤1e-15; that is not our assumption, it is the spec. **What the spec leaves open** is the noise that rises above 1 s (random-walk FM, drift, environment), and the frozen SA65 aging and temperature numbers say that part is CSAC-class. We simulated the worst spec-consistent case [SIM J]: 300 GHz coherence drops from 32 s to 22 s, the 60 s image is still lossless (−0.02 dB; quartz −3.8 dB), the X-band sync-outage tolerance stays at 100 s, and the anchor resync interval goes from 2 h to 1 h. If you insist on a floor of 1e-14, which violates the spec tenfold, the beachhead keeps 7 s at 300 GHz and the scale and vision phases are intact. At 1e-13 there is no venture, and no challenge either. The two things that actually decide the field advantage are under our control: drift estimation and thermal compensation (κ_T ≥ 0.99); without them the chip is no better than a compensated quartz. Milestone 1 of the seed is the measured curve from 1 to 10⁴ s.

**6. "Telecom is huge. Why not telecom?"** (juror suggestion)
Telecom pays for holdover over hours to days (ePRTC: <100 ns over 14 days). The challenge fixes long-term performance at SA65 level, which misses that by about three orders of magnitude [SRC: market-value ranking]. Rakon's telecom customers buy aging performance, not ADEV [INT]. We enter telecom through **positioning and ISAC** in the vision phase, where sub-ns coherence matters [SIM P3].

**7. "Where's PQC?"** (juror suggestion)
In the vision: trusted time. Coherence-derived timestamps are signed with post-quantum signatures, and physical-layer timing detects relays. SEALSQ (PQC, secure IoT) is a natural partner [INT].

**8. "Is the beachhead big enough?"**
No, and it doesn't need to be. It gives us paying design partners, field data on the flicker floor, and the reference customer that pulls the module into production radars (GESTRA, multistatic counter-UAS). Market sizes are in the research file. The beachhead is about evidence; scale and vision carry the valuation.

**9. "Who exactly has said they'd buy?"**
Fraunhofer Leistungszentrum Terahertzsensorik: pain confirmed, a digital LOI offered, and we may name them [INT]. Rakon: lab buyers are price-insensitive [INT]. Microchip pointed to T&M OEMs [INT]. [FILL: LOI status if signed today.]

**10. "Isn't the vision just GPS again?"**
GPS is one-way and fragile: jammable and spoofable. The Coherent Layer is terrestrial and redundant, works indoors, detects relays at 1.3 cm [SIM P3c], and computes positions on the device (privacy). It complements GNSS ("it has to be a universal system": u-blox [INT]).

**11. "Why does the vision need YOUR clock rather than OCXOs plus frequent sync?"**
A standard OCXO anchor stays within 100 ps for about 1 min, an HSO for 30 min, the chip for 2 h [SIM P3b]. Wired anchors can resync every minute, so they don't need us. The product is for anchors whose sync channel is wireless, power-limited or deniable for minutes to hours: resilience is the product.

**12. "Satellites?"**
Not our route; satellite swarms are a crowded field. We are ground and infrastructure first.

**13. "Defensibility once others get the clock?"**
- Supply partnership with imec.
- Coherence firmware and calibration data.
- Integration into radar processing.
- Per-node software licences.
- Qualification (MIL-STD-810).
- Later, the API network effect.

**14. "What do you need from imec?"**
Engineering samples for a flicker-floor and magnetic/thermal characterisation in 2027, plus a supply/licence term sheet.

**15. "Why this team?"**
[FILL from CVs: radar/RF, business, software, domain network. Mention that 18 organisations were contacted in 3 days (about 10 substantive interviews: Rakon, Microchip, Fraunhofer THz, u-blox, Skyworks, SEALSQ, NCODIN, ARONEA, MMT, Keysight) and the beachhead was pivoted on the evidence.]

**16. "Who owns the clock? What stops imec licensing it to Microchip?"**
Nothing yet, which is why the seed is conditional on it. Our proposal: TVA Labs as the imec co-creation spin-off with an exclusive field-of-use licence for coherent sensing and wireless infrastructure, wafer supply through the imec pilot line, and imec ventures in the round. Without exclusivity we are a reseller, and we say so.

**17. "Sixty lab customers is not a market. Why start there?"**
Because it is the only place the spec is mission-critical today, there is no qualification gate, buyers already pay for ultra-stable references, and it produces the one measurement that decides everything else: the ADEV curve on a real device. It buys proof, data and a reference customer, not revenue; our model shows €1.6 M in 2029 and we present it that way.

**18. "What happens when Microchip responds?"**
Microchip owns the CSAC line and the defence channels but not the 1e-15 physics. If they get the licence, they win; if we hold it, they are a potential partner or acquirer. The engineering that sets the field advantage (thermal, magnetic, drift, flywheel) is ours to build and is the second moat.

**19. "Your model had a bug?"**
Yes. We found it in our own review on the last night, fixed it, logged it, re-ran everything and corrected every number before submission. The quartz comparisons softened by 2–8x; the chip's results barely moved because they are environment-limited. That is what we mean by validation.

**20. "Why should I believe the field numbers if they depend on thermal compensation you have not built?"**
You should not, yet. That is why the product requirements are explicit (≥ 99 % compensation, ≤ 1 % drift residual) and why the Series A is gated on a ruggedised module demonstrating them in a field pilot.

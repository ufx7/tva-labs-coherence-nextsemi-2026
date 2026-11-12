# VC critique of the TVA Labs story
Written 12 Nov 2026, about 04:45, as the most critical deep-tech investor you could meet; §1b and §6 added at 05:30 after the floor analysis and the rewrite. Numbers below are the **corrected** ones (see §1).

## 0. Verdict
I would not fund this as written, and I would not tell you to start over. The analysis is the best thing you have: an auditable model, one external validation, and a pivot history that shows you kill your own ideas. That wins the 2x-weighted validation criterion. The *venture* wrapped around it does not survive diligence yet, for five reasons:

1. **The wedge is narrower than the story says.** After I reproduced the model and fixed a bug, the chip is mission-critical only at about 300 GHz over a minute (or 150 GHz over 5 minutes), or wherever the sync link is denied for longer than quartz tolerates: more than 30 s at X-band, more than a minute for indoor anchors. Everywhere else, quartz plus a sync link is good enough. Your own law says so. The flicker floor you were accused of assuming is actually bounded by the spec; what is not bounded is the noise above 1 s, and the venture survives its worst case (§1b).
2. **The three phases are three businesses stapled together.** A research-tools niche (grant buyers), a defence radar subsystem (primes, 3–5 year qualification), and a telecom infrastructure platform. The only word connecting them is "coherence". GESTRA, your flagship scale account, is L-band, where the chip is not needed.
3. **The unicorn lives entirely in the vision**, and the vision's necessity collapses wherever anchors have a wire: a standard OCXO resyncing once a minute meets the 100 ps budget. "A CSAC in every device" is physically implausible at 120 mW and 17 cc, and the €120 anchor price needs a 10–30x cost-down with no named mechanism.
4. **The three things every investor checks first are missing:** who owns the clock IP, who the team is, and what a unit costs to make and test.
5. **Exit math is against you.** Timing-component companies have historically sold for hundreds of millions (Symmetricom to Microsemi, $230M, 2013; Orolia to Safran, 2022, price undisclosed as far as I recall). SiTime is a volume MEMS company. A component company does not become a unicorn; only a platform with recurring revenue does, and that is the least proven part of your plan.

## 1. What I did first: reproduce. The model had a bug.
Your flicker-noise generator's amplitude scaled with the record length and was calibrated at one length only, which was also the only length validated. Scenarios using shorter records had 2–8x too much flicker noise. I fixed it (`sim/clock_noise.py`, per-length calibration, validation now sweeps 256–8192 samples) and re-ran everything.

| Claim | Before | After | Consequence |
|---|---|---|---|
| Best quartz coherence at 300 GHz, 10° | 0.46 s | **1 s** | Chip advantage 30x, not 70x |
| Best quartz image loss, 150 GHz, 60 s | −6 dB | **−1.3 dB** | At 150 GHz over a minute quartz is nearly fine |
| Best quartz image loss, 300 GHz, 60 s | −8.6 dB | **−4.3 dB** (P90–P10 −2.4 to −5.7) | Still blurred; chip −0.01 dB |
| 16-node X-band radar, sync outage tolerated | quartz 3 s vs chip 100 s | **quartz 30 s vs chip 100 s** | Advantage 3x, not 33x; W-band 3 s vs 30 s |
| Standard OCXO anchor drift per minute | 170 ps | **44 ps** | Wired anchors resyncing each minute don't need you |
| Resync interval for 100 ps | "quartz every second" | OCXO 1 min, HSO 30 min, **chip 2 h** | The chip buys sync-denied operation, not accuracy |
| Minimum ADEV, 300 GHz sounding, 60 s | 1.0e-15 | **2.1e-15** | Still only the chip (quartz 6e-14) |

The chip's own numbers barely moved, because in any real environment it is limited by residual temperature drift, not by its atomic noise: with 0.1% instead of 1% residual thermal sensitivity the chip holds 300 s at X-band instead of 100 s. That is the single most important engineering fact in the plan and it is not in the pitch: **your product's advantage is set by thermal and magnetic engineering, which Microchip and Safran are very good at.**

The one-way Doppler validation against JPL's measurement (11.5 vs 11 mm/s) used a correctly calibrated length and stands.

## 1b. The flicker-floor question, settled as far as it can be
The jury will ask whether a 7e-16 floor is an assumption. Half of it is not: a flicker-FM floor is flat in averaging time, so the challenge's own ADEV ≤ 1e-15 at 1 s bounds the flicker floor at ≤ 1e-15. A juror who says "the floor is really at SA65 level" is making a physics error, and a 1e-13 floor would void the challenge for every team. What the spec leaves open is the noise that *rises* above 1 s: random-walk FM, drift, environment; the frozen SA65 aging and temperature say that part is CSAC-class. I simulated the envelope (`sim/floor_envelope.py`):

| Case | 300 GHz coherence | 60 s image | X-band outage | Anchor resync (100 ps) |
|---|---|---|---|---|
| Base | 32 s | −0.01 dB | 100 s | 2 h |
| Worst spec-consistent (random-walk FM) | 22 s | −0.02 dB | 100 s | 1 h |
| + drift not estimated | 15 s | −0.07 dB | 100 s | 10 min |
| + 90 % thermal compensation | 10 s | −0.15 dB | 30 s (= quartz) | 5 min (< quartz) |
| Sceptic's floor 1e-14 (spec ×10) | 7 s | −0.16 dB | 100 s | 1 h |
| Floor 1e-13 (spec ×100) | 0.7 s | −5.8 dB | 30 s | 10 min |
| Best quartz | ~1 s | −3.8 dB | 30 s | 30 min |

Three conclusions. The venture survives the worst spec-consistent noise and a tenfold sceptic. What decides the field advantage is engineering under the team's control, not the floor: drift estimation to ≤ 1 % and thermal compensation ≥ 99 %, without which the chip is a quartz. And the single highest-value action before the deadline is to ask imec, who wrote the spec and is on site, what the curve does beyond 1 s. Presented this way (one sentence of physics, the envelope, milestone 1 = the measured curve), the assumption is exactly what the brief asks for and the jury will accept it.

## 2. Where it breaks, ranked

### 2.1 The physics gives you a narrow wedge; the story claims a wide one
Required stability is φ/(2π·f·T). That law is your best slide and your worst enemy. At L-band (GESTRA, 1.3 GHz) quartz holds 100 s within tolerance. At X-band (counter-UAS) quartz holds 30 s of sync outage, and real multistatic radars use direct-path or dedicated-link sync, not just GNSS. So the honest scale market is: mm-wave multistatic systems (W-band is still mostly research), plus any band where the sync channel is denied for longer than quartz tolerates. Say exactly that. Do not name GESTRA as a clock-limited account; keep it as a relationship and a channel to Hensoldt.

### 2.2 The beachhead is a research-tools niche, not a business
Count the buyers: perhaps 30–40 sub-THz channel-sounding groups and 20 THz radar groups worldwide, plus three T&M OEMs. At €25k and one or two units each, that is €3–4M of lifetime revenue, bought from grants, with no repeat. Your own revenue model shows €0.1M in 2027 and €1.6M in 2029. An investor hears "we will spend €4M to sell €1M a year of lab equipment to Fraunhofer." The only honest framing: **this phase buys proof, data and a reference customer, not revenue.** Say it in those words; investors respect that more than a fake beachhead.

Also: the Fraunhofer "pain" is softer than quoted. The same person said "single clock: no problem with drift", "clock speed: no idea", "PLL used to compensate". No price was discussed. An LOI from a research institute is a signal of interest, not willingness to pay.

### 2.3 The vision needs a wire-free world to be necessary
Indoor anchors on Ethernet can resync every minute with White Rabbit or PTP hardware timestamping; a standard OCXO then meets 100 ps. The chip is needed only where sync is wireless, power-limited, or deniable for minutes to hours. That is a real market (GNSS-denied, jammed, mobile, mesh), but it is a *resilience* story, not a *precision* story, and it is much smaller than "every device". Rebuild the vision around infrastructure nodes that have no wire (mm-wave small cells with wireless backhaul, IAB nodes, deployable networks, vehicles), with devices as *clients* of coherence rather than carriers of a vapour cell.

### 2.4 Not fundable as written: IP, team, unit cost
- **IP:** the clock is imec's. If imec licenses non-exclusively, Microchip ships a "coherent CSAC" into every defence prime through channels it already owns, and you are a reseller. The licence *is* the moat. One slide: imec co-creation spin-off, exclusive field-of-use licence for coherent sensing and networks, imec ventures in the seed.
- **Team:** four names, no roles. Who has built a precision oscillator product, sold to a radar prime, or run a Fraunhofer collaboration? If nobody, show the first three hires and an advisor from imec's clock group.
- **Unit economics:** no COGS, gross margin, or test cost. Testing a 1e-15 clock needs a better reference and hours per unit; Rakon gets 4–5 of 10 HSOs through calibration. Put a box on the slide: clock €2–4k, shield/thermal/RF €1.5k, test €0.5–1k, node price €12k, gross margin 55–65%, test via shared maser plus parallel racks.

### 2.5 Incumbents are missing
Microchip (owns the CSAC line and the channels), Safran/Orolia (military timing), Rakon, SiTime (just bought Renesas timing), Adtran/Oscilloquartz, Infleqtion (SPAC, $550M, targets GNSS-denied PNT), Vector Atomic/IonQ (DARPA Evergreen), Mesa Quantum (chip-scale, $11.8M seed), and on the sync side White Rabbit/Seven Solutions (Safran) and Meinberg. For each, one line on why they lose in *your* wedge. Right now the comparison table only lists technologies, not companies that will respond to you.

### 2.6 Internal inconsistencies a reader catches in minutes
- Series A "mid-2029, €3–5M revenue" against a model showing €1.6M in 2029. Corrected to late 2029/2030 with €1.5–2M revenue plus €5M backlog.
- The image at 300 GHz over 60 s is "cable-identical" while the rms phase error is 20°, above the 10° tolerance. True, because most of the error is a linear ramp that shifts the target (≤0.2 cell at 60 s, 2–4 cells at 300 s) rather than blurring it; say so, and claim 60 s, not "minutes".
- "No offensive targeting products" alongside Rheinmetall and Hensoldt as target accounts. Pick a position; "protective systems: airspace, space safety, critical infrastructure" is defensible and matches the NATO Innovation Fund's exclusions.
- Interviews are named although the brief asks for anonymised summaries; only Fraunhofer gave permission.

### 2.7 The spec itself is internally inconsistent, and you should say which half you believe
ADEV 1e-15 at 1 s implies close-in phase noise around −150 dBc/Hz at 1 Hz on 10 MHz. The frozen SA65 sell sheet says −44 dBc/Hz at 1 Hz, which corresponds to 3e-10. Both cannot be true. A technical juror (ex-Intel RF) may raise it. The right answer: "we take the time-domain spec as given, assume close-in phase noise consistent with it, and add a low-noise flywheel oscillator for offsets above the atomic loop bandwidth; our model is valid from 0.1 s upward and says so."

### 2.8 Multiples
SiTime at 22x revenue is a peak-cycle number for a profitable volume company; Infleqtion at 39x is a pre-revenue SPAC that Barron's warns about. For a hardware company with a software layer, 5–10x is what a Series B investor will underwrite. Your corrected bottom-up model gives €55M revenue in 2033 and €163M in 2035 *with* the vision, €76M without. At 5–10x that is €1–1.6B in 2035 only if the vision works. Present the three cases; do not present only the best one.

## 3. What is good, and what to keep
- The f×T law as the one-slide explanation of where you matter and where you don't.
- Auditable, reproducible simulation; an external validation; uncertainty bands; a bug log. Few hackathon teams have any of this.
- The pivot table: killed holdover, telecom, drone TDOA, satellites, optical interconnect; found the one place the spec is mission-critical.
- The GNSS-plus-chip "flywheel" result at Ka-band (6.6° → 0.6–0.9°) is an original, defensible idea.
- "Where 1e-15 buys nothing" as a slide. Investors trust people who show the losses.

## 4. How I would rebuild the venture narrative (same analysis, different spine)
**Thesis:** *Coherence where sync is denied or impossible.* One sentence, three phases that are the same product at rising volume:

1. **Prove (2027–28):** the only place the spec is mission-critical today, sub-THz coherent measurement. Two design partners, the measured ADEV curve from 1 to 10⁴ s (the floor is bounded by the spec; the rise above 1 s is not), first units. Revenue €1–2M total. Label it as proof, not a market. State the four product requirements that decide the field advantage: thermal compensation ≥ 99 %, drift estimation ≤ 1 %, magnetic shield, flywheel oscillator.
2. **Deploy (2028–31):** sync-denied coherent sensing. Deployable and mobile multistatic radar at X-band and above under GNSS and link jamming (the chip gives 100–300 s of coherence; quartz 30 s), mm-wave multistatic and ISAC pilots. Node plus per-node software licence. This is where the "why now" (spoofing +193%, record defence funding, EIC dual-use) belongs.
3. **Platform (2031+):** coherent wireless infrastructure. mm-wave small cells with wireless backhaul, IAB nodes, deployable networks and vehicles become one coherent instrument; positioning and physical-layer authenticity are services; devices are clients. PQC-signed trusted time stays. Drop "a CSAC in every device".

Add the four missing slides (IP, team, unit economics, incumbents), quantify one customer cost in euros (get it from Fraunhofer today: hours lost per campaign, or fibre per node), and present revenue as three cases.

## 5. What would make me write the cheque, and what would make me pass
- **Write:** a signed exclusive field-of-use licence from imec; a measured ADEV curve from 1 to 10⁴ s on a real sample at or below the random-walk envelope (≤ 2e-14 at 1000 s), with drift estimation and ≥ 99 % thermal compensation demonstrated in the module; one defence or T&M design partner paying for a pilot; a founder who has shipped a precision timing product; a per-node software licence attached to real nodes.
- **Pass:** "we will sell modules to labs and figure out the rest later"; an IP position that imec can also give to Microchip; a vision that requires a 30x clock cost-down with no mechanism; a team slide with no timing or radar operator; a module whose field advantage rests on thermal compensation nobody has built yet.

## 6. Status after the rewrite (05:30)
`VC_story.md` v2 applies the rebuild: one thesis ("coherence where sync is denied or impossible") in three volumes (prove, deploy, platform); the wedge stated narrowly; L-band radar demoted to a channel; the beachhead labelled as proof with its size stated; the platform re-based on nodes without a wire; IP, incumbents, unit economics, three revenue cases, exit comparables, the noise envelope, the flywheel statement, anonymised interviews, protective-systems values, corrected Series A milestone, blur-vs-shift footnote, uncertainty bands.
Still open, and only the team can close them today: the team slide (roles, full-time commitment, hires); the Fraunhofer LOI with a price or at least two numbers on it; imec's answer on the curve beyond 1 s; one customer cost in euros; the TVA deck's first four slides, which still carry the old story.

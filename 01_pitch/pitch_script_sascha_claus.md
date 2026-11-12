# Pitch script for Sascha and Claus: setting, suspense, wit, and the questions that will come
Stage format: 5 minutes, then 5 minutes of Q&A, judged on tech feasibility, innovation, market potential and **stage presence**. Round 1 is different: a technical review at your desk at 13:00, conversational, with the deck, the repo and a live model.

## 1. The setting
Two of you on stage. Claus stage-right with the clicker, Sascha stage-left. Claus owns the physics and the proof (S1–S4, S10); Sascha owns the venture (S5–S9). Hand over with eye contact, not with "and now Sascha will…".
Prop: a matchbox. The SA65 is 41 × 35 × 11 mm, 16 cc: a matchbox. Claus holds it up once, at S1, and puts it on the lectern. It stays visible for five minutes.
Tempo: 30 seconds per slide, 300 seconds total, one breath between slides. Rehearse with a timer three times; the first run will be 7 minutes, the third will be 5.

## 2. The arc (why it works)
- **Hook (S1):** a drift nobody noticed. Wit from precision: "about a millisecond" (two quartz watches at a few ppm drift about a millisecond in five minutes; true and checkable).
- **Tension (S2–S3):** everyone else's clock matters nowhere; ours matters in exactly two places, and we put the list of where we are useless on the slide. Confidence through self-restraint. The jury's brief asked teams to find "where the spec buys nothing"; you are the team that took it literally.
- **Reveal (S4):** the image. Green on black. Let the picture breathe for three seconds before speaking.
- **Build (S5–S7):** small, honest, bigger, biggest. Each phase has a number the jury can remember: 60 s at 300 GHz; 100 s against the jammer; 2 hours at 100 ps.
- **Twist (S8):** "Who stops us? Microchip, if they get the licence." Name your biggest threat yourself; the jury cannot use it against you afterwards.
- **Money (S9):** three cases, including the one that is not a unicorn. VCs trust people who show the downside.
- **Landing (S10):** the 4 a.m. bug. "We broke our own story and fixed it before you saw it." Then the ask, in one breath, and stop. Do not say "any questions"; the moderator does.

## 3. Lines worth keeping (and lines to avoid)
Keep: "coherence without a wire" · "we spent two days finding out where our clock is useless" · "the licence is the moat" · "proof, not revenue" · "measurements unlock rounds, not promises" · "timing components have never been unicorns; platforms have".
Avoid: "300,000x" (true only at 1 s) · "minutes" (say 60 s at 300 GHz) · "holdover" (we do not sell it) · "every device" (say infrastructure first) · "GPS replacement" (say complement) · "disrupt", "revolutionary", "unicorn" (let them say it).
If a number is challenged and you are not sure: "Emmanuele has that case open at our desk; the model runs it in five seconds." Never guess a number on stage.

## 4. Q&A playbook (5 minutes, about 5 questions)
Who answers: physics and model → Claus; market, money, IP, team → Sascha. If both want to answer, Sascha goes first. Twenty seconds per answer: claim, number, source. Bridge phrases: "The short answer is… the number is… it's in the repo."

### The questions, by juror
**Thomas Schiml (ex-Intel/Infineon, manufacturing):**
- "Who fabs it, and how do you test 1e-15 in production?" → imec pilot line first, foundry partner at Series B; test needs a better reference and hours per unit: shared hydrogen maser plus parallel racks, costed at €0.5–1 k per unit. A top-3 oscillator maker passes 4–5 of 10 of its best units; we budget for that.
- "Your spec says 1e-15 but the sheet's phase noise says 3e-10." → Yes; we take the time-domain spec, assume consistent close-in noise, add a flywheel; model valid from 0.1 s. (B16)

**Stefan Müller (FMC founder; imec.xpand led his Series B):**
- "What is your IP position with imec?" → A proposal, not a signature: co-creation spin-off, exclusive field-of-use licence, imec ventures in the seed. Without exclusivity we are a reseller and we would not raise. (B12)
- "FMC took 14 years. Why are your rounds faster?" → Phase 1 has no qualification gate and sells to labs; Series A is gated on a field pilot; Series B on 1,000 nodes. If the measured curve is worse than the envelope, we know by month 3.

**John Bell (HighTechXL, venture builder; added to the final jury):**
- "Who goes full-time on Monday?" → [FILL: names and dates]. First hires: RF/timing lead, radar systems engineer, defence BD. Advisor from imec's clock group.
- "What did customers actually commit to?" → [LOI status]; two numbers from Fraunhofer; quotes from a T&M OEM. Anything we did not get, say "not yet, and here is the experiment".

**Betsy Lindsey (CFO background; FSO telecom; suggested telecom and PQC):**
- "Why not telecom?" → We tested it: telecom pays for aging over 14 days, which the challenge freezes. We enter telecom through positioning and 6G sensing, and through fibre-free coherent backhaul, where free-space optics and coherence belong together.
- "Gross margin?" → 75 % module, 55–65 % node, 90 % software. COGS on B10.
- "Where is PQC?" → Trusted time: coherence-derived timestamps signed post-quantum; physical-layer relay detection at 1.3 cm; a PQC vendor we met has no trusted-time product.

**Cassandra Melvin (SEMI Europe; sovereignty, skills, diversity):**
- "Why Europe?" → A European-built reference that works when GNSS does not; imec, Fraunhofer, EIC dual-use, NATO Innovation Fund; protective systems only.

**Michael Machold (TUM Venture Labs):**
- "Will you found this?" → [FILL]. "What would make you stop?" → A measured floor above the envelope, or no exclusivity from imec. We would know both within six months.

**Track jury, Bruno Iafelice and Helen Kardan (investability; who signs the PO):**
- "Who signs the purchase order in phase 1?" → The institute's project lead from a project budget; the T&M OEM's product manager for an option. Price €25 k; lab reference buyers are price-insensitive (quote).
- "How much capital to first revenue? To break-even?" → First revenue 2027 (seed); break-even in the deploy phase around 2031–32 in the base case; €79 M raised across three rounds.

### The five hardest, regardless of who asks
1. **"Sixty labs is not a market."** → Correct, and it is not meant to be: proof, data, reference customer. The market is phase 2.
2. **"Why can't quartz plus a sync link do this?"** → It can, wherever the link exists. We are the product for when it does not: 300 GHz × 1 min, jammed links, anchors with no wire. The numbers: 1 s vs 32 s; 30 s vs 100 s; 1 min vs 2 h.
3. **"What if the floor is worse?"** → Bounded by the spec; worst spec-consistent case costs the beachhead a third and nothing else; milestone 1. (B1)
4. **"Your model had a bug."** → Yes, we found it at 4 a.m., fixed it, logged it, and corrected every number before you saw it. That is validation.
5. **"Your field advantage depends on thermal compensation you have not built."** → Yes; it is a product requirement, 99 %, standard in timing products, and Series A is gated on demonstrating it in a field pilot.

## 5. The workspace review at 13:00 (round 1, decides whether you reach the stage)
Ten minutes, conversational. Order: S1–S10 fast (4 minutes), then W1–W5 (technology honesty, what we must build, where 1e-15 buys nothing, the model, the interviews), then the live run: Emmanuele runs `floor_envelope.py` and block B of `scenarios.py` with a juror-chosen carrier. Have the repo open in a browser. Claus leads; Sascha fills in buyers and money; Emmanuele speaks only to the model; Sagar keeps time and takes notes of every question for the stage.
The track jury scores validation at 2x. Spend half the time there.

## 6. Stage mechanics
Arrive at the stage at 15:10 with the deck on a USB stick and on the laptop; PDF and the original. Check the clicker on S1. Water. Phones off. If a slide fails, keep talking: every speaker line in `deck_script.md` stands without its slide.
Posture: feet still, hands free except for the matchbox. Look at the jury, not at the screen. When Sascha speaks, Claus looks at Sascha; the audience follows the eyes.
Last word before walking off: "Thank you." Not "that's it".

# Session: the VC and the builder, on the morning the floor turns out SA65-class
12 Nov 2026, 08:50, TechArena desk. Two personas, one table, one premise taken as given for this session: **the first real curve (or imec's answer) shows the clock is 1e-15 at 1 s but reverts to SA65-class stability above a few seconds.** Everything below is derived from `03_sim/floor_sa65_premise.py` (`out/K_sa65_premise.csv`) and the challenge PDF. Status of the premise: a scenario until imec or a measurement confirms it; labelled as such everywhere.

---
**VC:** So the floor isn't 1e-15. It follows the SA65. Tell me in one sentence what that does to the pitch.
**Builder:** It depends on one thing you can't see in an ADEV plot. A *flat* flicker floor at SA65 level, 1e-12, is impossible if the 1 s value is 1e-15: a flicker floor is flat in averaging time, so it would also be 1e-12 at 1 s. The only way the finding can be true is that the curve *rises* above 1 s, drift-like or random-walk, to 1e-12 or 1e-11 at 1000 s. And a rise comes in two kinds: a stable drift, which firmware estimates and removes, or a random one, which nothing removes.
**VC:** Numbers.

| Reading of "the floor follows SA65" | ADEV 1 / 10 / 100 / 1000 s | 300 GHz coherence (10°) | 300 GHz image, 10 s / 60 s | X-band 16-node outage | Anchor resync for 100 ps |
|---|---|---|---|---|---|
| Base (what we pitched) | 1e-15 / 7e-16 / 7e-16 / 3e-15 | 32 s | 0.00 / −0.01 dB | 100 s | 2 h |
| Flat 1e-12 floor (literal; contradicts the 1 s spec 1000x) | 1e-12 flat | < 0.1 s | −7.6 / −14 dB | 3 s | 1 min |
| Rises to 1e-12 at 1000 s, **random** (not estimable) | 1.4e-15 / 1e-14 / 1e-13 / 1e-12 | 7 s | 0.00 / −1.1 dB | 100 s | 5 min |
| Rises to 1e-12 at 1000 s, **stable drift**, estimated to 1 % | 1e-15 / 7.5e-16 / 1.2e-15 / 1e-14 | 32 s | 0.00 / −0.01 dB | 100 s | 1 h |
| Rises to the SA65 table value 1e-11 at 1000 s, random | 1e-14 / 1e-13 / 1e-12 / 1e-11 | 2 s | −0.09 / −12 dB | 100 s | 1 min |
| Same, stable drift estimated to 1 % | 1e-15 / 1.2e-15 / 1e-14 / 1e-13 | 22 s | 0.00 / −0.02 dB | 100 s | 10 min |
| Best quartz (reference) | 6e-14 flat | ~1 s | −0.2 / −4.1 dB | 30 s | 30 min |

**Builder:** Read it by phase. Phase 1, sub-THz measurement: if the rise is random, the "60 s aperture" claim dies; we hold 2–7 s at 300 GHz, still 2–5x quartz, and a 10 s aperture is still lossless. If the rise is a stable drift, the firmware recovers the full 32 s. Phase 2, sync-denied sensing at X-band: untouched in every reading except the impossible flat one, because at 10 GHz the phase budget is 30x larger and the field environment, not the clock, sets the 100 s. Phase 3, the platform: dies if the rise is random (anchors last 1–5 minutes, quartz lasts 30), survives as "one hour" if the drift is stable.
**VC:** So in the random case I am looking at a defence sensing company, not a platform.
**Builder:** Yes. Deploy-only case: €76 M revenue in 2035, €0.4–0.8 B at 5–10x. Honest, fundable, not a unicorn.
**VC:** And in the stable-drift case the product is… the firmware.
**Builder:** The drift-tracking estimator and the thermal control. The licence stays the commercial moat; those two are the engineering moat. Which is what the model said before the floor question came up.

## Joint decisions (what the two of us change this morning)
1. **Seed milestone 1 is redefined.** Not "the ADEV curve" alone: **the drift stability to 10⁴ s** (Hadamard deviation, drift-rate stability over an hour) on the first samples, plus the drift-tracking firmware demonstrated on them. This is the measurement that decides between the two columns above.
2. **The pitch claims the base case and shows this table** (W1/B1 at the workspace review). One sentence on stage if asked: "If the rise above one second is random, the platform is off and we are a defence sensing company worth half a billion; if it is a stable drift, our firmware recovers the whole story. The first measurement of the seed decides which."
3. **Series A is sized to the deploy-only case** until the curve is in; the platform milestones move to a Series A option, not a promise.
4. **Product definition:** drift estimator and thermal control are promoted from "components" to the two engineering pillars, next to the licence.
5. **One question to imec this morning, verbatim:** "Above one second, is the degradation a stable drift or random?" Their answer turns this scenario into a finding, or retires it. Record the answer at the bottom of this file.

## Would the jury accept the floor assumption? The brief's own words, then the test
The challenge PDF (imec ventures, "Build the Next Timing Unicorn"):
- §2 "Important framing": *"This is a venture-design challenge, not a request to prove the underlying atomic-clock physics. However, teams must identify where the assumed specification is genuinely valuable and must not claim system benefits without a defensible calculation or simulation."*
- §4A: *"Build a transparent model … simple enough to audit and strong enough to challenge your assumptions."* and *"Clearly distinguish sourced inputs, engineering assumptions and simulated outputs. Provide reproducible files and state the model limitations."*
- §9 Guardrails: *"Make assumptions explicit. Where evidence is unavailable, define the experiment or milestone that would validate it."*

How our handling maps to each clause: the floor is an explicit parameter (`clock_noise.py`, tagged ASM); the physics bound (flicker is flat in τ, so the 1 s spec bounds the flicker floor) is stated; the full envelope including the SA65-class readings is simulated and shown, not hidden; the validating experiment is milestone 1 of the seed. By the brief's own rules the assumption is **admissible** when presented this way. Whether the jurors *accept* it is observable only at the 13:00 workspace review and the stage Q&A; it cannot be verified before then.

**Verification protocol (fill in today):**
- 09:00–10:00: imec's answer to the verbatim question above → write here: ______________________
- 13:00 workspace review: show W1/B1 and this table; note the track jury's reaction and any objection → ______________________
- 16:15 stage Q&A: if asked, the one sentence in decision 2; note the follow-up → ______________________

## Status
Premise: scenario, pending imec's answer. Analysis: done and reproducible. Decisions 1–4: applied to the pitch documents by reference to this file. Decision 5 and the verification protocol: the team's, this morning.

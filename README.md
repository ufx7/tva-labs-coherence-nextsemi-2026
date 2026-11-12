# TVA Labs: coherence where sync is denied or impossible
NextSEMI Hackathon (SEMICON Europa × TUM Venture Labs), Munich, 10–12 Nov 2026 · imec ventures challenge "Build the next timing unicorn" · Team: Emmanuele, Sascha, Sagar, Claus.
Repository: [URL to be added by Emmanuele] · Deck: `01_pitch/TVA_Labs_deck.pdf`

## What we built
Starting from a chip-scale atomic clock with an assumed short-term stability of 1e-15 at 1 s (all other specs as the Microchip SA65), we asked where that one number is mission-critical, built an auditable simulation that converts clock noise into application metrics (radar image blur, coherent gain under sync outage, positioning error, relay detection, Doppler error), interviewed ten organisations across seven stakeholder types, and designed a venture in three phases:
1. **Prove (2027–28):** a wire-free coherence module for sub-THz radar and 6G measurement labs, the only place the spec is mission-critical today.
2. **Deploy (2028–31):** sync-denied coherent sensing: multistatic radar that keeps coherence when its sync link is jammed.
3. **Platform (2031+):** coherent wireless infrastructure: nodes without a wire become one instrument; positioning, authenticity and post-quantum-signed trusted time as services.

One law organises everything: the stability a coherent system needs is φ / (2π · f · T). Our clock matters at high carrier frequency × long window, or whenever a sync link is denied. We say where it does not matter, too.

## How it works, and how to run it
- `03_sim/`: the model. `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`, then run `clock_noise.py` (generator validation), `scenarios.py`, `poc_phases.py`, `hybrid_gnss.py`, `redteam_checks.py`, `floor_envelope.py`, `navigator.py`. About 30 s total. Results and figures are committed in `03_sim/out/`. Method, inputs (sourced / challenge / assumed), validation, limitations and the bug log: `03_sim/README.md`.
- `02_tech/VC_story.md`: the venture, answering the challenge's nine questions with every number traced to the model, an interview or a source. `vc_critique.md` and `red_team_review.md` are our own adversarial reviews; `research_market_vc.md` holds market, comparables and sentiment data with URLs and credibility ratings; `exec_summary_tech_for_pitchers.md` explains the technology from the ground up; `plan_b_vc_builder_session_sa65_floor.md` is the contingency if the clock's stability above 1 s turns out SA65-class, with the jury-acceptance test.
- `04_validation/`: anonymised interview record with "how the concept changed", and the Market Opportunity Navigator scores.
- `01_pitch/`: deck script (stage 5 min, workspace extras, backup slides), pitch script, figures.
- `05_traction_plan/`: the morning's traction plan and LOI/outreach templates.
- `00_SUBMISSION_CHECKLIST.md`: requirements mapped to files, and the gaps.

## Headline results (corrected model, 12 Nov 2026)
| Metric | This clock | Best quartz (6e-14) | Rubidium |
|---|---|---|---|
| Free-running coherence at 300 GHz, 10° | 32 s | ~1 s | < 0.1 s |
| Radar image, 300 GHz, 60 s aperture, no cable | −0.01 dB | −4.3 dB (blurred) | −18 dB |
| 16-node X-band radar, sync link cut, ≥ 90 % gain | 100 s (300 s at 99.9 % thermal) | 30 s | < 0.1 s |
| Anchor resync interval for 100 ps | 2 h | 30 min | — |
| Worst spec-consistent noise above 1 s | 22 s at 300 GHz | — | — |

Validation: generated noise matches target ADEV within ±7 % across record lengths; the model reproduces JPL's measured one-way Doppler error with a CSAC (11.5 vs 11 mm/s); headline numbers carry P10–P90 bands; a flicker-calibration bug found on 12 Nov 04:20 is documented and corrected.

## Who does what today
Sagar builds the deck (`01_pitch/handover_sagar.md`). Emmanuele verifies the model and publishes the repo (`03_sim/handover_emmanuele.md`). Sascha and Claus pitch (`01_pitch/pitch_script_sascha_claus.md`, `02_tech/exec_summary_tech_for_pitchers.md`) and work the floor 09:00–10:00 (`05_traction_plan/`).

## Licence and privacy
Code and documents: MIT (`LICENSE`). `private/` holds raw interview notes and third-party PDFs and is excluded from the repository; interviewees are anonymised unless they gave permission to be named.

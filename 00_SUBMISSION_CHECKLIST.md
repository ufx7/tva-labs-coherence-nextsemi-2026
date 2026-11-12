# Submission checklist, NextSEMI Hackathon, hand-in Thursday 12 Nov 12:00 sharp
Source of requirements: pre-dinner slides (hand-in: pitch deck as PDF; code repository link with jury access; documentation "what you built, how it works, how to run it"; submission links provided Thursday morning), participants' manual (12:00 hard deadline; 13:00 technical jury at the workspace; 15:10 grand finale; finalists pitch 5 min + 5 min Q&A), and the imec challenge PDF (nine questions, validation A and B, Navigator, guardrails, funding plan).

## Hand-in items
| Item | File | Owner | Status |
|---|---|---|---|
| Pitch deck (PDF) | `01_pitch/TVA_Labs_deck.pdf` (+ `_stage.pdf`) | Sagar | ☐ build from `deck_script.md`, `backup_slides.md` |
| Repository link with jury access | public GitHub repo of this folder (without `private/`) | Emmanuele | ☐ `handover_emmanuele.md` §F; paste URL in README, S10, submission form |
| Documentation | `README.md` (root), `03_sim/README.md`, `02_tech/VC_story.md` | done | ☐ add repo URL |
| Submission form (links provided Thursday morning) | — | Claus | ☐ watch the WhatsApp group for the link |

## The challenge's nine questions → where answered
| # | Question | Where |
|---|---|---|
| 1 | Market landscape | `VC_story.md` §2 (mission-critical vs good-enough table); navigator |
| 2 | Market choice: beachhead vs expansion, why | §2 navigator scores, §3 "why here", §4–5 |
| 3 | Customer problem: buyer vs user, quantified cost | §3 "who pays"; fibre per node §4; **customer € cost still [FILL] from Fraunhofer** |
| 4 | Unique advantage vs CSAC/OCXO/GNSS/lab clocks at acceptable SWaP-C | §1 law and table, §6 incumbents |
| 5 | Unlocked applications: mission-critical vs nice-to-have | §2 table |
| 6 | Complete product | §3 "Coherence Module", §1 "what we must build" |
| 7 | Business model and defensibility | §7 (model, COGS, margins, IP, moat) |
| 8 | Go-to-market | §8 |
| 9 | Funding plan, two rounds minimum | §9 (three rounds, milestones, runway, benchmarks, three cases) |

## Validation A: system simulation (2x weight)
| Requirement | Evidence |
|---|---|
| Baseline + ≥ 1 competing architecture | quartz (HSO, OCXO, TCXO), rubidium, SA65, USO, GNSS sync, fibre; `scenarios.py`, `poc_phases.py` |
| Clock behaviour → application metric | phase error, image peak loss/ISLR, coherent gain, positioning error, relay detection, Doppler error |
| Non-clock noise where material | temperature, magnetic, drift, link noise (drone critique), positioner, extender thermal, air (`redteam_checks.py` R2) |
| Sensitivity: when the clock is the limit, minimum clock needed | `E_sensitivity_chip.csv`, `H_min_clock.csv`, `J_floor_envelope.csv` |
| Sourced inputs / assumptions / outputs separated; reproducible; limitations | tags in code and docs; `03_sim/README.md` incl. limitations and bug log |

## Validation B: interviews
| Requirement | Evidence |
|---|---|
| ≥ 2 stakeholder types | 7 types, 10 organisations (`04_validation/interviews_anonymised.md`) |
| Lead with the problem, not the tech | `private/interview_guide.md` (method) |
| Anonymised summaries; how the concept changed | `interviews_anonymised.md`; `VC_story.md` §11 |

## Navigator and guardrails
Navigator: `04_validation/navigator.csv`, `03_sim/navigator.py`, `VC_story.md` §2. Guardrails: "where 1e-15 buys nothing" (§2); TAM ≠ PMF (bottom-up model, §9); incumbents (§6); anonymised evidence; no over-engineering (each module component justified by a sensitivity, §1); assumptions explicit with experiments (§12).

## Gaps to close this morning (in priority order)
1. Team slide and §10: roles, full-time commitment, photos. **Only the team can do this.**
2. Fraunhofer LOI signed, with two numbers (drift °/min; hours lost per campaign) → S2, S5, §3.
3. imec's answer on the ADEV curve beyond 1 s (verbatim question and verification protocol in `02_tech/plan_b_vc_builder_session_sa65_floor.md`) → W1; record the answer in that file.
4. Repo URL in README, S10, submission form.
5. Deck PDF exported and checked on a phone.
6. `Questions Your Team Must Answer.docx` (team's own working doc in Kontext): check whether the organisers expect it filled; if so, copy the table above into it.
7. Final jury per the pre-dinner slide includes **John Bell (HighTechXL)**, not in our earlier research: Q&A prepared in `pitch_script_sascha_claus.md`.

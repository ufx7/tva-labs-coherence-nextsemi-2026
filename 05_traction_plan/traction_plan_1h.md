# Traction in one hour: where to go, who does what, what to ask
Assumption: the window is **Thursday 12 Nov, 09:00–10:00**, when the halls open and before the 12:00 deadline. If you meant Friday 13 Nov, it is after the finale and will not count for the jury; use Thursday.
Evidence gathered after 12:00 still counts verbally at the 13:00 workspace review and the 15:10 finale, so the window is really 09:00–12:45.

## 1. What "traction" means to this jury, in descending order
1. **A signed (digital) letter of interest** naming the use case and an evaluation in 2027. One is enough; two is a story.
2. **A written quote** (email or WhatsApp reply) from a named role at a named company, with permission to cite.
3. **A verbal quote** with role and company type, anonymised, captured within 60 s.
4. "They were interested." Worth nothing. Do not bring this back.
Every conversation ends with: "Can I quote you on that, and may I name the company?"

## 2. Targets, by value, with what we already know
| Priority | Who | Where | What we want | Who goes |
|---|---|---|---|---|
| 1 | **Fraunhofer Leistungszentrum Terahertzsensorik** (contact met on 11 Nov; LOI offered, manager contact offered) | their stand (ask at the Fraunhofer joint booth; check the SEMICON app) | signed digital LOI + two numbers: phase drift today in °/min between separate modules; hours lost per campaign when an aperture blurs | Claus (has the relationship) |
| 2 | **Rohde & Schwarz** (Hall A4 per our notes) | A4 | a quote on how customers keep TX/RX coherent above 100 GHz without a cable, and whether product management would evaluate an atomic reference option | Sascha |
| 3 | **Keysight / Anritsu** (sub-THz testbed makers; halls: check the electronica app) | T&M area | same two questions; plus "what does your high-stability reference option cost?" | Sascha |
| 4 | **The imec challenge owner** (in Hall B0 / TechArena) | B0 | the ADEV curve beyond 1 s; "would imec ventures consider a co-creation spin-off with field-of-use exclusivity?" One sentence we can quote | Claus or Emmanuele, 10 min |
| 5 | Timing vendors we met (major CSAC vendor; top-3 oscillator maker) | their stands (revisit) | one sentence each on "customers ask for longer coherence when the sync link is jammed" | Sascha if time |
| 6 | **Advantest** (B1706/B1712), Red Pitaya + ADI | B1 / check app | low fit (single clock); skip unless passing by | — |
| 7 | **Mentors** (WhatsApp group; 10:00–11:00 slot) | B0 | an introduction to a defence integrator or a Fraunhofer FHR manager; ask for one sentence of support we can cite | Claus |

Not to be contacted for traction: jury members (conflict of interest; the warm contact on the final jury is for a professional hello only).

## 3. Coordination
- **Sagar and Emmanuele stay at the workstation** (deck and repo). Claus and Sascha go to the floor, separately, 09:00–10:00.
- WhatsApp subgroup "TVA floor": every conversation logged within 60 seconds as one line: `ORG | role | quote (verbatim) | number | may name? y/n | LOI? y/n/sent`. Sagar pastes quotes straight into S5/S6 and the validation slide.
- Record with consent ("may I record so I quote you correctly?"); the Mac has an offline transcription skill; otherwise notes.
- 10:00–10:30: back at the desk, update deck and `04_validation/interviews_anonymised.md`; 10:00–11:00 mentor slot; 11:30 freeze; 12:00 submit.
- Carry: the one-page LOI (printed and as a link), a phone with the P1 image and the F-map, business cards.

## 4. Scripts (30 seconds each; lead with their problem, never with the clock)
**Fraunhofer THz (Claus):** "You told us separate-module apertures blur over minutes. Two numbers would make our pitch concrete: how many degrees of drift per minute do you see today, and how much campaign time is lost when it happens? If a 120 mW module held 10° at 300 GHz for a minute without a cable, would you evaluate one next year? Could you confirm that in one sentence by email today, so we can show the jury?"
**R&S / Keysight / Anritsu (Sascha):** "When your customers measure above 100 GHz with the transmitter and receiver apart, how do they keep them phase-coherent today? What happens beyond the reach of the cable or fibre? Would an atomic reference option that holds coherence for a minute at 300 GHz be something your product management would evaluate? May I quote you, and name the company?"
**Timing vendors (revisit):** "When a customer's sync link is jammed, how long can their system coast today, and do they ask for longer? May I quote you on that?"
**imec:** "Is 1e-15 at 1 s a white-noise number that keeps improving with averaging, or a point value? Does freezing aging and temperature mean the long-term is CSAC-class? And would imec ventures consider a co-creation spin-off with a field-of-use licence?"

## 5. Other channels, to send now (05:00–08:30), replies possible by 11:00
European groups are awake by 08:00; US groups will reply after the deadline but before the finale.
- **Email (template in `loi_template.md`)** to the corresponding authors of: the 300 GHz virtual-array channel-sounding paper (6G Flagship, Oulu); the phase-compensated radio-over-fibre sub-THz sounder papers (Aalborg University, wireless communication networks section); the 300 GHz sounder design paper (Fraunhofer HHI, Berlin); the 300 GHz street-canyon measurements (TU Braunschweig); the 142 GHz PTP-synced sounder (NYU Wireless); the bistatic ISAC calibration work (Surrey 6GIC / Lund). Ask one question and offer one sentence to confirm.
- **LinkedIn** (shorter template): Fraunhofer FHR space-surveillance (GESTRA) radar team; Hensoldt "Custodian" product line; DLR space situational awareness; one counter-UAS radar prime's sensor lead. Ask for a 10-minute call before 12:45 or a one-sentence confirmation.
- **Mentors' WhatsApp group**: ask the track mentors for an introduction to a defence integrator today.
- **Phone**: Fraunhofer switchboards open 08:00; ask for the THz centre's manager named by our contact.

## 6. What to do with each result
- Signed LOI → S5 "Traction" with the logo (if permitted), repo `04_validation/`, and one sentence in the pitch: "This morning Fraunhofer confirmed in writing…"
- Written quote → validation slide and `interviews_anonymised.md` with role and company (or type).
- Numbers (°/min, hours lost) → S2 problem slide, replacing "[FILL]". A customer cost in euros is the single most valuable number we lack.
- imec's answer on the curve → S8: say which envelope column is the base case.

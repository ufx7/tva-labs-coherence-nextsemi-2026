# Handover for Sagar: build the deck
Deadline: PDF exported and in `01_pitch/TVA_Labs_deck.pdf` by 11:30; submission at 12:00. Build in Google Slides or Keynote (16:9); export PDF; keep the editable original too.

## What to build, in order
1. **Stage deck S1–S10** from `deck_script.md` (5 minutes). This is the version the finale jury sees.
2. **Workspace extras W1–W5** (same file), after S10, separated by a section divider "Technical review".
3. **Backup B1–B17** from `backup_slides.md`, after a divider "Backup", grey title bars.
4. Replace the old deck entirely (`private/raw_notes/TVA Labs.pdf` is v1: drone-first, "300,000x"; nothing from it survives except the name and the 2027/2029 round timing, and the team slide layout).

## Design system (keep it boring and large)
- Background black for S1 and S4 (the image slide); white elsewhere. One accent colour (the green of the chip line in the figures, #2ca02c, so the slides and the plots agree).
- Fonts: one sans (Inter/Helvetica). Titles 40 pt, body never below 20 pt, footnotes 9 pt in grey with the source.
- One number per slide in 80 pt where the script gives one: S4 "−0.01 dB vs −4.3 dB", S6 "100 s vs 30 s", S7 "2 h", S9 "€163 M".
- Tables: maximum three rows on stage slides; full tables only in W/B.
- Figures: `figures/P1_beachhead_image_blur.png` (S4, full-bleed on black, crop the title off and set the legend in the slide), `figures/P2_scale_outage.png` (S6, left half), `figures/F_fT_map.png` and `figures/G_coherence_vs_carrier.png` (B3). If you have 20 minutes, re-plot S4 in the slide tool from `03_sim/out/P1_beachhead_image_blur.csv` with only three lines (ideal black, chip green, quartz orange) and no rubidium: cleaner.
- Logos: Fraunhofer only if the LOI permits naming (the contact said we may name them; confirm on the LOI checkbox). No logos of companies we interviewed anonymously. Target accounts on S6 as text, not logos.
- Footnote on every slide with a number: "Source: TVA Labs model, github.com/[repo] · 12 Nov 2026" or the interview/market source. Market sizes get "(syndicated research, low confidence)".

## Placeholders to resolve before export (ask in the WhatsApp group; do not invent)
- S2 and S5: LOI status line; the two Fraunhofer numbers (°/min drift; hours lost per campaign).
- S10 and B17: team roles, photos, who goes full-time; the repo URL from Emmanuele.
- S8: if imec answers the curve question, add one line on W1 ("imec: the 1 s value is white-noise-limited / a point value").
- Any quote from the floor: paste verbatim with role and company type on W5; add "may name: yes/no".

## Numbers: use only these (all corrected 12 Nov; if a doc disagrees, this list wins and tell Claus)
- 300 GHz coherence (10°): chip 32 s, best quartz ~1 s, rubidium < 0.1 s.
- 300 GHz / 60 s image: chip −0.01 dB (0.00 to −0.02), quartz −4.3 dB (−2.4 to −5.7), rubidium −18 dB; at 150 GHz quartz −1.3 dB.
- X-band 16-node outage: chip 100 s (300 s at 99.9 % thermal), quartz 30 s; W-band 30 s vs 3 s.
- Resync for 100 ps: OCXO 1 min, best quartz 30 min, chip 2 h.
- Positioning: 11.7 m (50 ns) → 2.3 cm (10 ps); relay detection 1.3 cm at 10 ps.
- Envelope: base 32 s / worst spec-consistent 22 s / sceptic 1e-14 7 s / 1e-13 0.7 s.
- Revenue 2035: base €163 M (€0.8–1.6 B at 5–10x), deploy-only €76 M, slow €27 M. Rounds: €4 M + €1.5–2 M (Q2 2027), €15 M + €2.5 M EIC (late 2029), €60 M (2031).
- Why now: spoofing +193 %, jamming +67 % (2025 vs 2023); $8.7 B European defence/resilience startups 2025; Ericsson $100 M ISAC; UK 93 % keyless thefts.
- Never on a slide: "300,000x", "minutes" without "60 s at 300 GHz", "holdover", "every device", "GESTRA needs our clock".

## Export and files
- `01_pitch/TVA_Labs_deck.pdf` (all sections), `01_pitch/TVA_Labs_deck_stage.pdf` (S1–S10 only, for the stage laptop), the editable original link in `README.md`.
- Also export S4 and S6 as PNG for the WhatsApp group (Claus and Sascha carry them on the floor).
- Check the PDF on a phone: if a footnote is unreadable there, it is unreadable from the jury table.

## Time plan
08:30 start, S1–S10 by 09:45, W1–W5 by 10:15, backups by 10:45, placeholders from the floor 10:00–11:00, review with Claus and Sascha 11:00, export 11:15, submitted 11:45.

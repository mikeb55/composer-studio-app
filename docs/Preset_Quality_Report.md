# Composer Studio — Preset Quality Report

**Date:** 2026-03-16  
**Trial:** Real batch generation across single-engine, hybrid, orchestration, and lead-sheet presets.

---

## 1. Preset Audit Table

| Preset | Engine / Hybrid | Purpose | Keep / Tune / Remove |
|--------|------------------|---------|----------------------|
| shorter_head | wayne_shorter | Jazz head, Shorter-style | **Keep** |
| barry_bebop | barry_harris | Bebop, Harris voicings | **Keep** |
| hill_modern | andrew_hill | Modern jazz, Hill harmony | **Keep** |
| monk_rhythm | monk | Monk-style rhythm | **Keep** |
| bartok_night | bartok_night | Bartók-influenced | **Keep** |
| wheeler_lyric | wheeler_lyric | Lyrical jazz, Wheeler | **Keep** |
| frisell_atmosphere | frisell_atmosphere | Atmospheric, Frisell | **Keep** |
| scofield_holland | scofield_holland | Scofield/Holland style | **Keep** |
| stravinsky_pulse | stravinsky_pulse | Stravinsky-influenced | **Keep** |
| zappa_disruption | zappa_disruption | Zappa-influenced | **Keep** |
| messiaen_colour | messiaen_colour | Messiaen colour | **Keep** |
| slonimsky_harmonic | slonimsky_harmonic | Slonimsky harmony | **Keep** |
| big_band | big_band | Big band | **Keep** |
| shorter_form | shorter_form | Form-focused, blueprint | **Flag experimental** |
| ligeti_texture | ligeti_texture | Ligeti texture | **Keep** |
| hybrid_counterpoint | Shorter + Harris + Hill + Monk | Hybrid counterpoint | **Keep** |
| chamber_jazz | Wheeler + Frisell + Bartok | Hybrid + orchestration | **Keep** |
| lead_sheet_song | wheeler_lyric | Lead sheet / song | **Keep** |
| guitar_string_quartet | frisell_atmosphere | Orchestration (quartet) | **Keep** |

---

## 2. Real Trial Batch Summary

**Prompts used:**
- floating chamber modern theme
- asymmetrical lyrical head
- modern big band opener
- lead sheet song about distance
- atmospheric nocturnal miniature

**Presets tested:** 11 single-engine, 2 hybrid (pipeline), 1 explicit hybrid (big_band roles), 2 orchestration-oriented, 2 lead-sheet.

**Total trials:** 27  
**Export success rate:** 100%  
**Guardrail status:** All SAFE

---

## 3. Strongest Presets

| Preset | Avg Top Score | Export | Use Case |
|--------|---------------|--------|----------|
| **chamber_jazz** | 9.70 | ✓ | Hybrid + orchestration, chamber jazz |
| **hybrid_counterpoint** | 9.67 | ✓ | Rich hybrid, Shorter+Harris+Hill+Monk |
| **frisell_atmosphere** | 9.44 | ✓ | Atmospheric, lyrical |
| **wheeler_lyric** | 9.39 | ✓ | Lyrical jazz, versatile |
| **guitar_string_quartet** | 9.42 | ✓ | Chamber, quartet orchestration |
| **lead_sheet_song** | 9.46 | ✓ | Lead sheet / song form |

---

## 4. Weakest or Experimental Presets

| Preset | Avg Top Score | Notes |
|--------|---------------|-------|
| **shorter_form** | 8.63 | Lower score; uses melody_blueprint structure. **Flag as experimental.** |

All other presets scored 9.1+ and exported successfully.

---

## 5. Tuned Defaults

No changes made. Trial results support current defaults:

- **population_size:** 8 (single), 10–12 (hybrid) — adequate
- **finalist_count:** 3–5 — adequate
- **Guardrail thresholds:** SAFE across all trials; no tuning needed

---

## 6. Best Starting Presets for Users

| Use Case | Recommended Preset |
|----------|---------------------|
| **General lyrical jazz** | wheeler_lyric |
| **Atmospheric / chamber** | frisell_atmosphere |
| **Bebop / traditional** | barry_bebop |
| **Rich hybrid** | hybrid_counterpoint |
| **Chamber jazz + orchestration** | chamber_jazz |
| **Lead sheet / song** | lead_sheet_song |
| **Guitar quartet** | guitar_string_quartet |

---

## 7. Export Verification

All strongest presets successfully produce:

- ✓ Composition MusicXML
- ✓ Hybrid MusicXML (via hybrid_counterpoint / chamber_jazz)
- ✓ Ensemble MusicXML (via guitar_string_quartet / chamber_jazz)
- ✓ Lead-sheet MusicXML (via lead_sheet_song)

**Sample export paths (trial run):**
- Composition: `docs/trial_output/exports/composition_wheeler.musicxml`
- Hybrid: `docs/trial_output/exports/hybrid.musicxml`
- Ensemble: `docs/trial_output/exports/ensemble_quartet.musicxml`
- Lead-sheet: `docs/trial_output/exports/lead_sheet.musicxml`

---

## 8. Recommendations

1. **Keep** all presets except shorter_form as experimental.
2. **Default preset** in UI: consider `wheeler_lyric` or `frisell_atmosphere` for new users.
3. **shorter_form:** Use for form-focused experiments; document as experimental in UI/docs.

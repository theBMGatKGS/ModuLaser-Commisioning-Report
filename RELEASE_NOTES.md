# Release Notes — Edwards ModuLaser MASD Field Report

Release-by-release summaries, newest first. Each GitHub release is tagged `vMM.mm.rrr`
and its text is taken from the matching section below. The itemized, per-change
history is in [CHANGELOG.md](CHANGELOG.md) and in the app under **Help → Revision Log**,
which is the source of truth.

Live site: [masdtools.net](https://masdtools.net) (served from the
`MASD-Commissioning-Report` branch).

---

## v01.00.004 — Revision archive (2026-10-07)

**In-app revision:** 01.00.004_261007 · **Includes:** 01.00.004

### Highlights
- **Help → Revision Log is now a complete release archive**, matching the ModuLaser Battery Calculator:
  - An identity card (Application / Revision / Authored by).
  - The amendments table with readable `YYYY-MM-DD` dates.
  - A new **01.00.000 Baseline** entry that inventories the full Rev 10 feature set.
  - A **Legacy history (pre-tracking) — reconstructed** section. It covers legacy r1–r10 and the 2026-09-30 conversion to an installable, offline-capable app (PWA).
- **Toolbar Revision and Date cells** show the running build at a glance, e.g. `01.00.004` · `2026-10-07`.
- **New repository docs:**
  - `CHANGELOG.md`, generated from the in-app log.
  - This `RELEASE_NOTES.md`.
  - Updated `README.md`.

### Notes
- No change to calculations, PASS/FAIL logic, import/export, autosave or print.
- Legacy r1–r10 detail was never recorded per revision. The archive summarizes it and says so, and it invents nothing.
- Installed copies (PWA) update automatically: the service-worker cache is bumped to `masd-field-report-01-00-004`. Close and reopen the app once to pick it up.

---

## v01.00.003 — Rev 11: Import PipeCAD (.pl) (2026-10-07)

**In-app revision:** 01.00.003_261007 · **Includes:** 01.00.002, 01.00.003

### New: Import PipeCAD (.pl)
- A new toolbar button reads a **PipeCAD 3.6 project export** (`.pl`, XML) entirely in the browser. Nothing is uploaded.
- **Preview before anything changes.** Every Section A field and every detector sheet is listed as Set, Replace, Keep or New/Update, with each detector's design check and margin. Cancel leaves the job untouched.
- **Section A** gets the site (ProjectName), the system designer, a "PipeCAD location" line in Notes, the installing company (only if blank), and the file name + PipeCAD version as the PipeCAD reference.
- **One detector sheet per PipeCAD detector.** A sheet whose descriptor matches the detector name is updated instead of duplicated. Each sheet gets:
  - Descriptor, fan speed, Alarm Factor and PipeCAD transport time.
  - Sampling-hole count, plus a performance target if none is set (from PipeCAD's max transit time).
  - A new **PipeCAD design data** block: pipe, pipe length (sum of the 3D segments, ft), total flow, hole balance, fittings, design sensitivity, and the full hole table (sizes shown as fractions).
- **Alarm Factor not activated in PipeCAD** is flagged "Verify — not activated in PipeCAD".
- **End-cap test points** are listed separately and excluded from the worst-hole and max-transport checks.
- **Not imported (left for field entry):** SenseNET address, part number, Alert / Action / Fire 1 / Fire 2 levels, flow limits.
- **Re-importing** an updated `.pl` keeps everything entered in the field.

### Fixed / behavior change
- **VEWFD per-hole sensitivity limit corrected from 0.2 to 1.0 %obs/ft.** It is now the Table 45 (p.112, FM 3230 / NFPA 76) **Fire 1** threshold. 0.2 %obs/ft is the VEWFD *Alert* stage and is not applied per hole.
- **SFD** now carries Table 45's ≤2.5 %obs/ft (it had no sensitivity limit before). EWFD is unchanged at ≤1.5 %obs/ft.
- **New per-detector design checks** feed the module result, deficiencies and summary:
  - PipeCAD worst-hole sensitivity vs Fire 1.
  - PipeCAD predicted transport vs the target's time limit.
  Both report pass/fail and margin.

> **Upgrade note:** existing jobs that use the VEWFD target are now evaluated against 1.0 %obs/ft. A sheet that previously failed only because of the 0.2 limit may now PASS. Re-check open jobs after updating.

### Verified with
`BWDG1.pl` (PipeCAD 3.6.2.139) imports 6 detectors, MASD 1-1 to 1-6, and all pass VEWFD Fire 1:

| Detector | Fan speed | Transport (s) | Worst hole (%obs/ft) |
|---|---|---|---|
| MASD 1-1 | 14 | 59.7 | 0.94 |
| MASD 1-2 | 12 | 60.0 | 0.95 |
| MASD 1-3 | 7 | 57.0 | 0.85 |
| MASD 1-4 | 9 | 59.2 | 0.94 |
| MASD 1-5 | 8 | 52.9 | 0.92 |
| MASD 1-6 | 6 | 55.4 | 0.98 |

MASD 1-2's transport is 59.98 s, a margin of 0.02 s.

### Unchanged
JSON Export/Import, autosave (same storage key, so existing jobs load as before) and Print / PDF.

---

## 01.00.001 — Revision tracking and Help menu (2026-09-30) · not tagged

- Moved from the legacy "Rev 10" integer to `MM.mm.rrr_YYMMDD` revision tracking.
- Added the 4-section Help menu: How to Use This Field Report, Standards and Formulas, FAQs, Revision Log.
- Same day, unnumbered: packaged as an installable, offline-capable app (PWA) with a web app manifest, service worker and icons, and published at masdtools.net.

## 01.00.000 — Rev 10 baseline (2026-09-30) · not tagged

This is the feature set at the start of formal tracking. It is inventoried in full in **Help → Revision Log** and `CHANGELOG.md`. The legacy revisions r1–r10 before it were not itemized at the time.

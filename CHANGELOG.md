# Changelog

All notable changes to the Edwards ModuLaser MASD Field Report are documented here.

Format: `MM.mm.rrr` (major.minor.revision), date `YYYY-MM-DD`. Major and minor
versions are set manually by the document owner; the revision counter increments by
one per distinct logical change and resets when the minor/major version changes.
This file is generated from the app's own in-app log (Help → Revision Log) — that
log (`AMENDMENTS` / `LEGACY` in `index.html`) is the source of truth; regenerate
this file from it rather than hand-editing both. Per-release summaries are in
[RELEASE_NOTES.md](RELEASE_NOTES.md).

## 01.00 — 2026-09-30 to 2026-10-09

- **01.00.005** (2026-10-09): Import PipeCAD (.pl) now accepts several files at once and merges them into one PipeCAD project, so the floors and detectors from separate .pl files land in one report. The first file supplies the project header (site, location, designer, units, version); every floor and saved result from the later files is appended. IDs that clash with an earlier file are renumbered and their detector-to-results links rewritten; a floor or detector name already used in an earlier file gets the source file name appended, since sheets are matched by detector name. Files in different units are refused. The preview lists every merge note, and Download merged .pl saves the combined file so later re-imports use one file.
- **01.00.004** (2026-10-07): Revision Log rebuilt as a complete release archive, matching the Battery Calculator: identity card (Application / Revision / Authored by), Revision and Date cells in the toolbar, readable YYYY-MM-DD dates, a 000 Baseline entry inventorying the Rev 10 feature set, and a reconstructed Legacy history section (legacy r1–r10 summary and the 260930 installable/offline packaging). Repository now carries CHANGELOG.md (generated from this log) and RELEASE_NOTES.md; GitHub releases are tagged vMM.mm.rrr starting with v01.00.003 (Rev 11).
- **01.00.003** (2026-10-07): Rev 11: corrected built-in performance targets to the Table 45 (p.112, FM 3230 / NFPA 76) Fire 1 per-hole sensitivity: VEWFD 0.2 → 1.0 %obs/ft (0.2 is the VEWFD Alert threshold and is not applied per hole), SFD now ≤2.5 %obs/ft. Added per-hole PipeCAD design checks (worst hole sensitivity vs Fire 1, predicted transport time vs target) with pass/fail and margin.
- **01.00.002** (2026-10-07): Rev 11: added Import PipeCAD (.pl). Reads a PipeCAD 3.6 project export in the browser, shows a preview for confirmation, then pre-fills Section A (site, designer, location note, installing company if blank, PipeCAD reference) and one detector sheet per PipeCAD detector (descriptor, fan speed, Alarm Factor with a not-activated flag, PipeCAD transport time, sampling-hole count) plus a new PipeCAD design-data block: pipe name/length, total flow, hole balance, fittings, design sensitivity and the full hole table. End-cap test points are listed separately and excluded from worst-hole and max-transport checks. Re-importing updates the matching sheets and keeps field-entered data. Address, part number, alarm levels and flow limits are not imported.
- **01.00.001** (2026-09-30): Migrated from the legacy single-integer “Rev 10” scheme to formal MM.mm.rrr_YYMMDD revision tracking (patch counter restarted at 001 per document owner). Prior r1–r10 history: iterative development of the module/PSU index, per-device sheets, automatic PASS/FAIL/INCOMPLETE evaluation, wiring verification, auto-collected deficiencies, module test summary, and sign-off — through Rev 10’s current single-page, autosaving, print-ready form. Added the 4-section Help menu (How to Use This Field Report, Standards and Formulas, FAQs, Revision Log) and this amendments table.
- **01.00.000** (2026-09-30): Baseline — the Rev 10 feature set at the start of formal revision tracking (before the 001 Help menu). A — Project Information (site, job, address, commissioning date, applicable standard, installing company, installer, commissioning engineer, system designer, owner contact, PipeCAD reference, FACU, SLC panel quantity, notes). B — 17-item Pre-Power-Up Inspection (Y / N / N/A with notes and a live rollup). C — Module & Power Supply Index — detector, standard display, command display and other modules kept in SenseNET address order (1–127, duplicates flagged), power supplies, and a shared Test setup block. D — per-module sheets — identity and location, IN1/IN2/OUT1–OUT3 FACU programming with PPP:CCC:DDDD address validation (display OUT1 fixed to General Fault), configuration (alarm levels, Alarm Factor 0–8, fan speed 1–16, flow limits ≤20%, delays, Day/Night, FastLearn, Demo Mode, access codes, baseline, filter); detector page 2 with performance target (NFPA 76 VEWFD/EWFD/SFD, EN 54-20 Class A/B/C, Custom), average hole sensitivity = chamber sensitivity × holes, T1 transport time vs PipeCAD with variance, T2 three-run smoke test with spread, T3 airflow fault, T4 input/output test. E — power supply sheets (identity, battery, AC-fail and trouble monitoring points, battery/standby test vs required hours). F — SenseNET / SNET+ node-to-node wiring verification (continuity, isolation, capacitance with total nF). G — 22-item Final Commissioning Checklist with auto-collected deficiencies. H — Module Test Summary. I — acceptance status and three-party sign-off. Automatic PASS / FAIL / INCOMPLETE per section and device, with an override applied only when a reason is entered. Autosave to the browser, Export / Import job (.json), New job, and Print / PDF on Portrait Letter with running headers, footers and Page X of Y.

## Legacy (pre-tracking) — reconstructed

Unnumbered history from before formal revision tracking, reconstructed from the
Rev 10 file and the repository history. Per-revision detail for legacy r1–r10 was
not recorded and is summarized rather than itemized.

- **PWA packaging** (2026-09-30): Packaged the Rev 10 report as an installable, offline-first web app: manifest.json (name, colors, icons), a service worker (sw.js) that caches the app shell and refreshes it in the background, app icons (192 px, 512 px, maskable 512 px, Apple touch), and install meta tags; published with GitHub Pages at masdtools.net. Recorded retroactively from the repository history — unnumbered, the app revision stayed 01.00.001.
- **r1–r10** (before 2026-09-30): Legacy integer revisions r1 through r10: iterative development of the module and power supply index, per-device sheets, automatic PASS / FAIL / INCOMPLETE evaluation, wiring verification, auto-collected deficiencies, the module test summary and sign-off, ending in Rev 10’s single-page, autosaving, print-ready form (inventoried in 01.00.000). Per-revision detail was not recorded at the time and cannot be itemized; this row is reconstructed from the Rev 10 file and the 01.00.001 migration note.

## Release tagging

GitHub releases are tagged `vMM.mm.rrr` matching the in-app revision (the
`_YYMMDD` date suffix appears in-app only). "Rev 11" is the field name for
01.00.002–01.00.003, released as **v01.00.003**; **v01.00.004** adds this
revision archive. Revisions 01.00.000–01.00.001 predate tagging.

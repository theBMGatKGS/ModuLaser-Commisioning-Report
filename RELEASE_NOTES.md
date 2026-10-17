# Release Notes — Edwards ModuLaser MASD Field Report

Release-by-release summaries, newest first. Each GitHub release is tagged `vMM.mm.rrr`
and its text is taken from the matching section below. The itemized, per-change
history is in [CHANGELOG.md](CHANGELOG.md) and in the app under **Help → Revision Log**,
which is the source of truth.

Live site: [masdtools.net](https://masdtools.net) (served from the
`MASD-Commissioning-Report` branch).

---

## v02.01.000 — MiniLaser ASD support (2026-10-16) · not yet released

- **MiniLaser ASD (FHSD8075-ULF) (Brent 2026-10-16).** New module type, standalone and never addressed (SenseNET checks don't apply). It comes in from the Battery Calculator 02.01.000 / Toolbox 00.02.000 project file, from a PipeCAD .pl (SOLO detectors), or via **+ MiniLaser**.
- **MiniLaser class from a .pl (Brent-approved):** area override → project standard → SFD (max transport time no longer used). A MiniLaser from a .pl is non-pre-engineered by default (Brent); DIP/Remote advice follows the fan 2/4/7/10 + AF 2/4/6/8 rule; `modulaser-project.js` 1.5.0 updated in place (identical in all three apps). A 40 % flow-fault level shows PASS with a warning note (Brent-approved).
- **QA delta (02.01.000 review).** F1: a new "Holes / pipe length (M p.66)" check fails a MiniLaser with more holes than its application allows (e.g. 20 holes on a VEWFD application, where the max is 10) or a longer pipe than allowed. F5: the 40% flow-fault note reads "UL/FM requires ≤20% (M p.71)" (still a PASS row with a warning). Tests: `minilaser_report_test.py` uses the fixture `/workspace/qa/minilaser/hoistway.mlproj.json` (no /tmp leftovers) and writes everything under `$MLP_TEST_OUT`.
- **Setup:** R1 Fault relay (fixed, fail-safe), R2 Relay output 1 (Prealarm), R3 Relay output 2 (Fire Alarm), IN1 (15 kΩ supervised). Each I/O Expansion Module (9-30521, 0–2) adds X1/X2 OUT1–5 (latched relays, 2 A @ 30 VDC) and IN1–2.
- **Configure:** fan speed and Alarm Factor come from the design. Application (Table 35), configuration method, alarm delay and flow-fault level/delay start blank, with no numeric prefills. A blank fan speed shows INCOMPLETE ⚠ in amber.
- **Checks:** hole sensitivity (Fire 1 for the alarm factor × holes) and measured transport time are checked against Table 35 for the selected application. A 40% flow fault on a UL/FM application is a warning only. Tests cover transport, smoke, airflow fault and relays/inputs. Print/Word/Excel exports include the MiniLaser sheet.
- `modulaser-project.js` 1.5.0. New test: `tests/minilaser_report_test.py` (20), which includes the pl-merge round trip.

### QA audit
- Pending.

---

## v02.00.003 — Revision order and Windows installer (2026-10-16) · released 2026-10-16

**In-app revision:** 02.00.003_261016

### Highlights
- **Revision order fixed.** The in-app revision log listed 02.00.002 before 02.00.001, and the app reads the last entry, so the live site, saved job files and the v02.00.002 installer build showed 02.00.001. The log is in order again; a new regression test (`tests/revision_order.test.js`) fails if it goes out of order or if the page title or offline cache name don't match.
- **Windows installer attached to the release.** This repo uses immutable releases, so the old workflow's upload after publishing failed (HTTP 422) and v02.00.001 / v02.00.002 have no installer. The workflow now builds `ModuLaser-MASD-Field-Report-Setup-02.00.003.exe`, attaches it to a **draft** release, and the release is published afterwards.
- **Workflow hardening (QA W1–W3).** Only the release job can write to the repo; manual release runs must come from `main`; if tag `v<rev>` already exists without a release, the run fails instead of attaching the draft to the old commit.
- No changes to checks, calculations or the project file (modulaser-project.js 1.4.0, MASD engine 1.0.0).
- The installer is unsigned, so Windows SmartScreen warns on first run (**More info → Run anyway**).

### QA audit
| Date | Commit audited | Result | Issue |
|---|---|---|---|
| 2026-10-16 | Report 2a388de | QA/Auditor PASS, no blockers: root cause reproduced on de287fb and fixed (02.00.003 in title, About, savedBy, site.rev and job filename); older .mlproj/job files import; workflow only creates/updates a draft; installer sha256 matches, version 2.0.3, packaged app files byte-identical to 2a388de; shared modulaser-project.js 1.4.0 identical in all three apps; suites revision_order 10/10, mlp_network 11/11, sens 14/14, sync 2/2, test_report 31/31, save_import 5/5, g1 13/13, empty 17/17. Non-blocking findings W1–W3 fixed before release; F2 (unsigned installer) known. | — |

---

## v02.00.002 — SenseNET networks (2026-10-16) · released 2026-10-16

**In-app revision:** 02.00.002_261016

### Highlights
- **SenseNET networks (G1, modulaser-project.js 1.4.0).** Each module keeps its SenseNET network from the Battery Calculator design (older files → SenseNET 1). The Device Index and Summary show it (*Net*: SN1, SN2…, SA = standalone), and you can edit it under Identity. Duplicate addresses are checked per network. More than 127 modules in total is allowed when every network has 127 or fewer; import is blocked only when one network would exceed 127.
- Shared **modulaser-project.js 1.4.0** (per-network validator, network in the design diff) is byte-identical in the Battery Calculator 02.00.004, MASD Engineering Toolbox 00.01.002 and this Report (harmonization rule). MASD engine 1.0.0 is unchanged.

### QA audit
| Date | Commit audited | Result | Issue |
|---|---|---|---|
| 2026-10-16 | Calculator 951f769 / Toolbox 956e1e1 / Report de287fb | QA 2026-10-16: Calculator 951f769 / Toolbox 956e1e1 / Report de287fb GO | — |

---

## v02.00.001 — Audit trail, field-change loop and Performance Criteria (2026-10-13) · released 2026-10-13

**In-app revision:** 02.00.001_261013

### Highlights
- **Append-only edit log** (who, when, old, new, why), typical-value confirmations logged, Saved-by holds the technician name.
- **Field changes / As-built** (Section J): each change to a design value logged with why and photo; technician sign-off; printable report. Changes and approvals (technician → designer → QA) round-trip with the **MASD Engineering Toolbox 00.01.000**.
- **Performance Criteria** from the Toolbox printed on the summary page: the referenced standard (NFPA presets with the UL 268, 7th Edition statement; FM DS 5-32/5-48 FM only; BS 5839-1 or Custom), code prescriptions, limits (pass at or below, ≤) with references, Area/Group overrides, narrative, Engineer of Record and spec reference.
- Save keeps unknown keys, changes and approvals. SHA-256 design and site hashes.
- **Shared MASD engine 1.0.0** and **modulaser-project.js 1.3.0**, identical in the Battery Calculator, this Report and the Toolbox. Harmonization rule: a change to a shared module bumps every app that carries it, with matching notes.

### QA audit
| Date | Commit audited | Result | Issue |
|---|---|---|---|
| 2026-10-13 | 6854f2e (v02.00.000) | Defaults citations FAIL → fixed · Solano rule PASS · Audit trail FAIL → fixed · Quick Start version FAIL → fixed | [#8](https://github.com/theBMGatKGS/ModuLaser-Commisioning-Report/issues/8) |
| 2026-10-13 re-check (8:28–8:45 PM ET) | 786337f | **CONDITIONAL PASS** — fixed after re-check: stable design hash, mis-cited table number removed, UL 268 confirmation required, UL thresholds (≤60/43/43 s), sign-off order enforced, name-gated edits, append-only log, ASAG44201 replaced by NFPA 76-2024 clauses, Quick Start 02.00.001+, legacy Ah checks | [#8](https://github.com/theBMGatKGS/ModuLaser-Commisioning-Report/issues/8) |

**Fixes included:** citations (App. A printed p.113 FM/UL hole limits, pass at or below (≤); EN 54-20 p.112; flow ±20% and 120 s delay Table 29 p.76; ClassiFire factors Table 24 p.71; Prealarm replaces "Action"); unsourced defaults labelled typical – unverified; Save preserves changes, approvals and unknown keys; append-only edit log; SHA-256 hashes; Saved-by name; metric hole-sensitivity warning.
**QA re-check (2026-10-13):** CONDITIONAL PASS; post-re-check fixes listed above and in the revision log.
**Final verdict:**

QA audit 2026-10-13, final re-check of commit 0625e4e (clean tree). **PASS with one minor open item.** Tests: test_report 31/31, report_audit_test 22/22. Verified: the hole-sensitivity rule (since changed to ≤, see the QA delta below), citations to Install Manual 04-4001-501-0803-05 (Table 24 p.71, Table 26, Table 29 p.76, App. A p.113) and NFPA 76-2024 clauses, no "Table 45" references, EWFD/SFD Alert labelled site/design choice, Save keeps changes, approvals and unknown fields, append-only edit log (no overwrite) with who/when, SHA-256 design and site hashes. Open: actions that aren't field edits (e.g. Confirm typical values) can still be logged as "(name not set)". Issue: https://github.com/theBMGatKGS/ModuLaser-Commisioning-Report/issues/8

QA delta re-check 2026-10-13, commit b965064 (clean). **PASS.** Verified: ≤ rule at the limit (1.00 passes, 1.01 fails), the more restrictive of UL and NFPA limits, UL range lower bounds for the most-sensitive hole and the fastest transport, and the technician-name gate on every edit, including Confirm typical values, stopwatch, photo and import (the earlier open item is closed). Tests: test_report 31/31, report_audit_test 31/31. Note: under UL, holes more sensitive than the Open Area lower limit (1.70 %obs/ft) and transport under 6 s are reported outside the listed range by design (per Brent). Final pre-tag pass 2026-10-13 (10:02–10:40 PM ET): Calculator 6adde0d / Report 5448488 (release a32d988) / Toolbox 8aa707a — GO; sens_rule 14/14; committed tests pass (release commits differ from these only by this release-note line).


---

## v02.00.000 — Redesign and shared project file (2026-10-13)

**In-app revision:** 02.00.000_261013 · **Includes:** 02.00.000 (folds in the unreleased 01.00.005 multi-file .pl import and merge tool, and the Windows installer)

### Highlights
- **ModuLaser project file (`.mlproj.json`)** shared with the Battery Calculator 02.00.001. Import project creates every detector, display and power supply sheet with addresses, Area/Group, power supply, battery and required Ah, and the PipeCAD pipe and hole data. Re-import shows a diff and never overwrites site results or hand edits unless you tick them. Save project writes site results back into the same file without touching the design.
- **New layout:** dark PipeCAD-style theme with a one-tap light theme; menus and quick row; sidebar with PASS/FAIL/INCOMPLETE dots; one sheet at a time with Setup / Configure / Test tabs; pinned results panel with transport-time and battery gauges.
- **Typical defaults** for alarm levels, flow limits and delays by performance class, tagged "confirm on site".
- **New checks:** duplicate SenseNET/FACU addresses, names over 16 characters, measured vs PipeCAD transport time, installed vs required battery Ah.
- **Print / Export:** Summary / Standard / Full, PDF, Word, HTML, Excel (CAD Schedule + Detail).
- **Mobile:** bottom bar, stopwatch, photos, Go to device (QR or text).
- **Windows installer** (Electron, NSIS) built from `electron/`.

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
- **VEWFD per-hole sensitivity limit corrected from 0.2 to 1.0 %obs/ft.** It is now the App. A table (printed p.113, FM 3230 / NFPA 76) **Fire 1** threshold. 0.2 %obs/ft is the VEWFD *Alert* stage and is not applied per hole.
- **SFD** now carries App. A p.113's ≤2.5 %obs/ft (it had no sensitivity limit before). EWFD is unchanged at ≤1.5 %obs/ft.
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

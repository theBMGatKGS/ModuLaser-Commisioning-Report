# Edwards ModuLaser MASD — Field Report

A single-file, offline HTML tool for commissioning Edwards ModuLaser Modular Aspirating Smoke Detector (MASD) installations. No install, no server, no dependencies — open the file in a browser and go.

**Current revision:** 01.00.001_260930 (see in-app Help → Revision Log for the full amendment history)

## What it does

This is a structured field-commissioning worksheet covering the full workflow for a ModuLaser cluster:

- **A — Project Information**: site, job, and contact details
- **B — Pre-Power-Up Inspection**: 17-item checklist before power is applied
- **C — Module & Power Supply Index**: add detector, display, and other modules, plus power supplies; each gets its own sheet
- **D — Module Sheets**: identity, I/O programming, configuration (alarm levels, fan speed, flow limits), and performance/transport-time/smoke/airflow tests for each module
- **E — Power Supply Sheets**: identity, FACU monitoring points, and battery/power tests
- **F — SenseNET / SNET+ Wiring Verification**: per-segment continuity, isolation, and capacitance checks
- **G — Final Commissioning Checklist**: 22-item final checklist, with deficiencies auto-collected from every failed item across the report
- **H — Module Test Summary**: pass/fail rollup tiles and tables across every device
- **I — System Acceptance & Sign-Off**: technician, engineer, and owner sign-off with acceptance status

Every module and power supply gets an automatic **PASS / FAIL / INCOMPLETE** result, with a technician-override mechanism that requires a documented reason to apply.

The toolbar's **Help** button opens reference material: a step-by-step Quick Start and worked example, the manual tables and specs the tool's limits are drawn from (with page citations), an FAQ, and the full revision log.

## How to use it

1. Download `ModuLaser_MASD_Field_Report_Rev10.html` from this repo.
2. Open it in any modern desktop browser (Chrome, Edge, Firefox, Safari).
3. Work through Sections A–I. Your entries **autosave to that browser** (no account, no server) a fraction of a second after each change — the toolbar shows the autosave status.
4. Use **Export job** to save a `.json` copy of the data (for backup, or to hand a job off to another technician's machine), and **Import job** to load one back in.
5. Use **Print / PDF** when the report is complete — it prints to a clean, plain Portrait Letter layout with running headers and footers.

## Notes

- All data stays local to your browser unless you explicitly export it — nothing is sent anywhere.
- Autosave is per-browser, per-device. It is not a substitute for exporting a `.json` copy if you need the job to survive a browser reset or move to another machine.
- Manual citations in the Help → Standards and Formulas section reference Edwards ModuLaser Installation Manual P/N 04-4001-501-2803-07, REV 007 (UL/FM Applications edition). See that section for two known discrepancies between the manual and this tool's built-in defaults that are flagged but intentionally not auto-corrected.

## License

Internal tool — not for redistribution outside its intended use.

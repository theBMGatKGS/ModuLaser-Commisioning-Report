# Edwards ModuLaser MASD — Field Report

An installable, offline-first web app for commissioning Edwards ModuLaser Modular Aspirating Smoke Detector (MASD) installations. No app store, no build step, no server-side code — deploy the static files and it installs like a native app.

**Current revision:** 01.00.004_261007, released as **v01.00.004**. "Rev 11" (PipeCAD import) is **v01.00.003**.
Full history: in-app **Help → Revision Log** (source of truth), [CHANGELOG.md](CHANGELOG.md) (generated from it) and [RELEASE_NOTES.md](RELEASE_NOTES.md) (per-release summaries).

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

**Import PipeCAD (.pl)** pre-fills the report from a PipeCAD 3.6 project export.
- It fills Section A and one detector sheet per PipeCAD detector: fan speed, Alarm Factor, predicted transport time, pipe length, flow, fittings, and the full hole table.
- It checks each sampling hole's sensitivity against the selected target's **Fire 1** limit (Table 45: VEWFD ≤1.0, EWFD ≤1.5, SFD ≤2.5 %obs/ft) and the predicted transport time against the time limit, showing pass/fail and margin.
- A preview lists every change, and nothing is written until you confirm.

### PipeCAD .pl Merge (separate tool)

[`pl-merge.html`](pl-merge.html) (live at `/pl-merge.html` next to the report) combines several PipeCAD `.pl` project files into one, for example one file per floor. It runs in the browser and nothing is uploaded.
- The first file in the list supplies the project header (name, location, designer, company, units, PipeCAD version). Reorder the list to choose it.
- Every floor, detector, pipe network and saved result from the other files is appended.
- IDs that clash are renumbered and their references updated. Repeated floor or detector names get the source file name added.
- Files with different units are refused.
- **Download merged .pl**, then import that one file into the report with **Import PipeCAD (.pl)**.
- End-cap test points are excluded from the checks.
- Address, part number, alarm levels and flow limits are left for field entry.

The toolbar shows the running **Revision** and **Date**. Its **Help** button opens reference material:
- a step-by-step Quick Start and worked example;
- the manual tables and specs the tool's limits are drawn from, with page citations;
- an FAQ;
- the full Revision Log: every change since the Rev 10 baseline, plus the reconstructed legacy history.

## Files in this repo

- `index.html` — the app itself
- `manifest.json` — the web app manifest (name, icons, colors) that makes it installable
- `sw.js` — service worker that caches the app shell so it loads and works with no signal
- `icons/` — app icons (192px, 512px, a maskable 512px variant for Android, and an Apple touch icon)
- `CHANGELOG.md` — itemized change history, generated from the in-app Revision Log
- `RELEASE_NOTES.md` — per-release summaries; the text used for each GitHub release (tags `vMM.mm.rrr`)

## Deploying it

This only needs static file hosting **over HTTPS** — service workers refuse to register over plain `file://` or `http://`, so a browser opened directly from a downloaded file will still *run* the tool but won't install it. GitHub Pages, Netlify, or any static host works:

1. Push this repo's contents to GitHub.
2. In the repo's Settings → Pages, set the source to your main branch (root).
3. GitHub gives you a URL like `https://yourusername.github.io/repo-name/`.

## Installing it

Open the hosted URL on the device that will use it:

- **Android / desktop Chrome or Edge**: an install icon appears in the address bar (or Menu → "Install app…" / "Add to Home screen"). It then opens in its own window with no browser chrome.
- **iOS / iPadOS Safari**: Share button → "Add to Home Screen." (iOS doesn't support the browser install prompt, but the home-screen icon works the same way.)
- **Desktop**, once installed, behaves like any other app — its own icon, its own window, launches without opening a browser tab first.

## Using it

1. Open the installed app (or the hosted URL — both work identically; installing just adds the icon and drops the browser chrome).
2. Work through Sections A–I. Your entries **autosave to the device** (no account, no server) a fraction of a second after each change — the toolbar shows the autosave status.
3. Optional: use **Import PipeCAD (.pl)** to pre-fill Section A and the detector sheets from the PipeCAD project file. Review the preview, then confirm. Re-importing an updated `.pl` keeps everything entered in the field.
4. Use **Export job** to save a `.json` copy of the data (for backup, or to hand a job off to another technician's device), and **Import job** to load one back in.
5. Use **Print / PDF** when the report is complete — it prints to a clean, plain Portrait Letter layout with running headers and footers.

Once installed, the app opens and works with **no signal or Wi-Fi** — the service worker caches everything it needs the first time it's loaded online. Autosave, printing, and export/import all continue to work offline; only fetching a newer version of the app itself requires connectivity.

## Notes

- All data stays local to the device unless you explicitly export it — nothing is sent anywhere.
- Autosave is per-browser, per-device. It is not a substitute for exporting a `.json` copy if you need the job to survive a browser reset, an uninstall, or a move to another device.
- When you push an update to `index.html`:
  - Bump `CACHE_NAME` at the top of `sw.js` to the next revision. That is what tells already-installed copies to fetch the new version instead of serving the cached one.
  - Add the change to `AMENDMENTS` in `index.html`.
  - Regenerate `CHANGELOG.md` from it.
  - Add a `RELEASE_NOTES.md` section for the new tag.
- Manual citations in the Help → Standards and Formulas section reference Edwards ModuLaser Installation Manual P/N 04-4001-501-2803-07, REV 007 (UL/FM Applications edition). That section lists the known discrepancies between the manual and this tool's built-in defaults. Two are still open and intentionally not auto-corrected: the EOL resistor tolerance wording in Section B, and the EN 54-20 Class A/B/C limits. The third, the VEWFD sensitivity figure, was resolved in 01.00.003: the per-hole limit is now the Table 45 Fire 1 value, 1.0 %obs/ft.

## License

Internal tool — not for redistribution outside its intended use.

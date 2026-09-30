# Edwards ModuLaser MASD — Field Report

An installable, offline-first web app for commissioning Edwards ModuLaser Modular Aspirating Smoke Detector (MASD) installations. No app store, no build step, no server-side code — deploy the static files and it installs like a native app.

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

## Files in this repo

- `index.html` — the app itself
- `manifest.json` — the web app manifest (name, icons, colors) that makes it installable
- `sw.js` — service worker that caches the app shell so it loads and works with no signal
- `icons/` — app icons (192px, 512px, a maskable 512px variant for Android, and an Apple touch icon)

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
3. Use **Export job** to save a `.json` copy of the data (for backup, or to hand a job off to another technician's device), and **Import job** to load one back in.
4. Use **Print / PDF** when the report is complete — it prints to a clean, plain Portrait Letter layout with running headers and footers.

Once installed, the app opens and works with **no signal or Wi-Fi** — the service worker caches everything it needs the first time it's loaded online. Autosave, printing, and export/import all continue to work offline; only fetching a newer version of the app itself requires connectivity.

## Notes

- All data stays local to the device unless you explicitly export it — nothing is sent anywhere.
- Autosave is per-browser, per-device. It is not a substitute for exporting a `.json` copy if you need the job to survive a browser reset, an uninstall, or a move to another device.
- When you push an update to `index.html`, bump `CACHE_NAME` at the top of `sw.js` (e.g. to the next revision) — that's what tells already-installed copies to fetch the new version instead of continuing to serve the cached one.
- Manual citations in the Help → Standards and Formulas section reference Edwards ModuLaser Installation Manual P/N 04-4001-501-2803-07, REV 007 (UL/FM Applications edition). See that section for two known discrepancies between the manual and this tool's built-in defaults that are flagged but intentionally not auto-corrected.

## License

Internal tool — not for redistribution outside its intended use.

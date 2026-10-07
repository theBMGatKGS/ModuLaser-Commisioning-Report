ModuLaser Tools

This repository holds two independent Edwards ModuLaser tools, each on its own branch. They don't share code or data — pick the one you need and follow its section below.

Tool	Branch	What it's for
ModuLaser Battery Calculator	MASD-Battery-Calculator	Sizing power supplies and batteries for a ModuLaser SenseNET network at design time
ModuLaser MASD Field Report	MASD-Commissioning-Report	Commissioning and field-testing an installed ModuLaser system
A note on branches vs. the live site

GitHub Pages can only serve one branch of a repo as a live website at a time — right now that's MASD-Commissioning-Report (the Field Report, published at masdtools.net). The MASD-Battery-Calculator branch holds real, complete code, but it isn't automatically published anywhere; to use it, either:

Switch to that branch on GitHub and download index.html (or the whole branch as a ZIP: Code → switch to MASD-Battery-Calculator in the branch dropdown → Code → Download ZIP), then open the file locally in a browser, or
Ask to have it published as its own site — that takes either a second repository with its own GitHub Pages site, or moving to a build process that publishes both tools as subfolders of one live site. Either is straightforward to set up if you want both tools live under one URL at the same time.
ModuLaser Battery Calculator

Branch: MASD-Battery-Calculator — switch to it here

A power-supply and battery sizing tool for a ModuLaser SenseNET network, built from Brent's original Excel sizing worksheet. Each "Location" page in the tool represents one power supply sheet; every sheet in a document together represents one SenseNET network.

What it covers:

Per-sheet module tables (address, zone, module type, model, cluster, power source, fan speed, current draw), with network-wide unique address/cluster/circuit enforcement
Ribbon vs. own-circuit power modeling, with automatic ribbon segment grouping and reordering
Battery and power supply sizing against multiple Design Basis presets — NFPA 72, NFPA 72 + NFPA 110 generator backup, UFC 3-600-01, AWS, BS 5839-1, CAN/ULC-S524 — each with its own formula and code citation
Automatic hardware recommendations and a generated Bill of Materials with real Edwards part numbers
Multi-supply load balancing when one power supply isn't enough
A granular formula-transparency view showing every calculation step
A 4-section in-app Help menu (How to Use the Calculator, Standards and Formulas, FAQs, Revision Log) and full MM.mm.rrr_YYMMDD revision history

How to use it:

Download index.html from the MASD-Battery-Calculator branch (see the note above).
Open it in any modern desktop browser — nothing to install.
Add a Location (power supply sheet) per physical power supply, then add modules to each.
Pick a Design Basis and battery size — the tool flags missing/invalid entries and recommends hardware and battery capacity automatically.
Use Save As to download a portable copy of your work, or rely on browser autosave for the current session (autosave doesn't move between devices — Save As is what does).
Export to Excel or print/PDF when the design is ready to hand off.

The in-app Help button covers all of this in more depth, including a full worked example.

ModuLaser MASD Field Report

Branch: MASD-Commissioning-Report — live at masdtools.net

An installable, offline-first commissioning worksheet for a ModuLaser system that's already being installed in the field — this is the tool a technician uses on-site, not at the design stage.

What it covers:

Project information, a 17-item pre-power-up inspection, and a 22-item final commissioning checklist
A module and power supply index, with a dedicated sheet per device covering identity, I/O programming, configuration, and performance/transport-time/smoke/airflow testing
SenseNET/SNET+ wiring verification per segment
Automatic PASS/FAIL/INCOMPLETE results per device, with a documented-reason override mechanism
Import PipeCAD (.pl): pre-fills project info and one detector sheet per PipeCAD detector from a PipeCAD 3.6 project export — preview and confirm first; each sampling hole's sensitivity is checked against the target's Fire 1 limit (Table 45: VEWFD ≤1.0 %obs/ft) and the predicted transport time against the time limit, with pass/fail and margin
An auto-collected deficiencies list pulling from every failed item across the whole report
A module test summary and full three-party sign-off (technician, engineer, owner)
The same 4-section Help menu structure and MM.mm.rrr_YYMMDD revision tracking as the battery calculator

How to use it:

Open masdtools.net on the device you'll use in the field.
Install it (Chrome/Edge: install icon in the address bar; iOS Safari: Share → Add to Home Screen) so it works with no signal on-site, or just use it in the browser tab — both work identically.
Work through Sections A–I in order. Entries autosave to the device automatically.
Use Export job / Import job to move a job's data between devices or archive it, and Print / PDF for a clean, signed printed copy once commissioning is complete.

The in-app Help button has the full Quick Start, a worked example, manual citations for every built-in limit, an FAQ, and the complete Revision Log. Current release: v01.00.004 ("Rev 11" PipeCAD import is v01.00.003). For release history, see CHANGELOG.md and RELEASE_NOTES.md on the MASD-Commissioning-Report branch.

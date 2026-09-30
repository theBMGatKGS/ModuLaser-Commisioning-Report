# Help Menu & Revision Tracking — Build Instructions for the ModuLaser Commissioning Guide

Extracted and generalized from the ModuLaser Battery Calculator's Help menu and
versioning system (currently Revision 01.04.008), for retrofitting onto the
ModuLaser commissioning guide (currently `modulaser-install-guide_r5.html`, an
11-step interactive HTML tool with a module log, auto-save, and print
stylesheet — built in a separate session, not this one).

Paste this whole document into whatever chat/session is actively working on the
commissioning guide, as the instructions for adding a Help menu and formalizing
its revision tracking.

---

## Part 1 — The Help menu: 4 sections, exactly this structure

A modal overlay (not a separate page), opened by a "Help" button in the main
toolbar, closed by an X button or clicking outside the card. Inside it, a nav bar
with 4 anchor links to 4 sections, in this order:

1. **How to Use the Calculator** *(keep this literal name even though this
   document isn't a calculator — it's the established convention; rename only if
   it reads as actively confusing once you see it in context)*
2. **Standards and Formulas**
3. **FAQs**
4. **Revision Log**

### 1.1 — "How to Use the Calculator"

Contains **two distinct subsections** (don't merge them):

- **Quick Start**: numbered, sequential steps — the actual set of things a user
  must do, in order, for a complete successful session. Each step gets a short
  title and a paragraph. Optionally illustrate a step with a small figure
  (wireframe image or screenshot) and a figcaption citing what it shows.
- **Worked Example**: one full, concrete walkthrough with real (example) values
  filled in start to finish — not abstract instructions, an actual worked case a
  reader can follow alongside their own real one.

**For the commissioning guide specifically:** the existing 11 HTML steps are
your Quick Start content almost directly — reorganize/renumber them into this
subsection rather than writing new content. For Worked Example, build one
concrete walkthrough of commissioning a single sample cluster end to end —
General Guidelines review → Designer Requirements gathered → physical
install → pipe connection + initial functional test → basic configuration
(alarm thresholds, fan speed, I/O) → FastLearn → final checks — with realistic
example values (an example address range, example fan speed settings, an
example transport-time reading) rather than instructions alone.

**Audit for completeness before finalizing this section** — the same review
done for the battery calculator's Quick Start surfaced real gaps that had
accumulated silently (a whole module type never mentioned, real toolbar features
like Save/Export never documented). Do the equivalent pass here: read through
the actual current guide end to end and confirm Quick Start actually mentions
every real feature/requirement — Auto-save + "Save now", the Print full guide
button, the Verified/Initials columns on the module log, the EOL-both-ends
caution, and the FastLearn/intermediate-learn timing notes are all real,
already-built pieces worth explicitly double-checking are represented.

### 1.2 — "Standards and Formulas"

For the battery calculator this section holds the actual sizing formulas, shown
in real notation, plus general regulatory content (listing requirements,
compatibility, circuit ratings, etc.) — it's the section that answers "what's
the actual technical/regulatory backing for this, and where does it come from."

**For the commissioning guide, this is the natural home for:**
- The installation manual's specific cited tables and figures — General
  Guidelines Table 2 (Do's/Don'ts), Table 20/21 (inputs), Table 22/23 (outputs),
  Table 24/25 (alarm thresholds), Table 29 (fan speed) — reproduce the
  substance, cite the exact manual P/N, table number, and page for each (you're
  already doing this per-step as "Manual reference" lines; this section is where
  they get collected and shown as reference material in their own right, not
  just scattered inline).
- Wiring specifications (16-18 AWG terminal requirements, EOL termination on
  both ends of distributed portions, SNET+ ribbon restrictions, EMT knockout
  notes) as a standalone reference, not just inline cautions.
- UL/FM listing information and any other manufacturer/regulatory citation that
  isn't itself a step in the procedure.
- **Explicitly note which manual edition/P/N each piece of content is sourced
  from** — the guide currently mixes citations from two manual editions
  (04-4001-501-2803-05 for most sections, 04-4001-501-2803-07 for Basic
  Configuration specifically) and a reader needs to know which applies where.

### 1.3 — "FAQs"

Deeper-dive Q&A for things that don't belong in the linear Quick Start flow:
edge cases, "why does it work this way," troubleshooting. Candidates already
implied by the existing build notes: what the Auto-save toggle actually does
and doesn't cover, why EOL termination is required on both ends specifically,
what FastLearn vs. the full intermediate learn period each actually verifies
and why the smoke-pen transport-time check is preliminary only (formal
validation still requires a certified technician), why access codes should be
changed from defaults, what happens if the module log's duplicate-address or
DIP-pattern check catches a conflict.

### 1.4 — "Revision Log"

The document's identity block (name, current revision, author) as this
section's **header**, with the full running amendments table below it as the
section's body — not two separate things, one flows into the other.

---

## Part 2 — Revision tracking: format `MM.mm.rrr_YYMMDD`

- **MM** (major) and **mm** (minor): controlled exclusively by the document
  owner (Brent). Never auto-incremented by whoever's building it. Bumped only
  when explicitly told to.
- **rrr** (patch): auto-increments by 1 per distinct logical change within a
  work session, each one logged as its own row in a running amendments array.
- **YYMMDD**: the actual date of the change.
- **Proactive suggestion, not automatic action**: when a change seems
  significant enough to warrant a major or minor bump, say so and suggest which
  one — but the decision and the actual bump stay with the document owner.
- **When mm or MM changes, rrr conventionally restarts** — confirm the exact
  restart value with the document owner when it happens (the battery
  calculator's convention was restarting at 001, not 000).
- **Each amendment log entry needs to be able to carry its own minor/major
  version snapshot**, separate from whatever the current global version is —
  see the pitfall below; this isn't optional polish, it prevents a real, already
  -encountered bug.
- Shown as identity cells (Revision / Date) somewhere visible in the main UI
  (title bar or similar), plus the full amendments table in Help → Revision Log.

### 2.1 — Migrating from the existing "rN" scheme

The guide is currently at "r5" with no visible amendment-by-amendment log (based
on the build history, each "rN" bump likely bundled multiple distinct changes
without a per-change record). Recommended migration:

1. Pick a starting `MM.mm` — this is the document owner's call, not something to
   assume. A reasonable default if none is specified: `01.00`, treating the
   current r5 state as the "before" snapshot and this migration itself as the
   first logged change under the new scheme.
2. Don't attempt to reverse-engineer a full per-change history for r1–r5 — log
   one entry summarizing "prior revisions r1 through r5: [brief summary of what
   they covered, from whatever history is available]" and start granular,
   per-change logging from this point forward.
3. Confirm the starting rrr value (000 vs 001) with the document owner rather
   than assuming.

### 2.2 — The implementation pattern (portable, concrete)

This is exactly how the battery calculator does it — directly reusable since
both documents are plain HTML/CSS/JS, not a framework:

```js
const APP_MAJOR = "01";
const APP_MINOR = "00";

const AMENDMENTS = [
  { rev: "000", date: "YYMMDD", desc: "Initial migration to formal revision tracking; summarizes prior r1-r5 history: ..." },
  { rev: "001", date: "YYMMDD", desc: "..." },
  // each new distinct change appends one entry here
];

function renderRevisionInfo(){
  const latest = AMENDMENTS[AMENDMENTS.length - 1];
  const revShort = `${APP_MAJOR}.${latest.minor || APP_MINOR}.${latest.rev}`;
  const fullRev = `${revShort}_${latest.date}`;
  // populate title-bar Revision/Date cells and the Help -> Revision Log header from fullRev

  const amendBody = document.getElementById('amendments-table-body');
  amendBody.innerHTML = AMENDMENTS.slice().reverse().map(a =>
    // .minor fallback below is what keeps OLD entries correctly labeled even
    // after a LATER minor-version bump changes APP_MINOR — see pitfall 3.1
    `<tr><td>${APP_MAJOR}.${a.minor || "00"}.${a.rev}</td><td>${a.date}</td><td>${a.desc}</td></tr>`
  ).join('');
}
```

---

## Part 3 — Pitfalls encountered building this pattern the first time

Don't rediscover these the hard way — they're real, already-fixed bugs from the
battery calculator's own history of building exactly this system.

1. **Amendment log entries need their own version snapshot.** A naive
   implementation renders every row using the *current* global `APP_MAJOR` /
   `APP_MINOR` — which silently relabels every historical entry the moment a
   later minor/major bump happens (a row logged under 01.00 gets shown as 01.01
   after the next bump, misrepresenting when it actually happened). Fix: give
   each amendment entry an optional `minor` (and, if it ever comes up, `major`)
   field, defaulting to whatever the value was *at the time that entry was
   logged*, and read from the entry's own field first, falling back to the
   current global only for entries that predate this fix.
2. **Verify before citing.** Any specific manual table/figure/page citation, or
   any manufacturer spec claim, should be checked against the actual source
   document before being written into Standards and Formulas — don't
   reconstruct a citation from memory or infer a page number.
3. **A completeness audit of "How to Use" is worth doing deliberately, not
   assumed.** The battery calculator's Quick Start had gone stale relative to
   real, already-built features (an entire module type, real toolbar buttons)
   simply through incremental drift over many rounds of work — nobody
   individually forgot anything, it just accumulated. Do one explicit read-
   through of the actual current tool against the actual current Quick Start
   content before considering this section done, not just when something is
   pointed out as missing.

---

## Part 4 — Suggested first steps, in order

1. Confirm the starting `MM.mm` and the rrr restart value with Brent (2.1).
2. Add the Help overlay shell (button, modal, nav, 4 empty section containers)
   and the identity block + amendments table skeleton in Revision Log.
3. Populate Quick Start by reorganizing the existing 11 steps' content into this
   subsection — don't rewrite from scratch, restructure what already exists.
4. Do the completeness audit (Part 1.1) before writing Worked Example — better
   to catch gaps before building the walkthrough than to write an example around
   an incomplete picture of the tool.
5. Write Worked Example, Standards and Formulas, and FAQs.
6. Log the migration itself as the first amendment entry (2.1, step 2).

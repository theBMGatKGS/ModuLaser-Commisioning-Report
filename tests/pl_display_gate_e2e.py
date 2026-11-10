"""Playwright E2E: Field Report bare PipeCAD .pl import → Displays prompt (same flow as the Calculator, Q7B),
job time zone (R4A) and S4B change records.  Synthetic fixtures from tests/pl_display_fixtures.py (temp folder).
Covers QA re-review RB1 (the gate shows and the import completes), RM3 (per-floor Accept / Change type / Skip and
grouping), RM1 (no silent device zone; invalid zones refused), and the S4B Low (MLP.changeId ids + dev field).
Run: python3 tests/pl_display_gate_e2e.py        (RPT= overrides the default index.html)
"""
import asyncio, os, sys
from pathlib import Path
from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pl_display_fixtures as FX
RPT = os.environ.get('RPT') or (HERE.parent / 'index.html').resolve().as_uri()
F = FX.write_all()

R = []
def ok(n, c, i=''):
    R.append((n, bool(c)))
    print(('PASS' if c else 'FAIL'), n, ('' if c else str(i)[:300]))

async def fresh(pg, tz_tech=True):
    await pg.goto(RPT)
    await pg.evaluate('localStorage.clear()'); await pg.reload()
    await pg.wait_for_function('typeof rpGateDisplaysThenImport==="function" && typeof state!=="undefined"')
    if tz_tech: await pg.evaluate("sessionStorage.setItem('mfr-technician','Example Tech')")

async def dlg_title(pg):
    return await pg.evaluate("document.getElementById('dlg').classList.contains('show') ? document.getElementById('dlgTitle').textContent : ''")

async def click_btn(pg, label):
    await pg.evaluate("""(l)=>{ const b=[...document.querySelectorAll('#dlgBtns button')].find(x=>x.textContent.trim().startsWith(l)); b.click(); }""", label)
    await pg.wait_for_timeout(200)

async def import_pl(pg, path):
    await pg.set_input_files('#importPl', [str(path)])
    await pg.wait_for_function("document.getElementById('dlg').classList.contains('show')")
    await pg.wait_for_timeout(100)

async def counts(pg):
    return await pg.evaluate("""()=>({ devs:(state.design&&state.design.devices||[]).length, assumed:(state.design&&state.design.devices||[]).filter(d=>d.origin==='assumed').length,
      mods: state.modules.length })""")

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 1400, 'height': 1000}, timezone_id='Asia/Tokyo')
        pg = await ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('dialog', lambda d: asyncio.ensure_future(d.accept()))

        # RB1: the gate shows after "Import 20 devices"
        await fresh(pg)
        await import_pl(pg, F['two_floor'])
        ok('Review dialog offers Import 20 devices', 'Import 20 devices' in await pg.inner_text('#dlgBtns'))
        await click_btn(pg, 'Import 20 devices')
        t = await dlg_title(pg)
        ok('RB1: Displays gate is visible after Import (not hidden by the review close)', t == 'Displays missing or under-provisioned', t)
        body = await pg.inner_text('#dlgBody')
        ok('S1A: both floors MISSING; PipeCAD-first copy', body.count('MISSING') == 2 and 'PipeCAD' in body, body[:200])
        pri = await pg.evaluate("[...document.querySelectorAll('#dlgBtns button.pri')].map(b=>b.textContent)")
        ok('S1A: Stop import is the primary button', pri and pri[0].startswith('Stop import'), pri)
        ok('Nothing imported while the gate is open', (await counts(pg))['devs'] == 0)
        # Stop
        await click_btn(pg, 'Stop import')
        ok('Stop: dialog closed, nothing imported', not await dlg_title(pg) and (await counts(pg))['devs'] == 0, await counts(pg))

        # Continue → per-floor step (RM3)
        await import_pl(pg, F['two_floor']); await click_btn(pg, 'Import 20 devices')
        await click_btn(pg, 'Continue without PipeCAD displays')
        t = await dlg_title(pg)
        ok('RM3: Continue opens the per-floor Displays step', t == 'Displays — choose per floor', t)
        body = await pg.inner_text('#dlgBody')
        ok('RM3: Delta (8 det) S2A Accept / type / Skip; Alpha (12 det) S3B grouping into 2 new displays',
           await pg.locator('[data-dacc]').count() == 1 and await pg.locator('[data-dtype]').count() == 1 and await pg.locator('[data-dskip]').count() == 2
           and await pg.locator('[data-dgrp]').count() == 12 and await pg.locator('[data-ntype]').count() == 2, body[:300])
        await click_btn(pg, 'Continue import')
        msg = await pg.inner_text('#dlgMsg')
        ok('RM3: undecided floors block Continue with a message', 'Accept' in msg or 'unassigned' in msg, msg)
        ok('RM3: still nothing imported', (await counts(pg))['devs'] == 0)
        # over 8 on one display is refused
        await pg.evaluate("()=>document.querySelectorAll('[data-dgrp]').forEach(s=>{ s.value='n:0'; })")
        await pg.evaluate("()=>{ const s=document.querySelector('[data-dtype]'); s.value='Minimum Display'; s.dispatchEvent(new Event('change')); }")
        await click_btn(pg, 'Continue import')
        msg = await pg.inner_text('#dlgMsg')
        ok('RM3: more than 8 detectors on one display refused', 'more than 8' in msg, msg)
        ok('RM3: Change type ticks Accept', await pg.evaluate("document.querySelector('[data-dacc]').checked"))
        await pg.evaluate("()=>[...document.querySelectorAll('[data-dgrp]')].forEach((s,i)=>{ s.value = i < 8 ? 'n:0' : 'n:1'; })")
        await pg.evaluate("()=>{ const s=document.querySelector('[data-ntype$=\"|1\"]'); s.value='Minimum Display'; }")
        await click_btn(pg, 'Continue import')
        await pg.wait_for_timeout(400)
        c = await counts(pg)
        ok('RB1: import completes — 20 devices + 3 assumed displays', c['devs'] == 23 and c['assumed'] == 3 and c['mods'] >= 23, c)
        info = await pg.evaluate("""()=>state.design.devices.filter(d=>d.origin==='assumed').map(d=>({area:d.area,type:d.type,rule:d.assumption.rule,n:(d.assumption.members||[]).length,name:d.name}))""")
        ok('RM3: Delta gets 1 Minimum (accepted type); Alpha gets Standard (8) + Minimum (4)',
           sorted((i['area'][-5:], i['type'], i['n']) for i in info) == [('Alpha', 'Minimum Display', 4), ('Alpha', 'Standard Display', 8), ('Delta', 'Minimum Display', 8)], info)
        ok('Assumed names ≤ 16 characters', all(len(i['name']) <= 16 for i in info), info)
        plan = await pg.evaluate("state.design.displayPlan || null")
        ok('Per-floor decisions recorded (displayPlan)', plan and len(plan) == 2, plan)
        ok('Dialog closed after import', not await dlg_title(pg))

        # Skip path
        await fresh(pg)
        await import_pl(pg, F['two_floor']); await click_btn(pg, 'Import 20 devices')
        await click_btn(pg, 'Continue without PipeCAD displays')
        await pg.evaluate("()=>document.querySelectorAll('[data-dskip]').forEach(c=>{ c.checked=true; c.dispatchEvent(new Event('change')); })")
        await click_btn(pg, 'Continue import'); await pg.wait_for_timeout(300)
        c = await counts(pg)
        ok('Skip all floors: import completes with no assumed displays', c['devs'] == 20 and c['assumed'] == 0, c)

        # No shortage: imports straight through
        await fresh(pg)
        await import_pl(pg, F['ok_one']); await click_btn(pg, 'Import 5 devices'); await pg.wait_for_timeout(300)
        c = await counts(pg)
        ok('No shortage: no gate, import completes', c['devs'] == 5 and not await dlg_title(pg), c)

        # RM1: job time zone
        tz = await pg.evaluate("rpJobTimeZone()")
        ok('RM1: blank job zone → device zone, said out loud, nothing stored', tz['source'] == 'device' and tz['timeZone'] == 'Asia/Tokyo' and 'not set' in tz['note'] and not (await pg.evaluate("state.project.timeZone")), tz)
        await pg.evaluate("()=>{ state.ui.view='sec:A'; renderAll(); }")
        ok('RM1: Project information shows the not-set warning', 'Job time zone not set' in await pg.inner_text('#app'))
        await pg.fill('[data-k="project.timeZone"]', 'Mars/Olympus'); await pg.press('[data-k="project.timeZone"]', 'Tab'); await pg.wait_for_timeout(300)
        ok('RM1: invalid zone refused (cleared + dialog)', await pg.evaluate("state.project.timeZone") == '' and await dlg_title(pg) == 'Job time zone', await pg.evaluate("state.project.timeZone"))
        await pg.evaluate("document.getElementById('dlg').classList.remove('show')")
        await pg.fill('[data-k="project.timeZone"]', 'america/chicago'); await pg.press('[data-k="project.timeZone"]', 'Tab'); await pg.wait_for_timeout(300)
        tz = await pg.evaluate("rpJobTimeZone()")
        ok('RM1: valid zone stored canonically and used', await pg.evaluate("state.project.timeZone") == 'America/Chicago' and tz['source'] == 'project' and tz['timeZone'] == 'America/Chicago', tz)
        when = await pg.evaluate("rpFmtWhen('2026-11-10T01:00:00Z')")
        ok('RM1: As-Built time in the job zone (01:00Z → 7:00 PM CT)', '7:00:00 PM' in when and '11/9/2026' in when, when)

        # S4B change record: MLP.changeId + dev
        await fresh(pg)
        await import_pl(pg, F['two_floor']); await click_btn(pg, 'Import 20 devices')
        await click_btn(pg, 'Continue without PipeCAD displays')
        await pg.evaluate("()=>{ document.querySelectorAll('[data-dskip]').forEach((c,i)=>{ if(i===0){ c.checked=true; c.dispatchEvent(new Event('change')); } }); document.querySelector('[data-dacc]').checked=true; }")
        await click_btn(pg, 'Continue import'); await pg.wait_for_timeout(300)
        dev = await pg.evaluate("state.design.devices.find(d=>d.origin==='assumed').id")
        await pg.evaluate("(id)=>rpAssumedDialog('confirm', id)", dev); await pg.wait_for_timeout(200)
        await pg.fill('#rp-assumed-why', 'Example: installed per drawing'); await click_btn(pg, 'Record'); await pg.wait_for_timeout(200)
        ch = await pg.evaluate("state.changes.slice(-1)[0]")
        ok('S4B Low: change entry uses MLP.changeId() and carries dev', ch and str(ch.get('id', '')).startswith('fc-') and ch.get('dev') == dev and ch.get('by') == 'Example Tech', ch)
        ok('S4B: design untouched (still assumed)', await pg.evaluate("(id)=>state.design.devices.find(d=>d.id===id).origin", dev) == 'assumed')

        ok('Report: no page errors', not errs, errs[:3])
        await b.close()
    failed = sum(1 for _, c in R if not c)
    print(f'{len(R) - failed}/{len(R)} passed' + (f', {failed} failed' if failed else ''))
    sys.exit(1 if failed else 0)

if __name__ == '__main__':
    asyncio.run(main())

"""Report 02.01.000 — MiniLaser ASD (FHSD8075-ULF). Real data: Brent's Hoistway .pl and a Calculator 02.01.000 project file built from it.
Run: python3 tests/minilaser_report_test.py   (ML_PROJECT=<.mlproj.json from the Calculator> ML_FIXTURE=<.pl> SHOTS=<dir>; MERGE_WITH=<second .pl for the pl-merge round trip>)"""
import asyncio, glob, json, os, sys, tempfile
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = 'file://' + ROOT + '/index.html'; MERGE = 'file://' + ROOT + '/pl-merge.html'
PROJ = os.environ.get('ML_PROJECT', '/tmp/mlout/hoistway.mlproj.json')
PL = os.environ.get('ML_FIXTURE', '/workspace/qa/minilaser/minilaser.pl')
OTHER = os.environ.get('MERGE_WITH') or (sorted(glob.glob('/workspace/pl-samples/*.pl')) or [''])[0]
SHOTS = os.environ.get('SHOTS') or tempfile.mkdtemp(prefix='rpt-ml-'); os.makedirs(SHOTS, exist_ok=True)
R = []
def ok(n, c, i=''): R.append(bool(c)); print('PASS' if c else 'FAIL', n, str(i)[:300])
async def confirm_dialog(pg):
    await pg.wait_for_timeout(400)
    btn = pg.locator('#dlgBtns .pbtn.pri'); 
    if await btn.count(): await btn.first.click(); await pg.wait_for_timeout(400)
async def ml(pg): return await pg.evaluate("(()=>{const i=state.modules.findIndex(m=>m.type==='ml'); return i<0?null:{i, m:state.modules[i]};})()")
async def setk(pg, k, v): await pg.evaluate("([k,v])=>{ s(k,v); save(); renderAll(); }", [k, v])
async def main():
  async with async_playwright() as p:
    b = await p.chromium.launch(); ctx = await b.new_context(viewport={'width': 1500, 'height': 1000}, accept_downloads=True); pg = await ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.goto(APP); await pg.evaluate('localStorage.clear()'); await pg.reload(); await pg.wait_for_timeout(600)
    v = await pg.evaluate('[fullRev(), MLP.VERSION, document.title]')
    ok('revision 02.01.000_261016, MLP 1.5.0', v[0] == '02.01.000_261016' and v[1] == '1.5.0' and '02.01.000' in v[2], v)
    # ---- Calculator project file
    await pg.evaluate('t=>importProjectText(t, "hoistway.mlproj.json")', open(PROJ).read()); await confirm_dialog(pg)
    x = await ml(pg)
    ok('project file: MiniLaser imported as type ml (standalone, no address)', x and x['m']['sn'] == '' and x['m']['net'] == 'S', x and {k: x['m'].get(k) for k in ('type', 'sn', 'net', 'model', 'desc')})
    i = x['i']; m = x['m']
    ok('fan 6, alarm factor 8, Remote, 8 holes from the design', m['cfg'].get('fan') == '6' and m['cfg'].get('af') == '8' and m['cfg'].get('method') == 'Remote' and m['perf'].get('holes') == '8', [m['cfg'], m['perf']])
    ok('model FHSD8075-ULF; R1 fixed Fault', m.get('model') == 'FHSD8075-ULF' and m['io'].get('r1', {}).get('used') and m['io']['r1'].get('fn') == 'Fault', [m.get('model'), m['io']])
    ok('no numeric alarm prefills (application, delay, flow blank; no typical values)', not any(m['cfg'].get(k) for k in ('app', 'alarmDly', 'flowLevel', 'flowDly')) and not m.get('typical'), m['cfg'])
    await setk(pg, f'modules.{i}.ioModules', '2'); await pg.evaluate(f"go('mod:'+state.modules[{i}].id,'setup')"); await pg.wait_for_timeout(300)
    ports = await pg.evaluate("[...document.querySelectorAll('.ml-io tbody td.n')].map(t=>t.childNodes[0].textContent.trim())")
    ok('relay labels exact', ports[:3] == ['R1 Fault relay (fixed)', 'R2 Relay output 1 (Prealarm)', 'R3 Relay output 2 (Fire Alarm)'], ports[:4])
    ok('IN1 + 2 expansion modules → 18 ports (X1/X2 OUT1–5, IN1–2)', len(ports) == 18 and ports[3].startswith('IN1') and any(p.startswith('X2 IN2') for p in ports), len(ports))
    ok('no SenseNET address field on the MiniLaser sheet', await pg.evaluate(f"!document.querySelector('[data-k=\"modules.{i}.sn\"]')"))
    await pg.screenshot(path=SHOTS + '/30-report-minilaser-setup.png')
    # ---- Table 35
    await setk(pg, f'modules.{i}.cfg.app', 'UL 268 Ed.7 OAP')
    e = await pg.evaluate(f"evalModule(state.modules[{i}]).it.filter(x=>x.sec==='perf')")
    ok('Table 35 OAP: 8 × 0.25 = 2.00 within 1.70–2.18 → PASS', e and e[0]['st'] == 'P', e)
    await setk(pg, f'modules.{i}.cfg.app', 'UL 268 Ed.7 SA Range 1')
    e = await pg.evaluate(f"evalModule(state.modules[{i}]).it.filter(x=>x.sec==='perf')")
    ok('Table 35 SA Range 1: 2.00 > 1.00 → FAIL with Table 35 note', e and e[0]['st'] == 'F' and 'Table 35' in e[0]['note'], e)
    await setk(pg, f'modules.{i}.cfg.app', 'FM 3230 SFD')
    e = await pg.evaluate(f"evalModule(state.modules[{i}]).it.filter(x=>x.sec==='perf')")
    ok('Table 35 FM 3230 SFD: 2.00 < 2.50 → PASS', e and e[0]['st'] == 'P', e)
    await setk(pg, f'modules.{i}.t.tt.meas', '130')
    e = await pg.evaluate(f"evalModule(state.modules[{i}]).it.filter(x=>x.sec==='tt' && x.label==='Measured transport time')")
    ok('FM 3230 SFD transport 130 s ≥ 120 → FAIL', e and e[0]['st'] == 'F', e)
    await setk(pg, f'modules.{i}.cfg.flowLevel', '40')
    e = await pg.evaluate(f"evalModule(state.modules[{i}]).it.filter(x=>/Flow fault level/.test(x.label))")
    ok('flow fault 40% on FM/UL → warning only (not FAIL)', all(x['st'] != 'F' for x in e) and any('Warning' in x['note'] for x in e), e)
    await pg.evaluate(f"go('mod:'+state.modules[{i}].id,'config')"); await pg.wait_for_timeout(300)
    ok('warning shown on the Configure tab', '40% flow fault on a UL/FM application' in await pg.evaluate("document.getElementById('app').textContent"))
    await pg.screenshot(path=SHOTS + '/31-report-minilaser-configure.png')
    await pg.evaluate(f"go('mod:'+state.modules[{i}].id,'test')"); await pg.wait_for_timeout(300)
    await pg.screenshot(path=SHOTS + '/32-report-minilaser-test.png')
    # ---- blank fan (hand-added) → incomplete amber
    await pg.evaluate("addModule('ml')"); await pg.wait_for_timeout(300)
    h = await pg.evaluate("(()=>{const m=state.modules.find(x=>x.type==='ml' && !x.dev); return [m.sn, m.net, m.io.r1, evalModule(m).it.find(x=>x.label==='Fan speed'), !!document.querySelector('tr.ml-needs')];})()")
    ok('+ MiniLaser: no address, R1 fixed, blank fan INCOMPLETE ⚠ (amber row)', h[0] == '' and h[1] == 'S' and h[2]['fn'] == 'Fault' and h[3]['st'] == 'B' and '⚠' in h[3]['note'] and h[4], h)
    # ---- print
    blocks = await pg.evaluate("JSON.stringify(buildBlocks({level:'standard', scope:'all', checklists:true, photos:false}))")
    ok('print/export: MiniLaser sheet with application row', 'MiniLaser (FHSD8075-ULF)' in blocks and 'Application (Table 35)' in blocks)
    # ---- .pl import straight into the Report
    await pg.evaluate("localStorage.clear(); setTech('QA MiniLaser'); state=upgradeState(blank()); save(); renderAll();")
    await pg.set_input_files('#importPl', PL); await confirm_dialog(pg)
    x = await ml(pg)
    ok('.pl import: SOLO → MiniLaser (fan 6, AF 8 derived, 8 holes)', x and x['m']['cfg'].get('fan') == '6' and x['m']['cfg'].get('af') == '8' and x['m']['perf'].get('holes') == '8', x and [x['m']['cfg'], x['m']['perf']])
    # ---- pl-merge round trip
    if OTHER:
        mp = await ctx.new_page(); mp.on('pageerror', lambda e: errs.append('merge: ' + str(e)))
        cands = [OTHER] + [x for x in sorted(glob.glob('/workspace/pl-samples/*.pl')) if x != OTHER]
        cp = os.path.join(tempfile.gettempdir(), 'minilaser-copy.pl'); open(cp, 'w').write(open(PL).read()); cands.append(cp)
        xml = None; used = None
        for c in cands:
            await mp.goto(MERGE); await mp.set_input_files('#pick', [c, PL]); await mp.wait_for_timeout(800)
            xml = await mp.evaluate("merged && merged.xml")
            if xml: used = os.path.basename(c); break
        ok('pl-merge: merged file produced', bool(xml), used)
        if xml:
            out = os.path.join(SHOTS, '..', 'merged-hoistway.pl') if False else os.path.join(tempfile.gettempdir(), 'merged-hoistway.pl'); open(out, 'w').write(xml)
            r = await pg.evaluate("t=>{ const pc=MLP.parsePl(t,'merged.pl'); const all=pc.groups.flatMap(g=>g.detectors); const s=all.filter(d=>d.kind==='minilaser'); return [s.length, s.every(d=>d.fan===6), s.every(d=>d.typeRaw==='SOLO'), all.length]; }", xml)
            ok('pl-merge round trip: every SOLO stays a MiniLaser (fan 6) after merge', r[0] >= 1 and r[1] and r[2] and r[0] == (r[3] if used == 'minilaser-copy.pl' else r[0]), r)
        await mp.close()
    ok('no page errors', not errs, errs)
    await b.close()
  print(f'SUMMARY {sum(R)} / {len(R)}'); sys.exit(0 if all(R) else 1)
asyncio.run(main())

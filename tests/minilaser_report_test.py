"""Report 02.01.000 — MiniLaser ASD (FHSD8075-ULF). Synthetic data: Example-Shaft-MiniLaser.pl and a Calculator project file built from it.
Run: python3 tests/minilaser_report_test.py   (ML_PROJECT=<.mlproj.json from the Calculator> ML_FIXTURE=<.pl> SHOTS=<dir>; MERGE_WITH=<second .pl for the pl-merge round trip>)
Fixtures: the synthetic .pl is generated at test time by tests/make_synthetic_pl.py; the project file is tests/fixtures/Example-Shaft-MiniLaser.mlproj.json
(written by the Calculator's tests/minilaser_test.py from that synthetic .pl). ML_PROJECT / ML_FIXTURE point at other files; checks SKIP when they are absent. All output goes to $MLP_TEST_OUT (or a fresh temp dir); nothing is written to fixed names in the system temp dir."""
import asyncio, glob, json, os, sys, tempfile
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = 'file://' + ROOT + '/index.html'; MERGE = 'file://' + ROOT + '/pl-merge.html'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import make_synthetic_pl
SYN = os.environ.get('SYNTH_DIR', '/workspace/plbuild/synth')
PROJ = os.environ.get('ML_PROJECT') or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'Example-Shaft-MiniLaser.mlproj.json')
PL = os.environ.get('ML_FIXTURE') or make_synthetic_pl.ensure('shaft_ml', SYN)
_missing = [x for x in (PROJ, PL) if not os.path.exists(x)]
REQUIRE = os.environ.get('REQUIRE_FIXTURES') == '1'   # set in release/CI runs: a missing fixture is then a failure
OTHER = os.environ.get('MERGE_WITH') or make_synthetic_pl.ensure('campus', SYN)
OUT = os.environ.get('MLP_TEST_OUT') or tempfile.mkdtemp(prefix='rpt-ml-'); os.makedirs(OUT, exist_ok=True)
SHOTS = os.environ.get('SHOTS') or os.path.join(OUT, 'shots'); os.makedirs(SHOTS, exist_ok=True)
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
    ok('revision 02.02.001_261020, MLP 1.6.3', v[0] == '02.02.001_261020' and v[1] == '1.6.3' and '02.02.001' in v[2], v)
    # QA F1 (M p.66 pipe limits) and F5 (40% flow wording)
    r = await pg.evaluate("""()=>{ const mk=(app,h,fl)=>({type:'ml',desc:'ML',cfg:{app,af:'2',flowLevel:fl},perf:{holes:String(h)},t:{},io:{}});
      const row=(m,re)=>evalMl(m).it.find(i=>re.test(i.label));
      return [row(mk('UL 268 Ed.7 SA Range 1',30,'20'),/Holes . pipe/), row(mk('FM 3230 VEWFD',20,'20'),/Holes . pipe/), row(mk('FM 3230 VEWFD',10,'20'),/Holes . pipe/), row(mk('FM 3230 SFD',8,'40'),/Flow fault level on a UL/)]; }""")
    ok('F1: SA Range 1 with 30 holes → FAIL (max 25, M p.66)', r[0] and r[0]['st'] == 'F' and 'maximum of 25' in r[0]['note'], r[0])
    ok('F1: FM VEWFD with 20 holes → FAIL (max 10); 10 holes → PASS', r[1] and r[1]['st'] == 'F' and 'maximum of 10' in r[1]['note'] and r[2] and r[2]['st'] == 'P', r[1:3])
    ok('F5: 40% flow on UL/FM → PASS row with "UL/FM requires ≤20% (M p.71)"', r[3] and r[3]['st'] == 'P' and 'UL/FM requires ≤20% (M p.71)' in r[3]['note'], r[3])
    if _missing:   # real fixtures stay off GitHub; the fixture-free checks above still ran
        print('SKIP MiniLaser project/.pl checks: fixture(s) not present: ' + ', '.join(_missing) + " (set ML_PROJECT / ML_FIXTURE)")
        ok('no page errors', not errs, errs); await b.close()
        print(f'SUMMARY {sum(R)} / {len(R)} passed, SKIPPED: MiniLaser project section (fixtures absent)' + (' — REQUIRE_FIXTURES=1, failing' if REQUIRE else ''))
        sys.exit(1 if (REQUIRE or not all(R)) else 0)
    # ---- Calculator project file
    await pg.evaluate('t=>importProjectText(t, "Example-Shaft-MiniLaser.mlproj.json")', open(PROJ).read()); await confirm_dialog(pg)
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
        cands = [OTHER] + [x for x in sorted(glob.glob(os.path.join(SYN, '*.pl'))) if x != OTHER and x != PL]
        cp = os.path.join(OUT, 'minilaser-copy.pl'); open(cp, 'w').write(open(PL).read()); cands.append(cp)
        xml = None; used = None
        for c in cands:
            await mp.goto(MERGE); await mp.set_input_files('#pick', [c, PL]); await mp.wait_for_timeout(800)
            xml = await mp.evaluate("merged && merged.xml")
            if xml: used = os.path.basename(c); break
        ok('pl-merge: merged file produced', bool(xml), used)
        if xml:
            out = os.path.join(OUT, 'merged-shaft.pl'); open(out, 'w').write(xml)
            r = await pg.evaluate("t=>{ const pc=MLP.parsePl(t,'merged.pl'); const all=pc.groups.flatMap(g=>g.detectors); const s=all.filter(d=>d.kind==='minilaser'); return [s.length, s.every(d=>d.fan===6), s.every(d=>d.typeRaw==='SOLO'), all.length]; }", xml)
            ok('pl-merge round trip: every SOLO stays a MiniLaser (fan 6) after merge', r[0] >= 1 and r[1] and r[2] and r[0] == (r[3] if used == 'minilaser-copy.pl' else r[0]), r)
        await mp.close()
    ok('no page errors', not errs, errs)
    await b.close()
  print(f'SUMMARY {sum(R)} / {len(R)}'); sys.exit(0 if all(R) else 1)
asyncio.run(main())

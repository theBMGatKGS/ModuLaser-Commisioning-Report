"""Report 02.02.000 — unidentified power source rolls to ⚠ Incomplete; Help / How do I / FAQ topics; About text; brand title; src copy in sync."""
import asyncio, os, re, sys
from playwright.async_api import async_playwright
D=os.path.join(os.path.dirname(__file__), '..'); URL=os.environ.get('RPT_URL','file://'+os.path.abspath(os.path.join(D,'index.html')))
R=[]
def ok(n,c,i=''): R.append(bool(c)); print('PASS' if c else 'FAIL',n,str(i)[:300])
s=open(os.path.join(D,'index.html')).read()
ok('src/rp-0202.js == inline <script id="rp-0202">', open(os.path.join(D,'src/rp-0202.js')).read().strip()==re.search(r'<script id="rp-0202">\n(.*?)\n</script>',s,re.S).group(1).strip())
ok('FAQ: Toolbox 00.03.000, engine 1.2.0, MLP 1.6.1 (QA F12)', 'The Toolbox (00.03.000)' in s and 'MASD engine 1.2.0 and modulaser-project.js 1.6.1' in s and 'The Toolbox (00.01.000)' not in s)
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.on('dialog',lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(URL); await pg.evaluate('localStorage.clear()'); await pg.reload(); await pg.wait_for_timeout(1200)
    h=await pg.evaluate("({s:[...document.querySelectorAll('.hstep .ht')].map(e=>e.textContent), q:[...document.querySelectorAll('.hq dt')].map(e=>e.textContent), about:(document.getElementById('rp-about-0202')||{}).textContent||'', title:document.title, app:(document.querySelector('.rp-app-name')||{}).textContent})")
    ok('Help steps: brand, ASD-160, FACU', all(any(k in t for t in h['s']) for k in ['Brand (Edwards | Kidde Commercial)','ASD-160 (Micra25','FACU powers the ASDs']), h['s'][-4:])
    ok('How do I: brand, ASD-160, power source', all(any(k in t for t in h['q']) for k in ['change the brand','commission an ASD-160','power source not identified']))
    ok('FAQ: part-number basis, +20 %, Incomplete after FACU', all(any(k in t for t in h['q']) for k in ['part-number basis','20 % over PipeCAD','Incomplete after unticking FACU']))
    ok('About: Edwards + Kidde Commercial, MiniLaser, ASD-160, MLP 1.6.1', all(k in h['about'] for k in ['Kidde Commercial','MiniLaser','ASD-160','1.6.1']), h['about'])
    ok('title/app name follow the brand, rev 02.02.001', h['title'].startswith('Edwards ModuLaser MASD') and '02.02.001' in h['title'] and h['app'].startswith('Edwards'), [h['title'],h['app']])
    r=await pg.evaluate("""(()=>{const p={label:'PS-1',model:'BPS6A',loc:'Riser',ckt:'1'}; state.project=state.project||{}; delete state.project.powerSource; const a=evalPsu(p);
      state.project.powerSource='unidentified'; const u=evalPsu(p); renderAll(); const bn=document.getElementById('psrcBanner');
      const out=[a.it.some(i=>i.label==='Power source identified'), u.auto, u.final, u.secs.id, u.it.slice(-1)[0].label, !!bn && !bn.hidden && bn.textContent.includes('\u26a0 Incomplete')];
      state.project.powerSource='in-house'; const f=evalPsu(p); renderAll(); out.push(f.it.some(i=>i.label==='Power source identified'), !document.getElementById('psrcBanner') || document.getElementById('psrcBanner').hidden); return out})()""")
    ok('unidentified power source → PSU INCOMPLETE with a blank item and amber banner; cleared when identified', r[0] is False and r[1]=='INCOMPLETE' and r[2]=='INCOMPLETE' and r[3]=='B' and r[4]=='Power source identified' and r[5] and r[6] is False and r[7], r)
    txt=await pg.evaluate("(()=>{const d=MLP.blank(); d.project={name:'Example Project'}; d.design={psus:[{id:'sheet-1',sheet:1,name:'PS-1',model:'BPS6A',powerSource:'unidentified',facuSource:false,status:'INCOMPLETE'}],devices:[]}; return MLP.stringify(d,'test','02.02.000_261019','QA')})()")
    import tempfile; fp=os.path.join(tempfile.mkdtemp(),'psrc.mlproj.json'); open(fp,'w').write(txt)
    await pg.evaluate('localStorage.clear()'); await pg.reload(); await pg.wait_for_timeout(1000)
    await pg.evaluate("sessionStorage.setItem('mfr-technician','QA Tech')")
    await pg.set_input_files('#importProj', fp); await pg.wait_for_selector('#dlg.show', timeout=15000); await pg.click('#dlgApply'); await pg.wait_for_timeout(800)
    r=await pg.evaluate("[state.project && state.project.powerSource, !!document.getElementById('psrcBanner') && !document.getElementById('psrcBanner').hidden]")
    ok('import: design.psus[].powerSource unidentified carries into the Report (banner shown)', r==['unidentified', True], r)
    ok('no page errors', not [e for e in errs], errs[:3])
    await b.close()
asyncio.run(main())
print(f'{sum(R)}/{len(R)} passed'); sys.exit(0 if all(R) else 1)

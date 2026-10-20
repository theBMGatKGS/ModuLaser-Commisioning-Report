"""02.02.001 QA delta (F1 + notice): Report validates the SFD/OAP target against the linked design's device kinds; one-time notice for older designs."""
import asyncio, os, sys
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); APP = 'file://' + ROOT + '/index.html'
R = []
def ok(n, c, i=''): R.append((n, bool(c))); print('PASS' if c else 'FAIL', n, str(i)[:300])
FM = "(()=>{const P=MLP.perfScopeInit({areas:{},sfdSchema:1,narrative:'x',narrativeConfirmed:true},'SFD – FM DS 5-48'); P.sfdTarget={value:3.5,ref:'FM letter',initials:'BW',family:'FM'}; return P;})()"
async def main():
  async with async_playwright() as p:
    b = await p.chromium.launch(); pg = await b.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.goto(APP); await pg.evaluate('localStorage.clear()'); await pg.reload(); await pg.wait_for_timeout(700)
    txt = await pg.evaluate("()=>{state.design={devices:[{id:'a1',kind:'asd160'},{id:'a2',kind:'asd160'}],performance:" + FM + "}; return JSON.stringify(buildBlocks({level:'standard',scope:'all',checklists:true,photos:false}))}")
    ok('F1: FM project, only ASD-160s, target 3.5 → no SFD/OAP deficiency printed', 'SFD/OAP target 3.5' not in txt and 'Performance Criteria' in txt, txt[txt.find('incomplete'):][:200] if 'incomplete' in txt else '')
    txt2 = await pg.evaluate("()=>{state.design={devices:[{id:'d1',kind:'detector'},{id:'a1',kind:'asd160'}],performance:" + FM + "}; return JSON.stringify(buildBlocks({level:'standard',scope:'all',checklists:true,photos:false}))}")
    ok('F1: same target with a ModuLaser present → deficiency printed (≤ 2.50)', 'SFD/OAP target 3.5' in txt2 and '2.50' in txt2)
    ok('rpSfdKinds reads design.devices', await pg.evaluate("JSON.stringify(rpSfdKinds())") == '["detector","asd160"]')
    await pg.evaluate("()=>{state.design={devices:[],performance:{standard:'SFD/OAP – NFPA 72',areas:{},limits:{},codeReqs:[]}};}")
    await pg.wait_for_timeout(1500)
    ok('older linked design: one-time notice shown', await pg.query_selector('#mlp-sfd-notice') is not None)
    sh = os.environ.get('SHOTS')
    if sh: os.makedirs(sh, exist_ok=True); await pg.screenshot(path=os.path.join(sh, 'sfd-09-report-notice.png'))
    await pg.click('#mlp-sfd-notice-ok'); await pg.wait_for_timeout(1300)
    ok('notice dismissed and not shown again', await pg.query_selector('#mlp-sfd-notice') is None and await pg.evaluate('state.design.performance.sfdNotice') is False)
    ok('no page errors', not errs, errs)
    await b.close()
  f = [n for n, c in R if not c]; print(f'\n{len(R)-len(f)} passed, {len(f)} failed'); sys.exit(1 if f else 0)
asyncio.run(main())

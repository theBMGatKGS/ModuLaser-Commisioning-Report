"""02.02.000 (Brent 10-19 12:35 PM CT): Report View menu checks for Sidebar / Results panel. Run: python3 tests/view_checks_test.py"""
import asyncio, os
from playwright.async_api import async_playwright
APP = 'file://' + os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
R=[]
def ok(n,c,i=''): R.append(bool(c)); print('PASS' if c else 'FAIL', n, i)
G="()=>[document.getElementById('mi-togglesb').getAttribute('aria-checked'),document.getElementById('mi-togglerp').getAttribute('aria-checked')]"
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':900}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto(APP); await pg.wait_for_timeout(800)
    await pg.click('#menu-view'); ok('defaults checked', await pg.evaluate(G)==['true','true'])
    await pg.click('#mi-togglerp'); await pg.click('#menu-view'); ok('results off via menu -> unchecked', await pg.evaluate(G)==['true','false'])
    await pg.keyboard.press('Escape'); await pg.click('button.qb[data-act=togglerp]'); await pg.click('#menu-view'); ok('quick button on -> checked', await pg.evaluate(G)==['true','true'])
    await pg.click('#mi-togglesb'); await pg.click('#menu-view'); ok('sidebar off -> unchecked', await pg.evaluate(G)==['false','true'])
    ok('no page errors', not errs, errs); await b.close()
  print(f"{sum(R)}/{len(R)} passed"); raise SystemExit(0 if all(R) else 1)
asyncio.run(main())

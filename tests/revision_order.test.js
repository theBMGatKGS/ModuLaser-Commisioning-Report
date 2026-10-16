// Regression test (Report 02.00.003): the in-app revision log must be in ascending order.
// The app (revShort/fullRev) and the installer build (electron/scripts/prepare.js) both use
// the LAST AMENDMENTS entry, so an out-of-order log ships the wrong revision.
// Run: node tests/revision_order.test.js
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
let fails = 0;
const chk = (name, ok, info = '') => { console.log((ok ? 'PASS ' : 'FAIL ') + name + (info ? ' — ' + info : '')); if (!ok) fails++; };

const major = html.match(/const APP_MAJOR = "(\d+)"/)[1];
const minor = html.match(/const APP_MINOR = "(\d+)"/)[1];
const entries = [...html.matchAll(/AMENDMENTS\.push\(\{\s*rev:\s*"(\d+)"(?:,\s*major:\s*"(\d+)")?(?:,\s*minor:\s*"(\d+)")?(?:,\s*date:\s*"(\d+)")?/g)]
  .map(m => ({ major: m[2] || major, minor: m[3] || minor, rev: m[1], date: m[4] || '' }));
const key = e => `${e.major}.${e.minor}.${e.rev}`;
chk('revision log has entries', entries.length > 0, String(entries.length));
for (let i = 1; i < entries.length; i++) {
  const a = entries[i - 1], b = entries[i];
  chk(`ascending: ${key(a)} < ${key(b)}`, key(a) < key(b));
  if (a.date && b.date) chk(`dates non-decreasing: ${a.date} <= ${b.date}`, a.date <= b.date);
}
// prepare.js uses the last `{ rev: "…"` match anywhere in the file — it must equal the last AMENDMENTS entry.
const anyRev = [...html.matchAll(/\{\s*rev:\s*"(\d+)"(?:[^}]*?minor:\s*"(\d+)")?/g)];
const lastAny = anyRev[anyRev.length - 1];
const latest = entries[entries.length - 1];
chk('installer build reads the latest revision', `${major}.${lastAny[2] || minor}.${lastAny[1]}` === key(latest), key(latest));
const title = (html.match(/<title>[^<]*?(\d\d\.\d\d\.\d\d\d)<\/title>/) || [])[1];
chk('<title> shows the latest revision', title === key(latest), `${title} vs ${key(latest)}`);
const sw = fs.readFileSync(path.join(root, 'sw.js'), 'utf8');
chk('sw.js cache name matches the latest revision', sw.includes(`'masd-field-report-${key(latest).replace(/\./g, '-')}'`));
console.log(fails ? `${fails} failed` : 'all passed');
process.exit(fails ? 1 : 0);

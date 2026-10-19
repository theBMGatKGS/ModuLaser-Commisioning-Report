/* 02.02.000 Commissioning Report layer — brand selector, logos/title, linked-design brand mismatch + part-number basis,
   ASD-160 device sheet, §8a benchmark test point fields (all detectors, additive), FACU powers the ASDs. Plan rev 4.23b B9/§4/§8a/B4b/B4c. */
const RP_BRAND_KEY = 'mlBrandDefault';
function rpBrand(){ return MLP.brandOf(state && state.project && state.project.brand); }
function rpBrandTitle(){ return MLP.BRANDS[rpBrand()].reportTitle; }
function rpDesignBrand(){ return MLP.brandOf(state && state.design && state.design.brand); }
function rpLogo(print){ const b = rpBrand(); const id = print ? (b === 'kidde-commercial' ? 'kidde-commercial-color' : 'edwards-gray') : (b === 'kidde-commercial' ? 'kidde-commercial-white' : 'edwards-white');
  const src = typeof APP_BRAND_LOGOS !== 'undefined' && APP_BRAND_LOGOS[id]; return src ? `<img class="br-logo" src="${src}" alt="${MLP.BRANDS[b].label}">` : ''; }
(function rpStyle(){ const st = document.createElement('style'); st.id = 'rp-0202-css';
  st.textContent = `.seg{display:inline-flex;border:1px solid var(--line,#2a3441);border-radius:6px;overflow:hidden}.seg button{background:transparent;color:var(--muted,#8b98a8);border:0;border-right:1px solid var(--line,#2a3441);padding:5px 11px;font:inherit;font-size:12.5px;cursor:pointer}
.seg button:last-child{border-right:0}.seg button[aria-pressed="true"]{background:var(--accent,#0c77bc);color:#fff;font-weight:600}.seg button:focus-visible{outline:2px solid var(--accent,#0c77bc);outline-offset:-2px}
.br-logo{height:22px;width:auto;display:block}.rp-chip{display:inline-block;margin-left:8px;padding:1px 7px;border:1px solid currentColor;border-radius:4px;font:600 10px/1.6 ui-monospace,monospace;letter-spacing:.06em;opacity:.85}
#brandBanner{margin:6px 0}.rp-amber{color:#f0b429}.rp-bench td,.rp-bench th{padding:3px 6px}
@media print{.rp-chip,#brandBanner .qb{display:none}}`; document.head.appendChild(st); })();
/* ---- header, title, print running header ---- */
function rpPaintBrand(){
  const b = MLP.BRANDS[rpBrand()];
  document.title = `${b.reportTitle} ${typeof revShort === 'function' ? revShort() : ''}`.trim();
  const md = document.querySelector('meta[name="description"]'); if (md) md.content = `Offline commissioning worksheet for ${b.label} ModuLaser Modular Aspirating Smoke Detector installations.`;
  const br = document.querySelector('header.top .brand'); if (br){ const mk = br.querySelector('.mark, .br-logo-wrap'); if (mk){ const w = document.createElement('span'); w.className = 'br-logo-wrap'; w.innerHTML = rpLogo(false) || 'ML'; mk.replaceWith(w); }
    let chip = br.querySelector('.rp-chip'); if (!chip){ chip = document.createElement('span'); chip.className = 'rp-chip noprint'; br.appendChild(chip); } chip.textContent = b.chip; }
  document.querySelectorAll('.rp-app-name').forEach(e => { e.textContent = b.reportTitle; });
  if (typeof updatePageStyle === 'function') updatePageStyle();
}
/* ---- Job sheet: brand control is the first field (B2) ---- */
(function rpHookSecA(){
  const _a = secA;
  secA = function (){ const h = _a.apply(this, arguments); const cur = rpBrand();
    const seg = `<div class="f s3 rp-brand-f"><span class="lb">Brand</span><div class="seg rp-brand-seg" role="group" aria-label="Brand">${Object.values(MLP.BRANDS).map(x => `<button type="button" data-brand="${x.id}" aria-pressed="${x.id === cur}">${x.label}</button>`).join('')}</div></div>`;
    const facu = !!(state.project && state.project.facuPowersAsds);
    const facuF = `<div class="f s3 rp-facu-f"><label><input type="checkbox" class="rp-facu"${facu ? ' checked' : ''}> FACU powers the ASDs</label>${facu ? `<div class="warnline">\u26A0 FACU powers these ASDs — do the battery calculation in that manufacturer's approved battery calculator; this tool does not account for non-ASD components.</div>` : ''}${state.project && state.project.powerSource === 'unidentified' ? '<div class="warnline">\u26A0 Incomplete — power source not identified. <a href="#" class="rp-psrc">Identify power source…</a></div>' : ''}</div>`;
    return h.replace('<div class="g3">', '<div class="g3">' + seg).replace(/(FACU manufacturer \/ model[\s\S]*?<\/div>)/, '$1' + facuF); };
  { const e = (typeof SEC_VIEWS !== 'undefined') && SEC_VIEWS.find(v => v[0] === 'A'); if (e) e[2] = secA; }
})();
document.addEventListener('click', e => {
  const bb = e.target.closest('.rp-brand-seg button'); if (bb){ rpSwitchBrand(bb.dataset.brand); return; }
  const ps = e.target.closest('.rp-psrc'); if (ps){ e.preventDefault(); rpAskPowerSource(); return; }
  const basis = e.target.closest('[data-rp-basis]'); if (basis){ rpSetBasis(basis.dataset.rpBasis); return; }
  if (e.target.closest('[data-rp-change]')) { rpAskBasis(); }
});
document.addEventListener('change', e => { const f = e.target.closest('.rp-facu'); if (!f) return; state.project = state.project || {}; state.project.facuPowersAsds = f.checked; state.project.facuUserSet = true;
  if (f.checked) delete state.project.powerSource; save(); if (!f.checked) rpAskPowerSource(); else renderAll(); });
function rpSwitchBrand(b){
  b = MLP.brandOf(b); if (b === rpBrand()) return;
  const go = () => { state.project = state.project || {}; state.project.brand = b; try { localStorage.setItem(RP_BRAND_KEY, b); } catch (e){}
    save(); rpPaintBrand(); renderAll(); if (state.design && rpDesignBrand() !== b) rpAskBasis(); else if (state.brandAck){ rpSetBasis(null, true); } };
  dlg('Switch brand', `<p>Set this report to <b>${MLP.BRANDS[b].label}</b>? Titles, logos and part numbers on this Report's own sheets follow the brand. The linked design file is not changed.</p>`, [{ label: 'Cancel' }, { label: 'Switch', pri: true, fn: go }]);
}
/* ---- part-number basis (F5) ---- */
function rpAskBasis(){
  const db = rpDesignBrand(), pb = rpBrand(), cur = (state.brandAck && state.brandAck.pnBasis) || db;
  const n = b => (state.modules || []).filter(m => m.model && MLP.translatePart(m.model, b) !== m.model).length + (state.psus || []).filter(p => p.model && MLP.translatePart(p.model, b) !== p.model).length;
  dlg('Part numbers on this Report', `<p>The linked design was built under <b>${MLP.BRANDS[db].label}</b>; this Report is set to <b>${MLP.BRANDS[pb].label}</b>. Show part numbers on this Report as:</p><p>The linked design file will not be changed. Sheets whose part numbers change: Edwards ${n('edwards')} · Kidde Commercial ${n('kidde-commercial')}. Models not in the catalog (third-party, free text) stay as entered.</p>`,
    Object.values(MLP.BRANDS).map(x => ({ label: x.label + (x.id === cur ? ' (current)' : ''), pri: x.id === pb, fn: () => rpSetBasis(x.id) })));
}
function rpSetBasis(b, clear){
  if (clear || !b){ delete state.brandAck; save(); renderAll(); return; }
  (state.modules || []).forEach(m => { if (m.model) m.model = MLP.translatePart(m.model, b); });
  (state.psus || []).forEach(p => { if (p.model) p.model = MLP.translatePart(p.model, b); });
  const d = state.design || {}; state.brandAck = { designBrand: rpDesignBrand(), projectBrand: rpBrand(), pnBasis: b, designId: d.id || '', designHash: d.hash || (state.design ? MLP.designHash(state.design) : ''), plFile: (state.link && state.link.name) || '', at: new Date().toISOString(), by: (state.project && state.project.commEng) || '' };
  save(); renderAll();
}
(function rpHookBanner(){
  const _b = renderBanner;
  renderBanner = function (){ const r = _b.apply(this, arguments);
    let el = document.getElementById('brandBanner'); const lb = document.getElementById('linkBanner');
    if (!el && lb){ el = document.createElement('div'); el.id = 'brandBanner'; lb.after(el); }
    if (!el) return r;
    const db = rpDesignBrand(), pb = rpBrand(), ack = state.brandAck, d = state.design;
    if (!d || db === pb){ el.hidden = true; if (ack && d && db === pb){ delete state.brandAck; } return r; }
    const h = d.hash || MLP.designHash(d), fresh = ack && ack.designHash === h && ack.projectBrand === pb && ack.designBrand === db;
    el.hidden = false; el.className = 'banner';
    el.innerHTML = fresh ? `Showing <b>${MLP.BRANDS[ack.pnBasis].label}</b> part numbers · linked design built under ${MLP.BRANDS[db].label} · <button class="qb" data-rp-change="1">Change…</button>`
      : `\u26A0 Linked design was built under <b>${MLP.BRANDS[db].label}</b>; this report is set to <b>${MLP.BRANDS[pb].label}</b>. Part numbers may differ. Show part numbers as: ${Object.values(MLP.BRANDS).map(x => `<button class="qb" data-rp-basis="${x.id}">${x.label}</button>`).join('')} <button class="qb" data-act="checklink">Check linked file…</button>`;
    return r; };
})();
/* ---- FACU untick → identify the power source (B4c) ---- */
function rpAskPowerSource(){
  const set = v => { state.project = state.project || {}; state.project.powerSource = v; save(); renderAll(); };
  dlg('What powers these ASDs?', `<p>Pick the power source so the batteries can be checked, or dismiss — the Report stays ⚠ Incomplete until it is identified.</p>`,
    [{ label: 'Dismiss', fn: () => set('unidentified') }, { label: 'Third-party (non-FACU)', fn: () => set('third-party') }, { label: `In-house supply (${MLP.BRANDS[rpBrand()].supplyLabel})`, pri: true, fn: () => set('in-house') }]);
}
/* ---- ASD-160 device sheet + §8a benchmark fields ---- */
TYPES.asd = 'ASD-160 (Micra25 / Senator 25)';
TYPE_FROM_DESIGN['ASD-160'] = 'asd';
function rpBench(pipe){ if (!pipe) return {}; const tr = MLP.asd160Transport(pipe); return tr; }
(function rpHookDevFields(){
  const _f = devFields;
  devFields = function (d){ const f = _f.apply(this, arguments); const p = d.pipe || {};
    if (d.pipe){ const tr = rpBench(p); if (tr.benchHole !== '' && tr.bench != null){ f['t.tt.benchHole'] = String(tr.benchHole); f['t.tt.benchPipecad'] = (+tr.bench).toFixed(1); } }
    if (d.kind === 'asd160'){ const a = d.asd160 || {}; f.type = 'asd'; f.sn = d.standalone ? '' : (d.address ? String(+d.address) : ''); f.net = d.standalone ? 'S' : String(MLP.devNetwork(d) || 1);
      f['cfg.af'] = a.alarmFactor != null ? String(a.alarmFactor) : ''; f['perf.holes'] = a.holes != null ? String(a.holes) : ''; f['perf.target'] = a.perfClass || '';
      const tr = rpBench(p); f['t.tt.pipecad'] = tr.target != null ? (+tr.target).toFixed(1) : (p.tt != null ? (+p.tt).toFixed(1) : ''); f.relayCard = d.relayCard ? 'Y' : 'N'; }
    if (state && state.brandAck && f.model) f.model = MLP.translatePart(f.model, state.brandAck.pnBasis);
    return f; };
})();
FIELD_LABEL['t.tt.benchHole'] = 'Benchmark test point'; FIELD_LABEL['t.tt.benchPipecad'] = 'Benchmark PipeCAD time (s)'; FIELD_LABEL.relayCard = 'Relay card';
function rpAsdPipe(m){ const d = m.dev && state.design && (state.design.devices || []).find(x => x.id === m.dev); return d && d.pipe ? d.pipe : null; }
function rpAsdEval(m){ const p = rpAsdPipe(m); if (!p) return null; return MLP.asd160Evaluate({ kind: 'asd160', pipe: p }, state.design && state.design.performance || null, m.area || '', { cls: m.perf && m.perf.target || null }); }
function rpTtItems(m, add){
  const lim = ttVarLimit(); const chk = (label, meas, pc) => { const mt = num(meas), p = num(pc); if (!ok(p)) return; if (!ok(mt)){ add('tt', label, 'B'); return; }
    const v = (mt - p) / p * 100; add('tt', label, v <= lim ? 'P' : 'F', v <= lim ? '' : `${fmt(mt, 1)} s is ${fmt(v, 1)}% over the PipeCAD ${fmt(p, 1)} s (allowed +${lim}%)`); };
  chk('Benchmark test point measured vs PipeCAD', m.t?.tt?.benchMeas, m.t?.tt?.benchPipecad);
  if ((m.t?.tt?.ahjHole || '').trim()) chk('Owner/AHJ test hole measured vs PipeCAD', m.t?.tt?.ahjMeas, m.t?.tt?.ahjPipecad);
}
function evalAsd(m){
  const it = []; const add = (sec, label, st, note = '') => it.push({ sec, label, st, note });
  const net = mNet(m);
  if (net === 'S') add('net', 'SenseNET address', String(m.sn || '').trim() ? 'F' : 'NA', String(m.sn || '').trim() ? 'a stand-alone ASD-160 is never addressed — clear the address' : 'stand-alone — not addressed');
  else { const sn = num(m.sn); if (sn === null) add('net', 'SenseNET address', 'B'); else if (!(sn >= 1 && sn <= 127) || !Number.isInteger(sn)) add('net', 'SenseNET address', 'F', 'must be 1–127'); else if (state.modules.filter(x => num(x.sn) === sn && sameScope(x, m)).length > 1) add('net', 'SenseNET address', 'F', 'duplicate address on SenseNET ' + net); else add('net', 'SenseNET address', 'P'); }
  if (!m.desc) add('net', 'Module name (descriptor)', 'B'); else add('net', 'Module name (descriptor)', String(m.desc).length > MLP.NAME_MAX ? 'F' : 'P');
  add('net', 'Serial number', m.serial ? 'P' : 'B');
  const ev = rpAsdEval(m);
  if (!ev) add('perf', 'PipeCAD design (ASD-160 rules)', 'B', 'link the PipeCAD design to check the ASD-160 limits');
  else { const errs = ev.issues.filter(x => x.level === 'error'); add('perf', `ASD-160 limits (${ev.ul ? 'UL 268 7th edition' : 'chosen standard'})`, errs.length ? 'F' : ev.issues.some(x => x.level === 'incomplete') ? 'B' : 'P', errs.map(x => x.msg).concat(ev.issues.filter(x => x.level !== 'error').map(x => '\u26A0 ' + x.msg)).join('; ')); }
  const cfg = MLP.asd160ConfigIssues(m.cfg || {});
  if (!['alert', 'action', 'fire1'].some(k => (m.cfg || {})[k] != null && (m.cfg || {})[k] !== '')) add('cfg', 'Alarm levels (Aux < Pre-Alarm < Fire < Fire 2)', 'B', 'enter the levels set with Remote');
  else add('cfg', 'Alarm levels (Aux < Pre-Alarm < Fire < Fire 2)', cfg.some(x => x.level === 'error') ? 'F' : cfg.some(x => x.level === 'incomplete') ? 'B' : 'P', cfg.map(x => x.msg).join('; '));
  const mt = num(m.t?.tt?.meas), pc = num(m.t?.tt?.pipecad);
  if (!ok(mt)) add('tt', 'Measured transport time (field target)', 'B');
  else { const lim = ev ? ev.limits.tt : MLP.ASD160.maxTt; add('tt', 'Measured transport time (field target)', lim != null && mt > lim + 1e-9 ? 'F' : 'P', lim != null && mt > lim + 1e-9 ? `${fmt(mt, 1)} s exceeds ${lim} s` : '');
    if (ok(pc) && pc > 0){ const v = (mt - pc) / pc * 100, L = ttVarLimit(); add('tt', 'Measured vs PipeCAD transport', v <= L ? 'P' : 'F', v <= L ? '' : `${fmt(mt, 1)} s is ${fmt(v, 1)}% over the PipeCAD ${fmt(pc, 1)} s (allowed +${L}%)`); } }
  rpTtItems(m, add);
  add('smoke', 'Smoke test — Fire relay operated', ynSt(m.t?.smoke?.fire)); add('smoke', 'FACU verified', ynSt(m.t?.smoke?.facu));
  add('flow', 'Flow fault', ynSt(m.t?.flow?.low)); add('flow', 'Faults cleared', ynSt(m.t?.flow?.clear));
  rpAsdRelays(m).forEach(r => add('out', `${r} relay test`, selSt(m.t?.out?.[r.replace(/\W/g, '').toLowerCase()])));
  const secs = {}; SECS.forEach(S => { const xs = it.filter(i => i.sec === S.k); secs[S.k] = !xs.length || xs.every(i => i.st === 'NA') ? 'NA' : xs.some(i => i.st === 'F') ? 'F' : xs.some(i => i.st === 'B') ? 'B' : 'P'; });
  const vals = Object.values(secs); const auto = vals.includes('F') ? 'FAIL' : vals.includes('B') ? 'INCOMPLETE' : 'PASS';
  const ov = m.ovr?.res || '', rs = (m.ovr?.reason || '').trim(); const applied = !!(ov && rs);
  return { it, secs, auto, final: applied ? ov : auto, overridden: applied && ov !== auto, ovPending: !!(ov && !rs), asd: ev };
}
function rpAsdRelays(m){ return MLP.ASD160.relayBase.concat(m.relayCard === 'Y' ? MLP.ASD160.relayCard : []); }
function rpBenchBlock(m, b){
  return `<div class="tc rp-bench-tc"><div class="tc-h"><span class="id">T1b</span>Benchmark test point &amp; Owner/AHJ hole (periodic tests)</div>
    <p class="note">Field transport target = longest sampling-hole time in PipeCAD (test point excluded). The benchmark test point time is the permitted transport test for all future periodic tests unless the Owner or AHJ requires a specific hole (usually the furthest, slowest sampling point). Pass at ≤ PipeCAD + ${ttVarLimit()} %.</p>
    <div class="g6">${F('Benchmark test point', b + '.t.tt.benchHole')}${F('Benchmark PipeCAD time', b + '.t.tt.benchPipecad', { num: 1, unit: 's' })}${F('Benchmark measured', b + '.t.tt.benchMeas', { num: 1, unit: 's' })}
    ${F('Owner/AHJ test hole', b + '.t.tt.ahjHole', { ph: 'optional — hole no.' })}${F('PipeCAD time', b + '.t.tt.ahjPipecad', { num: 1, unit: 's' })}${F('Measured', b + '.t.tt.ahjMeas', { num: 1, unit: 's' })}</div></div>`;
}
function asdSheet(m, i){
  const b = `modules.${i}`, psus = state.psus.map((p, j) => [p.id, psuName(p, j)]), e = evalAsd(m), ev = e.asd;
  const relays = rpAsdRelays(m);
  const ident = `<div class="blk"><div class="blk-h">1 · Identity &amp; network <span data-calc="${m.id}-sec-net"></span></div>
    <p class="note">ASD-160 (Micra25 / Senator 25) — ${mNet(m) === 'S' ? 'stand-alone: never addressed, not on SenseNET' : 'networked: addressed on SenseNET (DIP 1–127)'}; own dedicated AUX circuit; 250 mA; configured with Remote.</p>
    <div class="g4">${F('Module type', b + '.type', { opts: Object.entries(TYPES) })}${F('Model / part number', b + '.model')}${F('Module name (descriptor)', b + '.desc')}${F('Area / Group', b + '.area')}
      ${F('SenseNET network', b + '.net', { opts: [['S', 'Stand-alone'], ['1', 'SenseNET 1'], ['2', 'SenseNET 2'], ['3', 'SenseNET 3']] })}${F('DIP address', b + '.sn', { num: 1 })}${F('Relay card 33-30436A', b + '.relayCard', { opts: [['N', 'No'], ['Y', 'Yes']] })}${F('Supplying power supply', b + '.psu', { opts: psus })}
      ${F('Location / room', b + '.loc')}${F('Serial number', b + '.serial')}</div></div>`;
  const perf = `<div class="blk"><div class="blk-h">2 · PipeCAD design — ASD-160 limits <span data-calc="${m.id}-sec-perf"></span></div>
    ${ev ? `<div class="g6"><div class="f"><span class="lb">Alarm factor</span><span class="calc">AF ${ev.af.af} (${esc(ev.af.src)})</span></div><div class="f"><span class="lb">Class</span><span class="calc">${esc(ev.cls.cls || '—')} (${esc(ev.cls.src)})</span></div>
      <div class="f"><span class="lb">Sampling holes / all incl. end cap</span><span class="calc">${ev.counts.sampling} / ${ev.counts.all}</span></div><div class="f"><span class="lb">Worst hole</span><span class="calc">${ev.worst == null ? '—' : fmt(ev.worst, 4) + ' %obs/ft'}</span></div>
      <div class="f"><span class="lb">Limits</span><span class="calc">${ev.limits.sens == null ? '—' : '≤ ' + ev.limits.sens + ' %obs/ft'} · ${ev.limits.tt == null ? '—' : '≤ ' + ev.limits.tt + ' s'}${ev.ul ? ' · UL 268 7th ed.' : ''}</span></div><div class="f"><span class="lb">Field target / benchmark</span><span class="calc">${ev.transport.target == null ? '—' : fmt(ev.transport.target, 1) + ' s'} / ${ev.transport.bench == null ? '—' : fmt(ev.transport.bench, 1) + ' s'}</span></div></div>
      ${ev.issues.map(x => `<div class="warnline">${x.level === 'error' ? '' : '\u26A0 '}${esc(x.msg)}</div>`).join('')}` : '<p class="note">Link the PipeCAD design (.pl or project file) to check the ASD-160 limits.</p>'}</div>`;
  const lv = MLP.ASD160_LEVELS.map(L => F(`${L.label} level`, b + '.cfg.' + L.key, { num: 1, unit: '%obs/ft' })).join('');
  const cfg = `<div class="blk"><div class="blk-h">3 · Configuration (Remote) <span data-calc="${m.id}-sec-cfg"></span></div>
    <p class="note">Detector levels in %obs/ft. Fire = the alarm factor's Fire 1; Pre-Alarm and Aux use the Alarm Factor worksheet (defaults 0.5× and 0.2× Fire, verify); Fire 2 must be entered (0.00914–7.62). Strict order Aux &lt; Pre-Alarm &lt; Fire &lt; Fire 2. Delays 0–90 s; flow limits per the ModuLaser allowances.</p>
    <div class="g4">${lv}${F('Pre-Alarm delay', b + '.cfg.actionDly', { num: 1, unit: 's' })}${F('Fire delay', b + '.cfg.fire1Dly', { num: 1, unit: 's' })}${F('Flow low', b + '.cfg.flowLow', { num: 1, unit: '%' })}${F('Flow high', b + '.cfg.flowHigh', { num: 1, unit: '%' })}${F('Flow fault delay', b + '.cfg.flowDly', { num: 1, unit: 's' })}</div></div>`;
  const tests = `<div class="tc"><div class="tc-h"><span class="id">T1</span>Transport time<span data-calc="${m.id}-sec-tt"></span></div>
      <div class="g5">${F('Field transport target (PipeCAD, longest sampling hole)', b + '.t.tt.pipecad', { num: 1, unit: 's' })}${F('Measured transport time', b + '.t.tt.meas', { num: 1, unit: 's' })}</div>
      <p class="note">Senator 25 Handbook p34: measured transport time less than the calculated time is acceptable (context — the Report passes at ≤ PipeCAD + ${ttVarLimit()} %).</p>${testFoot(b + '.t.tt')}</div>
    ${rpBenchBlock(m, b)}
    <div class="tc"><div class="tc-h"><span class="id">T2</span>Smoke &amp; flow<span data-calc="${m.id}-sec-smoke"></span></div>
      <div class="g6">${YNF('Fire relay operated on smoke?', b + '.t.smoke.fire')}${YNF('Verified at FACU?', b + '.t.smoke.facu')}${YNF('Flow fault?', b + '.t.flow.low')}${YNF('Faults clear?', b + '.t.flow.clear')}</div>${testFoot(b + '.t.smoke')}</div>
    <div class="tc"><div class="tc-h"><span class="id">T3</span>Relay test (${relays.join(', ')})<span data-calc="${m.id}-sec-out"></span></div>
      <p class="note">Base unit: Fire (N/O, closes on Fire 1) and Fault (N/C, fail-safe), 500 mA @ 30 VDC.${m.relayCard === 'Y' ? ' Relay card 33-30436A adds Pre-Alarm, Aux and Fire 2.' : ''}</p>
      <div class="g6">${relays.map(r => F(r, b + '.t.out.' + r.replace(/\W/g, '').toLowerCase(), { opts: ['Pass', 'Fail', 'N/A'] })).join('')}</div>${testFoot(b + '.t.out')}</div>`;
  const result = `<div class="tc" style="border-width:2px;border-color:var(--accent2)"><div class="tc-h">Module result<span data-calc="${m.id}-st2"></span></div><div data-calc="${m.id}-secrow" style="margin-bottom:8px"></div>
    <div class="g4">${F('Override result', b + '.ovr.res', { opts: ['PASS', 'FAIL'] })}${F('Override reason (required to apply)', b + '.ovr.reason', { cls: 's3', ph: 'Reason, authorized by…' })}</div><div class="warnline" data-calc="${m.id}-ovwarn"></div></div>`;
  return `<div class="sheet" id="mod-${m.id}"><div class="sheet-h"><div><div class="kick">ASD-160 sheet${m.area ? ' · ' + esc(m.area) : ''}</div><h3>ASD-160 — ${esc(m.desc || m.model || '')}</h3><div class="sub" data-calc="${m.id}-sub"></div></div>
    <div class="right"><span class="lbl">Module result</span><span data-calc="${m.id}-st"></span></div></div>
    ${tabBar(m.id, [['setup', 'Setup'], ['config', 'Configure'], ['test', 'Test']])}${pane(m.id, 'setup', ident + photosBlock(b, m))}${pane(m.id, 'config', perf + cfg)}${pane(m.id, 'test', tests + result)}${navRow()}</div>`;
}
(function rpHookSheets(){
  const _s = moduleSheet, _e = evalModule;
  moduleSheet = function (m, i){ if (m.type === 'asd') return asdSheet(m, i); let h = _s.apply(this, arguments);
    if (m.type === 'det' || m.type === 'ml'){ const blk = rpBenchBlock(m, `modules.${i}`); const k = h.lastIndexOf('<div class="tc" style="border-width:2px'); h = k > 0 ? h.slice(0, k) + blk + h.slice(k) : h; }
    return h; };
  evalModule = function (m){ if (m.type === 'asd') return evalAsd(m); const e = _e.apply(this, arguments);
    if (m.type === 'det' || m.type === 'ml'){ const add = (sec, label, st, note = '') => e.it.push({ sec, label, st, note }); const n0 = e.it.length; rpTtItems(m, add);
      if (e.it.length > n0){ const xs = e.it.filter(i => i.sec === 'tt'); e.secs.tt = xs.some(i => i.st === 'F') ? 'F' : xs.some(i => i.st === 'B') ? 'B' : 'P';
        const vals = Object.values(e.secs); e.auto = vals.includes('F') ? 'FAIL' : vals.includes('B') ? 'INCOMPLETE' : 'PASS'; const ov = m.ovr?.res || '', rs = (m.ovr?.reason || '').trim(); e.final = ov && rs ? ov : e.auto; e.overridden = !!(ov && rs) && ov !== e.auto; } }
    return e; };
})();
/* project file: project.brand survives (projectInfoOut); new jobs use the remembered default; FACU pre-tick from design.psus[].facuSource */
(function rpHookProject(){
  const _o = projectInfoOut;
  projectInfoOut = function (){ const p = _o.apply(this, arguments); const b = rpBrand(); if (b !== 'edwards') p.brand = b; else delete p.brand; return p; };
  if (typeof applyPlan === 'function'){ const _ap = applyPlan; applyPlan = function (plan){ const r = _ap.apply(this, arguments);
    if (state.design && (state.design.psus || []).some(p => p.facuSource) && !(state.project && state.project.facuUserSet)){ state.project = state.project || {}; state.project.facuPowersAsds = true; }
    if (state.link && state.link.project && state.link.project.brand && !(state.project && state.project.brand)){ state.project.brand = MLP.brandOf(state.link.project.brand); }
    rpPaintBrand(); return r; }; }
  const _bl = blank; blank = function (){ const st = _bl.apply(this, arguments); try { const b = MLP.brandOf(localStorage.getItem(RP_BRAND_KEY)); if (b !== 'edwards'){ st.project = st.project || {}; st.project.brand = b; } } catch (e){} return st; };
})();
rpPaintBrand(); if (typeof renderAll === 'function') renderAll();

/* ===================== 02.02.000 completion (Brent 10-19 1:55 PM) ===================== */
/* (d3) Unidentified power source rolls fully to ⚠ Incomplete: every power supply sheet gets a blank item, so device, section,
   summary and print status all read INCOMPLETE until the source is identified. Imported designs carry it from design.psus[].powerSource. */
function rpPowerUnidentified(){ return !!(state.project && state.project.powerSource === 'unidentified'); }
(function rpPowerRollup(){
  const _e = evalPsu;
  evalPsu = function (p){ const r = _e.apply(this, arguments); if (!r || !rpPowerUnidentified()) return r;
    r.it.push({ sec: 'id', label: 'Power source identified', st: 'B', note: '⚠ Incomplete — FACU unticked and the power source is not identified' });
    if (r.secs.id !== 'F') r.secs.id = 'B';
    const vals = Object.values(r.secs); r.auto = vals.includes('F') ? 'FAIL' : vals.includes('B') ? 'INCOMPLETE' : 'PASS';
    if (!r.overridden) r.final = r.auto; else r.overridden = r.final !== r.auto;
    return r; };
  if (typeof applyPlan === 'function'){ const _ap = applyPlan; applyPlan = function (){ const r = _ap.apply(this, arguments);
    const ps = (state.design && state.design.psus) || [];
    if (ps.some(p => p.powerSource === 'unidentified') && !(state.project && state.project.powerSource && state.project.powerSource !== 'unidentified')){ state.project = state.project || {}; state.project.powerSource = 'unidentified'; }
    return r; }; }
  if (typeof renderBanner === 'function'){ const _rb = renderBanner; renderBanner = function (){ const r = _rb.apply(this, arguments);
    let b = document.getElementById('psrcBanner');
    if (rpPowerUnidentified()){ if (!b){ b = document.createElement('div'); b.id = 'psrcBanner'; b.className = 'banner warn'; b.style.cssText = 'background:#3a2c0a;color:#ffd27a;border:1px solid #b07a10;padding:8px 12px;margin:6px 0;border-radius:4px';
        const host = document.getElementById('brandBanner') || document.getElementById('app'); if (host && host.parentNode) host.parentNode.insertBefore(b, host); }
      b.innerHTML = '\u26A0 Incomplete — the ASD power source is not identified. <a href="#" id="psrcFix">Identify power source…</a>'; b.hidden = false;
      const a = document.getElementById('psrcFix'); if (a) a.onclick = e => { e.preventDefault(); rpAskPowerSource(); };
    } else if (b) b.hidden = true;
    return r; }; }
})();
/* (c) About text + Help / How do I / FAQ topics (brand, part-number basis, ASD-160, FACU power source). */
(function rpHelp0202(){
  const steps = document.querySelector('#help-qs') || document.querySelector('.hstep') && document.querySelector('.hstep').parentNode;
  const last = Array.from(document.querySelectorAll('.hstep')).pop();
  const S = [['Brand (Edwards | Kidde Commercial)', 'Brand is the first field in Project information. Titles, the header logo, the print band and part numbers follow it. If an imported project file uses the other brand, a banner offers the <b>part-number basis</b> dialog: keep the file’s part numbers or translate them to this brand.'],
    ['ASD-160 (Micra25 / Senator 25)', 'An ASD-160 sheet covers identity and SenseNET network, PipeCAD limits, Remote configuration levels, transport time (+20 % allowance) and the benchmark test point (end cap), smoke and flow tests, and Fire/Fault relays with the relay card.'],
    ['FACU powers the ASDs', 'The checkbox under the FACU field starts ticked when the design says the FACU powers the ASDs. Unticking it asks what powers them; until the source is identified every power supply sheet and the summary read ⚠ Incomplete.']];
  if (last && !document.getElementById('rp-hstep-0202')){ let n = +((last.querySelector('.hn') || {}).textContent || 10); let at = last;
    S.forEach(([t, b], i) => { const d = document.createElement('div'); d.className = 'hstep'; if (!i) d.id = 'rp-hstep-0202'; d.innerHTML = `<span class="hn">${++n}</span><div><div class="ht">${t}</div><p>${b}</p></div>`; at.after(d); at = d; }); }
  const hd = document.getElementById('help-howdoi'), fq = document.getElementById('help-faq');
  const H = [['…change the brand?', 'Project information → Brand. Confirm the switch; the title, logo and part numbers update. For an imported file with a different brand, choose the part-number basis in the banner dialog.'],
    ['…commission an ASD-160?', 'Open its sheet (Area/Group → ASD-160). Fill identity and network, check the PipeCAD limits and Remote configuration levels, record transport time at the benchmark test point, then the smoke, flow and relay tests.'],
    ['…clear “power source not identified”?', 'Tick “FACU powers the ASDs”, or click Identify power source… in the banner and pick In-house or Third-party.']];
  const F = [['Why does the Report ask for a part-number basis?', 'The project file was made with the other brand. The design is the same; only part numbers differ. Pick the file’s numbers or this brand’s; your choice is stored with the job.'],
    ['Why is an ASD-160 transport time allowed 20 % over PipeCAD?', 'The Report applies the same +20 % measured-vs-PipeCAD allowance to every detector, ASD-160 included (Senator 25 Handbook p.34 quoted as context).'],
    ['Why is everything ⚠ Incomplete after unticking FACU?', 'Without a known power source the batteries cannot be checked, so each power supply sheet gets a blank “Power source identified” item until you identify it.']];
  const add = (host, list, id) => { if (!host || document.getElementById(id)) return; const h3 = host.querySelector('h3'); let at = h3;
    list.forEach(([q, a], i) => { const d = document.createElement('div'); d.className = 'hq'; if (!i) d.id = id; d.innerHTML = `<dt>${q}</dt><dd>${a}</dd>`; at.after(d); at = d; }); };
  add(hd, H, 'rp-howdoi-0202'); add(fq, F, 'rp-faq-0202');
  const idc = document.querySelector('.idcard'); if (idc && !document.getElementById('rp-about-0202')){ const r = document.createElement('div'); r.className = 'row'; r.id = 'rp-about-0202';
    r.innerHTML = '<span class="k">Covers</span><span class="v">Edwards and Kidde Commercial ModuLaser MASD, MiniLaser (FHSD8075-ULF) and ASD-160 (Micra25 / Senator 25); shared project file modulaser-project.js ' + MLP.VERSION + '</span>'; idc.appendChild(r); }
})();

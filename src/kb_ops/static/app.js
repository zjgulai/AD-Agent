'use strict';
/* ad-agent-qa KB Workbench — hash 路由 SPA，全部 GET-only。 */

const $view = document.getElementById('view');
const $chips = document.getElementById('stats-chips');

const esc = (s) => String(s ?? '').replace(/[&<>"']/g,
  (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

async function api(path) {
  const r = await fetch('/api' + path);
  if (!r.ok) throw new Error(`${r.status} ${path}`);
  return r.json();
}

async function md(text) {
  const out = marked.parse(text, { gfm: true, breaks: true });
  return typeof out === 'string' ? out : await out;
}

const KIND_LABEL = { qa: 'QA', card: 'CARD', glossary: 'TERM' };

function sourceRoute(source) {
  const m = source.match(/^cards\/([a-z0-9-]+)\/([a-z0-9-]+)\.md/);
  if (m) return `#/cards/${m[1]}/${m[2]}`;
  const q = source.match(/^qa\/([a-z0-9-]+)\.md/);
  if (q) return `#/qa/${q[1]}`;
  return null;
}

/* ---------- 路由 ---------- */

let graphTeardown = null;

async function route() {
  if (graphTeardown) { try { graphTeardown(); } catch (_) {} graphTeardown = null; }
  const raw = location.hash.replace(/^#\/?/, '');
  const [pathPart, qs] = raw.split('?');
  const seg = pathPart.split('/').filter(Boolean);
  const params = new URLSearchParams(qs || '');
  const navKey = seg[0] || 'cards';
  document.querySelectorAll('#nav a').forEach(a =>
    a.classList.toggle('active', a.dataset.nav === navKey));
  try {
    if (seg[0] === 'cards' && seg.length >= 3) return await vCard(seg[1], seg[2]);
    if (seg[0] === 'cards') return await vCards(params.get('cluster') || '', params.get('q') || '');
    if (seg[0] === 'qa' && seg[1]) return await vQaDetail(seg[1]);
    if (seg[0] === 'qa') return await vQaList();
    if (seg[0] === 'graph') return await vGraph();
    if (seg[0] === 'health') return await vHealth(params.get('refresh') === '1');
    if (seg[0] === 'search') return await vSearch(params.get('q') || '');
    location.hash = '#/cards';
  } catch (e) {
    $view.innerHTML = `<div class="error">加载失败：${esc(e.message)}</div>`;
  }
}

/* ---------- Cards ---------- */

async function vCards(clusterFilter, q) {
  const { cards } = await api('/cards');
  const byCluster = new Map();
  cards.forEach(c => {
    if (!byCluster.has(c.cluster)) byCluster.set(c.cluster, []);
    byCluster.get(c.cluster).push(c);
  });
  const needle = q.trim().toLowerCase();
  const match = (c) => !needle ||
    c.title.toLowerCase().includes(needle) || c.name.includes(needle) ||
    (c.topic || '').toLowerCase().includes(needle);

  $view.innerHTML = `
    <div class="toolbar">
      <input type="search" id="cq" placeholder="过滤卡片：标题 / topic / 名称…" value="${esc(q)}" style="width:280px">
      <span class="muted">${cards.length} 张卡片 · ${byCluster.size} 个集群</span>
    </div>
    <div class="cards-layout">
      <div class="panel card-list" id="clist"></div>
      <div class="panel" id="cempty"><div class="muted" style="padding:40px;text-align:center">← 选择左侧卡片查看内容</div></div>
    </div>`;

  const renderList = () => {
    const needle2 = document.getElementById('cq').value.trim().toLowerCase();
    let html = '';
    for (const [cluster, items] of byCluster) {
      if (clusterFilter && cluster !== clusterFilter) continue;
      const shown = items.filter(c => !needle2 ||
        c.title.toLowerCase().includes(needle2) || c.name.includes(needle2) ||
        (c.topic || '').toLowerCase().includes(needle2));
      if (!shown.length) continue;
      html += `<div class="cluster-head">${esc(cluster)} · ${shown.length}</div>`;
      html += shown.map(c => `
        <a class="card-item" href="#/cards/${c.cluster}/${c.name}">
          <div class="t">${esc(c.title)}</div>
          <div class="m">${esc(c.name)} · ${esc(c.status)} · ${esc(c.updated)}</div>
        </a>`).join('');
    }
    document.getElementById('clist').innerHTML = html || '<div class="muted" style="padding:20px">无匹配卡片</div>';
  };
  renderList();
  document.getElementById('cq').addEventListener('input', renderList);
}

async function vCard(cluster, name) {
  const c = await api(`/cards/${encodeURIComponent(cluster)}/${encodeURIComponent(name)}`);
  const fm = c.meta || {};
  const body = (c.body || '').replace(/^# [^\n]*\n/, '');
  const html = await md(body);
  const srcDocs = (fm.source_docs || []).map(s => `<span class="tag">${esc(s)}</span>`).join('');
  $view.innerHTML = `
    <a class="back-link" href="#/cards">← 返回卡片列表</a>
    <div class="card-meta">
      <span class="tag">${esc(c.cluster)}</span>
      <span class="tag">${esc(fm.status || c.status || '')}</span>
      ${fm.updated ? `<span class="tag">更新 ${esc(fm.updated)}</span>` : ''}
      ${srcDocs}
    </div>
    <div class="doc-body md">${html}</div>`;
}

/* ---------- QA ---------- */

async function vQaList() {
  const { files } = await api('/qa');
  $view.innerHTML = `
    <div class="toolbar"><span class="muted">${files.length} 个集群文件</span></div>
    <div class="panel">
      ${files.map(f => `
        <a class="card-item" href="#/qa/${f.cluster}">
          <div class="t">${esc(f.title)}</div>
          <div class="m">${esc(f.cluster)}.md · ${f.count} 条 Q&A</div>
        </a>`).join('')}
    </div>`;
}

async function vQaDetail(cluster) {
  const d = await api(`/qa/${encodeURIComponent(cluster)}`);
  $view.innerHTML = `
    <a class="back-link" href="#/qa">← 返回 QA 列表</a>
    <div class="toolbar"><span class="muted">${d.entries.length} 条 · ${esc(cluster)}</span></div>
    <div id="qalist"></div>`;
  const list = document.getElementById('qalist');
  list.innerHTML = d.entries.map((e, i) => `
    <div class="qa-item">
      <div class="qa-q" data-i="${i}">
        <span class="qid">${esc(e.qid)}.</span><span class="qq">${esc(e.question)}</span>
      </div>
      <div class="qa-a md" data-i="${i}" style="display:none"></div>
    </div>`).join('');
  const answers = {};
  list.querySelectorAll('.qa-q').forEach(q => {
    q.addEventListener('click', async () => {
      const i = +q.dataset.i;
      const box = list.querySelector(`.qa-a[data-i="${i}"]`);
      if (box.style.display !== 'none') { box.style.display = 'none'; return; }
      box.style.display = 'block';
      if (!answers[i]) {
        box.innerHTML = '<div class="muted">渲染中…</div>';
        const e = d.entries[i];
        answers[i] = await md(e.answer);
        box.innerHTML = answers[i] +
          (e.source ? `<div class="qa-src">溯源：${esc(e.source)}</div>` : '');
      }
    });
  });
}

/* ---------- Graph ---------- */

const TYPE_COLORS = {
  'ad:Playbook': '#4A90D9', 'ad:Benchmark': '#50C878', 'ad:Rule': '#E85D75',
  'ad:WorkflowStage': '#F5A623', 'ad:KnowledgeAsset': '#9B59B6',
  'ad:Metric': '#1ABC9C', 'ad:AdProduct': '#34495E', 'ad:Platform': '#16A085',
  'ad:Channel': '#27AE60', 'ad:Concept': '#8E44AD', 'ad:Symptom': '#E67E22',
  'ad:DiagnosisCheck': '#C0392B', 'ad:Action': '#2980B9', 'ad:Agent': '#8E44AD',
  'ad:AgentLoop': '#7F8C8D', 'ad:Role': '#95A5A6', 'ad:Audience': '#F39C12',
  'ad:Product': '#2C3E50', 'ad:Campaign': '#3D566E', 'ad:AdSet': '#5D6D7E',
  'ad:AdEntity': '#707B7C', 'ad:Competitor': '#B03A2E', 'ad:SourceDoc': '#BDC3C7',
  'ad:LifecycleStage': '#16A085', 'ad:HITLGate': '#C0392B',
};
const COMM_COLORS = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6',
  '#1ABC9C', '#E67E22', '#34495E', '#16A085', '#C0392B', '#8E44AD', '#F1C40F'];
const DIRECTIONAL = new Set(['ad:depends_on', 'ad:triggers', 'ad:checks', 'ad:applies_when',
  'ad:affects', 'ad:measures', 'ad:has_threshold', 'ad:recommends', 'ad:implements',
  'ad:escalates_to', 'ad:supersedes', 'ad:deprecated_by', 'ad:sourced_from',
  'ad:defined_in', 'ad:pending_data', 'ad:belongs_to', 'ad:part_of', 'ad:targets', 'ad:involves']);

let visPromise = null;
function loadVis() {
  if (window.vis) return Promise.resolve();
  if (!visPromise) visPromise = new Promise((res, rej) => {
    const s = document.createElement('script');
    s.src = '/vendor/vis-network.min.js';
    s.onload = res; s.onerror = () => rej(new Error('vis-network 加载失败'));
    document.head.appendChild(s);
  });
  return visPromise;
}

async function vGraph() {
  $view.innerHTML = `
    <div class="graph-layout">
      <div id="g-side">
        <div class="filter-group"><label>搜索节点</label><input type="search" id="g-search" placeholder="label / @id…"></div>
        <div class="filter-group"><label>类型</label><select id="g-type"><option value="">全部类型</option></select></div>
        <div class="filter-group"><label>分片</label><select id="g-cluster"><option value="">全部分片</option></select></div>
        <div class="filter-group"><label>关系</label><select id="g-rel"><option value="">全部关系</option></select></div>
        <div class="muted" id="g-hint">点击节点查看详情与邻居</div>
        <div id="g-detail"></div>
      </div>
      <div id="g-canvas"></div>
    </div>`;
  const data = await api('/graph');
  await loadVis();

  const NODES = data.nodes, EDGES = data.edges;
  const byId = new Map(NODES.map(n => [n.id, n]));
  const adj = new Map();
  EDGES.forEach(e => {
    const lbl = e.type.replace('ad:', '');
    if (!adj.has(e.source)) adj.set(e.source, []);
    adj.get(e.source).push({ rel: lbl, other: e.target, dir: 'out', ref: e.ref || '' });
    if (!adj.has(e.target)) adj.set(e.target, []);
    adj.get(e.target).push({ rel: lbl, other: e.source, dir: 'in', ref: e.ref || '' });
  });

  const nodesDS = new vis.DataSet(NODES.map(n => {
    const commColor = n.community >= 0 ? COMM_COLORS[n.community % COMM_COLORS.length] : '#555';
    return {
      id: n.id, label: n.label,
      color: { background: TYPE_COLORS[n.type] || '#7F8C8D', border: commColor,
               highlight: { border: commColor } },
      borderWidth: n.community >= 0 ? 3 : 1,
      font: { color: '#dfe3e8', size: 11, face: 'PingFang SC, sans-serif',
              strokeWidth: 2, strokeColor: '#1a1d23' },
      shape: 'dot', size: Math.min(6 + Math.sqrt(n.degree) * 2.5, 22),
      title: n.id + '\n' + n.type,
      _type: n.type, _cluster: n.cluster,
    };
  }));
  const edgesDS = new vis.DataSet(EDGES.map((e, i) => {
    const dir = DIRECTIONAL.has(e.type);
    return { id: i, from: e.source, to: e.target, label: e.type.replace('ad:', ''),
      title: e.ref || '', arrows: dir ? 'to' : '',
      color: { color: dir ? '#5b6b7f' : '#3a4150', highlight: '#6cb6ff' },
      font: { color: '#6b7484', size: 8, align: 'middle' }, smooth: { type: 'continuous' } };
  }));

  const network = new vis.Network(document.getElementById('g-canvas'),
    { nodes: nodesDS, edges: edgesDS },
    { physics: { stabilization: true, barnesHut: { gravitationalConstant: -6000, springLength: 90 } },
      interaction: { hover: true, tooltipDelay: 120, navigationButtons: true },
      nodes: { shape: 'dot' } });
  graphTeardown = () => { try { network.destroy(); } catch (_) {} };
  window.__kbGraph = { network, nodesDS, edgesDS, showDetail, focusNode };  // 调试/测试钩子

  // 筛选器
  const $type = document.getElementById('g-type'), $cluster = document.getElementById('g-cluster'),
        $rel = document.getElementById('g-rel'), $search = document.getElementById('g-search');
  [...new Set(NODES.map(n => n.type))].sort().forEach(t => $type.add(new Option(t, t)));
  [...new Set(NODES.map(n => n.cluster))].sort().forEach(c => $cluster.add(new Option(c, c)));
  [...new Set(EDGES.map(e => e.type.replace('ad:', '')))].sort().forEach(r => $rel.add(new Option(r, r)));

  function applyFilters() {
    const q = $search.value.trim().toLowerCase();
    const tf = $type.value, cf = $cluster.value, rf = $rel.value;
    nodesDS.update(NODES.map(n => {
      let vis = true;
      if (tf && n.type !== tf) vis = false;
      if (cf && n.cluster !== cf) vis = false;
      if (rf && !(adj.get(n.id) || []).some(a => a.rel === rf)) vis = false;
      if (q && !(n.id.toLowerCase().includes(q) || n.label.toLowerCase().includes(q))) vis = false;
      return { id: n.id, hidden: !vis };
    }));
    const visible = new Set(nodesDS.get({ filter: n => !n.hidden }).map(n => n.id));
    edgesDS.update(EDGES.map((e, i) =>
      ({ id: i, hidden: !(visible.has(e.source) && visible.has(e.target)) })));
  }
  [$search, $type, $cluster, $rel].forEach(el => el.addEventListener('input', applyFilters));

  // 节点详情
  const $detail = document.getElementById('g-detail');
  function showDetail(id) {
    const n = byId.get(id); if (!n) return;
    const rows = Object.entries(n.props || {})
      .map(([k, v]) => `<tr><td>${esc(k)}</td><td>${esc(typeof v === 'object' ? JSON.stringify(v) : v)}</td></tr>`).join('');
    const nbrs = (adj.get(id) || []).slice(0, 30).map(nb => {
      const arrow = nb.dir === 'out' ? '→' : '←';
      const other = (byId.get(nb.other) || {}).label || nb.other;
      return `<span class="nbr" data-id="${esc(nb.other)}">${arrow} ${esc(nb.rel)} ${esc(other)}</span>`;
    }).join('');
    $detail.style.display = 'block';
    $detail.innerHTML = `<h4>${esc(n.label)}</h4>
      <div class="meta">${esc(n.id)}<br>${esc(n.type)} · ${esc(n.cluster)} · 社区${n.community >= 0 ? n.community : '—'} · 度${n.degree}</div>
      ${rows ? `<table>${rows}</table>` : ''}
      <div style="margin-top:8px;color:var(--mut)">邻居：</div>${nbrs || '<i>无</i>'}`;
    $detail.querySelectorAll('.nbr').forEach(el => el.addEventListener('click', () => focusNode(el.dataset.id)));
  }
  function focusNode(id) {
    network.focus(id, { scale: 1.2, animation: true });
    showDetail(id);
  }
  network.on('click', p => { if (p.nodes.length) showDetail(p.nodes[0]); });
  network.once('stabilizationIterationsDone', () => network.setOptions({ physics: { enabled: false } }));
  document.getElementById('g-hint').textContent =
    `${data.stats.nodes} 节点 · ${data.stats.edges} 边 · ${data.stats.communities} 社区`;
}

/* ---------- Health ---------- */

async function vHealth(refresh) {
  $view.innerHTML = `<div class="loading">${refresh ? '重新审计中（可能需要数秒）…' : '加载健康数据…'}</div>`;
  const h = await api(`/health${refresh ? '?refresh=1' : ''}`);
  const v = h.audit.validate || {}, a = h.audit.audit || {};
  const lintFindings = [];
  (h.missing_card_files || []).forEach(m => lintFindings.push(`卡片文件缺失：${m.node} → ${m.path}`));
  (h.uncovered_cards || []).slice(0, 30).forEach(c => lintFindings.push(`未被图谱覆盖：${c}`));
  const orphans = h.orphan_nodes || [];

  const qaMax = Math.max(1, ...Object.values(h.qa_counts || {}));
  const qaBars = Object.entries(h.qa_counts || {})
    .sort((x, y) => y[1] - x[1])
    .map(([k, n]) => {
      const pct = Math.min(100, n / qaMax * 100);
      return `<div class="qa-bar"><span class="lbl" title="${esc(k)}">${esc(k)}</span>
        <div class="track"><div class="fill" style="width:${pct}%"></div></div><span class="n">${n}</span></div>`;
    }).join('');

  const adjRows = (h.conflict_table.adjudication || []).map(r => `
    <tr><td>${esc(r.id)}</td><td>${esc(r.status)}</td><td>${esc(r.decision)}</td></tr>`).join('');
  const cfRows = (h.conflict_table.rows || []).map(r => `
    <tr><td>${esc(r.id)}</td><td>${esc(r.conflict)}</td><td class="muted">${esc(r.nature)}</td><td>${esc(r.status)}</td></tr>`).join('');

  $view.innerHTML = `
    <div class="toolbar">
      <span class="muted">审计快照 ${esc(h.cached_at)} · graph ${h.graph.nodes}n/${h.graph.edges}e</span>
      <span style="flex:1"></span>
      <button onclick="location.hash='#/health?refresh=1'">↻ 重新审计</button>
      <button onclick="showDoc('CONFLICTS.md')">CONFLICTS.md</button>
      <button onclick="showDoc('REVIEW-PRECHECK.md')">REVIEW-PRECHECK.md</button>
    </div>
    <div class="health-grid">
      <div>
        <div class="panel">
          <h3>审计</h3>
          <div class="stat-row">
            <div class="s"><b><span class="badge ${v.status === 'PASS' ? 'ok' : 'bad'}">${esc(v.status || '?')}</span></b><span>validate.py</span></div>
            <div class="s"><b>${a.fail ?? '—'}</b><span>kb_audit FAIL</span></div>
            <div class="s"><b>${a.warn ?? '—'}</b><span>WARN</span></div>
            <div class="s"><b>${a.info ?? '—'}</b><span>INFO</span></div>
            <div class="s"><b>${h.qa_total}</b><span>QA 条目</span></div>
          </div>
          ${[...(v.error_lines || []), ...(a.warning_lines || [])].length ?
            `<div class="finding-list">${[...(v.error_lines || []), ...(a.warning_lines || [])].slice(0, 30).map(l => `<div>${esc(l)}</div>`).join('')}</div>` :
            '<div class="muted">无错误/警告行</div>'}
        </div>
        <div class="panel">
          <h3>语义 lint</h3>
          <div class="stat-row">
            <div class="s"><b>${orphans.length}<span class="muted" style="font-size:12px">/${h.orphan_total}</span></b><span>孤儿节点(度0)</span></div>
            <div class="s"><b>${(h.uncovered_cards || []).length}</b><span>未覆盖卡片</span></div>
            <div class="s"><b>${(h.missing_card_files || []).length}</b><span>缺失卡片文件</span></div>
            <div class="s"><b>${h.conflicts.pending_business}</b><span>待确认冲突</span></div>
          </div>
          ${lintFindings.length ? `<div class="finding-list">${lintFindings.map(l => `<div>${esc(l)}</div>`).join('')}</div>`
            : '<div class="muted">覆盖完整</div>'}
          ${orphans.length ? `<details style="margin-top:8px"><summary class="muted">孤儿节点列表（前 ${orphans.length}）</summary>
            <div class="finding-list">${orphans.slice(0, 40).map(n => `<div>${esc(n.id)} — ${esc(n.label)}（${esc(n.type)}）</div>`).join('')}</div></details>` : ''}
        </div>
      </div>
      <div>
        <div class="panel">
          <h3>QA 集群分布（${h.qa_total} 条）</h3>
          <div class="qa-bars">${qaBars}</div>
        </div>
        <div class="panel">
          <h3>CONFLICTS 裁决状态</h3>
          <div class="table-wrap"><table class="data">
            <tr><th>#</th><th>状态</th><th>裁决/处置</th></tr>${adjRows}
          </table></div>
        </div>
      </div>
    </div>
    <div class="panel">
      <h3>冲突总表（${(h.conflict_table.rows || []).length} 行）</h3>
      <div class="table-wrap"><table class="data">
        <tr><th>#</th><th>冲突点</th><th>性质判定</th><th>卡片现状</th></tr>${cfRows}
      </table></div>
    </div>`;
}

/* ---------- Search ---------- */

async function vSearch(q) {
  $view.innerHTML = `
    <form class="toolbar" id="sform">
      <input type="search" id="sq" placeholder="BM25 检索：卡片 / QA / 术语…" value="${esc(q)}" style="width:420px" autofocus>
      <button class="primary" type="submit">搜索</button>
      <span class="muted" id="shint">输入关键词开始检索</span>
    </form>
    <div id="sresults"></div>`;
  const form = document.getElementById('sform');
  form.addEventListener('submit', e => {
    e.preventDefault();
    const v = document.getElementById('sq').value.trim();
    if (v) location.hash = `#/search?q=${encodeURIComponent(v)}`;
  });
  if (!q) return;
  document.getElementById('shint').textContent = '检索中…';
  const d = await api(`/search?q=${encodeURIComponent(q)}&k=12`);
  document.getElementById('shint').textContent = `${d.results.length} 条结果`;
  document.getElementById('sresults').innerHTML = d.results.map(r => {
    const route = sourceRoute(r.source);
    const inner = `
      <div class="top">
        <span class="kind-badge kind-${r.kind}">${KIND_LABEL[r.kind] || r.kind}</span>
        <span class="src">${esc(r.source)}</span>
        <span class="score">${r.score.toFixed(1)}</span>
      </div>
      <div class="snip">${esc(r.text.slice(0, 260))}${r.text.length > 260 ? '…' : ''}</div>`;
    return route
      ? `<a class="result-item" href="${route}" style="display:block;color:inherit">${inner}</a>`
      : `<div class="result-item">${inner}</div>`;
  }).join('') || '<div class="muted" style="padding:30px;text-align:center">无结果</div>';
}

/* ---------- Modal（原始文档） ---------- */

async function showDoc(name) {
  const d = await api(`/doc/${encodeURIComponent(name)}`);
  document.getElementById('modal-title').textContent = name;
  document.getElementById('modal-body').innerHTML = await md(d.markdown);
  document.getElementById('modal').classList.remove('hidden');
}
document.getElementById('modal-close').addEventListener('click',
  () => document.getElementById('modal').classList.add('hidden'));
document.getElementById('modal').addEventListener('click', e => {
  if (e.target.id === 'modal') document.getElementById('modal').classList.add('hidden');
});
window.showDoc = showDoc;

/* ---------- 启动 ---------- */

(async () => {
  try {
    const s = await api('/stats');
    $chips.innerHTML =
      `<span class="chip"><b>${s.cards}</b> 卡片</span>` +
      `<span class="chip"><b>${s.qa_entries}</b> QA</span>` +
      `<span class="chip"><b>${s.graph_nodes}</b> 节点 / <b>${s.graph_edges}</b> 边</span>`;
  } catch (_) { /* stats 失败不阻塞 */ }
  route();
})();
window.addEventListener('hashchange', route);

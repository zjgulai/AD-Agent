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

async function apiPost(path, body) {
  const r = await fetch('/api' + path, {
    method: 'POST',
    headers: body instanceof FormData ? {} : { 'Content-Type': 'application/json' },
    body: body instanceof FormData ? body : JSON.stringify(body || {}),
  });
  if (!r.ok) {
    let msg = `${r.status}`;
    try { msg = (await r.json()).detail || msg; } catch (_) {}
    throw new Error(msg);
  }
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
    if (seg[0] === 'ingest' && seg[1]) return await vIngestDetail(seg[1]);
    if (seg[0] === 'ingest') return await vIngest();
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

/* sagegogo 深色主题 kg-* 域色板（sagegogo.com ontology-foundation） */
const TYPE_COLORS = {
  'ad:Playbook': '#89a9f1', 'ad:Benchmark': '#7acbbf', 'ad:Rule': '#e79db6',
  'ad:WorkflowStage': '#edb76c', 'ad:KnowledgeAsset': '#bd98e5',
  'ad:Metric': '#b4cd85', 'ad:AdProduct': '#74bfe8', 'ad:Platform': '#7acbbf',
  'ad:Channel': '#b4cd85', 'ad:Concept': '#bd98e5', 'ad:Symptom': '#e79db6',
  'ad:DiagnosisCheck': '#e88f7f', 'ad:Action': '#89a9f1', 'ad:Agent': '#bd98e5',
  'ad:AgentLoop': '#8ba0b8', 'ad:Role': '#c9d6e4', 'ad:Audience': '#edb76c',
  'ad:Product': '#74bfe8', 'ad:Campaign': '#89a9f1', 'ad:AdSet': '#8ba0b8',
  'ad:AdEntity': '#a9bcd4', 'ad:Competitor': '#e88f7f', 'ad:SourceDoc': '#7d92a8',
  'ad:LifecycleStage': '#7acbbf', 'ad:HITLGate': '#e88f7f',
};
const COMM_COLORS = ['#89a9f1', '#bd98e5', '#7acbbf', '#edb76c', '#74bfe8',
  '#e79db6', '#b4cd85', '#a9c6ee', '#cbb0ec', '#9fd8cf', '#f0cd8d',
  '#e8b3c4', '#c8dba0', '#8ba0b8'];
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

  // 布局位置缓存：同版本图谱二次进入直接禁用物理引擎，秒开
  const POS_KEY = 'kb-graph-pos-v1';
  let posCache = null, posSig = '';
  try {
    let h = 5381;
    const sigSrc = (data.generated || '') + '|' + NODES.length + '|' + EDGES.length + '|' +
      NODES.map(n => n.id).join('');
    for (let i = 0; i < sigSrc.length; i++) h = ((h << 5) + h + sigSrc.charCodeAt(i)) | 0;
    posSig = String(h);
    posCache = JSON.parse(localStorage.getItem(POS_KEY) || 'null');
    if (posCache && posCache.sig !== posSig) posCache = null;
  } catch (_) { posCache = null; }

  // 确定性种子布局：按 cluster 分组摆圆环，物理引擎只需少量迭代收敛
  const seedPos = {};
  if (!posCache) {
    const clusters = [...new Set(NODES.map(n => n.cluster))].sort();
    const R = 700 + clusters.length * 55;
    clusters.forEach((c, ci) => {
      const a = (ci / clusters.length) * Math.PI * 2;
      const cx = Math.cos(a) * R, cy = Math.sin(a) * R;
      const members = NODES.filter(n => n.cluster === c);
      members.forEach((n, ni) => {
        const golden = ni * 2.399963;
        const rr = 25 + Math.sqrt(ni / Math.max(members.length, 1)) * 210;
        seedPos[n.id] = [cx + Math.cos(golden) * rr, cy + Math.sin(golden) * rr];
      });
    });
  }

  const nodesDS = new vis.DataSet(NODES.map(n => {
    const commColor = n.community >= 0 ? COMM_COLORS[n.community % COMM_COLORS.length] : '#555';
    const p = posCache ? posCache.pos[n.id] : seedPos[n.id];
    return {
      id: n.id, label: n.label,
      ...(p ? { x: p[0], y: p[1] } : {}),
      color: { background: TYPE_COLORS[n.type] || '#7F8C8D', border: commColor,
               highlight: { border: commColor } },
      borderWidth: n.community >= 0 ? 3 : 1,
      font: { color: '#eef4fa', size: 11, face: 'PingFang SC, sans-serif',
              strokeWidth: 2, strokeColor: '#0a1a2c' },
      shape: 'dot', size: Math.min(6 + Math.sqrt(n.degree) * 2.5, 22),
      title: n.id + '\n' + n.type,
      _type: n.type, _cluster: n.cluster,
    };
  }));
  const edgeRel = e => e.type.replace('ad:', '');
  const edgesDS = new vis.DataSet(EDGES.map((e, i) => {
    const dir = DIRECTIONAL.has(e.type);
    return { id: i, from: e.source, to: e.target,
      title: edgeRel(e) + (e.ref ? ' — ' + e.ref : ''),
      arrows: dir ? 'to' : '',
      color: { color: dir ? '#4a627d' : '#33465c', highlight: '#89a9f1' },
      font: { color: '#8ba0b8', size: 8, align: 'middle' }, smooth: { type: 'continuous' } };
  }));

  const network = new vis.Network(document.getElementById('g-canvas'),
    { nodes: nodesDS, edges: edgesDS },
    { physics: posCache ? { enabled: false, stabilization: { enabled: false } } : {
        stabilization: { enabled: true, iterations: 400, updateInterval: 80, fit: true },
        barnesHut: { gravitationalConstant: -6000, springLength: 90, theta: 0.6 } },
      interaction: { hover: true, tooltipDelay: 120, navigationButtons: true },
      nodes: { shape: 'dot' } });
  if (posCache) {
    requestAnimationFrame(() => network.fit(undefined, { animation: false }));
  } else {
    let saved = false;
    const trySave = () => {
      if (saved) return;
      saved = true;
      try {
        const pos = {};
        for (const [id, nd] of Object.entries(network.body.nodes)) pos[id] = [nd.x, nd.y];
        localStorage.setItem(POS_KEY, JSON.stringify({ sig: posSig, pos }));
      } catch (_) {}
    };
    // stabilization 事件发在 body.emitter；稳定后关闭物理（947 节点常驻 barnesHut 是持续 CPU 开销），
    // 节点仍可拖拽。15s 兜底防事件未触发。
    const finish = () => {
      trySave();
      try { network.setOptions({ physics: { enabled: false } }); } catch (_) {}
    };
    network.body.emitter.once('stabilizationIterationsDone', finish);
    setTimeout(finish, 15000);
  }
  // 边标签按需显示：点击节点时仅标注其关联边（全量 1976 条边标签是主要渲染开销）
  function labelEdgesFor(edgeIds) {
    const keep = new Set(edgeIds);
    const ups = edgeIds.map(id => ({ id, label: edgeRel(EDGES[id]) }));
    const clear = edgesDS.get({ filter: e => e.label && !keep.has(e.id) })
      .map(e => ({ id: e.id, label: '' }));
    if (ups.length || clear.length) edgesDS.update([...ups, ...clear]);
  }
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
      <div style="margin-top:8px;color:var(--muted)">邻居：</div>${nbrs || '<i>无</i>'}`;
    $detail.querySelectorAll('.nbr').forEach(el => el.addEventListener('click', () => focusNode(el.dataset.id)));
  }
  function focusNode(id) {
    network.focus(id, { scale: 1.2, animation: true });
    showDetail(id);
  }
  network.on('click', p => {
    labelEdgesFor(p.edges || []);
    if (p.nodes.length) showDetail(p.nodes[0]);
  });
  document.getElementById('g-hint').textContent =
    `${data.stats.nodes} 节点 · ${data.stats.edges} 边 · ${data.stats.communities} 社区`;
}

/* ---------- Ingest ---------- */

const INGEST_STATUS = {
  uploaded: '已上传', extracted: '已提取', briefed: '已简报',
  distilled: '已蒸馏', published: '已发布',
};

async function vIngest() {
  const { items } = await api('/ingest');
  $view.innerHTML = `
    <div class="ingest-layout">
      <div>
        <div class="upload-box" id="dropzone">
          <div class="muted">拖入文件或点击选择</div>
          <div class="hint">支持 PDF / DOCX / XLSX / PPTX / HTML / TXT / MD / CSV / 图片（≤50MB）</div>
          <input type="file" id="fileinput" multiple style="display:none">
          <div style="margin-top:10px"><button id="pickbtn">选择文件</button></div>
          <div id="upload-status" class="muted" style="margin-top:8px"></div>
        </div>
        <div class="panel item-list" id="ilist">
          ${items.length ? items.map(it => `
            <div class="item-row" data-id="${esc(it.id)}">
              <span class="status-badge st-${it.status}">${INGEST_STATUS[it.status] || it.status}</span>
              <div style="flex:1;min-width:0">
                <div class="fn">${esc(it.filename)}</div>
                <div class="sub">${esc(it.id)} · ${(it.size_bytes / 1024).toFixed(0)}KB · ${esc((it.uploaded_at || '').slice(5, 16))}</div>
              </div>
            </div>`).join('') : '<div class="muted" style="padding:20px;text-align:center">暂无摄入记录</div>'}
        </div>
      </div>
      <div class="panel" id="idetail"><div class="muted" style="padding:30px;text-align:center">← 选择左侧记录查看详情，或上传新文件</div></div>
    </div>`;

  // 上传
  const input = document.getElementById('fileinput');
  const pick = document.getElementById('pickbtn');
  const dz = document.getElementById('dropzone');
  const status = document.getElementById('upload-status');
  pick.addEventListener('click', () => input.click());
  dz.addEventListener('dragover', e => { e.preventDefault(); dz.classList.add('drag'); });
  dz.addEventListener('dragleave', () => dz.classList.remove('drag'));
  dz.addEventListener('drop', e => { e.preventDefault(); dz.classList.remove('drag'); uploadFiles(e.dataTransfer.files); });
  input.addEventListener('change', () => uploadFiles(input.files));

  async function uploadFiles(files) {
    for (const f of files) {
      status.textContent = `上传中: ${f.name}…`;
      try {
        const fd = new FormData();
        fd.append('file', f);
        const it = await apiPost('/ingest/upload', fd);
        status.textContent = `✓ ${it.filename} → ${it.id}（${it.content_chars} 字）`;
        location.hash = `#/ingest/${it.id}`;
        return;
      } catch (e) {
        status.textContent = `✗ ${f.name}: ${e.message}`;
      }
    }
  }

  document.querySelectorAll('.item-row').forEach(el =>
    el.addEventListener('click', () => { location.hash = `#/ingest/${el.dataset.id}`; }));
}

async function vIngestDetail(id) {
  const it = await api(`/ingest/${encodeURIComponent(id)}`);
  const errs = (it.errors || []).map(e => `<div class="muted">⚠ ${esc(e)}</div>`).join('');
  $view.innerHTML = `
    <a class="back-link" href="#/ingest">← 返回摄入列表</a>
    <div class="card-meta">
      <span class="status-badge st-${it.status}">${INGEST_STATUS[it.status] || it.status}</span>
      <span class="tag">${esc(it.filename)}</span>
      <span class="tag">${esc(it.ext)}</span>
      <span class="tag">${(it.size_bytes / 1024).toFixed(1)} KB</span>
      <span class="tag">${it.content_chars} 字 / ${it.tables} 表</span>
      <span class="tag">${esc(it.uploaded_at || '')}</span>
    </div>
    ${errs}
    <div class="panel">
      <h3>提取预览</h3>
      <div class="extract-preview">${esc(it.extracted_preview || '（无内容）')}</div>
      <div class="action-row">
        <button onclick="ingestContent('${esc(id)}')">查看提取全文</button>
        <button class="primary" onclick="ingestBrief('${esc(id)}')">${it.has_brief ? '重新生成简报' : '生成蒸馏简报'}</button>
        ${it.has_brief ? '<button onclick="ingestShowBrief(\'' + esc(id) + '\')">查看简报</button>' : ''}
        ${it.status === 'briefed' ? '<button onclick="ingestStatus(\'' + esc(id) + '\',\'distilled\')">标记已蒸馏</button>' : ''}
        ${it.status === 'distilled' ? '<button onclick="ingestStatus(\'' + esc(id) + '\',\'published\')">标记已发布</button>' : ''}
      </div>
      <div id="briefbox"></div>
    </div>`;
}

let _ingestBriefRaw = '';

window.ingestBrief = async function (id) {
  const box = document.getElementById('briefbox');
  box.innerHTML = '<div class="muted">生成简报中（含 BM25 相关度分析）…</div>';
  try {
    const d = await apiPost(`/ingest/${id}/brief`);
    _ingestBriefRaw = d.brief;
    const html = await md(d.brief);
    box.innerHTML = `<h3>蒸馏简报</h3>
      <div class="action-row"><button onclick="ingestCopyBrief(this)">复制简报 markdown</button></div>
      <div class="doc-body" style="padding:14px 18px">${html}</div>`;
  } catch (e) {
    box.innerHTML = `<div class="error">简报生成失败：${esc(e.message)}</div>`;
  }
};

window.ingestCopyBrief = function (btn) {
  navigator.clipboard.writeText(_ingestBriefRaw).then(() => {
    btn.textContent = '已复制';
    setTimeout(() => { btn.textContent = '复制简报 markdown'; }, 1500);
  });
};

window.ingestShowBrief = async function (id) {
  const d = await api(`/ingest/${id}/brief`);
  _ingestBriefRaw = d.brief;
  await showDocRaw('蒸馏简报 ' + id, d.brief);
};

window.ingestContent = async function (id) {
  const d = await api(`/ingest/${id}/content`);
  await showDocRaw('提取全文 ' + id, d.markdown);
};

window.ingestStatus = async function (id, status) {
  try {
    await apiPost(`/ingest/${id}/status`, { status });
    location.reload();
  } catch (e) {
    alert('状态更新失败: ' + e.message);
  }
};

async function showDocRaw(title, markdown) {
  const html = await md(markdown);
  document.getElementById('modal-title').textContent = title;
  document.getElementById('modal-body').innerHTML = html;
  document.getElementById('modal').classList.remove('hidden');
}

/* ---------- Health ---------- */

async function vHealth(refresh) {
  $view.innerHTML = `<div class="loading">${refresh ? '重新审计中（可能需要数秒）…' : '加载健康数据…'}</div>`;
  const [h, ov] = await Promise.all([
    api(`/health${refresh ? '?refresh=1' : ''}`),
    api('/doc/OVERVIEW.md').catch(() => null),
  ]);
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
        ${ov ? `<div class="panel">
          <h3>KB 概览 <button class="ghost" style="float:right;font-size:12px" onclick="showDoc('OVERVIEW.md')">原文</button></h3>
          <div class="md" style="font-size:13px">${await md(ov.markdown)}</div>
        </div>` : `<div class="panel"><h3>KB 概览</h3><div class="muted">OVERVIEW.md 未生成——运行 <code>python -m kb_ops audit</code> 刷新</div></div>`}
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

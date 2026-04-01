'use strict';

// ── Constants ──────────────────────────────────────────────────────────────
const MANIFEST_URL = './manifest.json';

// ── State ──────────────────────────────────────────────────────────────────
let currentLang = 'en';  // 'ko' | 'en'
let allArtifacts = [];
let currentFilter = 'all';
let cardObserver = null;
let currentDetailArtifactId = null;
let currentDetailData = null;
let detailRequestToken = 0;
let skipNextHashChange = false;

const FILTER_LABELS = {
  all: '전체',
  'national-treasures': '국보·보물',
  kdh: 'KDH',
};

function updateKdhHeaderText() {
  const grid = document.getElementById('card-grid');
  if (!grid || !grid.parentNode) return;

  let headerText = document.getElementById('kdh-header-text');
  if (!headerText) {
    headerText = document.createElement('div');
    headerText.id = 'kdh-header-text';
    headerText.className = 'hidden';
    headerText.innerHTML = `
      <span data-lang="ko">이 유물들은 드라마 '케이팝 데몬 헌터스'에 등장하는 실제 국보·보물입니다</span>
      <span data-lang="en">These artifacts appear in the drama 'K-pop Demon Hunters' and are real National Treasures</span>
    `;
    grid.parentNode.insertBefore(headerText, grid);
  }

  if (currentFilter === 'kdh') {
    headerText.classList.remove('hidden');
  } else {
    headerText.classList.add('hidden');
  }
}

function ensureFilterTabs(counts) {
  const grid = document.getElementById('card-grid');
  if (!grid) return;

  let tabs = document.getElementById('filter-tabs');
  if (!tabs) {
    tabs = document.createElement('div');
    tabs.id = 'filter-tabs';
    tabs.className = 'filter-tabs';
    grid.parentNode?.insertBefore(tabs, grid);
  }

  const filters = [
    { id: 'all', label: `${FILTER_LABELS.all} (${counts.totalCount})` },
    {
      id: 'national-treasures',
      label: `${FILTER_LABELS['national-treasures']} (${counts.nationalTreasuresCount})`,
    },
    { id: 'kdh', label: `${FILTER_LABELS.kdh} (${counts.kdhCount})` },
  ];

  tabs.innerHTML = '';

  filters.forEach((filter) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = `filter-tab${currentFilter === filter.id ? ' active' : ''}`;
    button.dataset.filter = filter.id;
    button.textContent = filter.label;
    button.addEventListener('click', () => {
      currentFilter = filter.id;
      ensureFilterTabs(counts);
      const filteredArtifacts = currentFilter === 'all'
        ? allArtifacts
        : allArtifacts.filter((artifact) => artifact.collection === currentFilter);
      renderCards(filteredArtifacts);
    });
    tabs.appendChild(button);
  });
}

function observeCards(cards) {
  if (cardObserver) {
    cardObserver.disconnect();
  }

  if (!('IntersectionObserver' in window)) {
    cards.forEach((card) => {
      card.classList.add('visible');
      card.classList.remove('card-skeleton');
    });
    return;
  }

  cardObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && entry.intersectionRatio >= 0.1) {
          entry.target.classList.add('visible');
          entry.target.classList.remove('card-skeleton');
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: [0.1],
    },
  );

  cards.forEach((card) => {
    cardObserver.observe(card);
  });
}

function getFilteredArtifacts() {
  return currentFilter === 'all'
    ? allArtifacts
    : allArtifacts.filter((artifact) => artifact.collection === currentFilter);
}

function normalizePath(path) {
  if (typeof path !== 'string' || path.length === 0) return '';
  if (path.startsWith('./') || path.startsWith('../') || path.startsWith('/')) return path;
  return `./${path}`;
}

function getFallbackPath(path) {
  if (typeof path !== 'string' || path.length === 0) return '';
  const trimmed = path.replace(/^\.?\//, '');
  return `../${trimmed}`;
}

async function fetchWithFallback(path) {
  const primaryPath = normalizePath(path);
  const fallbackPath = getFallbackPath(path);
  const candidates = fallbackPath && fallbackPath !== primaryPath
    ? [primaryPath, fallbackPath]
    : [primaryPath];

  let lastError = null;
  for (const candidatePath of candidates) {
    const response = await fetch(candidatePath);
    if (response.ok) {
      return response;
    }

    lastError = new Error(`Fetch failed for ${candidatePath} with status ${response.status}`);
  }

  throw lastError ?? new Error(`Fetch failed for ${path}`);
}

function escapeHtml(text) {
  if (text == null) return '';
  return String(text)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function highlightCode(text) {
  if (text == null) return '';
  let escaped = escapeHtml(text);
  escaped = escaped.replace(
    /(이름|영문명|지정번호|분류|시대|재질|크기|소장처|지정|설명):/g,
    '<span class="kw">$1</span>:'
  );
  escaped = escaped.replace(/(\/\/[^\n]*)/g, '<span class="cm">$1</span>');
  return escaped;
}
function getHashArtifactId() {
  const match = window.location.hash.match(/^#artifact-(.+)$/);
  return match ? decodeURIComponent(match[1]) : null;
}

function closeDetail({ clearHash = true } = {}) {
  document.getElementById('artifact-detail')?.classList.add('hidden');
  currentDetailArtifactId = null;
  currentDetailData = null;

  if (!clearHash) return;
  if (window.location.hash.startsWith('#artifact-')) {
    history.replaceState(null, '', `${window.location.pathname}${window.location.search}`);
  }
}

function renderDetailContent(detailData) {
  const detailContent = document.getElementById('detail-content');
  if (!detailContent) return;

  const {
    artifact,
    sidecar,
    hglContent,
  } = detailData;

  const nameKo = sidecar.name ?? artifact.name_ko ?? '';
  const nameEn = sidecar.name_en ?? artifact.name_en ?? '';
  const descriptionKo = sidecar.description ?? '';
  const descriptionEn = sidecar.description_en ?? sidecar.descriptionEn ?? '';
  const dramaKo = sidecar.drama_connection?.ko ?? '';
  const dramaEn = sidecar.drama_connection?.en ?? '';

  const metadataRows = [
    ['시대 / Era', sidecar.era ?? artifact.period ?? ''],
    ['재질 / Material', sidecar.material ?? ''],
    ['크기 / Size', sidecar.size ?? ''],
    ['소장처 / Location', sidecar.location ?? ''],
    ['지정 / Designation', sidecar.designation ?? artifact.designation ?? ''],
  ]
    .filter(([, value]) => value)
    .map(([label, value]) => `<li><strong>${escapeHtml(label)}:</strong> ${escapeHtml(value)}</li>`)
    .join('');

  detailContent.innerHTML = `
    <h2 class="detail-name-ko" data-lang="ko">${escapeHtml(nameKo)}</h2>
    <p class="detail-name-en" data-lang="en">${escapeHtml(nameEn)}</p>
    <ul class="detail-meta">${metadataRows}</ul>
    <pre><code class="detail-code">${highlightCode(hglContent)}</code></pre>
    <p class="detail-description" data-lang="ko">${escapeHtml(descriptionKo)}</p>
    <p class="detail-description" data-lang="en">${escapeHtml(descriptionEn)}</p>
    ${dramaKo || dramaEn ? `
      <div class="detail-drama-connection">
        ${dramaKo ? `<span data-lang="ko"><strong>드라마 연결:</strong> ${escapeHtml(dramaKo)}</span>` : ''}
        ${dramaEn ? `<span data-lang="en"><strong>Drama connection:</strong> ${escapeHtml(dramaEn)}</span>` : ''}
      </div>
    ` : ''}
  `;
}

async function loadManifest() {
  const grid = document.getElementById('card-grid');

  try {
    const response = await fetch(MANIFEST_URL);
    if (!response.ok) {
      throw new Error(`Manifest fetch failed with status ${response.status}`);
    }

    const manifest = await response.json();
    allArtifacts = Array.isArray(manifest.artifacts) ? manifest.artifacts : [];

    const collections = Array.isArray(manifest.collections) ? manifest.collections : [];
    const nationalTreasuresCount =
      collections.find((collection) => collection.id === 'national-treasures')?.count
      ?? allArtifacts.filter((artifact) => artifact.collection === 'national-treasures').length;
    const kdhCount =
      collections.find((collection) => collection.id === 'kdh')?.count
      ?? allArtifacts.filter((artifact) => artifact.collection === 'kdh').length;
    const totalCount = manifest.total_count ?? allArtifacts.length;

    ensureFilterTabs({
      totalCount,
      nationalTreasuresCount,
      kdhCount,
    });

    renderCards(allArtifacts);
  } catch (error) {
    console.error('manifest.json 로드 실패:', error);
    if (grid) {
      grid.innerHTML = '<p class="error">manifest.json 로드 실패</p>';
    }
  }
}

/**
 * artifact 배열을 받아 #card-grid에 카드를 렌더링한다.
 * @param {Array} artifacts - manifest.json의 artifacts 배열
 */
function renderCards(artifacts) {
  const grid = document.getElementById('card-grid');
  if (!grid) return;

  updateKdhHeaderText();

  grid.innerHTML = '';

  if (!Array.isArray(artifacts) || artifacts.length === 0) {
    return;
  }

  const fragment = document.createDocumentFragment();

  const cardElements = artifacts.map((artifact) => {
    const card = document.createElement('div');
    const isKdh = artifact.collection === 'kdh';

    card.className = `artifact-card card-skeleton${isKdh ? ' kdh kdh-special' : ''}`;
    card.dataset.id = artifact.id;
    card.dataset.collection = artifact.collection;
    card.setAttribute('role', 'button');

    const img = document.createElement('img');
    img.src = artifact.image_url ?? '';
    img.loading = 'lazy';
    img.alt = currentLang === 'ko' ? (artifact.name_ko ?? '') : (artifact.name_en ?? artifact.name_ko ?? '');
    img.onerror = function() { this.style.display = 'none'; };

    if (!artifact.image_url) {
      img.style.display = 'none';
    }

    card.appendChild(img);

    const cardBody = document.createElement('div');
    cardBody.className = 'card-body';

    if (isKdh) {
      const badge = document.createElement('span');
      badge.className = 'kdh-badge';
      badge.textContent = '🎬 K-pop Demon Hunters';
      cardBody.appendChild(badge);
    }

    const title = document.createElement('h3');
    title.className = 'card-title';
    title.textContent = currentLang === 'ko'
      ? (artifact.name_ko ?? '')
      : (artifact.name_en ?? artifact.name_ko ?? '');

    const subtitle = document.createElement('p');
    subtitle.className = 'card-subtitle';
    subtitle.textContent = currentLang === 'ko'
      ? (artifact.name_en ?? '')
      : (artifact.name_ko ?? '');

    const designation = document.createElement('p');
    designation.className = 'card-designation';
    designation.textContent = artifact.designation ?? '';

    const period = document.createElement('p');
    period.className = 'card-period';
    period.textContent = artifact.period ?? '';

    cardBody.append(title, subtitle, designation, period);
    card.appendChild(cardBody);

    const handleOpenDetail = () => {
      showDetail(artifact.id);
    };

    card.addEventListener('click', handleOpenDetail);
    fragment.appendChild(card);
    return card;
  });

  grid.appendChild(fragment);

  observeCards(cardElements);
}

/**
 * 특정 artifact의 상세 overlay를 표시한다.
 * @param {string} artifactId - artifact의 id 필드 (예: "nb_001", "kdh_001")
 */
async function showDetail(artifactId) {
  const overlay = document.getElementById('artifact-detail');
  const detailContent = document.getElementById('detail-content');
  if (!overlay || !detailContent) return;

  if (
    currentDetailArtifactId === artifactId
    && !overlay.classList.contains('hidden')
    && currentDetailData
  ) {
    renderDetailContent(currentDetailData);
    return;
  }

  const artifact = allArtifacts.find((item) => item.id === artifactId);
  if (!artifact) {
    detailContent.innerHTML = '<p class="error">상세 정보를 찾을 수 없습니다.</p>';
    overlay.classList.remove('hidden');
    return;
  }

  const requestToken = Date.now() + (++detailRequestToken);

  try {
    const [sidecarResponse, hglResponse] = await Promise.all([
      fetchWithFallback(artifact.json_path),
      fetchWithFallback(artifact.hgl_path),
    ]);

    const sidecar = await sidecarResponse.json();
    const hglContent = await hglResponse.text();

    if (requestToken < detailRequestToken) {
      return;
    }

    currentDetailData = { artifact, sidecar, hglContent };
    renderDetailContent(currentDetailData);

    currentDetailArtifactId = artifactId;
    overlay.classList.remove('hidden');

    const nextHash = `#artifact-${encodeURIComponent(artifactId)}`;
    if (window.location.hash !== nextHash) {
      skipNextHashChange = true;
      window.location.hash = nextHash;
    }
  } catch (error) {
    console.error('상세 데이터 로드 실패:', error);
    detailContent.innerHTML = '<p class="error">상세 정보를 불러오지 못했습니다.</p>';
    overlay.classList.remove('hidden');
  }
}

/**
 * ko/en 언어를 토글하고 모든 렌더링을 업데이트한다.
 */
function toggleLang() {
  currentLang = currentLang === 'ko' ? 'en' : 'ko';
  document.body.dataset.lang = currentLang;

  // Swap text for elements with data-lang-ko / data-lang-en attributes
  document.querySelectorAll('[data-lang-ko]').forEach(el => {
    el.textContent = currentLang === 'ko' ? el.dataset.langKo : el.dataset.langEn;
  });

  const btn = document.getElementById('lang-toggle');
  if (btn) btn.textContent = currentLang === 'ko' ? 'EN / 한' : '한 / EN';

  renderCards(getFilteredArtifacts());

  const overlay = document.getElementById('artifact-detail');
  if (overlay && !overlay.classList.contains('hidden') && currentDetailData) {
    renderDetailContent(currentDetailData);
  }
  if (typeof updateGraphLabels === 'function') { updateGraphLabels(currentLang); }
}

// ── Event Bindings ─────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
  document.body.dataset.lang = currentLang;

  // 언어 토글
  document.getElementById('lang-toggle')?.addEventListener('click', toggleLang);

  // 상세 뷰 닫기
  document.getElementById('detail-close')?.addEventListener('click', () => {
    closeDetail();
  });

  document.getElementById('artifact-detail')?.addEventListener('click', (event) => {
    if (event.target === event.currentTarget) {
      closeDetail();
    }
  });

  // ESC 키로 상세 뷰 닫기
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeDetail();
    }
  });

  window.addEventListener('hashchange', () => {
    if (skipNextHashChange) {
      skipNextHashChange = false;
      return;
    }

    const artifactId = getHashArtifactId();
    if (artifactId) {
      showDetail(artifactId);
      return;
    }

    closeDetail({ clearHash: false });
  });

  await loadManifest();

  const initialArtifactId = getHashArtifactId();
  if (initialArtifactId) {
    showDetail(initialArtifactId);
  }
});

// ── Graph / Cards Tab Switching ──────────────────────────────────────────
(function () {
  var graphInitialized = false;

  document.querySelectorAll('.tab-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var tab = btn.dataset.tab;
      document.querySelectorAll('.tab-btn').forEach(function (b) { b.classList.remove('active'); });
      document.querySelectorAll('.tab-content').forEach(function (c) { c.classList.remove('active'); });
      btn.classList.add('active');
      var panel = tab === 'graph' ? document.getElementById('cy') : document.getElementById('card-grid');
      if (panel) { panel.classList.add('active'); }
      if (tab === 'graph' && !graphInitialized) {
        graphInitialized = true;
        if (typeof initGraph === 'function') { initGraph(); }
      }
    });
  });

  (function () {
    var activeBtn = document.querySelector('.tab-btn.active');
    if (activeBtn && activeBtn.dataset.tab === 'graph' && !graphInitialized) {
      graphInitialized = true;
      if (typeof initGraph === 'function') { initGraph(); }
    }
  }());

  document.querySelectorAll('#edge-filters input[type="checkbox"]').forEach(function (cb) {
    cb.addEventListener('change', function () {
      var active = [];
      document.querySelectorAll('#edge-filters input[type="checkbox"]:checked').forEach(function (c) {
        active.push(c.dataset.edgeType);
      });
      if (typeof filterEdges === 'function') { filterEdges(active); }
    });
  });
})();

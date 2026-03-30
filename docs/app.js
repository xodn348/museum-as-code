'use strict';

// ── Constants ──────────────────────────────────────────────────────────────
const MANIFEST_URL = './manifest.json';

// ── State ──────────────────────────────────────────────────────────────────
let currentLang = 'ko';  // 'ko' | 'en'
let allArtifacts = [];
let currentFilter = 'all';
let cardObserver = null;

const FILTER_LABELS = {
  all: '전체',
  'national-treasures': '국보·보물',
  kdh: 'KDH',
};

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

// ── Stubs (T13/T14에서 구현됨) ────────────────────────────────────────────

/**
 * T12에서 생성될 manifest.json을 페치한다.
 */
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

  grid.innerHTML = '';

  if (!Array.isArray(artifacts) || artifacts.length === 0) {
    return;
  }

  const cardElements = artifacts.map((artifact) => {
    const card = document.createElement('div');
    const isKdh = artifact.collection === 'kdh';

    card.className = `artifact-card card-skeleton${isKdh ? ' kdh' : ''}`;
    card.dataset.id = artifact.id;
    card.dataset.collection = artifact.collection;
    card.setAttribute('role', 'button');
    card.setAttribute('tabindex', '0');

    const badge = isKdh ? '<span class="kdh-badge">KDH</span>' : '';
    card.innerHTML = `
      <div class="card-body">
        ${badge}
        <h3 class="card-title">${artifact.name_ko ?? ''}</h3>
        <p class="card-subtitle">${artifact.name_en ?? ''}</p>
        <p class="card-designation">${artifact.designation ?? ''}</p>
        <p class="card-period">${artifact.period ?? ''}</p>
      </div>
    `;

    const handleOpenDetail = () => {
      showDetail(artifact.id);
    };

    card.addEventListener('click', handleOpenDetail);
    card.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        handleOpenDetail();
      }
    });

    grid.appendChild(card);
    return card;
  });

  observeCards(cardElements);
}

/**
 * 특정 artifact의 상세 overlay를 표시한다.
 * @param {string} artifactId - artifact의 id 필드 (예: "nb_001", "kdh_001")
 * TODO: T14에서 구현
 */
function showDetail(artifactId) {
  // TODO: T14에서 구현
}

/**
 * ko/en 언어를 토글하고 모든 렌더링을 업데이트한다.
 * TODO: T14에서 완전 구현 — 현재는 버튼 텍스트만 업데이트
 */
function toggleLang() {
  currentLang = currentLang === 'ko' ? 'en' : 'ko';
  const btn = document.getElementById('lang-toggle');
  if (btn) btn.textContent = currentLang === 'ko' ? 'EN / 한' : '한 / EN';
  // TODO: T14에서 카드/상세 뷰 재렌더링 로직 추가
}

// ── Event Bindings ─────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // 언어 토글
  document.getElementById('lang-toggle')?.addEventListener('click', toggleLang);

  // 상세 뷰 닫기
  document.getElementById('detail-close')?.addEventListener('click', () => {
    document.getElementById('artifact-detail')?.classList.add('hidden');
  });

  // ESC 키로 상세 뷰 닫기
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      document.getElementById('artifact-detail')?.classList.add('hidden');
    }
  });

  // manifest 로드 시작 (T13에서 이 호출이 실제로 작동)
  loadManifest();
});

'use strict';

// ── Constants ──────────────────────────────────────────────────────────────
const MANIFEST_URL = './manifest.json';
const HERO_INDEX_URL = './data/heroes/index.json';
const ROOMS_URL = './data/rooms.json';
const GITHUB_URL = 'https://github.com/xodn348/museum-as-code';

// ── State ──────────────────────────────────────────────────────────────────
// Language is owned by window.MuseumI18n (see docs/i18n.js). We mirror it
// here for compatibility with existing render code that reads currentLang.
let currentLang = (window.MuseumI18n && window.MuseumI18n.lang) || 'en';
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



function buildMiniHglArtifact({ nameKo, nameEn, designation, room, sourcePath }) {
  const safeNameKo = nameKo || '유물';
  const safeNameEn = nameEn || safeNameKo;
  return [
    `구조 유물 {`,
    `  이름: "${safeNameKo}"`,
    `  english: "${safeNameEn}"`,
    designation ? `  지정: "${designation}"` : '',
    room ? `  방: "${room}"` : '',
    sourcePath ? `  소스: "${sourcePath}"` : '',
    `}`,
  ].filter(Boolean).join('\n');
}

function isExactImageVerified(record) {
  if (!record) return false;
  if (record.exact_image_verified === true) return true;
  if (record.sidecar?.exact_image_verified === true) return true;
  const firstImage = Array.isArray(record.images) ? record.images[0] : null;
  if (firstImage?.exact_image_verified === true) return true;
  const sidecarImage = Array.isArray(record.sidecar?.images) ? record.sidecar.images[0] : null;
  return sidecarImage?.exact_image_verified === true;
}

function getVerifiedImagePath(record) {
  if (!isExactImageVerified(record)) return '';
  const sidecarImage = Array.isArray(record.sidecar?.images) ? record.sidecar.images[0] : null;
  const ownImage = Array.isArray(record.images) ? record.images[0] : null;
  return sidecarImage?.path
    || record.sidecar?.cover_image
    || record.sidecar?.image_url
    || ownImage?.path
    || record.cover_image
    || record.image_url
    || '';
}

function imageVerificationNote(record) {
  return record?.verification_note
    || record?.sidecar?.verification_note
    || record?.needs_verification
    || record?.sidecar?.needs_verification
    || 'Image withheld until the exact object, license, and local file are verified.';
}

function getOfficialImageUrl(record) {
  if (!record) return '';
  return record.image_official_url
    || record.sidecar?.image_official_url
    || '';
}

// Shared image-caption resolver. Honors `image_display_mode` ∈
// {exact, official, representative} so room cards, archive figures,
// and featured cards all label the image truthfully (e.g. celadon
// 매병 is representative — not "exact image verified").
function resolveImageCaption(record) {
  const sidecar = record?.sidecar || record || {};
  const firstImage = Array.isArray(sidecar.images) ? sidecar.images[0] : null;
  const mode = sidecar.image_display_mode
    || firstImage?.image_display_mode
    || (sidecar.exact_image_verified ? 'exact' : '');
  const ko = sidecar.image_caption_ko
    || firstImage?.caption_ko
    || (mode === 'official' ? '공식 도판 · 국가유산청'
      : mode === 'representative' ? '대표 도판'
      : '실물 이미지 검증 완료');
  const en = sidecar.image_caption_en
    || firstImage?.caption_en
    || (mode === 'official' ? 'official photograph · CHA'
      : mode === 'representative' ? 'representative work'
      : 'exact image verified');
  return { mode, ko, en };
}

function getOfficialImageMeta(record) {
  if (!record) return null;
  const src = record.image_source_api || record.sidecar?.image_source_api || '';
  const license = record.image_official_license || record.sidecar?.image_official_license || '';
  const credit = record.image_official_credit || record.sidecar?.image_official_credit || '';
  const sourceName = record.image_official_source_name_ko
    || record.sidecar?.image_official_source_name_ko
    || '';
  if (!src && !license && !credit) return null;
  return { src, license, credit, sourceName };
}

function trimHglPreview(text, maxLines = 9) {
  if (!text) return '';
  const lines = text
    .split('\n')
    .map((line) => line.replace(/,\s*$/, ''))
    .filter((line) => {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('//')) return false;
      if (/^구조\s/.test(trimmed)) return true;
      if (/^(함수|main\(|})/.test(trimmed)) return false;
      if (/:\s*(문자열|정수|부울|목록|날짜|실수)$/.test(trimmed)) return false;
      // Drop the English-translation field from previews; the Korean
      // 이야기 line is what carries the meaning on the card.
      if (/^이야기_영문\s*:/.test(trimmed)) return false;
      return /^(변수|출력|[\p{L}\p{N}_]+:)/u.test(trimmed);
    });
  return lines.slice(0, maxLines).join('\n');
}

async function fetchTextPreview(path, maxLines = 9) {
  if (!path) return '';
  try {
    const response = await fetch(path);
    if (!response.ok) return '';
    return trimHglPreview(await response.text(), maxLines);
  } catch (_) {
    return '';
  }
}

async function hydrateHeroHgl(heroes) {
  return Promise.all(heroes.map(async (hero) => ({
    ...hero,
    hglPreview: await fetchTextPreview(hero.hgl_path, 8),
  })));
}

function setGithubLinks() {
  document.querySelectorAll('[data-github-url]').forEach((link) => {
    link.href = GITHUB_URL;
  });
}

async function loadRooms() {
  const grid = document.getElementById('rooms-grid');
  if (!grid) return;
  try {
    const [roomsResponse, heroesResponse] = await Promise.all([
      fetch(ROOMS_URL),
      fetch(HERO_INDEX_URL),
    ]);
    if (!roomsResponse.ok) throw new Error(`Rooms fetch failed with status ${roomsResponse.status}`);
    if (!heroesResponse.ok) throw new Error(`Hero index fetch failed with status ${heroesResponse.status}`);
    const rooms = await roomsResponse.json();
    const heroIndex = await heroesResponse.json();
    const hydratedHeroes = await hydrateHeroHgl(Array.isArray(heroIndex.heroes) ? heroIndex.heroes : []);
    renderRooms(Array.isArray(rooms.rooms) ? rooms.rooms : [], hydratedHeroes);
  } catch (error) {
    console.error('rooms 로드 실패:', error);
    grid.innerHTML = '<p class="error">Rooms failed to load.</p>';
  }
}

function renderRooms(rooms, heroes) {
  const grid = document.getElementById('rooms-grid');
  if (!grid) return;
  const heroById = new Map(heroes.map((hero) => [hero.id, hero]));
  grid.innerHTML = '';
  const fragment = document.createDocumentFragment();
  rooms
    .slice()
    .sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0))
    .forEach((room) => {
      const card = document.createElement('section');
      card.className = 'room-card';
      const roomHeroes = (room.hero_ids || []).map((id) => heroById.get(id)).filter(Boolean);
      const preview = roomHeroes.slice(0, 3).map((hero) => {
        const title = currentLang === 'ko' ? (hero.name_ko || '') : (hero.name_en || hero.name_ko || '');
        const imagePath = getVerifiedImagePath(hero);
        if (imagePath) {
          const cap = resolveImageCaption(hero);
          const captionText = currentLang === 'ko' ? cap.ko : cap.en;
          const repClass = cap.mode === 'representative' ? ' representative' : '';
          return `
            <a class="room-hero-link image-room-link${repClass}" href="hero.html?id=${encodeURIComponent(hero.id)}">
              <img src="${escapeHtml(imagePath)}" alt="${escapeHtml(title)}" loading="lazy" decoding="async">
              <span class="room-code-label">${escapeHtml(title)}<small>${escapeHtml(captionText)}</small></span>
            </a>
          `;
        }

        const code = hero.hglPreview || buildMiniHglArtifact({
          nameKo: hero.name_ko,
          nameEn: hero.name_en,
          designation: hero.designation,
          room: hero.room,
          sourcePath: hero.hgl_path,
        });
        return `
          <a class="room-hero-link code-room-link needs-source-review" href="hero.html?id=${encodeURIComponent(hero.id)}" title="${escapeHtml(imageVerificationNote(hero))}">
            <span class="room-code-label">${escapeHtml(title)}</span>
            <pre class="hgl" aria-hidden="true"><code class="hgl">${highlightCode(code)}</code></pre>
          </a>
        `;
      }).join('');
      card.innerHTML = `
        <div class="room-card-heading">
          <p class="room-count">${String(roomHeroes.length).padStart(2, '0')} hero pages</p>
          <h3>${escapeHtml(currentLang === 'ko' ? room.name_ko : room.name_en)}</h3>
          <p>${escapeHtml(currentLang === 'ko' ? room.intro_ko : room.intro_en)}</p>
        </div>
        <div class="room-hero-strip">${preview}</div>
      `;
      fragment.appendChild(card);
    });
  grid.appendChild(fragment);
}

async function loadFeaturedHeroes() {
  const grid = document.getElementById('featured-grid');
  if (!grid) return;

  try {
    const response = await fetch(HERO_INDEX_URL);
    if (!response.ok) {
      throw new Error(`Hero index fetch failed with status ${response.status}`);
    }
    const index = await response.json();
    const baseHeroes = Array.isArray(index.heroes) ? index.heroes : [];
    const heroesWithSidecar = await Promise.all(baseHeroes.map(async (hero) => {
      const sidecar = await fetchHeroSidecar(hero);
      return { ...hero, sidecar };
    }));
    renderFeaturedHeroes(heroesWithSidecar);
  } catch (error) {
    console.error('hero index 로드 실패:', error);
    grid.innerHTML = '<p class="error">Hero artifacts failed to load.</p>';
  }
}

async function fetchHeroSidecar(hero) {
  if (!hero || !hero.data_file) return {};
  try {
    const res = await fetch(hero.data_file);
    if (!res.ok) return {};
    return await res.json();
  } catch (_) {
    return {};
  }
}

// KPDH-A: short id derived from hero.id (drop "hero_" prefix) for use as variable name
function kpdhVarName(heroId) {
  if (typeof heroId !== 'string') return 'artifact';
  return heroId.replace(/^hero_/, '') || 'artifact';
}

// KPDH-A: build the per-card Han instance snippet that matches the shared
// 히어로유물 schema declared once on the page.
function buildKpdhCardCode(hero) {
  const sidecar = hero.sidecar || {};
  const designationKo = sidecar.designation_ko || hero.designation || '';
  const eraKo = sidecar.era || hero.period || '';
  const materialKo = sidecar.material || sidecar.material_en || '';
  const sizeRaw = sidecar.size || '';
  const sizeShort = sizeRaw.replace(/\s*\(source verification required\)/i, '').trim();
  const locationKo = sidecar.location || '';
  const verified = isExactImageVerified(hero);
  const storyKo = sidecar.story_ko || '';
  const storyOpener = storyKo
    ? storyKo.split(/(?<=[.…])\s+/)[0].replace(/"/g, "'")
    : '';

  const lines = [
    `// ${designationKo || hero.designation || ''}`.trim(),
    `변수 ${kpdhVarName(hero.id)} = 히어로유물 {`,
    `    이름:     "${hero.name_ko || ''}",`,
    `    영문명:   "${hero.name_en || ''}",`,
    `    지정:     "${designationKo || hero.designation || ''}",`,
    `    시대:     "${eraKo}",`,
    `    재료:     "${materialKo}",`,
    `    크기:     "${sizeShort}",`,
    `    소장처:   "${locationKo}",`,
    storyOpener ? `    이야기:   "${storyOpener}…",` : null,
    `    출처검증: ${verified ? '참' : '거짓'}`,
    `}`,
    `설명출력(${kpdhVarName(hero.id)})`,
  ].filter(Boolean);
  return lines.join('\n');
}

function renderFeaturedHeroes(heroes) {
  const grid = document.getElementById('featured-grid');
  if (!grid) return;
  grid.innerHTML = '';
  const fragment = document.createDocumentFragment();

  heroes.forEach((hero, index) => {
    const card = document.createElement('a');
    const imagePath = getVerifiedImagePath(hero);
    const verified = Boolean(imagePath);
    card.className = `kpdh-card${verified ? ' image-verified' : ' needs-source-review'}`;
    card.href = `hero.html?id=${encodeURIComponent(hero.id)}`;
    card.style.setProperty('--delay', `${Math.min(index * 40, 320)}ms`);

    const titleEn = hero.name_en || hero.name_ko || '';
    const titleKr = hero.name_ko || '';
    const seal = String(index + 1).padStart(2, '0');
    const room = (hero.room || '').toUpperCase();
    const fileTag = `heroes/${kpdhVarName(hero.id)}.hgl`;
    const code = buildKpdhCardCode(hero);
    const cap = resolveImageCaption(hero);
    const repClass = cap.mode === 'representative' ? ' representative' : '';
    const imageMarkup = verified ? `
      <figure class="kpdh-card-figure${repClass}">
        <img src="${escapeHtml(imagePath)}" alt="${escapeHtml(titleEn)}" loading="lazy" decoding="async">
        <figcaption>
          <span data-lang="ko">${escapeHtml(cap.ko)}</span>
          <span data-lang="en">${escapeHtml(cap.en)}</span>
        </figcaption>
      </figure>
    ` : `
      <div class="kpdh-card-image-pending" title="${escapeHtml(imageVerificationNote(hero))}">
        <span>IMAGE WITHHELD</span>
        <small>source match pending</small>
      </div>
    `;

    card.innerHTML = `
      <div class="seal">${escapeHtml(seal)}</div>
      <div class="num">// HERO_${escapeHtml(seal)}${room ? ' · ' + escapeHtml(room) : ''}</div>
      <div class="file-tag">${escapeHtml(fileTag)}</div>
      ${imageMarkup}
      <pre class="hgl"><code class="hgl">${highlightCode(code)}</code></pre>
      <div class="title-en">${escapeHtml(titleEn)}</div>
      <div class="title-kr">${escapeHtml(titleKr)}</div>
      <div class="meta">→ ${verified ? 'exact image · source-backed · .hgl' : 'awaiting exact image · .hgl'}</div>
    `;
    fragment.appendChild(card);
  });

  grid.appendChild(fragment);
}

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
      activeCategoryFilter = 'all';
      ensureFilterTabs(counts);
      const filteredArtifacts = currentFilter === 'all'
        ? allArtifacts
        : allArtifacts.filter((artifact) => artifact.collection === currentFilter);
      renderCategoryPills(filteredArtifacts);
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

// Delegate Han syntax highlighting to the standalone han-highlight.js module
// (window.Han.highlight). Falls back to escaped text if loaded before the
// highlighter script attaches — the auto highlightAll() pass will then style
// any <pre class="hgl"> / <code class="hgl"> elements after DOMContentLoaded.
function highlightCode(text) {
  if (text == null) return '';
  if (window.Han && typeof window.Han.highlight === 'function') {
    return window.Han.highlight(String(text));
  }
  return escapeHtml(String(text));
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
    <pre class="hgl"><code class="hgl detail-code">${highlightCode(hglContent)}</code></pre>
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

async function hydrateArtifactExtras(artifacts) {
  // For each artifact: pull sidecar.category (drives filter pills) and a real
  // .hgl preview (drives the rose-bordered code plate on each card). Both are
  // best-effort — failures fall back to manifest fields and the synthetic
  // buildMiniHglArtifact placeholder.
  await Promise.all(artifacts.map(async (a) => {
    try {
      const [sidecarRes, hglRes] = await Promise.all([
        fetch(a.json_path),
        fetch(a.hgl_path),
      ]);
      if (sidecarRes.ok) {
        const sidecar = await sidecarRes.json();
        a.categoryRaw = sidecar.category || '';
        a.sidecar = sidecar;
        a.exact_image_verified = a.exact_image_verified || sidecar.exact_image_verified === true;
      }
      if (hglRes.ok) {
        a.hglPreview = trimHglPreview(await hglRes.text(), 8);
      }
    } catch (_) {
      // ignore — card still renders with the synthetic preview
    }
  }));
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

    const periodOrder = {
      '선사시대': 1, '고조선': 2,
      '삼국시대': 3, '백제': 3, '신라': 3, '가야': 3, '가야시대': 3,
      '통일신라시대': 4, '고려시대': 5, '조선시대': 6, '근현대': 7,
    };
    allArtifacts.sort((a, b) => (periodOrder[a.period] ?? 99) - (periodOrder[b.period] ?? 99));

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

    updateArchiveCount(totalCount);
    renderCards(allArtifacts);

    // Hydrate sidecar + .hgl preview in the background, then re-render so
    // every card carries a real Han snippet and category pills become useful.
    hydrateArtifactExtras(allArtifacts).then(() => {
      const collectionFiltered = getFilteredArtifacts();
      renderCategoryPills(collectionFiltered);
      renderCards(applyCategoryFilter(collectionFiltered));
    });
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
function createArtifactCodePlate(artifact) {
  const placeholder = document.createElement('div');
  placeholder.className = 'artifact-image-placeholder artifact-code-plate';
  const code = buildMiniHglArtifact({
    nameKo: artifact.name_ko,
    nameEn: artifact.name_en,
    designation: artifact.designation,
    room: artifact.period,
    sourcePath: artifact.hgl_path,
  });
  placeholder.innerHTML = `<pre class="hgl"><code class="hgl">${highlightCode(code)}</code></pre>`;
  return placeholder;
}

function createVerifiedArtifactImage(artifact) {
  const imagePath = getVerifiedImagePath(artifact);
  if (!imagePath) return createArtifactCodePlate(artifact);

  const figure = document.createElement('figure');
  figure.className = 'artifact-image verified-artifact-image';

  const img = document.createElement('img');
  img.src = imagePath;
  img.alt = currentLang === 'ko'
    ? (artifact.name_ko ?? artifact.name_en ?? '')
    : (artifact.name_en ?? artifact.name_ko ?? '');
  img.loading = 'lazy';
  img.decoding = 'async';

  const cap = resolveImageCaption(artifact);
  if (cap.mode === 'representative') figure.classList.add('representative');
  const caption = document.createElement('figcaption');
  caption.innerHTML = `<span data-lang="ko">${escapeHtml(cap.ko)}</span><span data-lang="en">${escapeHtml(cap.en)}</span>`;

  figure.append(img, caption);
  return figure;
}

function createImagePlaceholder() {
  const placeholder = document.createElement('div');
  placeholder.className = 'artifact-image-placeholder';
  placeholder.textContent = 'Museum as Code';
  return placeholder;
}

// KPDH-A archive card: file-tag, rose-bordered code plate, dual-script title,
// source-backed meta. The .hgl preview comes from the real artifact file (8
// lines, comments + `함수`/`}` stripped) so every card is a tiny window into
// runnable Han.
function archiveFileTag(artifact) {
  const path = String(artifact.hgl_path || '').replace(/^\.?\//, '').replace(/^data\//, '');
  return path || `${artifact.collection || 'archive'}/${artifact.id || 'unknown'}.hgl`;
}

function buildArchiveCardCode(artifact) {
  if (artifact.hglPreview) return artifact.hglPreview;
  return buildMiniHglArtifact({
    nameKo: artifact.name_ko,
    nameEn: artifact.name_en,
    designation: artifact.designation,
    room: artifact.period,
    sourcePath: artifact.hgl_path,
  });
}

// Map the heterogeneous sidecar.category strings (불교 조각, 금속공예, 도자기,
// 전적류, 민화, 회화, 유적건조물, ...) onto a small set of filter buckets that
// match the brief: Sculpture, Ceramic, Records, Metal, Painting, Architecture.
const CATEGORY_GROUPS = [
  { id: 'sculpture',   labelEn: 'Sculpture',    labelKo: '조각',  match: /조각|석조|신앙器材/ },
  { id: 'ceramic',     labelEn: 'Ceramic',      labelKo: '도자',  match: /도자|토기/ },
  { id: 'metal',       labelEn: 'Metal',        labelKo: '금속',  match: /금속|철조/ },
  { id: 'painting',    labelEn: 'Painting',     labelKo: '회화',  match: /회화|민화|불교 화/ },
  { id: 'records',     labelEn: 'Records',      labelKo: '기록',  match: /전적|서예|비문|금석문|지형도/ },
  { id: 'architecture',labelEn: 'Architecture', labelKo: '건축',  match: /건조물|시설|고분|과학기술유적|직물/ },
];

function categoryGroupFor(rawCategory) {
  const c = String(rawCategory || '').trim();
  if (!c) return 'other';
  for (const g of CATEGORY_GROUPS) {
    if (g.match.test(c)) return g.id;
  }
  return 'other';
}

let activeCategoryFilter = 'all'; // 'all' | one of CATEGORY_GROUPS[].id | 'other'

function renderCategoryPills(artifacts) {
  const host = document.getElementById('archive-category-pills');
  if (!host) return;
  if (!Array.isArray(artifacts) || artifacts.length === 0) {
    host.innerHTML = '';
    return;
  }
  // Count categories within the currently-collection-filtered set.
  const counts = { all: artifacts.length, other: 0 };
  for (const g of CATEGORY_GROUPS) counts[g.id] = 0;
  for (const a of artifacts) {
    const id = categoryGroupFor(a.categoryRaw);
    counts[id] = (counts[id] || 0) + 1;
  }
  const pills = [
    { id: 'all', labelEn: 'All', labelKo: '전체' },
    ...CATEGORY_GROUPS,
  ];
  if (counts.other > 0) {
    pills.push({ id: 'other', labelEn: 'Other', labelKo: '기타' });
  }
  host.innerHTML = '';
  pills.forEach((p) => {
    if (counts[p.id] === 0 && p.id !== 'all') return;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = `kpdh-pill${activeCategoryFilter === p.id ? ' active' : ''}`;
    btn.dataset.category = p.id;
    const label = currentLang === 'ko' ? p.labelKo : p.labelEn;
    btn.innerHTML = `${escapeHtml(label)}<span class="count">${counts[p.id]}</span>`;
    btn.addEventListener('click', () => {
      activeCategoryFilter = p.id;
      const collectionFiltered = getFilteredArtifacts();
      renderCards(applyCategoryFilter(collectionFiltered));
      renderCategoryPills(collectionFiltered);
    });
    host.appendChild(btn);
  });
}

function applyCategoryFilter(artifacts) {
  if (activeCategoryFilter === 'all') return artifacts;
  return artifacts.filter((a) => categoryGroupFor(a.categoryRaw) === activeCategoryFilter);
}

function updateArchiveCount(total) {
  const el = document.getElementById('archive-count');
  if (el) el.textContent = `국보·보물 · ${total} · written in .hgl`;
}

function renderCards(artifacts) {
  const grid = document.getElementById('card-grid');
  if (!grid) return;

  updateKdhHeaderText();

  grid.innerHTML = '';

  if (!Array.isArray(artifacts) || artifacts.length === 0) {
    return;
  }

  const fragment = document.createDocumentFragment();

  const cardElements = artifacts.map((artifact, index) => {
    const card = document.createElement('a');
    const isKdh = artifact.collection === 'kdh';
    const verified = isExactImageVerified(artifact);
    const hasOfficialImage = Boolean(getOfficialImageUrl(artifact));
    const cardImageState = verified
      ? ' image-verified'
      : hasOfficialImage
        ? ' image-official'
        : ' needs-source-review';

    card.className = `kpdh-card archive-card${isKdh ? ' kdh' : ''}${cardImageState}`;
    card.href = `#artifact-${encodeURIComponent(artifact.id)}`;
    card.dataset.id = artifact.id;
    card.dataset.collection = artifact.collection;
    card.style.setProperty('--delay', `${Math.min(index * 16, 320)}ms`);

    const titleEn = artifact.name_en || artifact.name_ko || '';
    const titleKr = artifact.name_ko || '';
    const designation = artifact.designation || '';
    const period = artifact.period || '';
    const seal = (designation.match(/(\d+)/)?.[1] || String(index + 1)).padStart(3, '0');
    const fileTag = archiveFileTag(artifact);
    const code = buildArchiveCardCode(artifact);
    const imagePath = getVerifiedImagePath(artifact);
    const officialUrl = getOfficialImageUrl(artifact);
    const officialMeta = getOfficialImageMeta(artifact);
    let imageMarkup;
    if (officialUrl) {
      const sourceLabel = officialMeta?.src === 'cha'
        ? '국가유산청 (CHA)'
        : (officialMeta?.src || 'official source');
      const licenseLabel = officialMeta?.license || '';
      const captionParts = [sourceLabel, licenseLabel].filter(Boolean).join(' · ');
      imageMarkup = `
      <figure class="kpdh-card-figure official-image">
        <img src="${escapeHtml(officialUrl)}" alt="${escapeHtml(titleEn)}" loading="lazy" decoding="async" referrerpolicy="no-referrer">
        <figcaption class="image-credit">${escapeHtml(captionParts)}</figcaption>
      </figure>
    `;
    } else if (imagePath) {
      const cap = resolveImageCaption(artifact);
      const repClass = cap.mode === 'representative' ? ' representative' : '';
      imageMarkup = `
      <figure class="kpdh-card-figure${repClass}">
        <img src="${escapeHtml(imagePath)}" alt="${escapeHtml(titleEn)}" loading="lazy" decoding="async">
        <figcaption>
          <span data-lang="ko">${escapeHtml(cap.ko)}</span>
          <span data-lang="en">${escapeHtml(cap.en)}</span>
        </figcaption>
      </figure>
    `;
    } else {
      imageMarkup = `
      <div class="kpdh-card-image-pending" title="${escapeHtml(imageVerificationNote(artifact))}">
        <span>IMAGE WITHHELD</span>
        <small>source match pending</small>
      </div>
    `;
    }
    const tagBits = [
      designation,
      period,
      isKdh ? '🎬 K-pop Demon Hunters' : '',
    ].filter(Boolean).map((t) => escapeHtml(t)).join(' · ');

    card.innerHTML = `
      <div class="seal">${escapeHtml(seal)}</div>
      <div class="num">// ${escapeHtml((artifact.id || '').toUpperCase())}${period ? ' · ' + escapeHtml(period) : ''}</div>
      <div class="file-tag">${escapeHtml(fileTag)}</div>
      ${imageMarkup}
      <pre class="hgl"><code class="hgl">${highlightCode(code)}</code></pre>
      <div class="title-en">${escapeHtml(titleEn)}</div>
      <div class="title-kr">${escapeHtml(titleKr)}</div>
      <div class="meta">→ ${tagBits || '.hgl'}</div>
    `;

    card.addEventListener('click', (event) => {
      event.preventDefault();
      showDetail(artifact.id);
    });

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
 * Re-render every dynamic surface after the language flips. i18n.js handles
 * the toggle button click + body[data-lang] + static text-swap; this only
 * re-runs the data-bound renderers (cards, rooms, featured heroes, detail).
 */
function applyLanguage(nextLang) {
  currentLang = nextLang;
  setGithubLinks();

  const collectionFiltered = getFilteredArtifacts();
  renderCategoryPills(collectionFiltered);
  renderCards(applyCategoryFilter(collectionFiltered));
  loadFeaturedHeroes();
  loadRooms();

  const overlay = document.getElementById('artifact-detail');
  if (overlay && !overlay.classList.contains('hidden') && currentDetailData) {
    renderDetailContent(currentDetailData);
  }
  if (typeof updateGraphLabels === 'function') { updateGraphLabels(currentLang); }
}

// i18n.js owns the toggle button + localStorage. We register at module scope
// (not inside DOMContentLoaded) so we don't miss the initial languagechange
// that i18n.js dispatches during its own DOMContentLoaded init.
document.addEventListener('languagechange', (e) => applyLanguage(e.detail.lang));

// ── KPDH tab system ──────────────────────────────────────────────────────────
// 3 panes (Featured / Rooms / Archive) replace the long-scroll layout.
// The hero section sits above the tab bar. URL hash (#featured, #rooms,
// #archive) is the source of truth so deep-links and the back button work.
const TAB_NAMES = ['featured', 'rooms', 'archive'];
function getTabFromHash() {
  const raw = (location.hash || '').replace(/^#/, '').toLowerCase();
  if (TAB_NAMES.includes(raw)) return raw;
  // Legacy anchor support (#featured-heroes, #card-grid)
  if (raw === 'featured-heroes') return 'featured';
  if (raw === 'card-grid') return 'archive';
  return null;
}
function activateTab(name, opts) {
  if (!TAB_NAMES.includes(name)) name = 'featured';
  const pushHash = !(opts && opts.silent);
  document.querySelectorAll('.kpdh-tab-btn').forEach((btn) => {
    const on = btn.dataset.tab === name;
    btn.setAttribute('aria-selected', on ? 'true' : 'false');
  });
  document.querySelectorAll('.kpdh-tab-pane').forEach((pane) => {
    pane.classList.toggle('active', pane.dataset.pane === name);
  });
  if (pushHash && location.hash !== '#' + name) {
    history.replaceState(null, '', '#' + name);
  }
}
function initTabs() {
  document.querySelectorAll('.kpdh-tab-btn').forEach((btn) => {
    btn.addEventListener('click', () => activateTab(btn.dataset.tab));
  });
  document.querySelectorAll('[data-tab-link]').forEach((link) => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      activateTab(link.dataset.tabLink);
      window.scrollTo({ top: document.querySelector('.kpdh-tab-bar')?.offsetTop || 0, behavior: 'smooth' });
    });
  });
  window.addEventListener('hashchange', () => {
    const t = getTabFromHash();
    if (t) activateTab(t, { silent: true });
  });
  const initial = getTabFromHash() || 'featured';
  activateTab(initial, { silent: true });
}

// ── Event Bindings ─────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
  document.body.dataset.lang = currentLang;
  setGithubLinks();
  initTabs();

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

  await Promise.all([loadManifest(), loadFeaturedHeroes(), loadRooms()]);

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
      var panel = tab === 'graph' ? document.getElementById('cy') : (tab === 'featured' ? document.getElementById('featured-heroes') : (tab === 'rooms' ? document.getElementById('rooms') : document.getElementById('card-grid')));
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
    var activeGraphPanel = document.getElementById('cy');
    if (!activeBtn && activeGraphPanel && activeGraphPanel.classList.contains('active') && !graphInitialized) {
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

// Image error fallback — when khs.go.kr (or any external host) refuses a
// hotlink, swap the broken <img> for the same "IMAGE WITHHELD" placeholder
// the unverified cards already use. Delegated at the document root so it
// catches images rendered after re-render. Capture phase because img.error
// does not bubble.
document.addEventListener('error', function (e) {
  var img = e.target;
  if (!(img instanceof HTMLImageElement)) return;
  var figure = img.closest('.kpdh-card-figure, .room-hero-link.image-room-link, .verified-artifact-image');
  if (!figure) return;
  var placeholder = document.createElement('div');
  placeholder.className = 'kpdh-card-image-pending';
  placeholder.title = 'Source image unreachable — falling back to code plate.';
  placeholder.innerHTML = '<span>IMAGE UNREACHABLE</span><small>source host blocked the request</small>';
  figure.replaceWith(placeholder);
}, true);

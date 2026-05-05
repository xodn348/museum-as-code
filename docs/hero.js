'use strict';

// hero.js — Phase C hero detail loader, KPDH talisman skin.
// Loads the real .hgl source (no mock) and renders Han syntax highlighting
// with: rose=keyword (구조/함수/변수/...), gold=built-in (출력/형식/...),
// violet=type (문자열/정수/불/참/거짓), jade=string, faint=comment.

const HERO_INDEX_URL = './data/heroes/index.json';
const PLAYGROUND_URL = 'https://xodn348.github.io/han/playground/';
const GITHUB_RAW_PREFIX = 'https://raw.githubusercontent.com/xodn348/museum-as-code/main/';
const GITHUB_BLOB_PREFIX = 'https://github.com/xodn348/museum-as-code/blob/main/';

// Language is owned by window.MuseumI18n (see docs/i18n.js). Read it lazily
// so we always reflect the latest user choice without re-binding listeners.
function getLang() {
  return (window.MuseumI18n && window.MuseumI18n.lang) || 'en';
}
let currentHero = null;
let currentEntry = null;
let currentIndex = null;
let currentHglText = '';

function escapeHtml(text) {
  if (text == null) return '';
  return String(text)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text || '';
}

function isExactImageVerified(hero) {
  if (!hero) return false;
  if (hero.exact_image_verified === true) return true;
  const image = Array.isArray(hero.images) ? hero.images[0] : null;
  return image?.exact_image_verified === true;
}

function getPrimaryImage(hero) {
  const image = Array.isArray(hero?.images) ? hero.images[0] : null;
  return {
    path: image?.path || hero?.cover_image || hero?.image_url || '',
    sourceUrl: image?.source_url || hero?.source_url || '',
    license: image?.license || hero?.license || '',
    credit: image?.credit || hero?.credit || '',
    note: image?.verification_note || hero?.verification_note || hero?.needs_verification || '',
  };
}

function renderVerifiedImageState(hero) {
  const verified = isExactImageVerified(hero);
  const image = getPrimaryImage(hero);
  const img = document.getElementById('hero-image');
  const detail = document.getElementById('detail-image');
  const wrap = document.querySelector('.hero-image-wrap');
  const detailFigure = detail?.closest('figure');
  const note = image.note || 'Image withheld until the exact object, local file, and source license are verified.';

  document.getElementById('hero-image-pending')?.remove();
  document.getElementById('detail-image-pending')?.remove();
  wrap?.classList.toggle('image-withheld', !verified);
  detailFigure?.classList.toggle('image-withheld', !verified);

  if (verified && image.path) {
    if (img) {
      img.src = image.path;
      img.alt = hero.name_en || hero.name_ko || '';
      img.hidden = false;
    }
    if (detail) {
      detail.src = image.path;
      detail.alt = hero.name_en || hero.name_ko || '';
      detail.hidden = false;
    }
    setText('image-credit', `${image.credit} · ${image.license}`);
    setText('license-line', `${image.license} — ${image.credit}${image.sourceUrl ? ` (${image.sourceUrl})` : ''}`);
    return;
  }

  if (img) {
    img.removeAttribute('src');
    img.alt = '';
    img.hidden = true;
  }
  if (detail) {
    detail.removeAttribute('src');
    detail.alt = '';
    detail.hidden = true;
  }

  // No "IMAGE WITHHELD" panel — the Han code plate IS the artifact in this
  // museum. Hide the empty image frame entirely so the page reads cleanly.
  wrap?.classList.add('image-suppressed');
  detailFigure?.classList.add('image-suppressed');
  setText('image-credit', '');
  setText('license-line', '');
}

// Delegate Han highlighting to the standalone han-highlight module
// (window.Han.highlight). The shared module emits .han-* spans styled by
// han-highlight.css, ensuring identical token colors across home + hero.
function highlightHan(text) {
  if (text == null) return '';
  if (window.Han && typeof window.Han.highlight === 'function') {
    return window.Han.highlight(String(text));
  }
  return escapeHtml(String(text));
}

// i18n.js owns static text-swap and the lang-toggle button label. We only
// re-render dynamic surfaces (titles, meta, narrative copy) on languagechange.
function localizeStaticText() {
  // No-op kept for call-site compatibility; remove once renderLanguage drops it.
}

function renderLanguage() {
  document.body.dataset.lang = getLang();
  localizeStaticText();
  if (!currentHero) return;

  const titleKo = currentHero.name_ko;
  const titleEn = currentHero.name_en;
  setText('hero-title', getLang() === 'ko' ? titleKo : titleEn);
  setText('hero-subtitle', getLang() === 'ko' ? titleEn : titleKo);
  setText('hero-room', currentHero.room || '');
  setText('hero-hook', currentHero.hook || '');

  const designation = currentHero.designation || '';
  const chip = document.getElementById('hero-designation-chip');
  if (chip) chip.textContent = designation || '국보';

  const stampLabel = document.getElementById('hero-stamp-label');
  if (stampLabel) {
    const id = currentHero.id || currentEntry?.id || 'HERO';
    const seal = id.replace(/^hero_/, '').toUpperCase().slice(0, 14);
    stampLabel.textContent = `${seal} · 히어로유물`;
  }

  const sections = getLang() === 'ko' ? currentHero.sections_ko : currentHero.sections;
  const fallbackSummary = getLang() === 'ko' ? currentHero.summary_ko : currentHero.summary_en;
  setText('why-copy', sections?.why_this_matters || fallbackSummary);
  setText('looking-copy', sections?.what_you_are_looking_at || fallbackSummary);
  setText('story-copy', sections?.the_story || fallbackSummary);

  const meta = [
    [getLang() === 'ko' ? '지정' : 'Designation', currentHero.designation],
    [getLang() === 'ko' ? '시대' : 'Period', getLang() === 'ko' ? currentHero.period_ko : currentHero.period],
    [getLang() === 'ko' ? '재질' : 'Medium', getLang() === 'ko' ? currentHero.medium_ko : currentHero.medium],
    [
      getLang() === 'ko' ? '크기' : 'Size',
      currentHero.size || currentHero.dimensions || '—',
    ],
    [getLang() === 'ko' ? '소장처' : 'Location', getLang() === 'ko' ? currentHero.location_ko : currentHero.location],
  ];
  const metaEl = document.getElementById('hero-meta');
  if (metaEl) {
    metaEl.innerHTML = meta
      .filter(([, v]) => v)
      .map(([k, v]) => `<div><dt>${escapeHtml(k)}</dt><dd>${escapeHtml(v)}</dd></div>`)
      .join('');
  }
}

async function fetchJson(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Failed to fetch ${path}: ${response.status}`);
  return response.json();
}

async function fetchText(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Failed to fetch ${path}: ${response.status}`);
  return response.text();
}

function resolveId(index) {
  const params = new URLSearchParams(window.location.search);
  const id = params.get('id');
  if (id) return id;
  return index.heroes?.[0]?.id || '';
}

function renderNavigation(index, heroId) {
  const nav = document.getElementById('next-prev');
  if (!nav) return;
  const heroes = index.heroes || [];
  if (heroes.length === 0) return;
  const pos = heroes.findIndex((hero) => hero.id === heroId);
  const prev = heroes[(pos - 1 + heroes.length) % heroes.length];
  const next = heroes[(pos + 1) % heroes.length];
  nav.innerHTML = `
    ${prev ? `<a href="hero.html?id=${encodeURIComponent(prev.id)}">← ${escapeHtml(prev.name_en)}</a>` : ''}
    ${next ? `<a href="hero.html?id=${encodeURIComponent(next.id)}">${escapeHtml(next.name_en)} →</a>` : ''}
  `;
}

/** Wire download / playground / github buttons once we know the hero id + .hgl text.
 *
 * Note on the playground link: as of 2026-04, the Han playground at
 * xodn348.github.io/han/playground/ has NO query-string deep-link API —
 * it loads code from localStorage and has no URLSearchParams handling
 * (verified by reading web/index.html on main). So the button just
 * opens the bare playground; users paste the .hgl text from the page or
 * use the 'Download .hgl' button to grab the source. See DESIGN.md
 * 'Playground integration findings' for full notes.
 */
function wireSourceButtons(entry, hglText) {
  const heroId = entry.id;
  const filename = `${heroId}.hgl`;
  const fileEl = document.getElementById('hgl-filename');
  if (fileEl) fileEl.textContent = `📜 ${filename}`;

  // Use a Blob URL for download (works regardless of host path).
  const blob = new Blob([hglText], { type: 'text/plain;charset=utf-8' });
  const blobUrl = URL.createObjectURL(blob);

  const githubHref = `${GITHUB_BLOB_PREFIX}artifacts/heroes/${filename}`;

  for (const id of ['cta-playground', 'cta-playground-2']) {
    const el = document.getElementById(id);
    if (el) el.href = PLAYGROUND_URL;
  }
  for (const id of ['cta-download', 'cta-download-2']) {
    const el = document.getElementById(id);
    if (el) {
      el.href = blobUrl;
      el.setAttribute('download', filename);
    }
  }
  const gh = document.getElementById('cta-github');
  if (gh) gh.href = githubHref;
}

async function loadHero() {
  try {
    currentIndex = await fetchJson(HERO_INDEX_URL);
    const heroId = resolveId(currentIndex);
    const entry = (currentIndex.heroes || []).find((hero) => hero.id === heroId);
    if (!entry) throw new Error(`Unknown hero id: ${heroId}`);
    currentEntry = entry;
    currentHero = await fetchJson(entry.data_file);
    if (!currentHero.id) currentHero.id = entry.id;

    renderVerifiedImageState(currentHero);

    // The .hgl source is the canonical artifact — fetch and render verbatim.
    currentHglText = await fetchText(currentHero.hgl_path);
    const code = document.getElementById('hero-hgl');
    if (code) code.innerHTML = highlightHan(currentHglText);

    wireSourceButtons(entry, currentHglText);
    renderNavigation(currentIndex, heroId);
    renderLanguage();
    document.getElementById('hero-root')?.classList.remove('loading');
  } catch (error) {
    console.error(error);
    const errorEl = document.getElementById('hero-error');
    if (errorEl) {
      errorEl.classList.remove('hidden');
      errorEl.textContent = `Hero artifact failed to load: ${error.message}`;
    }
  }
}

// i18n.js owns the toggle button click + localStorage. We just re-render
// our dynamic content (titles, meta, narrative copy) when the language flips.
document.addEventListener('languagechange', () => {
  if (currentHero) renderLanguage();
});

document.addEventListener('DOMContentLoaded', () => {
  loadHero();
});

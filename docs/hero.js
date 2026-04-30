'use strict';

// hero.js — Phase C hero detail loader, KPDH talisman skin.
// Loads the real .hgl source (no mock) and renders Han syntax highlighting
// with: rose=keyword (구조/함수/변수/...), gold=built-in (출력/형식/...),
// violet=type (문자열/정수/불/참/거짓), jade=string, faint=comment.

const HERO_INDEX_URL = './data/heroes/index.json';
const PLAYGROUND_URL = 'https://xodn348.github.io/han/playground/';
const GITHUB_RAW_PREFIX = 'https://raw.githubusercontent.com/xodn348/museum-as-code/main/';
const GITHUB_BLOB_PREFIX = 'https://github.com/xodn348/museum-as-code/blob/main/';

const HAN_KEYWORDS = [
  '구조', '함수', '반환', '변수', '상수', '만약', '이면', '아니면',
  '그리고', '또는', '반복', '동안', '멈춰', '계속', '구현', '열거',
  '시도', '처리', '맞춤', '포함', '안에서'
];
const HAN_BUILTINS = [
  '출력', '형식', '길이', '입력', '정수변환', '실수변환',
  '사전', '파일읽기', '파일쓰기', 'main'
];
const HAN_TYPES = [
  '문자열', '정수', '실수', '불', '없음', '참', '거짓',
  '목록', '날짜', '부울'
];

let currentLang = 'en';
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

  const pending = document.createElement('div');
  pending.id = 'hero-image-pending';
  pending.className = 'image-pending-panel';
  pending.innerHTML = `
    <strong>IMAGE WITHHELD</strong>
    <span>${escapeHtml(note)}</span>
  `;
  wrap?.appendChild(pending);

  const detailPending = pending.cloneNode(true);
  detailPending.id = 'detail-image-pending';
  detailFigure?.appendChild(detailPending);

  setText('image-credit', note);
  setText('license-line', `Image withheld — ${note}`);
}

/**
 * Tokenize one already-html-escaped Han line.
 * Walks left-to-right, peeling off comments, strings, and identifiers.
 * Comments + strings short-circuit (regex on the rest of the line).
 */
function highlightLine(line) {
  // Comment: `//` to end of line. Everything before still tokenizes.
  const commentIdx = line.indexOf('//');
  if (commentIdx !== -1) {
    const before = line.slice(0, commentIdx);
    const comment = line.slice(commentIdx);
    return highlightLine(before) + `<span class="tok-cm">${comment}</span>`;
  }

  // Token boundary regex: identifiers (CJK + ASCII letters + digits + _),
  // numbers, strings, anything else passes through.
  const tokenRe = /(&quot;[^&]*?&quot;)|([\p{L}\p{N}_]+)|(\d+)/gu;
  let out = '';
  let last = 0;
  let m;
  while ((m = tokenRe.exec(line)) !== null) {
    out += line.slice(last, m.index);
    const tok = m[0];
    if (m[1]) {
      // String literal
      out += `<span class="tok-str">${tok}</span>`;
    } else if (HAN_KEYWORDS.includes(tok)) {
      out += `<span class="tok-kw">${tok}</span>`;
    } else if (HAN_TYPES.includes(tok)) {
      out += `<span class="tok-ty">${tok}</span>`;
    } else if (HAN_BUILTINS.includes(tok)) {
      out += `<span class="tok-bi">${tok}</span>`;
    } else if (/^\d+$/.test(tok)) {
      out += `<span class="tok-num">${tok}</span>`;
    } else {
      out += tok;
    }
    last = m.index + tok.length;
  }
  out += line.slice(last);
  return out;
}

function highlightHan(text) {
  const escaped = escapeHtml(text);
  return escaped.split('\n').map(highlightLine).join('\n');
}

function localizeStaticText() {
  document.querySelectorAll('[data-lang-ko]').forEach((el) => {
    el.textContent = currentLang === 'ko' ? el.dataset.langKo : el.dataset.langEn;
  });
  const button = document.getElementById('lang-toggle');
  if (button) button.textContent = currentLang === 'ko' ? 'EN / 한' : '한 / EN';
}

function renderLanguage() {
  document.body.dataset.lang = currentLang;
  localizeStaticText();
  if (!currentHero) return;

  const titleKo = currentHero.name_ko;
  const titleEn = currentHero.name_en;
  setText('hero-title', currentLang === 'ko' ? titleKo : titleEn);
  setText('hero-subtitle', currentLang === 'ko' ? titleEn : titleKo);
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

  const sections = currentLang === 'ko' ? currentHero.sections_ko : currentHero.sections;
  const fallbackSummary = currentLang === 'ko' ? currentHero.summary_ko : currentHero.summary_en;
  setText('why-copy', sections?.why_this_matters || fallbackSummary);
  setText('looking-copy', sections?.what_you_are_looking_at || fallbackSummary);
  setText('story-copy', sections?.the_story || fallbackSummary);

  const meta = [
    [currentLang === 'ko' ? '지정' : 'Designation', currentHero.designation],
    [currentLang === 'ko' ? '시대' : 'Period', currentLang === 'ko' ? currentHero.period_ko : currentHero.period],
    [currentLang === 'ko' ? '재질' : 'Medium', currentLang === 'ko' ? currentHero.medium_ko : currentHero.medium],
    [
      currentLang === 'ko' ? '크기' : 'Size',
      currentHero.size || currentHero.dimensions || '—',
    ],
    [currentLang === 'ko' ? '소장처' : 'Location', currentLang === 'ko' ? currentHero.location_ko : currentHero.location],
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

/** Wire download / playground / github buttons once we know the hero id + .hgl text. */
function wireSourceButtons(entry, hglText) {
  const heroId = entry.id;
  const filename = `${heroId}.hgl`;
  const fileEl = document.getElementById('hgl-filename');
  if (fileEl) fileEl.textContent = `📜 ${filename}`;

  // Try playground deep-link with ?code=<base64>; harmless if unsupported (still navigates).
  let playgroundHref = PLAYGROUND_URL;
  try {
    const encoded = btoa(unescape(encodeURIComponent(hglText)));
    playgroundHref = `${PLAYGROUND_URL}?code=${encodeURIComponent(encoded)}`;
  } catch (_) {
    // fall back to bare playground
  }

  // Use a Blob URL for download (works regardless of host path).
  const blob = new Blob([hglText], { type: 'text/plain;charset=utf-8' });
  const blobUrl = URL.createObjectURL(blob);

  const githubHref = `${GITHUB_BLOB_PREFIX}artifacts/heroes/${filename}`;

  for (const id of ['cta-playground', 'cta-playground-2']) {
    const el = document.getElementById(id);
    if (el) el.href = playgroundHref;
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

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('lang-toggle')?.addEventListener('click', () => {
    currentLang = currentLang === 'ko' ? 'en' : 'ko';
    renderLanguage();
  });
  loadHero();
});

'use strict';

const HERO_INDEX_URL = './data/heroes/index.json';
let currentLang = 'en';
let currentHero = null;
let currentIndex = null;

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
  const escaped = escapeHtml(text);
  return escaped
    .split('\n')
    .map((line) => {
      if (/^[ \t]*\/\//.test(line)) return `<span class="cm">${line}</span>`;
      return line
        .replace(/(^|[^\p{L}\p{N}_])(구조|문자열|정수|부울|목록|날짜|실수|구현|함수|변수|출력|형식)(?=[^\p{L}\p{N}_]|$)/gu, '$1<span class="kw">$2</span>')
        .replace(/(^[ \t]*)([\p{L}\p{N}_]+)(?=:(?!\/\/))/gu, '$1<span class="prop">$2</span>')
        .replace(/&quot;[^\n]*?&quot;/g, '<span class="str">$&</span>');
    })
    .join('\n');
}

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text || '';
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

  setText('hero-title', currentLang === 'ko' ? currentHero.name_ko : currentHero.name_en);
  setText('hero-subtitle', currentLang === 'ko' ? currentHero.name_en : currentHero.name_ko);
  setText('hero-room', currentHero.room);
  setText('hero-hook', currentHero.hook);

  const sections = currentLang === 'ko' ? currentHero.sections_ko : currentHero.sections;
  setText('why-copy', sections?.why_this_matters || currentHero.summary_ko || currentHero.summary_en);
  setText('looking-copy', sections?.what_you_are_looking_at || currentHero.summary_ko || currentHero.summary_en);
  setText('story-copy', sections?.the_story || currentHero.summary_ko || currentHero.summary_en);

  const meta = [
    [currentLang === 'ko' ? '지정' : 'Designation', currentHero.designation],
    [currentLang === 'ko' ? '시대' : 'Period', currentLang === 'ko' ? currentHero.period_ko : currentHero.period],
    [currentLang === 'ko' ? '재질' : 'Medium', currentLang === 'ko' ? currentHero.medium_ko : currentHero.medium],
    [currentLang === 'ko' ? '소장처' : 'Location', currentLang === 'ko' ? currentHero.location_ko : currentHero.location],
  ];
  const metaEl = document.getElementById('hero-meta');
  if (metaEl) {
    metaEl.innerHTML = meta.map(([k, v]) => `<div><dt>${escapeHtml(k)}</dt><dd>${escapeHtml(v || '')}</dd></div>`).join('');
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
  const pos = heroes.findIndex((hero) => hero.id === heroId);
  const prev = heroes[(pos - 1 + heroes.length) % heroes.length];
  const next = heroes[(pos + 1) % heroes.length];
  nav.innerHTML = `
    ${prev ? `<a href="hero.html?id=${encodeURIComponent(prev.id)}">← ${escapeHtml(prev.name_en)}</a>` : ''}
    ${next ? `<a href="hero.html?id=${encodeURIComponent(next.id)}">${escapeHtml(next.name_en)} →</a>` : ''}
  `;
}

async function loadHero() {
  try {
    currentIndex = await fetchJson(HERO_INDEX_URL);
    const heroId = resolveId(currentIndex);
    const entry = (currentIndex.heroes || []).find((hero) => hero.id === heroId);
    if (!entry) throw new Error(`Unknown hero id: ${heroId}`);
    currentHero = await fetchJson(entry.data_file);

    const img = document.getElementById('hero-image');
    const detail = document.getElementById('detail-image');
    const image = currentHero.images?.[0];
    if (img) {
      img.src = currentHero.cover_image;
      img.alt = currentHero.name_en;
    }
    if (detail) {
      detail.src = image?.path || currentHero.cover_image;
      detail.alt = currentHero.name_en;
    }
    setText('image-credit', image ? `${image.credit} · ${image.license}` : '');
    setText('license-line', image ? `${image.license} — ${image.credit} (${image.source_url})` : '');

    const hgl = await fetchText(currentHero.hgl_path);
    const code = document.getElementById('hero-hgl');
    if (code) code.innerHTML = highlightCode(hgl);

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

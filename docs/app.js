'use strict';

// ── Constants ──────────────────────────────────────────────────────────────
const MANIFEST_URL = './manifest.json';

// ── State ──────────────────────────────────────────────────────────────────
let currentLang = 'ko';  // 'ko' | 'en'

// ── Stubs (T13/T14에서 구현됨) ────────────────────────────────────────────

/**
 * T12에서 생성될 manifest.json을 페치한다.
 * TODO: T13에서 구현 — return await fetch(MANIFEST_URL).then(r => r.json())
 */
async function loadManifest() {
  // TODO: T13에서 구현
}

/**
 * artifact 배열을 받아 #card-grid에 카드를 렌더링한다.
 * @param {Array} artifacts - manifest.json의 artifacts 배열
 * TODO: T13에서 구현
 */
function renderCards(artifacts) {
  // TODO: T13에서 구현
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

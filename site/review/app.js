/**
 * study-vault 复习引擎（纯前端版）
 * SM-2 算法 — 单源真理
 * localStorage 自动保存 — 关页不丢
 * 结果导出 / GitHub API 直写
 */

// ═══════════════════════════════════════════════
// SM-2 算法（单源真理 — Python 版只消费此结果）
// ═══════════════════════════════════════════════

function sm2Next(interval, ease, rating) {
  if (rating < 3) {
    interval = 1;
  } else {
    if (interval === 0) interval = 1;
    else if (interval === 1) interval = 6;
    else interval = Math.round(interval * ease);
    ease = ease + (0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02));
    ease = Math.max(1.3, ease);
  }
  const next = new Date();
  next.setDate(next.getDate() + interval);
  return {
    interval,
    ease: Math.round(ease * 100) / 100,
    nextReview: next.toISOString().split('T')[0],
  };
}

// ═══════════════════════════════════════════════
// 卡片存储
// ═══════════════════════════════════════════════

const LS_KEY = 'study_vault_review_session';

class CardStore {
  constructor() {
    this.allCards = [];       // 全量卡片
    this.dueCards = [];        // 本次待复习
    this.results = {};         // cardId → { rating, interval, ease, nextReview }
    this.currentIndex = 0;     // 当前卡索引
    this.isComplete = false;   // 是否完成
    this._restoreSession();
  }

  async load() {
    const resp = await fetch('../data/cards.json');
    const data = await resp.json();
    this.allCards = data.cards;
    this.dueCards = this._getDueCards(data.cards);
    // 如果有未完成的 session，恢复
    if (this._sessionId && this.currentIndex > 0) {
      // 检查数据是否匹配（用 session 的 id 列表）
      const sessionIds = this._sessionIds || [];
      const currentDueIds = this.dueCards.map(c => c.id).sort().join(',');
      if (sessionIds.sort().join(',') !== currentDueIds) {
        // 卡片池变了，清除旧 session
        this._clearSession();
      } else {
        // 恢复进度：跳过已评分的卡
        const remaining = this.dueCards.filter(c => !this.results[c.id]);
        this.dueCards = remaining;
        this.currentIndex = 0;
        return { restored: true, total: this._sessionTotal, completed: Object.keys(this.results).length };
      }
    }
    this.currentIndex = 0;
    this.isComplete = false;
    return { restored: false, total: this.dueCards.length, completed: 0 };
  }

  get currentCard() {
    return this.dueCards[this.currentIndex] || null;
  }

  get totalDue() { return this.dueCards.length; }

  get completedCount() { return Object.keys(this.results).length; }

  recordRating(rating) {
    const card = this.currentCard;
    if (!card) return null;

    const result = sm2Next(card.interval || 0, card.ease || 2.5, rating);
    result.cardId = card.id;
    result.domain = card.domain;
    result.q = card.q;
    result.a = card.a;
    result.rating = rating;
    result.lastReviewed = new Date().toISOString().split('T')[0];

    this.results[card.id] = result;
    this.currentIndex++;

    this._saveSession();

    if (this.currentIndex >= this.dueCards.length) {
      this.isComplete = true;
    }

    return result;
  }

  exportResults() {
    return {
      version: 1,
      exported: new Date().toISOString().split('T')[0],
      totalReviewed: Object.keys(this.results).length,
      results: Object.values(this.results),
    };
  }

  // ── 筛选到期卡片 ──

  _getDueCards(cards) {
    const today = new Date().toISOString().split('T')[0];
    return cards
      .filter(c => (c.next_review || today) <= today)
      .sort((a, b) => (a.next_review || '').localeCompare(b.next_review || ''));
  }

  // ── localStorage 持久化 ──

  _sessionId() {
    return this._sid || (this._sid = 'sess_' + Date.now());
  }

  _saveSession() {
    const data = {
      sessionId: this._sessionId(),
      timestamp: Date.now(),
      total: this.totalDue,
      cardIds: this.dueCards.map(c => c.id),
      results: this.results,
      currentIndex: this.currentIndex,
    };
    try {
      localStorage.setItem(LS_KEY, JSON.stringify(data));
    } catch (e) {
      // localStorage 满或禁用，静默失败
    }
  }

  _restoreSession() {
    try {
      const raw = localStorage.getItem(LS_KEY);
      if (!raw) return;
      const data = JSON.parse(raw);
      // 只恢复 1 小时内的 session
      if (Date.now() - (data.timestamp || 0) > 3600000) {
        localStorage.removeItem(LS_KEY);
        return;
      }
      this._sid = data.sessionId;
      this._sessionIds = data.cardIds || [];
      this._sessionTotal = data.total || 0;
      this.results = data.results || {};
      this.currentIndex = data.currentIndex || 0;
    } catch (e) {
      // 解析失败，忽略
    }
  }

  _clearSession() {
    this.results = {};
    this.currentIndex = 0;
    this._sid = null;
    this._sessionIds = null;
    this._sessionTotal = 0;
    localStorage.removeItem(LS_KEY);
  }

  clearCompletedSession() {
    this._clearSession();
  }
}

// ═══════════════════════════════════════════════
// UI
// ═══════════════════════════════════════════════

class ReviewUI {
  constructor(store) {
    this.store = store;
    this.answerRevealed = false;
  }

  init() {
    this._bindElements();
    this.loading(true);
    this.store.load().then(status => {
      this.loading(false);
      if (this.store.totalDue === 0) {
        this._showEmpty();
        return;
      }
      if (status.restored) {
        this._showToast(`已恢复上次复习进度（${status.completed}/${status.total}）`);
      }
      this._showProgress();
      this._showCard();
    }).catch(err => {
      this.loading(false);
      this._showError('加载卡片数据失败：' + err.message);
    });
  }

  _bindElements() {
    this.el = {
      progress: document.getElementById('progress'),
      progressFill: document.getElementById('progress-fill'),
      progressCount: document.getElementById('progress-count'),
      progressLabel: document.getElementById('progress-label'),
      cardContainer: document.getElementById('card-container'),
      domain: document.getElementById('domain'),
      domainBadge: document.getElementById('domain-badge'),
      question: document.getElementById('question'),
      answer: document.getElementById('answer'),
      revealSection: document.getElementById('reveal-section'),
      ratingSection: document.getElementById('rating-section'),
      summarySection: document.getElementById('summary'),
      summaryStats: document.getElementById('summary-stats'),
      summaryActions: document.getElementById('summary-actions'),
      emptyState: document.getElementById('empty-state'),
      loadingEl: document.getElementById('loading'),
      errorEl: document.getElementById('error'),
      toast: document.getElementById('toast'),
    };
    // Reveal
    document.getElementById('reveal-btn').addEventListener('click', () => this._revealAnswer());
    // Rating
    document.querySelectorAll('.rating-btn').forEach(btn => {
      btn.addEventListener('click', () => this._rate(parseInt(btn.dataset.rating)));
    });
    // Keyboard
    document.addEventListener('keydown', (e) => {
      if (e.key === ' ' || e.key === 'Enter') {
        if (!this.answerRevealed) {
          e.preventDefault();
          this._revealAnswer();
        }
      }
      if (this.answerRevealed && e.key >= '0' && e.key <= '5') {
        this._rate(parseInt(e.key));
      }
    });
    // Summary actions
    document.getElementById('download-btn').addEventListener('click', () => this._downloadResults());
    document.getElementById('restart-btn').addEventListener('click', () => this._restart());
  }

  loading(show) {
    this.el.loadingEl.style.display = show ? 'block' : 'none';
    this.el.cardContainer.style.display = show ? 'none' : 'block';
  }

  _showEmpty() {
    this.el.emptyState.style.display = 'block';
    this.el.cardContainer.style.display = 'none';
    this.el.progress.style.display = 'none';
  }

  _showError(msg) {
    this.el.errorEl.textContent = msg;
    this.el.errorEl.style.display = 'block';
  }

  _showProgress() {
    const total = this.store.totalDue;
    const done = this.store.completedCount;
    const pct = total > 0 ? (done / total * 100) : 0;
    this.el.progressFill.style.width = pct + '%';
    this.el.progressCount.textContent = `${done} / ${total}`;
    this.el.progressLabel.textContent = pct < 50 ? '加油 💪' : pct < 100 ? '稳住 👍' : '即将完成 🎯';
  }

  _showCard() {
    const card = this.store.currentCard;
    if (!card) { this._finish(); return; }

    this.answerRevealed = false;

    // Domain badge
    this.el.domain.textContent = card.domain;
    this.el.domainBadge.className = 'domain-badge domain-' + card.domain;

    // Question
    this.el.question.textContent = card.q;

    // Answer (hidden)
    this.el.answer.textContent = card.a;
    this.el.answer.classList.remove('visible');

    // Show reveal, hide rating
    this.el.revealSection.style.display = 'block';
    this.el.ratingSection.classList.remove('visible');

    // Progress
    this._showProgress();
  }

  _revealAnswer() {
    if (this.answerRevealed) return;
    this.answerRevealed = true;
    this.el.answer.classList.add('visible');
    this.el.revealSection.style.display = 'none';
    this.el.ratingSection.classList.add('visible');
  }

  _rate(rating) {
    if (!this.answerRevealed) return;

    // Visual feedback
    document.querySelectorAll('.rating-btn').forEach(b => b.classList.remove('selected'));
    document.querySelector(`.rating-btn[data-rating="${rating}"]`).classList.add('selected');

    const result = this.store.recordRating(rating);
    if (!result) return;

    // Brief pause to show selection
    setTimeout(() => {
      this._showCard();
    }, 200);
  }

  _finish() {
    const results = this.store.exportResults();
    const total = results.totalReviewed;
    const forgotten = results.results.filter(r => r.rating < 3).length;
    const remembered = total - forgotten;
    const rate = total > 0 ? Math.round(remembered / total * 100) : 0;

    // Hide card, show summary
    document.getElementById('card-area').style.display = 'none';
    this.el.summarySection.classList.add('visible');

    // Stats
    this.el.summaryStats.innerHTML = `
      <div class="stat-box">
        <div class="stat-value orange">${total}</div>
        <div class="stat-label">复习卡片</div>
      </div>
      <div class="stat-box">
        <div class="stat-value green">${remembered}</div>
        <div class="stat-label">已记住</div>
      </div>
      <div class="stat-box">
        <div class="stat-value red">${forgotten}</div>
        <div class="stat-label">需回顾</div>
      </div>
    `;

    // Update progress bar to 100%
    this.el.progressFill.style.width = '100%';
    this.el.progressCount.textContent = `${total} / ${total}`;
    this.el.progressLabel.textContent = '复习完成 🎉';

    // Save results summary to localStorage for the dashboard
    try {
      const today = new Date().toISOString().split('T')[0];
      const history = JSON.parse(localStorage.getItem('study_vault_review_history') || '{}');
      history[today] = { total, remembered, forgotten, rate };
      localStorage.setItem('study_vault_review_history', JSON.stringify(history));
    } catch (e) {}

    this._showToast(`复习完成！正确率 ${rate}%`);

    // Clear session from localStorage
    this.store.clearCompletedSession();
  }

  _downloadResults() {
    const results = this.store.exportResults();
    const blob = new Blob([JSON.stringify(results, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `review-results-${results.exported}.json`;
    a.click();
    URL.revokeObjectURL(url);
    this._showToast('已下载结果文件，拖到项目根目录后运行 review.py import --results');
  }

  _restart() {
    // Reload the page to start fresh
    window.location.reload();
  }

  _showToast(msg) {
    this.el.toast.textContent = msg;
    this.el.toast.classList.add('visible');
    clearTimeout(this._toastTimer);
    this._toastTimer = setTimeout(() => {
      this.el.toast.classList.remove('visible');
    }, 3000);
  }
}

// ═══════════════════════════════════════════════
// 启动
// ═══════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
  const store = new CardStore();
  const ui = new ReviewUI(store);
  ui.init();
});

// 暴露给全局，方便调试
window.__review = { CardStore, ReviewUI, sm2Next };

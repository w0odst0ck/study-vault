/**
 * study-vault 复习引擎 v2（分批 + 智能推荐）
 * SM-2 算法 + 分批续接 + 优先级排序
 * localStorage 自动保存 — 关页不丢
 */

// ═══ 常量 ═══
const BATCH_OPTIONS = [10, 20, 50, 0];  // 0 = 全部
const LS_KEY = 'study_vault_session';
const HIST_KEY = 'study_vault_review_history';

// ═══════════════════════════════════════════════
// SM-2 算法
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

class CardStore {
  constructor() {
    // 全量数据
    this.allCards = [];         // 所有卡片
    this.dueCards = [];         // 今日到期（排序后）

    // 批次控制
    this.batchSize = 10;        // 当前批大小
    this.cursor = 0;            // 当前批在 dueCards 中的起始偏移

    // 结果
    this.results = {};          // cardId → { rating, interval, ease, nextReview }
    this.currentIndex = 0;      // 当前在批内的索引

    // 统计
    this.allDueCount = 0;       // 总到期数
    this.isComplete = false;    // 全部刷完
    this._restoreSession();
  }

  /** 加载卡片数据 */
  async load() {
    const resp = await fetch('../data/cards.json');
    const data = await resp.json();
    this.allCards = data.cards || [];
    this.dueCards = this._getSortedDue(this.allCards);
    this.allDueCount = this.dueCards.length;

    // 恢复未完成 session
    if (this._sid && this.currentIndex > 0) {
      const sessionIds = this._sessionIds || [];
      const currentIds = this.dueCards.map(c => c.id).sort().join(',');
      if (sessionIds.sort().join(',') !== currentIds) {
        this._clearSession();
      } else {
        const remaining = this.dueCards.slice(this.cursor + this.currentIndex);
        const remainingIds = remaining.map(c => c.id);
        const newSlice = [];
        let found = 0;
        for (const c of this.dueCards) {
          if (remainingIds.includes(c.id) && found < this.batchSize) {
            newSlice.push(c);
            found++;
          }
        }
        // Recalculate cursor
        const doneCount = Object.keys(this.results).length;
        this.cursor = doneCount;
        this.currentIndex = 0;
        return {
          restored: true,
          total: this._sessionTotal,
          completed: doneCount,
        };
      }
    }

    // 新 session
    this.cursor = 0;
    this.currentIndex = 0;
    this.results = {};
    this.isComplete = false;
    return { restored: false, total: this.allDueCount, completed: 0 };
  }

  /** 获取当前批的卡片 */
  get batchCards() {
    return this.dueCards.slice(this.cursor, this.cursor + this.batchSize);
  }

  /** 当前批有几张 */
  get batchCount() {
    return Math.min(this.batchSize, this.allDueCount - this.cursor);
  }

  /** 当前批内还剩几张（含当前卡） */
  get batchRemaining() {
    return this.batchCount - this.currentIndex;
  }

  /** 当前卡 */
  get currentCard() {
    const batch = this.batchCards;
    return batch[this.currentIndex] || null;
  }

  /** 当前批已完成数 */
  get batchDone() {
    return this.currentIndex;
  }

  /** 全局已完成数 */
  get totalDone() {
    return this.cursor + this.currentIndex;
  }

  /** 全部到期数 */
  get totalDue() { return this.allDueCount; }

  /** 当前批之外还有到期卡 */
  get hasMoreDue() {
    return this.cursor + this.batchSize < this.allDueCount;
  }

  /** 当前批是否已完成 */
  get isBatchComplete() {
    return this.currentIndex >= this.batchCount && !this.isComplete;
  }

  /** 所有到期卡是否都已刷完 */
  get allDone() {
    return this.totalDone >= this.allDueCount;
  }

  /** 打分 & 记录 */
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

    // 检查批次/全局是否完成
    if (this.currentIndex >= this.batchCount) {
      if (this.cursor + this.batchSize >= this.allDueCount) {
        this.isComplete = true;
      }
    }

    return result;
  }

  /** 续接：开始下一批 */
  extendBatch(overrideSize) {
    const nextSize = overrideSize || this.batchSize;
    // 前进 cursor
    this.cursor += this.batchCount;
    this.currentIndex = 0;
    // 如果指定了新大小，更新
    if (overrideSize) {
      this.batchSize = overrideSize;
    }
    // 如果已经到末尾
    if (this.cursor >= this.allDueCount) {
      this.isComplete = true;
    }
    this._saveSession();
  }

  /** 改变批大小（仅对新 session 生效） */
  setBatchSize(size) {
    this.batchSize = size > 0 ? size : this.allDueCount;
  }

  /** 导出结果 */
  exportResults() {
    return {
      version: 1,
      exported: new Date().toISOString().split('T')[0],
      totalReviewed: Object.keys(this.results).length,
      results: Object.values(this.results),
    };
  }

  /** 获取本批统计 */
  getBatchStats() {
    const batchIds = this.batchCards.map(c => c.id);
    const batchResults = batchIds
      .map(id => this.results[id])
      .filter(Boolean);
    const total = batchResults.length;
    const forgotten = batchResults.filter(r => r.rating < 3).length;
    const remembered = total - forgotten;
    const rate = total > 0 ? Math.round(remembered / total * 100) : 0;

    // 按领域统计遗忘
    const domainStats = {};
    batchResults.forEach(r => {
      const d = r.domain || '?';
      if (!domainStats[d]) domainStats[d] = { total: 0, forgotten: 0 };
      domainStats[d].total++;
      if (r.rating < 3) domainStats[d].forgotten++;
    });

    return { total, remembered, forgotten, rate, domainStats };
  }

  /** 获取全局统计 */
  getAllStats() {
    const results = Object.values(this.results);
    const total = results.length;
    const forgotten = results.filter(r => r.rating < 3).length;
    const remembered = total - forgotten;
    const rate = total > 0 ? Math.round(remembered / total * 100) : 0;
    return { total, remembered, forgotten, rate };
  }

  // ── 排序：遗忘率高的优先 ──

  _getSortedDue(cards) {
    const today = new Date().toISOString().split('T')[0];
    const due = cards
      .filter(c => (c.next_review || today) <= today)
      .sort((a, b) => {
        // 1. ease 越低越优先（遗忘倾向高）
        const easeA = a.ease || 2.5;
        const easeB = b.ease || 2.5;
        if (easeA !== easeB) return easeA - easeB;
        // 2. 过期越久越优先
        return ((a.next_review || today).localeCompare(b.next_review || today));
      });
    return due;
  }

  // ── localStorage 持久化 ──

  _sessionId() {
    return this._sid || (this._sid = 'sess_' + Date.now());
  }

  _saveSession() {
    const data = {
      sessionId: this._sessionId(),
      timestamp: Date.now(),
      total: this.allDueCount,
      batchSize: this.batchSize,
      cursor: this.cursor,
      cardIds: this.dueCards.map(c => c.id),
      results: this.results,
      currentIndex: this.currentIndex,
    };
    try {
      localStorage.setItem(LS_KEY, JSON.stringify(data));
    } catch (e) { /* ignored */ }
  }

  _restoreSession() {
    try {
      const raw = localStorage.getItem(LS_KEY);
      if (!raw) return;
      const data = JSON.parse(raw);
      if (Date.now() - (data.timestamp || 0) > 3600000) {
        localStorage.removeItem(LS_KEY);
        return;
      }
      this._sid = data.sessionId;
      this._sessionIds = data.cardIds || [];
      this._sessionTotal = data.total || 0;
      this.results = data.results || {};
      this.currentIndex = data.currentIndex || 0;
      this.cursor = data.cursor || 0;
      this.batchSize = data.batchSize || 10;
    } catch (e) { /* ignored */ }
  }

  _clearSession() {
    this.results = {};
    this.currentIndex = 0;
    this.cursor = 0;
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
    this.recommendations = {
      great: '状态不错 👍 正确率很高，再来一组巩固？',
      good: '继续加油 💪  趁热打铁再来一批',
      meh: '有几张不太熟 🤔 可以先把笔记过一遍再继续',
      poor: '遗忘有点多 ⚠️ 建议先看笔记再继续复习',
    };
  }

  init() {
    this._bindElements();
    this._initBatchSelector();
    this.loading(true);
    this.store.load().then(status => {
      this.loading(false);
      if (this.store.totalDue === 0) {
        this._showEmpty();
        return;
      }
      if (status.restored) {
        this._showToast(`已恢复上次进度（${status.completed}/${status.total}）`);
      }
      this._showProgress();
      this._startBatch();
    }).catch(err => {
      this.loading(false);
      this._showError('加载数据失败：' + err.message);
    });
  }

  _bindElements() {
    this.el = {
      // 批选择器
      batchSelector: document.getElementById('batch-selector'),
      // 进度
      progress: document.getElementById('progress'),
      progressFill: document.getElementById('progress-fill'),
      progressCount: document.getElementById('progress-count'),
      progressGlobal: document.getElementById('progress-global'),
      progressLabel: document.getElementById('progress-label'),
      // 卡片
      cardContainer: document.getElementById('card-container'),
      cardArea: document.getElementById('card-area'),
      domain: document.getElementById('domain'),
      domainBadge: document.getElementById('domain-badge'),
      question: document.getElementById('question'),
      answer: document.getElementById('answer'),
      revealSection: document.getElementById('reveal-section'),
      ratingSection: document.getElementById('rating-section'),
      // 批次完成
      batchComplete: document.getElementById('batch-complete'),
      batchStats: document.getElementById('batch-stats'),
      batchDomainBreakdown: document.getElementById('batch-domain-breakdown'),
      batchRecommendation: document.getElementById('batch-recommendation'),
      // 总完成
      summary: document.getElementById('summary'),
      summaryStats: document.getElementById('summary-stats'),
      // 工具
      emptyState: document.getElementById('empty-state'),
      loadingEl: document.getElementById('loading'),
      errorEl: document.getElementById('error'),
      toast: document.getElementById('toast'),
    };

    // Button events
    document.getElementById('reveal-btn').addEventListener('click', () => this._revealAnswer());
    document.querySelectorAll('.rating-btn').forEach(btn => {
      btn.addEventListener('click', () => this._rate(parseInt(btn.dataset.rating)));
    });
    document.getElementById('next-batch-btn').addEventListener('click', () => this._nextBatch());
    document.getElementById('next-all-btn').addEventListener('click', () => this._nextAll());
    document.getElementById('stop-btn').addEventListener('click', () => this._stopReview());
    document.getElementById('download-btn').addEventListener('click', () => this._downloadResults());
    document.getElementById('restart-btn').addEventListener('click', () => this._restart());

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
  }

  _initBatchSelector() {
    const sel = this.el.batchSelector;
    sel.innerHTML = BATCH_OPTIONS.map(v => {
      const label = v === 0 ? '全部' : `${v} 张/批`;
      return `<option value="${v}" ${v === 10 ? 'selected' : ''}>${label}</option>`;
    }).join('');
    sel.addEventListener('change', () => {
      const val = parseInt(sel.value);
      this.store.setBatchSize(val);
    });
  }

  // ── 批次完成 / 续接 ──

  _startBatch() {
    // 隐藏批次完成、总完成
    this.el.batchComplete.style.display = 'none';
    this.el.summary.classList.remove('visible');
    this.el.cardArea.style.display = 'block';
    this._showCard();
  }

  _nextBatch() {
    this.store.extendBatch();
    // 如果 extendBatch 后发现全部刷完了
    if (this.store.isComplete) {
      this._finishAll();
    } else {
      this._startBatch();
    }
  }

  _nextAll() {
    // 一次性刷完全部剩余
    this.store.extendBatch(this.store.allDueCount - this.store.cursor);
    this._startBatch();
  }

  _stopReview() {
    this._finishAll();
  }

  // ── 卡片展示 ──

  _showCard() {
    // 检查批次边界
    if (this.store.isBatchComplete || this.store.allDone) {
      if (this.store.allDone) {
        this._finishAll();
      } else {
        this._showBatchComplete();
      }
      return;
    }

    const card = this.store.currentCard;
    if (!card) {
      if (this.store.allDone) {
        this._finishAll();
      } else {
        this._showBatchComplete();
      }
      return;
    }

    this.answerRevealed = false;
    this.el.domain.textContent = card.domain;
    this.el.domainBadge.className = 'domain-badge domain-' + card.domain;
    this.el.question.textContent = card.q;
    this.el.answer.textContent = card.a;
    this.el.answer.classList.remove('visible');
    this.el.revealSection.style.display = 'block';
    this.el.ratingSection.classList.remove('visible');
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
    document.querySelectorAll('.rating-btn').forEach(b => b.classList.remove('selected'));
    document.querySelector(`.rating-btn[data-rating="${rating}"]`).classList.add('selected');
    const result = this.store.recordRating(rating);
    if (!result) return;
    setTimeout(() => this._showCard(), 200);
  }

  // ── 批次完成插页 ──

  _showBatchComplete() {
    this.el.cardArea.style.display = 'none';
    this.el.summary.classList.remove('visible');

    const stats = this.store.getBatchStats();
    const globalStats = this.store.getAllStats();

    // 批次统计
    this.el.batchStats.innerHTML = `
      <div class="stat-box">
        <div class="stat-value orange">${stats.total}</div>
        <div class="stat-label">本批</div>
      </div>
      <div class="stat-box">
        <div class="stat-value green">${stats.remembered}</div>
        <div class="stat-label">已记住</div>
      </div>
      <div class="stat-box">
        <div class="stat-value red">${stats.forgotten}</div>
        <div class="stat-label">需回顾</div>
      </div>
    `;

    // 领域明细
    const domains = Object.entries(stats.domainStats);
    this.el.batchDomainBreakdown.innerHTML = domains.map(([d, s]) => {
      const pct = s.forgotten > 0 ? `<span class="domain-forgotten">✗${s.forgotten}</span>` : '';
      return `<span class="domain-chip">${d} ${s.total}张 ${pct}</span>`;
    }).join(' ');

    // 智能推荐
    let recText;
    if (stats.rate >= 90) {
      recText = this.recommendations.great;
    } else if (stats.rate >= 70) {
      recText = this.recommendations.good;
    } else if (stats.rate >= 50) {
      recText = this.recommendations.meh;
    } else {
      recText = this.recommendations.poor;
    }
    this.el.batchRecommendation.textContent = recText;

    // 按钮文案
    const remaining = this.store.allDueCount - this.store.totalDone;
    document.getElementById('next-batch-btn').innerHTML = `▶ 再来 ${Math.min(this.store.batchSize, remaining)} 张`;
    if (remaining <= this.store.batchSize) {
      document.getElementById('next-all-btn').textContent = `▶ 刷完剩余 ${remaining} 张`;
    } else {
      document.getElementById('next-all-btn').textContent = `▶ 刷完全部 (${remaining} 张)`;
    }

    // 更新进度
    this._showProgress();
    this.el.batchComplete.style.display = 'block';
  }

  // ── 全部完成 ──

  _finishAll() {
    const results = this.store.exportResults();
    const total = results.totalReviewed;
    const forgotten = results.results.filter(r => r.rating < 3).length;
    const remembered = total - forgotten;
    const rate = total > 0 ? Math.round(remembered / total * 100) : 0;

    this.el.cardArea.style.display = 'none';
    this.el.batchComplete.style.display = 'none';
    this.el.summary.classList.add('visible');

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

    this.el.progressFill.style.width = '100%';
    this.el.progressCount.textContent = `${total} / ${total}`;
    this.el.progressGlobal.textContent = `全部完成 🎉`;
    this.el.progressLabel.textContent = '今日复习完成';

    // 保存历史
    try {
      const today = new Date().toISOString().split('T')[0];
      const history = JSON.parse(localStorage.getItem(HIST_KEY) || '{}');
      history[today] = { total, remembered, forgotten, rate };
      localStorage.setItem(HIST_KEY, JSON.stringify(history));
    } catch (e) { /* ignored */ }

    this._showToast(`全部完成！正确率 ${rate}%`);
    this.store.clearCompletedSession();
  }

  // ── 进度 ──

  _showProgress() {
    const batchDone = this.store.batchDone;
    const batchTotal = this.store.batchCount > 0 ? this.store.batchCount : 1;
    const pct = Math.round(batchDone / batchTotal * 100);

    // 批进度
    this.el.progressFill.style.width = pct + '%';
    if (this.store.isComplete || this.store.allDone) {
      this.el.progressCount.textContent = `${this.store.totalDone} / ${this.store.totalDue}`;
    } else {
      this.el.progressCount.textContent = `${batchDone} / ${batchTotal}`;
    }

    // 全局进度
    const remaining = this.store.totalDue - this.store.totalDone;
    if (this.store.allDone || this.store.isComplete) {
      this.el.progressGlobal.textContent = `全部完成`;
    } else if (remaining > 0) {
      this.el.progressGlobal.textContent = `已复习 ${this.store.totalDone} · 剩余 ${remaining}`;
    } else {
      this.el.progressGlobal.textContent = `今日共 ${this.store.totalDue} 张到期`;
    }

    // 鼓励语
    if (this.store.isComplete) {
      this.el.progressLabel.textContent = '全部完成 🎉';
    } else if (pct < 50) {
      this.el.progressLabel.textContent = '加油 💪';
    } else if (pct < 100) {
      this.el.progressLabel.textContent = '稳住 👍';
    } else {
      this.el.progressLabel.textContent = '即将完成 🎯';
    }
  }

  // ── 工具 ──

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

  _downloadResults() {
    const results = this.store.exportResults();
    const blob = new Blob([JSON.stringify(results, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `review-results-${results.exported}.json`;
    a.click();
    URL.revokeObjectURL(url);
    this._showToast('已下载结果文件');
  }

  _restart() {
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

// ═══ 启动 ═══

document.addEventListener('DOMContentLoaded', () => {
  const store = new CardStore();
  const ui = new ReviewUI(store);
  ui.init();
});

window.__review = { CardStore, ReviewUI, sm2Next };

/**
 * study-vault 复习引擎 v2（分批 + 跨设备同步）
 * SM-2 算法 + 分批续接 + 优先级排序 + GitHub API 云端同步
 * localStorage 持久化 — 关页不丢 · 跨设备同步
 */

// ═══ 常量 ═══
const BATCH_OPTIONS = [10, 20, 50, 0];  // 0 = 全部
const LS_KEY = 'study_vault_session';
const HIST_KEY = 'study_vault_review_history';
const PERSIST_KEY = 'study_vault_persisted';  // 持久化卡片状态 (version 2)
const PAT_KEY = 'study_vault_gh_pat';         // GitHub PAT
const SCHEMA_VER = 2;

const GITHUB_REPO = 'w0odst0ck/study-vault';
const GITHUB_API = 'https://api.github.com';

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
// 工具：Unicode 安全的 base64
// ═══════════════════════════════════════════════

function base64Encode(str) {
  const bytes = new TextEncoder().encode(str);
  const bin = Array.from(bytes, b => String.fromCharCode(b)).join('');
  return btoa(bin);
}

function base64Decode(b64) {
  const bin = atob(b64);
  const bytes = new Uint8Array(Array.from(bin, c => c.charCodeAt(0)));
  return new TextDecoder().decode(bytes);
}

// ═══════════════════════════════════════════════
// 卡片存储
// ═══════════════════════════════════════════════

class CardStore {
  constructor() {
    // 全量数据
    this.allCards = [];
    this.dueCards = [];

    // 批次控制
    this.batchSize = 10;
    this.cursor = 0;
    this.currentIndex = 0;

    // 结果
    this.results = {};

    // 统计
    this.allDueCount = 0;
    this.isComplete = false;

    // 持久化数据（早于 session）
    this._persisted = {};  // cardId → { interval, ease, next_review, last_reviewed }

    this._loadPersisted();
    this._restoreSession();
  }

  // ── 持久化层（localStorage） ──

  _loadPersisted() {
    try {
      const raw = localStorage.getItem(PERSIST_KEY);
      if (!raw) return;
      const data = JSON.parse(raw);
      // Schema 版本检查
      if (data.schema !== SCHEMA_VER) {
        localStorage.removeItem(PERSIST_KEY);
        return;
      }
      this._persisted = data.cards || {};
    } catch (e) { /* 格式错误直接丢弃 */ }
  }

  _savePersisted() {
    // 只保留最新状态，不保留历史
    const cards = {};
    for (const [id, result] of Object.entries(this.results)) {
      cards[id] = {
        interval: result.interval,
        ease: result.ease,
        next_review: result.nextReview,
        last_reviewed: result.lastReviewed,
        rating: result.rating,
      };
    }
    try {
      const data = {
        schema: SCHEMA_VER,
        updated: new Date().toISOString(),
        cards,
      };
      localStorage.setItem(PERSIST_KEY, JSON.stringify(data));
    } catch (e) { /* ignored */ }
  }

  /** 清理过期卡片（cards.json 更新后删除的卡） */
  _cleanupPersisted(allCardIds) {
    const oldKeys = Object.keys(this._persisted);
    let changed = false;
    for (const id of oldKeys) {
      if (!allCardIds.has(id)) {
        delete this._persisted[id];
        changed = true;
      }
    }
    if (changed) {
      try {
        localStorage.setItem(PERSIST_KEY, JSON.stringify({
          schema: SCHEMA_VER,
          updated: new Date().toISOString(),
          cards: this._persisted,
        }));
      } catch (e) { /* ignored */ }
    }
  }

  // ── 加载 + 合并持久化数据 ──

  async load() {
    const resp = await fetch('../data/cards.json');
    const data = await resp.json();
    this.allCards = (data.cards || []).map(c => {
      // 合并持久化的 SM-2 状态
      const p = this._persisted[c.id];
      if (p) {
        c.interval = p.interval;
        c.ease = p.ease;
        c.next_review = p.next_review;
        c.last_reviewed = p.last_reviewed;
      }
      return c;
    });

    // 清理过期持久化数据
    const allIds = new Set(this.allCards.map(c => c.id));
    this._cleanupPersisted(allIds);

    this.dueCards = this._getSortedDue(this.allCards);
    this.allDueCount = this.dueCards.length;

    // 恢复未完成 session
    if (this._sid && this.currentIndex > 0) {
      const sessionIds = this._sessionIds || [];
      const currentIds = this.dueCards.map(c => c.id).sort().join(',');
      if (sessionIds.sort().join(',') !== currentIds) {
        this._clearSession();
      } else {
        const doneCount = this.totalDone;
        this.cursor = doneCount;
        this.currentIndex = 0;
        return {
          restored: true,
          total: this._sessionTotal,
          completed: doneCount,
        };
      }
    }

    this.cursor = 0;
    this.currentIndex = 0;
    this.results = {};
    this.isComplete = false;
    return { restored: false, total: this.allDueCount, completed: 0 };
  }

  // ── 批处理 ──

  get batchCards() {
    return this.dueCards.slice(this.cursor, this.cursor + this.batchSize);
  }

  get batchCount() {
    return Math.min(this.batchSize, this.allDueCount - this.cursor);
  }

  get batchRemaining() {
    return this.batchCount - this.currentIndex;
  }

  get currentCard() {
    const batch = this.batchCards;
    return batch[this.currentIndex] || null;
  }

  get batchDone() {
    return this.currentIndex;
  }

  get totalDone() {
    return this.cursor + this.currentIndex;
  }

  get totalDue() { return this.allDueCount; }

  get hasMoreDue() {
    return this.cursor + this.batchSize < this.allDueCount;
  }

  get isBatchComplete() {
    return this.currentIndex >= this.batchCount && !this.isComplete;
  }

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

    if (this.currentIndex >= this.batchCount) {
      if (this.cursor + this.batchSize >= this.allDueCount) {
        this.isComplete = true;
      }
    }

    return result;
  }

  extendBatch(overrideSize) {
    const nextSize = overrideSize || this.batchSize;
    this.cursor += this.batchCount;
    this.currentIndex = 0;
    if (overrideSize) this.batchSize = overrideSize;
    if (this.cursor >= this.allDueCount) this.isComplete = true;
    this._saveSession();
  }

  setBatchSize(size) {
    this.batchSize = size > 0 ? size : this.allDueCount;
  }

  // ── 持久化存储（每次批完后调用） ──

  persistResults() {
    this._savePersisted();
  }

  // ── GitHub API 云端同步 ──

  /** 是否有已经评分但未同步的结果 */
  get hasUnsyncedResults() {
    return Object.keys(this.results).length > 0;
  }

  /** 最近的同步时间 */
  get lastSyncTime() {
    try {
      const raw = localStorage.getItem(PERSIST_KEY);
      if (!raw) return null;
      return JSON.parse(raw).updated || null;
    } catch { return null; }
  }

  /** 同步到 GitHub */
  async syncToGithub(pat) {
    if (!pat || Object.keys(this.results).length === 0) return { ok: false, error: '没有需要同步的结果' };

    const content = {
      cards: {},
      synced: new Date().toISOString(),
    };

    for (const [id, r] of Object.entries(this.results)) {
      content.cards[id] = {
        interval: r.interval,
        ease: r.ease,
        next_review: r.nextReview,
        last_reviewed: r.lastReviewed,
        rating: r.rating,
      };
    }

    // 1. 先获取文件 SHA（如果存在）
    let sha = null;
    try {
      const getResp = await fetch(
        `${GITHUB_API}/repos/${GITHUB_REPO}/contents/review/sync-results.json?ref=main`,
        { headers: { Authorization: `Bearer ${pat}` } }
      );
      if (getResp.ok) {
        const data = await getResp.json();
        sha = data.sha;
      }
    } catch { /* 新文件，无 SHA */ }

    // 2. 写入文件
    const encoded = base64Encode(JSON.stringify(content, null, 2));
    const body = {
      message: `sync: ${Object.keys(content.cards).length} 张卡片`,
      content: encoded,
      branch: 'main',
    };
    if (sha) body.sha = sha;

    const putResp = await fetch(
      `${GITHUB_API}/repos/${GITHUB_REPO}/contents/review/sync-results.json`,
      {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${pat}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      }
    );

    if (!putResp.ok) {
      const err = await putResp.json().catch(() => ({}));
      return { ok: false, error: err.message || `HTTP ${putResp.status}` };
    }

    return { ok: true, count: Object.keys(content.cards).length };
  }

  // ── 统计 ──

  getBatchStats() {
    const batchIds = this.batchCards.map(c => c.id);
    const batchResults = batchIds.map(id => this.results[id]).filter(Boolean);
    const total = batchResults.length;
    const forgotten = batchResults.filter(r => r.rating < 3).length;
    const remembered = total - forgotten;
    const rate = total > 0 ? Math.round(remembered / total * 100) : 0;

    const domainStats = {};
    batchResults.forEach(r => {
      const d = r.domain || '?';
      if (!domainStats[d]) domainStats[d] = { total: 0, forgotten: 0 };
      domainStats[d].total++;
      if (r.rating < 3) domainStats[d].forgotten++;
    });

    return { total, remembered, forgotten, rate, domainStats };
  }

  getAllStats() {
    const results = Object.values(this.results);
    const total = results.length;
    const forgotten = results.filter(r => r.rating < 3).length;
    const remembered = total - forgotten;
    const rate = total > 0 ? Math.round(remembered / total * 100) : 0;
    return { total, remembered, forgotten, rate };
  }

  // ── 排序 ──

  _getSortedDue(cards) {
    const today = new Date().toISOString().split('T')[0];
    return cards
      .filter(c => (c.next_review || today) <= today)
      .sort((a, b) => {
        const easeA = a.ease || 2.5;
        const easeB = b.ease || 2.5;
        if (easeA !== easeB) return easeA - easeB;
        return ((a.next_review || '').localeCompare(b.next_review || ''));
      });
  }

  // ── localStorage Session ──

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
    try { localStorage.setItem(LS_KEY, JSON.stringify(data)); } catch (e) {}
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
    } catch (e) {}
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
    this.ghPat = localStorage.getItem(PAT_KEY) || '';
    this.isSyncing = false;
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
    this._initSyncPanel();
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
      this._updateSyncStatus();
      this._startBatch();
    }).catch(err => {
      this.loading(false);
      this._showError('加载数据失败：' + err.message);
    });
  }

  _bindElements() {
    this.el = {
      batchSelector: document.getElementById('batch-selector'),
      progress: document.getElementById('progress'),
      progressFill: document.getElementById('progress-fill'),
      progressCount: document.getElementById('progress-count'),
      progressGlobal: document.getElementById('progress-global'),
      progressLabel: document.getElementById('progress-label'),
      cardContainer: document.getElementById('card-container'),
      cardArea: document.getElementById('card-area'),
      domain: document.getElementById('domain'),
      domainBadge: document.getElementById('domain-badge'),
      question: document.getElementById('question'),
      answer: document.getElementById('answer'),
      revealSection: document.getElementById('reveal-section'),
      ratingSection: document.getElementById('rating-section'),
      batchComplete: document.getElementById('batch-complete'),
      batchStats: document.getElementById('batch-stats'),
      batchDomainBreakdown: document.getElementById('batch-domain-breakdown'),
      batchRecommendation: document.getElementById('batch-recommendation'),
      syncBtn: document.getElementById('sync-btn'),
      syncStatus: document.getElementById('sync-status'),
      patInput: document.getElementById('pat-input'),
      patSaveBtn: document.getElementById('pat-save-btn'),
      patConfig: document.getElementById('pat-config'),
      summary: document.getElementById('summary'),
      summaryStats: document.getElementById('summary-stats'),
      emptyState: document.getElementById('empty-state'),
      loadingEl: document.getElementById('loading'),
      errorEl: document.getElementById('error'),
      toast: document.getElementById('toast'),
    };

    document.getElementById('reveal-btn').addEventListener('click', () => this._revealAnswer());
    document.querySelectorAll('.rating-btn').forEach(btn => {
      btn.addEventListener('click', () => this._rate(parseInt(btn.dataset.rating)));
    });
    document.getElementById('next-batch-btn').addEventListener('click', () => { this.store.persistResults(); this._nextBatch(); });
    document.getElementById('next-all-btn').addEventListener('click', () => { this.store.persistResults(); this._nextAll(); });
    document.getElementById('stop-btn').addEventListener('click', () => { this.store.persistResults(); this._stopReview(); });
    document.getElementById('download-btn').addEventListener('click', () => this._downloadResults());
    document.getElementById('restart-btn').addEventListener('click', () => this._restart());
    this.el.syncBtn.addEventListener('click', () => this._doSync());
    this.el.patSaveBtn.addEventListener('click', () => this._savePat());

    document.addEventListener('keydown', (e) => {
      if (e.key === ' ' || e.key === 'Enter') {
        if (!this.answerRevealed) { e.preventDefault(); this._revealAnswer(); }
      }
      if (this.answerRevealed && e.key >= '0' && e.key <= '5') this._rate(parseInt(e.key));
    });
  }

  _initBatchSelector() {
    const sel = this.el.batchSelector;
    sel.innerHTML = BATCH_OPTIONS.map(v => {
      const label = v === 0 ? '全部' : `${v} 张/批`;
      return `<option value="${v}" ${v === 10 ? 'selected' : ''}>${label}</option>`;
    }).join('');
    sel.addEventListener('change', () => this.store.setBatchSize(parseInt(sel.value)));
  }

  _initSyncPanel() {
    if (this.ghPat) {
      this.el.patConfig.style.display = 'none';
    } else {
      this.el.syncBtn.textContent = '🔑 配置 Git Token';
      this.el.syncBtn.disabled = false;
    }
  }

  _savePat() {
    const pat = this.el.patInput.value.trim();
    if (!pat || pat.length < 20) {
      this._showToast('Token 格式不对');
      return;
    }
    this.ghPat = pat;
    localStorage.setItem(PAT_KEY, pat);
    this.el.patConfig.style.display = 'none';
    this.el.syncBtn.textContent = '☁️ 同步到 GitHub';
    this.el.syncBtn.disabled = false;
    this._showToast('Token 已保存');
  }

  _updateSyncStatus() {
    const synced = this.store.hasUnsyncedResults;
    const lastSync = this.store.lastSyncTime;
    if (lastSync) {
      const d = new Date(lastSync);
      this.el.syncStatus.textContent = `上次同步: ${d.getHours()}:${String(d.getMinutes()).padStart(2, '0')}`;
    }
    if (synced && this.ghPat) {
      this.el.syncBtn.disabled = false;
      this.el.syncBtn.textContent = `☁️ 同步 (${Object.keys(this.store.results).length} 张)`;
    }
  }

  async _doSync() {
    if (this.isSyncing) return;
    this.isSyncing = true;
    this.el.syncBtn.textContent = '⏳ 同步中...';
    this.el.syncBtn.disabled = true;

    try {
      const result = await this.store.syncToGithub(this.ghPat);
      if (result.ok) {
        this._showToast(`✅ 已同步 ${result.count} 张卡片到 GitHub，自动触发部署更新`);
        this.el.syncStatus.textContent = `已同步: ${result.count} 张 · ${new Date().toLocaleTimeString()}`;
        this.el.syncBtn.textContent = '✅ 已同步';
        // 持久化标记为已同步
        this.store.persistResults();
      } else {
        this._showToast(`❌ 同步失败: ${result.error}`);
        this.el.syncBtn.textContent = '☁️ 同步失败，重试';
        this.el.syncBtn.disabled = false;
      }
    } catch (err) {
      this._showToast(`❌ 同步出错: ${err.message}`);
      this.el.syncBtn.textContent = '☁️ 重试同步';
      this.el.syncBtn.disabled = false;
    }
    this.isSyncing = false;
  }

  // ── 批次完成 / 续接 ──

  _startBatch() {
    this.el.batchComplete.style.display = 'none';
    this.el.summary.classList.remove('visible');
    this.el.cardArea.style.display = 'block';
    this._showCard();
  }

  _nextBatch() {
    this.store.extendBatch();
    if (this.store.isComplete) {
      this._finishAll();
    } else {
      this._startBatch();
    }
  }

  _nextAll() {
    this.store.extendBatch(this.store.allDueCount - this.store.cursor);
    this._startBatch();
  }

  _stopReview() {
    this._finishAll();
  }

  // ── 卡片展示 ──

  _showCard() {
    if (this.store.isBatchComplete || this.store.allDone) {
      if (this.store.allDone) { this._finishAll(); return; }
      this._showBatchComplete();
      return;
    }

    const card = this.store.currentCard;
    if (!card) {
      if (this.store.allDone) { this._finishAll(); return; }
      this._showBatchComplete();
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

    // 持久化本次结果到 localStorage（跨设备/跨刷新的基础）
    this.store.persistResults();

    const stats = this.store.getBatchStats();

    // 统计
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
    }).join(' ') || '<span class="domain-chip" style="opacity:0.5;">暂无数据</span>';

    // 推荐
    let recText;
    if (stats.rate >= 90) recText = this.recommendations.great;
    else if (stats.rate >= 70) recText = this.recommendations.good;
    else if (stats.rate >= 50) recText = this.recommendations.meh;
    else recText = this.recommendations.poor;
    this.el.batchRecommendation.textContent = recText;

    // 按钮
    const remaining = this.store.allDueCount - this.store.totalDone;
    document.getElementById('next-batch-btn').innerHTML = `▶ 再来 ${Math.min(this.store.batchSize, remaining)} 张`;
    document.getElementById('next-all-btn').textContent = remaining <= this.store.batchSize
      ? `▶ 刷完剩余 ${remaining} 张`
      : `▶ 刷完全部 (${remaining} 张)`;

    // 同步按钮
    this._updateSyncStatus();

    this._showProgress();
    this.el.batchComplete.style.display = 'block';
  }

  // ── 全部完成 ──

  _finishAll() {
    this.store.persistResults();

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
    this.el.progressGlobal.textContent = '全部完成 🎉';
    this.el.progressLabel.textContent = '今日复习完成';

    // 历史记录
    try {
      const today = new Date().toISOString().split('T')[0];
      const history = JSON.parse(localStorage.getItem(HIST_KEY) || '{}');
      history[today] = { total, remembered, forgotten, rate };
      localStorage.setItem(HIST_KEY, JSON.stringify(history));
    } catch (e) {}

    this._showToast(`全部完成！正确率 ${rate}%`);
    this.store.clearCompletedSession();
  }

  // ── 进度 ──

  _showProgress() {
    const batchDone = this.store.batchDone;
    const batchTotal = this.store.batchCount > 0 ? this.store.batchCount : 1;
    const pct = Math.round(batchDone / batchTotal * 100);

    this.el.progressFill.style.width = pct + '%';
    this.el.progressCount.textContent = `${batchDone} / ${batchTotal}`;

    const remaining = this.store.totalDue - this.store.totalDone;
    if (this.store.allDone || this.store.isComplete) {
      this.el.progressGlobal.textContent = '全部完成';
    } else if (remaining > 0) {
      this.el.progressGlobal.textContent = `已复习 ${this.store.totalDone} · 剩余 ${remaining}`;
    } else {
      this.el.progressGlobal.textContent = `今日共 ${this.store.totalDue} 张到期`;
    }

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

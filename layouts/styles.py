"""
styles.py — CSS global de Athletica Pro.
Diseño enterprise nivel Nike/Adidas/Salomon.
Fuentes: Barlow Condensed (display), Plus Jakarta Sans (body), JetBrains Mono (datos)
Paleta: Negro profundo + Lima neón + Cian eléctrico
"""

GLOBAL_CSS = """
/* ═══════════════════════════════════════════════════════════════
   IMPORTS
══════════════════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ═══════════════════════════════════════════════════════════════
   TOKENS
══════════════════════════════════════════════════════════════════ */
:root {
  --lime:    #E8FF47;
  --cyan:    #00F5FF;
  --red:     #EF5350;
  --orange:  #FFB74D;
  --green:   #81C784;
  --bg0:     #090909;
  --bg1:     #0D0D0D;
  --bg2:     #141414;
  --bg3:     #1C1C1C;
  --bg4:     #242424;
  --border:  rgba(255,255,255,0.06);
  --border-h:rgba(232,255,71,0.2);
  --muted:   #6B7280;
  --text:    #E5E7EB;
  --text-dim:#9CA3AF;
  --r:       12px;
  --r-sm:    8px;
  --r-lg:    18px;
  --shadow:  0 4px 24px rgba(0,0,0,0.5);
  --shadow-glow: 0 0 20px rgba(232,255,71,0.12);
  --font-display: 'Barlow Condensed', sans-serif;
  --font-body:    'Plus Jakarta Sans', sans-serif;
  --font-mono:    'JetBrains Mono', monospace;
  --sidebar-w:    280px;
  --header-h:     60px;
  --transition:   all 0.2s cubic-bezier(0.4,0,0.2,1);
}

/* ═══════════════════════════════════════════════════════════════
   RESET & BASE
══════════════════════════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body {
  height: 100%;
  font-family: var(--font-body);
  background-color: var(--bg0);
  color: var(--text);
  -webkit-font-smoothing: antialiased;
  font-size: 14px;
}

/* ── Scrollbar ── */
::-webkit-scrollbar              { width: 4px; height: 4px; }
::-webkit-scrollbar-track        { background: var(--bg2); }
::-webkit-scrollbar-thumb        { background: rgba(232,255,71,0.25); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover  { background: rgba(232,255,71,0.45); }

/* ── Page fade in ── */
#page-content { animation: fadeUp 0.4s ease-out; }
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0);    }
}

/* ═══════════════════════════════════════════════════════════════
   SELECT DROPDOWN (dark theme override)
══════════════════════════════════════════════════════════════════ */
.Select-control                   { background-color: var(--bg4) !important; border: 1px solid var(--border) !important; color: var(--text) !important; border-radius: var(--r-sm) !important; min-height: 40px !important; }
.Select-menu-outer                { background-color: var(--bg3) !important; border: 1px solid var(--border) !important; border-radius: var(--r-sm) !important; box-shadow: var(--shadow) !important; z-index: 9999 !important; }
.Select-value-label               { color: var(--text) !important; font-family: var(--font-body) !important; }
.Select-input > input             { color: var(--text) !important; }
.Select-placeholder               { color: var(--muted) !important; font-size: 0.88rem; }
.Select-option                    { background-color: var(--bg3) !important; color: var(--text-dim) !important; font-size: 0.88rem; }
.Select-option.is-focused         { background-color: var(--bg4) !important; }
.Select-option.is-selected        { background-color: rgba(232,255,71,0.1) !important; color: var(--lime) !important; }
.Select-arrow-zone .Select-arrow  { border-top-color: var(--muted) !important; }

/* ═══════════════════════════════════════════════════════════════
   BOOTSTRAP OVERRIDES
══════════════════════════════════════════════════════════════════ */
.modal-content  { background: var(--bg2); border: 1px solid var(--border); border-radius: var(--r-lg); }
.modal-backdrop { background: rgba(0,0,0,0.8); }

/* ═══════════════════════════════════════════════════════════════
   APP SHELL
══════════════════════════════════════════════════════════════════ */
.athlete-root {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--bg1);
}

.app-body {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* ── Main content ── */
.main-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  min-height: calc(100vh - var(--header-h));
}

.section-content {
  padding: 28px 32px;
  max-width: 100%;
  width: 100%;
}

/* ═══════════════════════════════════════════════════════════════
   HEADER
══════════════════════════════════════════════════════════════════ */
.top-header {
  height: var(--header-h);
  background: var(--bg2);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 24px;
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(12px);
}

/* Brand */
.header-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  flex-shrink: 0;
}

.brand-mark {
  width: 34px;
  height: 34px;
  background: var(--lime);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-letter {
  font-family: var(--font-display);
  font-weight: 900;
  font-size: 1.1rem;
  color: var(--bg1);
  line-height: 1;
}

.brand-text {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.brand-name {
  font-family: var(--font-display);
  font-size: 1.3rem;
  font-weight: 800;
  letter-spacing: 2px;
  color: var(--lime);
  line-height: 1;
}

.brand-suffix {
  font-family: var(--font-display);
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--cyan);
  letter-spacing: 1px;
  background: rgba(0,245,255,0.1);
  padding: 1px 5px;
  border-radius: 4px;
}

/* Header center */
.header-center {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.doctor-banner {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 14px;
  background: rgba(0,245,255,0.1);
  border: 1px solid rgba(0,245,255,0.2);
  border-radius: 20px;
  color: var(--cyan);
  font-size: 0.8rem;
  font-weight: 600;
}

.weekly-bar-wrap {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 180px;
}

.weekly-bar-label {
  font-size: 0.7rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.weekly-bar-track {
  height: 4px;
  background: var(--bg4);
  border-radius: 4px;
  overflow: hidden;
}

.weekly-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--lime), var(--cyan));
  border-radius: 4px;
  transition: width 0.8s ease;
}

/* Header profile */
.header-profile {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-avatar {
  width: 34px;
  height: 34px;
  background: var(--lime);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--bg1);
  font-weight: 700;
  font-size: 0.9rem;
  font-family: var(--font-display);
  flex-shrink: 0;
}

.header-user-name {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--text);
}

.header-user-type {
  font-size: 0.72rem;
  color: var(--lime);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ═══════════════════════════════════════════════════════════════
   SIDEBAR
══════════════════════════════════════════════════════════════════ */
.sidebar {
  width: var(--sidebar-w);
  flex-shrink: 0;
  background: var(--bg2);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: 20px 14px;
  min-height: calc(100vh - var(--header-h));
  position: sticky;
  top: var(--header-h);
  overflow-y: auto;
}

/* Sidebar profile */
.sidebar-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--bg3);
  border-radius: var(--r);
  border: 1px solid var(--border);
  margin-bottom: 16px;
}

.sidebar-avatar {
  width: 42px;
  height: 42px;
  background: var(--lime);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--bg1);
  font-weight: 800;
  font-size: 1.1rem;
  font-family: var(--font-display);
  flex-shrink: 0;
}

.sidebar-name {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-level {
  font-size: 0.72rem;
  color: var(--lime);
  font-family: var(--font-mono);
  margin-top: 2px;
}

/* Sidebar score */
.sidebar-score-block {
  padding: 12px 14px;
  background: var(--bg3);
  border-radius: var(--r);
  border: 1px solid var(--border);
  margin-bottom: 16px;
}

.sidebar-score-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--muted);
  margin-bottom: 8px;
}

.score-dots {
  display: flex;
  gap: 6px;
  margin-bottom: 8px;
}

.score-dot {
  width: 12px;
  height: 12px;
  border-radius: 3px;
  background: var(--bg4);
  border: 1px solid var(--border);
  transition: var(--transition);
}

.score-dot--active {
  background: var(--lime);
  border-color: var(--lime);
  box-shadow: 0 0 8px rgba(232,255,71,0.4);
}

.score-desc {
  font-size: 0.72rem;
  color: var(--text-dim);
  line-height: 1.4;
}

/* Nav */
.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-bottom: 16px;
}

.nav-section-label {
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--muted);
  padding: 8px 10px 4px;
  font-weight: 600;
}

.nav-item {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 9px 12px;
  background: transparent;
  border: none;
  border-radius: var(--r-sm);
  color: var(--text-dim);
  font-family: var(--font-body);
  font-size: 0.88rem;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
  text-align: left;
}

.nav-item:hover {
  background: var(--bg4);
  color: var(--text);
}

.nav-item--active {
  background: rgba(232,255,71,0.1);
  color: var(--lime);
  font-weight: 600;
}

.nav-item--active .bi {
  color: var(--lime);
}

/* Sidebar footer */
.sidebar-footer {
  margin-top: auto;
}

.btn-logout {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 9px 12px;
  background: transparent;
  border: 1px solid rgba(239,83,80,0.2);
  border-radius: var(--r-sm);
  color: #EF5350;
  font-family: var(--font-body);
  font-size: 0.85rem;
  cursor: pointer;
  transition: var(--transition);
}

.btn-logout:hover {
  background: rgba(239,83,80,0.08);
  border-color: rgba(239,83,80,0.4);
}

/* ═══════════════════════════════════════════════════════════════
   SECTION HEADERS
══════════════════════════════════════════════════════════════════ */
.section-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 28px;
}

.section-title {
  font-family: var(--font-display);
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: 1px;
  color: var(--text);
  line-height: 1;
}

.section-subtitle {
  font-size: 0.85rem;
  color: var(--muted);
  margin-top: 6px;
  font-weight: 400;
}

.section-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 12px;
  background: rgba(232,255,71,0.1);
  border: 1px solid rgba(232,255,71,0.2);
  border-radius: 20px;
  font-size: 0.72rem;
  color: var(--lime);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  flex-shrink: 0;
}

/* ═══════════════════════════════════════════════════════════════
   PRO CARDS
══════════════════════════════════════════════════════════════════ */
.pro-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 20px 22px;
  transition: var(--transition);
}

.pro-card:hover {
  border-color: rgba(232,255,71,0.1);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.card-title {
  font-size: 0.92rem;
  font-weight: 600;
  color: var(--text);
}

.card-badge {
  font-size: 0.7rem;
  color: var(--muted);
  background: var(--bg4);
  padding: 3px 8px;
  border-radius: 6px;
  font-family: var(--font-mono);
}

.card-help-link {
  font-size: 0.75rem;
  color: var(--cyan);
  text-decoration: none;
  opacity: 0.7;
}

.card-help-link:hover { opacity: 1; }

/* ═══════════════════════════════════════════════════════════════
   KPI CARDS
══════════════════════════════════════════════════════════════════ */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-bottom: 24px;
}

.kpi-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: var(--transition);
  position: relative;
  overflow: hidden;
}

.kpi-card::before {
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 60px; height: 60px;
  background: radial-gradient(circle, rgba(232,255,71,0.05), transparent 70%);
  border-radius: 50%;
}

.kpi-card:hover {
  border-color: var(--border-h);
  transform: translateY(-1px);
  box-shadow: var(--shadow-glow);
}

.kpi-icon {
  font-size: 1.4rem;
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  background: var(--bg4);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.kpi-value {
  font-family: var(--font-mono);
  font-size: 1.6rem;
  font-weight: 600;
  line-height: 1;
  margin-bottom: 4px;
}

.kpi-label {
  font-size: 0.72rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.kpi-sublabel {
  font-size: 0.72rem;
  color: var(--text-dim);
  margin-top: 2px;
}

/* ═══════════════════════════════════════════════════════════════
   SECTION: INICIO
══════════════════════════════════════════════════════════════════ */
.inicio-grid {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 16px;
}

.inicio-right-col {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ECG */
.ecg-upload-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: var(--bg4);
  border: 1px solid var(--border);
  border-radius: var(--r-sm);
  color: var(--text-dim);
  font-size: 0.8rem;
  cursor: pointer;
  transition: var(--transition);
  white-space: nowrap;
}

.ecg-upload-btn:hover {
  border-color: var(--border-h);
  color: var(--lime);
}

.ecg-graph { border-radius: var(--r-sm); overflow: hidden; }

.ecg-bpm-badge {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--lime);
  padding: 4px 10px;
  background: rgba(232,255,71,0.1);
  border-radius: 20px;
}

.ecg-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
  padding-top: 12px;
  border-top: 1px solid var(--border);
}

.ecg-status {
  font-size: 0.75rem;
  color: var(--muted);
  font-family: var(--font-mono);
}

/* Recent workouts */
.recent-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.recent-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  background: var(--bg3);
  border-radius: var(--r-sm);
  transition: var(--transition);
}

.recent-item:hover { background: var(--bg4); }

.recent-icon { font-size: 1.1rem; width: 24px; text-align: center; flex-shrink: 0; }

.recent-info { flex: 1; min-width: 0; }

.recent-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.recent-meta {
  font-size: 0.72rem;
  color: var(--muted);
  font-family: var(--font-mono);
}

.recent-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 3px;
}

.rpe-chip {
  font-size: 0.7rem;
  font-weight: 600;
  font-family: var(--font-mono);
  border: 1px solid;
  padding: 2px 7px;
  border-radius: 10px;
}

.recent-date {
  font-size: 0.68rem;
  color: var(--muted);
  font-family: var(--font-mono);
}

/* Personal records */
.records-list { display: flex; flex-direction: column; gap: 6px; }

.pr-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 10px;
  background: var(--bg3);
  border-radius: var(--r-sm);
}

.pr-distance {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text);
}

.pr-time {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--lime);
}

/* ═══════════════════════════════════════════════════════════════
   SECTION: MÉTRICAS
══════════════════════════════════════════════════════════════════ */
.metrics-summary-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.mini-stat {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: 14px 16px;
  text-align: center;
}

.mini-stat-val {
  font-family: var(--font-mono);
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--lime);
  margin-bottom: 4px;
}

.mini-stat-label {
  font-size: 0.7rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.chart-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-dim);
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ACWR */
.acwr-display {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 12px 0;
}

.acwr-value {
  font-family: var(--font-mono);
  font-size: 2rem;
  font-weight: 600;
}

.acwr-status {
  font-size: 0.9rem;
  font-weight: 600;
  background: var(--bg4);
  padding: 6px 14px;
  border-radius: 20px;
}

.acwr-bar-wrap { flex: 1; }

/* ═══════════════════════════════════════════════════════════════
   SECTION: OBJETIVOS
══════════════════════════════════════════════════════════════════ */
.objetivos-layout {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 20px;
}

.panel-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  gap: 12px;
}

.goal-tabs {
  display: flex;
  gap: 4px;
  background: var(--bg3);
  border-radius: var(--r-sm);
  padding: 3px;
}

.goal-tab {
  padding: 5px 12px;
  border: none;
  background: transparent;
  border-radius: 6px;
  color: var(--muted);
  font-size: 0.8rem;
  font-family: var(--font-body);
  cursor: pointer;
  transition: var(--transition);
  font-weight: 500;
}

.goal-tab--active, .goal-tab:hover {
  background: var(--bg4);
  color: var(--text);
}

.goals-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

/* Goal card */
.goal-card {
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: 16px;
  transition: var(--transition);
}

.goal-card:hover {
  border-color: rgba(232,255,71,0.15);
  background: var(--bg4);
}

.goal-card--done {
  opacity: 0.6;
}

.goal-card-header {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 8px;
}

.goal-emoji {
  font-size: 1.4rem;
  flex-shrink: 0;
  margin-top: 1px;
}

.goal-card-info { flex: 1; min-width: 0; }

.goal-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 3px;
}

.goal-desc {
  font-size: 0.78rem;
  color: var(--muted);
  line-height: 1.3;
}

.goal-type-tag {
  font-size: 0.68rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border: 1px solid;
  padding: 2px 7px;
  border-radius: 10px;
  white-space: nowrap;
  flex-shrink: 0;
}

.goal-meta-row {
  display: flex;
  gap: 12px;
  margin-bottom: 10px;
}

.goal-target, .goal-deadline {
  font-size: 0.72rem;
  color: var(--muted);
  font-family: var(--font-mono);
}

.goal-target { color: var(--lime); }

/* Progress bar */
.goal-progress-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
}

.goal-progress-track {
  flex: 1;
  height: 4px;
  background: var(--bg4);
  border-radius: 4px;
  overflow: hidden;
}

.goal-progress-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.6s ease;
}

.goal-progress-label {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 600;
  min-width: 32px;
  text-align: right;
}

/* Sidebar objetivos */
.goals-stats-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.goals-stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: var(--bg3);
  border-radius: var(--r-sm);
}

.goals-stat-num {
  font-family: var(--font-mono);
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text);
}

.goals-stat-label {
  font-size: 0.78rem;
  color: var(--muted);
}

.deadline-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid var(--border);
}

.deadline-item:last-child { border-bottom: none; }

.deadline-emoji { font-size: 1.1rem; }

.deadline-name {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text);
}

.deadline-when {
  font-size: 0.72rem;
  color: var(--muted);
  font-family: var(--font-mono);
}

/* ═══════════════════════════════════════════════════════════════
   MODAL GOALS
══════════════════════════════════════════════════════════════════ */
.goal-type-picker {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 4px;
}

.goal-type-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px 16px;
  background: var(--bg4);
  border: 1px solid var(--border);
  border-radius: var(--r);
  cursor: pointer;
  transition: var(--transition);
  font-family: var(--font-body);
}

.goal-type-card .bi { font-size: 1.6rem; color: var(--lime); }
.goal-type-card span { font-size: 0.95rem; font-weight: 600; color: var(--text); }
.goal-type-card small { font-size: 0.75rem; color: var(--muted); }

.goal-type-card:hover {
  border-color: var(--border-h);
  background: rgba(232,255,71,0.05);
}

.goal-form-type-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  padding: 8px 12px;
  background: var(--bg4);
  border-radius: var(--r-sm);
  font-size: 0.85rem;
  color: var(--lime);
  font-weight: 600;
}

.link-btn {
  background: none;
  border: none;
  color: var(--muted);
  font-size: 0.78rem;
  cursor: pointer;
  margin-left: auto;
  padding: 0;
  font-family: var(--font-body);
}

.link-btn:hover { color: var(--text); }

/* ═══════════════════════════════════════════════════════════════
   SECTION: NUTRICIÓN
══════════════════════════════════════════════════════════════════ */
.nutricion-layout {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 20px;
}

.nutricion-main {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Macro summary */
.macro-summary-row {
  display: flex;
  align-items: center;
  gap: 24px;
}

.macro-total-cal { text-align: center; flex-shrink: 0; }

.macro-cal-number {
  font-family: var(--font-mono);
  font-size: 2rem;
  font-weight: 600;
  color: var(--lime);
  line-height: 1;
}

.macro-cal-label {
  font-size: 0.72rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  margin-top: 4px;
}

.macro-bars { flex: 1; display: flex; flex-direction: column; gap: 10px; }

.macro-bar-item { display: flex; flex-direction: column; gap: 4px; }

.macro-bar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.macro-name {
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.macro-name.carbs   { color: var(--lime); }
.macro-name.protein { color: var(--cyan); }
.macro-name.fat     { color: var(--orange); }

.macro-val {
  font-family: var(--font-mono);
  font-size: 0.78rem;
  color: var(--text-dim);
}

.macro-bar-track {
  height: 6px;
  background: var(--bg4);
  border-radius: 6px;
  overflow: hidden;
}

.macro-bar-fill {
  height: 100%;
  border-radius: 6px;
  transition: width 0.6s ease;
}

.macro-bar-fill.carbs   { background: var(--lime); }
.macro-bar-fill.protein { background: var(--cyan); }
.macro-bar-fill.fat     { background: var(--orange); }

/* Hydration */
.hydration-controls { display: flex; gap: 8px; }

.btn-water {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  background: rgba(79,195,247,0.1);
  border: 1px solid rgba(79,195,247,0.2);
  border-radius: var(--r-sm);
  color: #4FC3F7;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
  font-family: var(--font-body);
}

.btn-water:hover {
  background: rgba(79,195,247,0.2);
}

.hydration-display {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 12px;
}

.hydration-big-num {
  font-family: var(--font-mono);
  font-size: 2.2rem;
  font-weight: 600;
  color: #4FC3F7;
}

.hydration-goal {
  font-size: 0.82rem;
  color: var(--muted);
}

.hydration-bar-track {
  height: 8px;
  background: var(--bg4);
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 12px;
}

.hydration-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #4FC3F7, var(--cyan));
  border-radius: 8px;
  transition: width 0.6s ease;
}

.hydration-milestones {
  display: flex;
  justify-content: space-between;
}

.h-milestone {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
}

.h-milestone-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--bg4);
  border: 1px solid var(--border);
  transition: var(--transition);
}

.h-milestone--reached .h-milestone-dot {
  background: #4FC3F7;
  border-color: #4FC3F7;
  box-shadow: 0 0 6px rgba(79,195,247,0.5);
}

.h-milestone-label {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  color: var(--muted);
}

.h-milestone--reached .h-milestone-label { color: #4FC3F7; }

/* Meal form */
.meal-form { display: flex; flex-direction: column; gap: 12px; }

.meal-type-selector {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.meal-tab {
  padding: 6px 14px;
  border: 1px solid var(--border);
  border-radius: 20px;
  background: var(--bg3);
  color: var(--muted);
  font-size: 0.8rem;
  font-family: var(--font-body);
  cursor: pointer;
  transition: var(--transition);
  font-weight: 500;
}

.meal-tab--active, .meal-tab:hover {
  border-color: var(--border-h);
  background: rgba(232,255,71,0.08);
  color: var(--lime);
}

.meal-input-row {
  display: flex;
  gap: 8px;
}

.meal-input { flex: 1; }

/* Meals log */
.nutricion-sidebar { display: flex; flex-direction: column; gap: 16px; }

.meals-log { display: flex; flex-direction: column; gap: 14px; }

.meal-group {}

.meal-group-title {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--border);
}

.meal-entries { display: flex; flex-direction: column; gap: 5px; }

.meal-entry {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
  background: var(--bg3);
  border-radius: 6px;
}

.meal-desc {
  font-size: 0.8rem;
  color: var(--text);
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.meal-cal {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--lime);
  white-space: nowrap;
  flex-shrink: 0;
}

.empty-meal { font-size: 0.8rem; color: var(--muted); padding: 4px 0; }

/* ═══════════════════════════════════════════════════════════════
   SECTION: ENTRENAMIENTOS
══════════════════════════════════════════════════════════════════ */
.entrenamientos-layout {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 20px;
}

.workout-filters {
  display: flex;
  gap: 6px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.wf-btn {
  padding: 5px 14px;
  border: 1px solid var(--border);
  border-radius: 20px;
  background: var(--bg3);
  color: var(--muted);
  font-size: 0.8rem;
  font-family: var(--font-body);
  cursor: pointer;
  transition: var(--transition);
  font-weight: 500;
}

.wf-btn--active, .wf-btn:hover {
  border-color: var(--border-h);
  color: var(--lime);
  background: rgba(232,255,71,0.06);
}

.workout-history-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 560px;
  overflow-y: auto;
  padding-right: 4px;
}

/* Workout card */
.workout-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: var(--r);
  transition: var(--transition);
}

.workout-card:hover {
  background: var(--bg4);
  border-color: rgba(232,255,71,0.1);
}

.workout-card-icon {
  width: 40px;
  height: 40px;
  background: var(--bg4);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.workout-card-body { flex: 1; min-width: 0; }

.workout-card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.workout-type-label {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--text);
}

.workout-date {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--muted);
}

.workout-meta {
  font-size: 0.78rem;
  color: var(--text-dim);
  font-family: var(--font-mono);
  margin-bottom: 3px;
}

.workout-notes {
  font-size: 0.75rem;
  color: var(--muted);
  font-style: italic;
}

.workout-card-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
  flex-shrink: 0;
}

.rpe-badge-sm {
  font-size: 0.7rem;
  font-weight: 700;
  font-family: var(--font-mono);
  border: 1px solid;
  padding: 2px 8px;
  border-radius: 10px;
}

.zone-badge {
  font-size: 0.68rem;
  font-weight: 600;
  font-family: var(--font-mono);
}

/* Sidebar entrenamientos */
.month-stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.month-stat { text-align: center; }

.month-stat-val {
  font-family: var(--font-mono);
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--lime);
  margin-bottom: 3px;
}

.month-stat-label {
  font-size: 0.68rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.training-tip-text {
  font-size: 0.85rem;
  color: var(--text-dim);
  line-height: 1.6;
}

/* ═══════════════════════════════════════════════════════════════
   MODAL POST-ENTRENAMIENTO
══════════════════════════════════════════════════════════════════ */
.pro-modal .modal-content {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
}

.pro-modal-header {
  background: var(--bg3);
  border-bottom: 1px solid var(--border) !important;
  padding: 16px 20px;
  border-radius: var(--r-lg) var(--r-lg) 0 0;
}

.modal-title-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.modal-icon-wrap {
  width: 38px;
  height: 38px;
  background: rgba(232,255,71,0.1);
  border: 1px solid rgba(232,255,71,0.2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--lime);
  font-size: 1.1rem;
}

.modal-title-text {
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text);
  letter-spacing: 0.5px;
  margin: 0;
}

.modal-subtitle { font-size: 0.78rem; color: var(--muted); margin: 2px 0 0; }

.pro-modal-body { background: var(--bg2); padding: 20px; }

.pro-modal-footer {
  background: var(--bg3);
  border-top: 1px solid var(--border) !important;
  padding: 12px 20px;
  border-radius: 0 0 var(--r-lg) var(--r-lg);
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

/* Survey grid */
.survey-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.survey-col { display: flex; flex-direction: column; gap: 14px; }

/* RPE */
.rpe-group { }

.rpe-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.rpe-badge {
  font-family: var(--font-mono);
  font-size: 0.82rem;
  font-weight: 600;
  padding: 3px 10px;
  background: var(--bg4);
  border-radius: 20px;
}

.rpe-scale-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.68rem;
  color: var(--muted);
  margin-top: 4px;
}

/* Sliders */
.rpe-slider, .energy-slider, .pain-slider {
  padding: 0 4px;
}

/* Mood picker */
.mood-picker {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.mood-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  padding: 8px 10px;
  background: var(--bg4);
  border: 1px solid var(--border);
  border-radius: var(--r);
  cursor: pointer;
  transition: var(--transition);
  font-family: var(--font-body);
  flex: 1;
  min-width: 50px;
}

.mood-emoji { font-size: 1.3rem; line-height: 1; }

.mood-label {
  font-size: 0.65rem;
  color: var(--muted);
  white-space: nowrap;
}

.mood-btn:hover { border-color: var(--border-h); }

.mood-btn--selected {
  border-color: var(--lime);
  background: rgba(232,255,71,0.08);
}

.mood-btn--selected .mood-label { color: var(--lime); }

/* Pain header */
.pain-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.form-hint { font-size: 0.72rem; color: var(--muted); }

/* ═══════════════════════════════════════════════════════════════
   FORM ELEMENTS
══════════════════════════════════════════════════════════════════ */
.form-group { display: flex; flex-direction: column; gap: 6px; }

.form-group label {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-dim);
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.pro-input {
  width: 100%;
  padding: 9px 12px;
  background: var(--bg4);
  border: 1px solid var(--border);
  border-radius: var(--r-sm);
  color: var(--text);
  font-family: var(--font-body);
  font-size: 0.88rem;
  transition: var(--transition);
  outline: none;
  box-sizing: border-box;
}

.pro-input:focus {
  border-color: rgba(232,255,71,0.4);
  box-shadow: 0 0 0 3px rgba(232,255,71,0.06);
}

.pro-textarea {
  width: 100%;
  padding: 9px 12px;
  background: var(--bg4);
  border: 1px solid var(--border);
  border-radius: var(--r-sm);
  color: var(--text);
  font-family: var(--font-body);
  font-size: 0.88rem;
  resize: vertical;
  outline: none;
  box-sizing: border-box;
  transition: var(--transition);
}

.pro-textarea:focus {
  border-color: rgba(232,255,71,0.4);
}

.modal-subtitle {
  font-size: 0.88rem;
  color: var(--muted);
  margin-bottom: 16px;
}

/* ═══════════════════════════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════════════════════════════ */
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 9px 20px;
  background: var(--lime);
  border: none;
  border-radius: var(--r-sm);
  color: var(--bg1);
  font-family: var(--font-body);
  font-size: 0.88rem;
  font-weight: 700;
  cursor: pointer;
  transition: var(--transition);
  line-height: 1;
}

.btn-primary:hover {
  background: #f5ff6e;
  box-shadow: 0 0 16px rgba(232,255,71,0.3);
  transform: translateY(-1px);
}

.btn-primary-sm {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 14px;
  background: var(--lime);
  border: none;
  border-radius: var(--r-sm);
  color: var(--bg1);
  font-family: var(--font-body);
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  transition: var(--transition);
  white-space: nowrap;
}

.btn-primary-sm:hover {
  background: #f5ff6e;
  box-shadow: 0 0 12px rgba(232,255,71,0.25);
}

.btn-ghost {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 9px 20px;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: var(--r-sm);
  color: var(--muted);
  font-family: var(--font-body);
  font-size: 0.88rem;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
  text-decoration: none;
}

.btn-ghost:hover {
  color: var(--text);
  border-color: rgba(255,255,255,0.15);
  background: var(--bg4);
}

.btn-ghost-sm {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 12px;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: var(--r-sm);
  color: var(--muted);
  font-family: var(--font-body);
  font-size: 0.78rem;
  cursor: pointer;
  transition: var(--transition);
}

.btn-ghost-sm:hover { color: var(--text); border-color: rgba(255,255,255,0.15); }

/* ═══════════════════════════════════════════════════════════════
   MISC
══════════════════════════════════════════════════════════════════ */
.success-msg {
  font-size: 0.82rem;
  min-height: 20px;
  font-weight: 500;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
  gap: 8px;
}

.empty-state-sm {
  font-size: 0.82rem;
  color: var(--muted);
  font-style: italic;
  text-align: center;
  padding: 8px 0;
}

/* RC Slider overrides */
.rc-slider-rail            { background: var(--bg4); height: 4px; }
.rc-slider-track           { background: var(--lime); height: 4px; }
.rc-slider-handle          { background: var(--lime); border-color: var(--lime); box-shadow: 0 0 8px rgba(232,255,71,0.5); }
.rc-slider-handle:hover    { border-color: var(--lime); box-shadow: 0 0 12px rgba(232,255,71,0.6); }
.rc-slider-handle-dragging { border-color: var(--lime) !important; box-shadow: 0 0 12px rgba(232,255,71,0.6) !important; }
.rc-slider-mark-text       { color: var(--muted); font-size: 0.72rem; font-family: var(--font-mono); }
.rc-slider-dot-active      { border-color: var(--lime); }

/* ═══════════════════════════════════════════════════════════════
   WELCOME / AUTH / ONBOARDING (unchanged base)
══════════════════════════════════════════════════════════════════ */
.welcome-container {
  position: relative; min-height: 100vh; display: flex; flex-direction: column;
  justify-content: center; align-items: center; text-align: center; padding: 40px 20px;
  background-color: var(--bg1);
}

.main-title {
  font-family: var(--font-display);
  font-size: 5rem; font-weight: 900; color: var(--lime); letter-spacing: 6px;
  text-shadow: 0 0 30px rgba(232,255,71,0.5), 0 0 8px var(--lime); margin-bottom: 10px;
}

.subtitle { font-size: 1.2rem; color: var(--text-dim); margin-bottom: 30px; font-weight: 400; }

.features-grid {
  display: grid; grid-template-columns: repeat(auto-fit,minmax(280px,1fr));
  gap: 20px; max-width: 1000px; width: 100%; margin: 0 auto 50px;
}

.feature-card {
  background: var(--bg2); border-radius: var(--r-lg); padding: 28px;
  transition: var(--transition); text-align: left; border: 1px solid var(--border);
}

.feature-card:hover { transform: translateY(-4px); border-color: var(--border-h); box-shadow: var(--shadow-glow); }

.icon { font-size: 2.2rem; color: var(--lime); margin-bottom: 12px; }
.card-title { font-size: 1.2rem; font-weight: 700; color: white; margin-bottom: 8px; }
.card-text { font-size: 0.95rem; color: var(--muted); font-weight: 400; line-height: 1.5; }

.auth-container {
  min-height: 100vh; display: flex; justify-content: center; align-items: center;
  background-color: var(--bg1); padding: 40px 20px;
}

.auth-wrapper {
  background-color: var(--bg2); border-radius: var(--r-lg);
  box-shadow: 0 10px 40px rgba(0,0,0,0.9); width: 1200px; max-width: 95%; min-height: 700px;
  max-height: 95vh; display: flex; overflow: hidden; border: 1px solid var(--border);
}

.auth-form-side {
  width: 55%; padding: 60px 70px; display: flex; flex-direction: column;
  background-color: var(--bg2); overflow-y: auto;
}

.auth-form-side h2 { margin-bottom: 2rem; color: #fff; font-weight: 700; font-size: 2rem; }

.auth-toggle-side {
  width: 45%; background: linear-gradient(145deg, #1a1a1a, #0d0d0d);
  border-left: 1px solid var(--border);
  color: white; display: flex; flex-direction: column; justify-content: center;
  align-items: center; padding: 50px; text-align: center;
}

.auth-input {
  width: 100%; padding: 12px 40px 12px 40px; background-color: var(--bg4);
  border: 1px solid var(--border); border-radius: var(--r-sm); color: white; font-size: 1rem;
  transition: var(--transition); box-sizing: border-box;
}

.auth-input:focus { border-color: rgba(232,255,71,0.5); outline: none; box-shadow: 0 0 0 3px rgba(232,255,71,0.08); }

.auth-btn {
  width: 100%; background-color: var(--lime); border: none; font-weight: 700;
  padding: 13px; border-radius: var(--r-sm); margin-top: 20px; color: var(--bg1);
  font-size: 1rem; cursor: pointer; transition: var(--transition);
  font-family: var(--font-body);
}

.auth-btn:hover { background-color: #f0ff6a; box-shadow: 0 4px 20px rgba(232,255,71,0.3); }

.toggle-btn-promo {
  padding: 10px 28px; background-color: transparent; border: 2px solid rgba(255,255,255,0.2);
  color: white; border-radius: 50px; font-weight: 600; transition: var(--transition); cursor: pointer;
}

.toggle-btn-promo:hover { background-color: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.4); }

.input-group { position: relative; margin-bottom: 20px; width: 100%; }
.forgot-password { color: var(--lime); margin-top: 8px; font-size: 0.9rem; cursor: pointer; }

/* Onboarding */
.onboarding-container {
  min-height: 100vh; display: flex; flex-direction: column; align-items: center;
  background-color: var(--bg1); padding: 30px 20px;
}

.onboarding-card {
  background-color: var(--bg2); border-radius: var(--r-lg);
  box-shadow: 0 10px 40px rgba(0,0,0,0.9); width: 850px; max-width: 100%;
  padding: 40px; margin-top: 40px; border: 1px solid var(--border);
}

.step-title { color: var(--lime); font-family: var(--font-display); font-size: 2.2rem; font-weight: 800; margin-bottom: 5px; }
.step-subtitle { color: var(--text-dim); font-size: 1rem; font-weight: 300; }

.progress-bar-container { height: 3px; background: var(--bg4); border-radius: 4px; overflow: hidden; margin: 20px 0; }
.progress-bar { height: 100%; background: linear-gradient(90deg, var(--lime), var(--cyan)); transition: width 0.5s ease-in-out; }

.onboarding-input {
  background-color: var(--bg4); border: 1px solid var(--border); border-radius: var(--r-sm);
  color: white; padding: 11px 12px; width: 100%; transition: var(--transition);
  font-family: var(--font-body);
}

.onboarding-input:focus { border-color: rgba(232,255,71,0.4); outline: none; }

.radio-card-group { display: grid; grid-template-columns: repeat(auto-fit,minmax(120px,1fr)); gap: 12px; margin-top: 12px; }

.radio-card {
  background: var(--bg4); color: var(--muted); padding: 18px 10px !important;
  border-radius: var(--r-sm); cursor: pointer; text-align: center;
  transition: var(--transition); border: 2px solid var(--border);
  display: flex !important; flex-direction: column !important; align-items: center !important;
  justify-content: center !important; min-height: 95px !important;
}

.radio-card:hover { border-color: rgba(232,255,71,0.2); background: rgba(232,255,71,0.04); }

.radio-card-checked {
  border-color: var(--lime) !important;
  background: rgba(232,255,71,0.08) !important;
  color: var(--lime) !important;
}

.radio-card .bi { font-size: 1.6rem !important; margin-bottom: 8px !important; display: block !important; }



/* ═══════════════════════════════════════════════════════════════
   INICIO V2 — Dashboard cards
══════════════════════════════════════════════════════════════════ */

/* Welcome banner */
.inicio-welcome-banner {
  background: linear-gradient(135deg, var(--bg2) 0%, rgba(232,255,71,0.06) 100%);
  border-radius: var(--r-lg);
  border: 1px solid rgba(232,255,71,0.15);
  padding: 24px 28px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* KPI row override — full width */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.kpi-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 20px 22px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: var(--transition);
}

.kpi-card:hover {
  border-color: rgba(232,255,71,0.12);
  transform: translateY(-1px);
}

.kpi-icon {
  font-size: 1.4rem;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: rgba(255,255,255,0.04);
  flex-shrink: 0;
}

.kpi-value {
  font-family: var(--font-display);
  font-size: 1.8rem;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.5px;
}

.kpi-label {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  color: var(--muted);
  margin-top: 4px;
}

.kpi-sublabel {
  font-size: 0.75rem;
  color: var(--text-dim);
  margin-top: 2px;
}

/* Pro card bigger padding */
.pro-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 20px 22px;
  transition: var(--transition);
}

.pro-card:hover {
  border-color: rgba(232,255,71,0.1);
}

/* Recent list items */
.recent-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

/* ACWR display bigger */
.acwr-value {
  font-family: var(--font-display);
  font-size: 2.4rem;
  font-weight: 900;
  line-height: 1;
  margin-bottom: 4px;
}

.acwr-status {
  font-size: 0.82rem;
  font-weight: 600;
}

/* Section header */
.section-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 24px;
}

.section-title {
  font-family: var(--font-display);
  font-size: 1.8rem;
  font-weight: 800;
  letter-spacing: 0.5px;
  color: var(--text);
  line-height: 1.1;
}

.section-subtitle {
  font-size: 0.85rem;
  color: var(--muted);
  margin-top: 4px;
}

/* Card header */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.card-title {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--text);
  letter-spacing: 0.2px;
}

.card-badge {
  font-size: 0.72rem;
  color: var(--muted);
  background: var(--bg4);
  padding: 2px 8px;
  border-radius: 6px;
}

/* Empty state */
.empty-state-sm {
  color: var(--muted);
  font-size: 0.83rem;
  padding: 8px 0;
}

/* Records list */
.records-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.pr-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 10px;
  background: var(--bg3);
  border-radius: 8px;
}

.pr-distance {
  font-size: 0.85rem;
  color: var(--text-dim);
  font-weight: 600;
}

.pr-time {
  font-size: 0.85rem;
  color: var(--lime);
  font-family: var(--font-mono);
  font-weight: 600;
}

/* ═══════════════════════════════════════════════════════════════
   RESPONSIVE
══════════════════════════════════════════════════════════════════ */
@media (max-width: 1200px) {
  .inicio-grid             { grid-template-columns: 1fr; }
  .inicio-right-col        { grid-template-columns: 1fr 1fr; display: grid; }
  .kpi-row                 { grid-template-columns: repeat(2, 1fr); }
  .metrics-grid            { grid-template-columns: 1fr; }
  .metrics-summary-row     { grid-template-columns: repeat(3, 1fr); }
}

@media (max-width: 900px) {
  :root { --sidebar-w: 200px; }
  .section-content         { padding: 20px; }
  .nutricion-layout,
  .entrenamientos-layout,
  .objetivos-layout        { grid-template-columns: 1fr; }
  .goals-grid              { grid-template-columns: 1fr; }
  .survey-grid             { grid-template-columns: 1fr; }
}

@media (max-width: 700px) {
  .sidebar                 { display: none; }
  .main-content            { margin-left: 0; }
  .kpi-row                 { grid-template-columns: 1fr 1fr; }
  .main-title              { font-size: 3rem; letter-spacing: 3px; }
  .auth-wrapper            { flex-direction: column; height: auto; }
  .auth-form-side,
  .auth-toggle-side        { width: 100%; padding: 30px 24px; }
  .auth-toggle-side        { order: -1; min-height: 180px; }
}
"""
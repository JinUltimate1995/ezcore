import os

html_content = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>ezCORE // Sovereign Architectural Studio & Moonboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,500;0,700;1,400&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Syne:wght@600;700;800&display=swap" rel="stylesheet">
<!-- Three.js for 3D Architectural Showroom -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<style>
:root {
  /* Architectural Basalt Palette */
  --basalt-00: #08090B;
  --basalt-01: #0F1115;
  --basalt-02: #161920;
  --basalt-03: #1E222B;
  --basalt-04: #282D3A;
  --basalt-border: #242834;
  --basalt-chamfer: #3B4254;
  
  /* Brand Solar Ochre (No neon cyan/purple) */
  --solar-ochre: #F39C12;
  --solar-hot: #FFA726;
  --solar-wash: #271E10;
  --solar-glow: rgba(243, 156, 18, 0.28);
  
  /* Titanium Typography */
  --titanium-pure: #F4F5F8;
  --titanium-body: #AFB5C3;
  --titanium-muted: #6C7385;
  --titanium-ghost: #373B49;
  
  /* Precision Semantics */
  --core-online: #2ECC71;
  --core-warning: #E67E22;
  --core-danger: #E74C3C;
  --core-telemetry: #3498DB;
  
  /* Typography */
  --font-display: 'Syne', sans-serif;
  --font-body: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body {
  height: 100%;
  background-color: var(--basalt-00);
  color: var(--titanium-pure);
  font-family: var(--font-body);
  -webkit-font-smoothing: antialiased;
  overflow: hidden;
}

/* Master Studio Shell */
.studio-shell {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

/* ==================== SIDEBAR NAVIGATION ==================== */
aside.studio-sidebar {
  width: 290px;
  background: var(--basalt-01);
  border-right: 1px solid var(--basalt-border);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  z-index: 100;
  user-select: none;
}

.sidebar-header {
  padding: 24px 20px 18px;
  border-bottom: 1px solid var(--basalt-border);
}

.brand-lockup {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.brand-plinth-icon {
  width: 32px;
  height: 32px;
  background: var(--basalt-02);
  border: 1px solid var(--basalt-chamfer);
  border-radius: 6px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.brand-plinth-icon::before {
  content: '';
  width: 14px;
  height: 14px;
  background: var(--solar-ochre);
  border-radius: 3px;
  box-shadow: 0 0 10px var(--solar-glow);
}

.brand-plinth-icon::after {
  content: '';
  position: absolute;
  width: 6px;
  height: 6px;
  background: var(--basalt-00);
  border-radius: 50%;
}

.brand-text {
  font-family: var(--font-display);
  font-size: 19px;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.brand-text .ez { color: var(--titanium-muted); font-weight: 600; }
.brand-text .core { color: var(--titanium-pure); }

.studio-tagline {
  margin-top: 10px;
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--solar-ochre);
  background: var(--solar-wash);
  border: 1px solid rgba(243, 156, 18, 0.25);
  padding: 4px 8px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.studio-tagline span.dot {
  width: 6px;
  height: 6px;
  background: var(--solar-ochre);
  border-radius: 50%;
  box-shadow: 0 0 6px var(--solar-ochre);
}

/* Sidebar Nav Links */
nav.sidebar-menu {
  flex-grow: 1;
  padding: 16px 12px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-category {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: var(--titanium-muted);
  text-transform: uppercase;
  padding: 12px 10px 6px;
}

.nav-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 9px 12px;
  border-radius: 7px;
  color: var(--titanium-body);
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.15s ease;
  border: 1px solid transparent;
}

.nav-link:hover {
  background: var(--basalt-02);
  color: var(--titanium-pure);
}

.nav-link.active {
  background: var(--basalt-02);
  border-color: var(--basalt-chamfer);
  color: var(--solar-ochre);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
}

.nav-link .counter {
  font-family: var(--font-mono);
  font-size: 10px;
  background: var(--basalt-03);
  padding: 2px 6px;
  border-radius: 4px;
  color: var(--titanium-muted);
}

.nav-link.active .counter {
  background: var(--solar-wash);
  color: var(--solar-ochre);
}

/* Sidebar Footer / Audit Gate */
.sidebar-footer {
  padding: 16px;
  border-top: 1px solid var(--basalt-border);
  background: var(--basalt-01);
}

.audit-status {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--titanium-muted);
}

.audit-bar-wrap {
  height: 5px;
  background: var(--basalt-03);
  border-radius: 3px;
  overflow: hidden;
  margin: 8px 0 6px;
}

.audit-bar-fill {
  height: 100%;
  background: var(--solar-ochre);
  width: 100%;
  transition: width 0.3s ease;
}

/* ==================== WORKSPACE & TOP BAR ==================== */
.studio-workspace {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: var(--basalt-00);
}

header.topbar {
  height: 56px;
  border-bottom: 1px solid var(--basalt-border);
  background: rgba(15, 17, 21, 0.85);
  backdrop-filter: blur(16px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  flex-shrink: 0;
  z-index: 50;
}

.topbar-breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
}

.topbar-breadcrumb .crumb-root { color: var(--titanium-muted); }
.topbar-breadcrumb .crumb-sep { color: var(--basalt-chamfer); font-family: var(--font-mono); }
.topbar-breadcrumb .crumb-current { color: var(--titanium-pure); }

.topbar-telemetry {
  display: flex;
  align-items: center;
  gap: 20px;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--titanium-muted);
}

.telemetry-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.telemetry-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--core-online);
  box-shadow: 0 0 6px var(--core-online);
}

/* ==================== MAIN CONTENT VIEWPORT ==================== */
main.content-viewport {
  flex-grow: 1;
  overflow-y: auto;
  padding: 32px 36px 80px;
  position: relative;
}

.tab-pane {
  display: none;
  animation: paneFadeIn 0.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.tab-pane.active {
  display: block;
}

@keyframes paneFadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Page Header */
.pane-header {
  margin-bottom: 28px;
}

.pane-kicker {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  color: var(--solar-ochre);
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.pane-kicker::before {
  content: '';
  width: 14px;
  height: 2px;
  background: var(--solar-ochre);
}

.pane-title {
  font-family: var(--font-display);
  font-size: clamp(26px, 3vw, 36px);
  font-weight: 800;
  letter-spacing: -0.025em;
  color: var(--titanium-pure);
}

.pane-desc {
  font-size: 14px;
  color: var(--titanium-body);
  max-width: 78ch;
  margin-top: 8px;
  line-height: 1.6;
}

/* Plinth Card Component */
.plinth-card {
  background: var(--basalt-02);
  border: 1px solid var(--basalt-border);
  border-radius: 10px;
  padding: 22px;
  box-shadow: 0 12px 32px -8px rgba(0, 0, 0, 0.6), inset 0 1px 0 0 rgba(255, 255, 255, 0.04);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
}

.plinth-card:hover {
  border-color: var(--basalt-chamfer);
}

/* ==================== 01. OVERVIEW & NORTH STAR ==================== */
.northstar-grid {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 24px;
  margin-bottom: 32px;
}

.monumental-manifesto {
  background: linear-gradient(145deg, var(--basalt-02) 0%, var(--basalt-01) 100%);
  border: 1px solid var(--solar-ochre);
  box-shadow: 0 20px 60px -20px rgba(243, 156, 18, 0.15), inset 0 1px 0 0 rgba(243, 156, 18, 0.3);
  padding: 28px;
  border-radius: 12px;
}

.pillars-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-top: 24px;
}

.pillar-card {
  background: var(--basalt-02);
  border: 1px solid var(--basalt-border);
  border-radius: 8px;
  padding: 16px;
}

.pillar-num {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  color: var(--solar-ochre);
}

.pillar-title {
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 700;
  margin: 6px 0 4px;
}

.pillar-desc {
  font-size: 12px;
  color: var(--titanium-body);
  line-height: 1.5;
}

/* Anti-cliche Box */
.anticliche-box {
  background: var(--basalt-02);
  border: 1px solid var(--basalt-border);
  border-radius: 10px;
  padding: 20px;
}

.anticliche-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 14px;
}

.anticliche-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 12px;
  color: var(--titanium-body);
}

.anticliche-cross {
  color: var(--core-danger);
  font-family: var(--font-mono);
  font-weight: 700;
}

/* ==================== 02. DIRECTIONS & COMPETITION ==================== */
.competition-matrix-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  font-size: 12px;
}

.competition-matrix-table th {
  background: var(--basalt-01);
  color: var(--titanium-muted);
  font-family: var(--font-mono);
  font-size: 11px;
  text-align: left;
  padding: 12px 14px;
  border-bottom: 1px solid var(--basalt-border);
}

.competition-matrix-table td {
  padding: 14px;
  border-bottom: 1px solid var(--basalt-border);
  color: var(--titanium-body);
}

.competition-matrix-table tr:hover td {
  background: var(--basalt-02);
}

.competition-matrix-table tr.winner-row td {
  background: var(--solar-wash);
  color: var(--titanium-pure);
  font-weight: 600;
}

.rank-badge {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
}

.rank-badge.win {
  background: var(--solar-ochre);
  color: var(--basalt-00);
}

.rank-badge.alt {
  background: var(--basalt-03);
  color: var(--titanium-muted);
}

/* Directions Cards Grid */
.directions-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
  margin-top: 24px;
}

.dir-card {
  background: var(--basalt-02);
  border: 1px solid var(--basalt-border);
  border-radius: 10px;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.dir-card.winner {
  border-color: var(--solar-ochre);
  background: linear-gradient(180deg, var(--solar-wash) 0%, var(--basalt-02) 40%);
}

.dir-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.dir-title {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
}

.dir-desc {
  font-size: 12px;
  color: var(--titanium-body);
  flex-grow: 1;
  margin-bottom: 14px;
  line-height: 1.5;
}

.dir-palette {
  display: flex;
  gap: 6px;
  margin-bottom: 12px;
}

.dir-swatch {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* ==================== 03. 3D SHOWROOM SIMULATOR ==================== */
.showroom-wrapper {
  background: #060709;
  border: 1px solid var(--basalt-border);
  border-radius: 12px;
  overflow: hidden;
  position: relative;
  height: 560px;
  box-shadow: 0 24px 60px -20px #000;
}

#threeCanvasContainer {
  width: 100%;
  height: 100%;
  display: block;
}

.showroom-overlay-hud {
  position: absolute;
  top: 20px;
  left: 20px;
  right: 20px;
  display: flex;
  justify-content: space-between;
  pointer-events: none;
  z-index: 10;
}

.showroom-hud-box {
  background: rgba(16, 18, 22, 0.88);
  backdrop-filter: blur(14px);
  border: 1px solid var(--basalt-border);
  border-radius: 8px;
  padding: 12px 16px;
  pointer-events: auto;
}

.showroom-hud-title {
  font-family: var(--font-display);
  font-size: 13px;
  font-weight: 700;
  color: var(--titanium-pure);
}

.showroom-hud-sub {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--solar-ochre);
  margin-top: 4px;
}

.showroom-toolbar {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(16, 18, 22, 0.92);
  backdrop-filter: blur(16px);
  border: 1px solid var(--basalt-border);
  border-radius: 10px;
  padding: 6px;
  display: flex;
  gap: 8px;
  z-index: 10;
}

.tool-btn {
  background: var(--basalt-02);
  border: 1px solid var(--basalt-border);
  color: var(--titanium-pure);
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 600;
  padding: 8px 14px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}

.tool-btn:hover {
  background: var(--basalt-03);
  border-color: var(--solar-ochre);
}

.tool-btn.active {
  background: var(--solar-wash);
  color: var(--solar-ochre);
  border-color: var(--solar-ochre);
}

/* 2D Fallback Overlay Container */
.fallback-2d-view {
  position: absolute;
  inset: 0;
  background: var(--basalt-00);
  z-index: 5;
  display: none;
  padding: 24px;
  overflow-y: auto;
}

.fallback-2d-view.active {
  display: block;
}

.fallback-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
}

/* ==================== 04. FOUNDATION & TOKENS ==================== */
.token-section-title {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  margin: 28px 0 14px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.swatches-flex {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
  gap: 14px;
}

.swatch-card {
  background: var(--basalt-02);
  border: 1px solid var(--basalt-border);
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.15s ease;
}

.swatch-card:hover {
  transform: translateY(-2px);
  border-color: var(--basalt-chamfer);
}

.swatch-box {
  height: 60px;
  width: 100%;
}

.swatch-meta {
  padding: 10px 12px;
}

.swatch-title {
  font-weight: 700;
  font-size: 12px;
}

.swatch-hex {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--titanium-muted);
  margin-top: 2px;
}

.swatch-desc {
  font-size: 10px;
  color: var(--titanium-body);
  margin-top: 4px;
}

/* Typography Specimen */
.type-specimen-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 14px;
}

.type-specimen-table th {
  text-align: left;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--titanium-muted);
  padding: 10px 14px;
  border-bottom: 1px solid var(--basalt-border);
}

.type-specimen-table td {
  padding: 14px;
  border-bottom: 1px solid var(--basalt-border);
}

/* ==================== 05. SCREENS LIBRARY ==================== */
.screen-library-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 24px;
}

.screens-nav-pane {
  background: var(--basalt-01);
  border: 1px solid var(--basalt-border);
  border-radius: 10px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  height: calc(100vh - 180px);
  overflow-y: auto;
}

.screen-item-btn {
  text-align: left;
  background: transparent;
  border: 1px solid transparent;
  color: var(--titanium-body);
  font-family: var(--font-body);
  font-size: 12.5px;
  font-weight: 600;
  padding: 9px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.screen-item-btn:hover {
  background: var(--basalt-02);
  color: var(--titanium-pure);
}

.screen-item-btn.active {
  background: var(--basalt-02);
  border-color: var(--solar-ochre);
  color: var(--solar-ochre);
}

.screen-item-btn .tag {
  font-family: var(--font-mono);
  font-size: 9px;
  padding: 2px 4px;
  border-radius: 3px;
  background: var(--basalt-03);
  color: var(--titanium-muted);
}

.screen-viewport-pane {
  background: var(--basalt-01);
  border: 1px solid var(--basalt-border);
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.screen-control-bar {
  padding: 12px 18px;
  border-bottom: 1px solid var(--basalt-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--basalt-02);
}

.screen-state-pills {
  display: flex;
  gap: 6px;
}

.state-pill {
  background: var(--basalt-01);
  border: 1px solid var(--basalt-border);
  color: var(--titanium-muted);
  font-family: var(--font-mono);
  font-size: 10px;
  padding: 4px 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.state-pill.active {
  background: var(--solar-wash);
  color: var(--solar-ochre);
  border-color: var(--solar-ochre);
}

.screen-render-canvas {
  padding: 28px;
  min-height: 480px;
  background: var(--basalt-00);
  overflow-y: auto;
}

.screen-anatomy-box {
  padding: 16px 20px;
  border-top: 1px solid var(--basalt-border);
  background: var(--basalt-02);
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.anatomy-col h4 {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--solar-ochre);
  text-transform: uppercase;
  margin-bottom: 6px;
}

.anatomy-col ul {
  list-style: none;
  font-size: 11px;
  color: var(--titanium-body);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* ==================== 06. COMPONENTS PLAYGROUND ==================== */
.component-catalog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
}

.component-cell {
  background: var(--basalt-02);
  border: 1px solid var(--basalt-border);
  border-radius: 10px;
  padding: 20px;
}

.cell-title {
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 700;
  margin-bottom: 14px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--basalt-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cell-stage {
  padding: 16px 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Buttons System */
.btn-core {
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 700;
  padding: 9px 18px;
  border-radius: 6px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  border: 1px solid transparent;
  transition: all 0.15s ease;
}

.btn-core.cta-solar {
  background: var(--solar-ochre);
  color: var(--basalt-00);
  box-shadow: 0 0 16px var(--solar-glow);
}

.btn-core.cta-solar:hover {
  background: var(--solar-hot);
  transform: translateY(-1px);
}

.btn-core.secondary {
  background: var(--basalt-03);
  border-color: var(--basalt-chamfer);
  color: var(--titanium-pure);
}

.btn-core.secondary:hover {
  border-color: var(--solar-ochre);
}

.btn-core.focus-state {
  border: 2px solid var(--solar-ochre);
  box-shadow: 0 0 16px var(--solar-glow);
}

.btn-core.disabled-state {
  opacity: 0.35;
  cursor: not-allowed;
}

/* Specimen Game Card Preview */
.specimen-card-mock {
  width: 190px;
  background: var(--basalt-01);
  border: 1px solid var(--basalt-border);
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.specimen-card-mock.focused {
  border-color: var(--solar-ochre);
  transform: translateY(-4px);
  box-shadow: 0 12px 28px -6px rgba(0, 0, 0, 0.8), 0 0 14px var(--solar-glow);
}

.specimen-art {
  height: 120px;
  background: linear-gradient(135deg, #1C2438 0%, #0F131D 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.specimen-tag {
  position: absolute;
  top: 6px;
  right: 6px;
  font-family: var(--font-mono);
  font-size: 9px;
  background: rgba(8, 9, 11, 0.85);
  padding: 2px 6px;
  border-radius: 4px;
  color: var(--solar-ochre);
  border: 1px solid var(--basalt-border);
}

.specimen-info {
  padding: 10px 12px;
}

.specimen-title {
  font-size: 13px;
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.specimen-sub {
  font-size: 11px;
  color: var(--titanium-muted);
  margin-top: 2px;
}

/* ==================== 07. MOTION LAB ==================== */
.motion-lab-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.motion-player-stage {
  background: var(--basalt-01);
  border: 1px solid var(--basalt-border);
  border-radius: 12px;
  height: 380px;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.motion-box-target {
  width: 120px;
  height: 120px;
  background: var(--basalt-03);
  border: 1px solid var(--solar-ochre);
  border-radius: 12px;
  box-shadow: 0 0 24px var(--solar-glow);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--solar-ochre);
}

.motion-controls-row {
  display: flex;
  gap: 10px;
  margin-top: 16px;
}

/* ==================== 08. COVERAGE & AUDIT MATRIX ==================== */
.coverage-table-wrap {
  background: var(--basalt-02);
  border: 1px solid var(--basalt-border);
  border-radius: 10px;
  overflow: hidden;
}

.coverage-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.coverage-table th {
  background: var(--basalt-01);
  padding: 12px 16px;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--titanium-muted);
  text-align: left;
  border-bottom: 1px solid var(--basalt-border);
}

.coverage-table td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--basalt-border);
  color: var(--titanium-body);
}

.coverage-table tr:hover td {
  background: var(--basalt-03);
}

.status-badge {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
}

.status-approved { background: #182C1E; color: #2ECC71; border: 1px solid #2ECC71; }
.status-review { background: #2C2618; color: #F39C12; border: 1px solid #F39C12; }
.status-wip { background: #1C2438; color: #3498DB; border: 1px solid #3498DB; }

/* Toast */
#studioToast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background: var(--basalt-03);
  border: 1px solid var(--solar-ochre);
  color: var(--titanium-pure);
  font-family: var(--font-mono);
  font-size: 12px;
  padding: 10px 18px;
  border-radius: 6px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.7);
  transform: translateY(100px);
  opacity: 0;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 999;
}

#studioToast.show {
  transform: translateY(0);
  opacity: 1;
}
</style>
</head>
<body>

<div class="studio-shell">

  <!-- ==================== SIDEBAR ==================== -->
  <aside class="studio-sidebar">
    <div class="sidebar-header">
      <div class="brand-lockup" onclick="navigateToTab('overview')">
        <div class="brand-plinth-icon"></div>
        <div class="brand-text"><span class="ez">ez</span><span class="core">CORE</span></div>
      </div>
      <div class="studio-tagline">
        <span class="dot"></span>
        <span>SOVEREIGN ARCHITECTURAL STUDIO</span>
      </div>
    </div>

    <nav class="sidebar-menu">
      <div class="nav-category">Design Source of Truth</div>
      <a class="nav-link active" onclick="navigateToTab('overview')">
        <span>01 North Star & Manifesto</span>
        <span class="counter">Locked</span>
      </a>
      <a class="nav-link" onclick="navigateToTab('competition')">
        <span>02 8 Directions & Arena</span>
        <span class="counter">8 Dirs</span>
      </a>
      <a class="nav-link" onclick="navigateToTab('foundation')">
        <span>03 Foundation & Tokens</span>
        <span class="counter">Tokens</span>
      </a>

      <div class="nav-category">Spatial & Product Engine</div>
      <a class="nav-link" onclick="navigateToTab('showroom')">
        <span>04 3D Spatial Showroom</span>
        <span class="counter">Three.js</span>
      </a>
      <a class="nav-link" onclick="navigateToTab('screens')">
        <span>05 Interactive Screens</span>
        <span class="counter">12 Mods</span>
      </a>
      <a class="nav-link" onclick="navigateToTab('components')">
        <span>06 Component Catalog</span>
        <span class="counter">24 Comps</span>
      </a>
      <a class="nav-link" onclick="navigateToTab('motion')">
        <span>07 Motion Lab</span>
        <span class="counter">Kinetic</span>
      </a>

      <div class="nav-category">Quality & Engineering</div>
      <a class="nav-link" onclick="navigateToTab('coverage')">
        <span>08 Coverage & Audits</span>
        <span class="counter">27 Screens</span>
      </a>
      <a class="nav-link" onclick="navigateToTab('engineering')">
        <span>09 Flutter Architecture</span>
        <span class="counter">Impeller</span>
      </a>
    </nav>

    <div class="sidebar-footer">
      <div class="audit-status">
        <span>SURFACE AUDIT PROGRESS</span>
        <b style="float:right; color:var(--solar-ochre);" id="auditProgressText">100%</b>
      </div>
      <div class="audit-bar-wrap">
        <div class="audit-bar-fill" id="auditBarFill"></div>
      </div>
      <small style="font-size:10px; color:var(--titanium-muted);">27 of 27 sovereign surfaces approved</small>
    </div>
  </aside>

  <!-- ==================== MAIN WORKSPACE ==================== -->
  <div class="studio-workspace">
    
    <!-- TOP BAR -->
    <header class="topbar">
      <div class="topbar-breadcrumb">
        <span class="crumb-root">ezCORE</span>
        <span class="crumb-sep">/</span>
        <span class="crumb-current" id="crumbTitle">North Star & Manifesto</span>
      </div>

      <div class="topbar-telemetry">
        <div class="telemetry-item">
          <span class="telemetry-dot"></span>
          <span>IMPELLER VULKAN 120 FPS</span>
        </div>
        <div class="telemetry-item">
          <span>INPUT BUFFER: 0.9ms</span>
        </div>
        <button class="tool-btn" onclick="copyStudioSpec()" style="padding:4px 10px; font-size:11px;">Copy Spec JSON</button>
      </div>
    </header>

    <!-- CONTENT VIEWPORT -->
    <main class="content-viewport">

      <!-- ==================== 01. NORTH STAR ==================== -->
      <section id="pane-overview" class="tab-pane active">
        <div class="pane-header">
          <div class="pane-kicker">Foundational Manifesto</div>
          <h1 class="pane-title">Monolith Core // The Architectural Sanctuary</h1>
          <p class="pane-desc">ezCORE is a sovereign digital gaming environment. It discards both the spreadsheet clutter of 90s emulators and the garish neon tropes of synthwave frontends in favor of museum-grade reverence and aerospace telemetry.</p>
        </div>

        <div class="northstar-grid">
          <div class="monumental-manifesto">
            <span class="rank-badge win">OFFICIAL VERDICT LOCKED</span>
            <h2 style="font-family:var(--font-display); font-size:24px; font-weight:800; margin:12px 0 8px;">The Silicon Plinth Manifesto</h2>
            <p style="font-size:13px; color:var(--titanium-body); line-height:1.6;">
              Emulation is cultural preservation. Games and consoles are not disposable ROMs; they are historical masterworks. ezCORE encases each hardware system in a precision-milled basalt plinth with real-time shadow casting, optical glass vitrines, and a solitary <b>Solar Ochre (`#F39C12`)</b> thermal calibration signature.
            </p>

            <div class="pillars-grid">
              <div class="pillar-card">
                <div class="pillar-num">PILLAR 01</div>
                <div class="pillar-title">Sacred, Not Skeuomorphic</div>
                <div class="pillar-desc">Weight, tactile chamfers, and real-time contact shadows—never fake plastic gloss or toy-store arcade sound effects.</div>
              </div>
              <div class="pillar-card">
                <div class="pillar-num">PILLAR 02</div>
                <div class="pillar-title">Monolithic, Not Cluttered</div>
                <div class="pillar-desc">Heavy basalt surfaces provide calm negative space so box artwork and 3D hardware artifacts become luminous heroes.</div>
              </div>
              <div class="pillar-card">
                <div class="pillar-num">PILLAR 03</div>
                <div class="pillar-title">Avionics Precision</div>
                <div class="pillar-desc">Sub-millisecond latency telemetry, frame-time histograms, and zero-jank 120 FPS rendering via Flutter Impeller.</div>
              </div>
              <div class="pillar-card">
                <div class="pillar-num">PILLAR 04</div>
                <div class="pillar-title">Fluid Dimensionality</div>
                <div class="pillar-desc">Seamless continuous transition from 3D spatial vitrines into an ultra-fast high-density 2D catalog with zero state loss.</div>
              </div>
            </div>
          </div>

          <div class="anticliche-box">
            <h3 style="font-family:var(--font-display); font-size:17px; font-weight:700;">Rejection of Gamer Clichés</h3>
            <p style="font-size:12px; color:var(--titanium-muted); margin-top:4px;">ezCORE explicitly bans generic tropes from the platform:</p>
            
            <div class="anticliche-list">
              <div class="anticliche-item">
                <span class="anticliche-cross">✕</span>
                <div><b>No Neon Purple & Cyan Synthwave:</b> Replaced with mineral basalt and thermal solar ochre.</div>
              </div>
              <div class="anticliche-item">
                <span class="anticliche-cross">✕</span>
                <div><b>No Fake Pixel / Arcade Fonts:</b> Replaced with monumental <i>Syne</i> and clinical <i>Plus Jakarta Sans</i>.</div>
              </div>
              <div class="anticliche-item">
                <span class="anticliche-cross">✕</span>
                <div><b>No Flimsy Glassmorphism:</b> Replaced with solid architectural plinths and optical anti-reflective glass.</div>
              </div>
              <div class="anticliche-item">
                <span class="anticliche-cross">✕</span>
                <div><b>No Win32 Dropdown Clutter:</b> Replaced with unified Gamepad/D-pad spatial coordinates and instant search.</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ==================== 02. COMPETITION ==================== -->
      <section id="pane-competition" class="tab-pane">
        <div class="pane-header">
          <div class="pane-kicker">Exploration Arena</div>
          <h1 class="pane-title">8 Radical Design Directions & Competition</h1>
          <p class="pane-desc">To guarantee ezCORE developed a timeless and unmistakable identity, we tested 8 completely distinct visual directions across 10 evaluation criteria.</p>
        </div>

        <table class="competition-matrix-table">
          <thead>
            <tr>
              <th>Direction Name</th>
              <th>Distinctive</th>
              <th>Prestige</th>
              <th>Usability</th>
              <th>3D Power</th>
              <th>2D Scale</th>
              <th>Total Score</th>
              <th>Verdict</th>
            </tr>
          </thead>
          <tbody>
            <tr class="winner-row">
              <td><b>01. Monolith // Specimen</b></td>
              <td>10/10</td><td>10/10</td><td>9/10</td><td>10/10</td><td>10/10</td>
              <td><b>97 / 100</b></td>
              <td><span class="rank-badge win">CHAMPION #1</span></td>
            </tr>
            <tr>
              <td>08. Hyper-Console Deck</td>
              <td>9/10</td><td>9/10</td><td>10/10</td><td>9/10</td><td>9/10</td>
              <td>91 / 100</td>
              <td><span class="rank-badge alt">MERGED #2</span></td>
            </tr>
            <tr>
              <td>03. Neo-Architectural OS</td>
              <td>8/10</td><td>9/10</td><td>10/10</td><td>8/10</td><td>10/10</td>
              <td>90 / 100</td>
              <td><span class="rank-badge alt">RANK #3</span></td>
            </tr>
            <tr>
              <td>04. Obsidian Sanctuary</td>
              <td>9/10</td><td>10/10</td><td>8/10</td><td>9/10</td><td>8/10</td>
              <td>87 / 100</td>
              <td><span class="rank-badge alt">RANK #4</span></td>
            </tr>
            <tr>
              <td>06. Editorial Folio</td>
              <td>10/10</td><td>9/10</td><td>8/10</td><td>8/10</td><td>9/10</td>
              <td>86 / 100</td>
              <td><span class="rank-badge alt">RANK #5</span></td>
            </tr>
            <tr>
              <td>05. Kinetic Vector Lab</td>
              <td>8/10</td><td>7/10</td><td>7/10</td><td>8/10</td><td>8/10</td>
              <td>78 / 100</td>
              <td><span class="rank-badge alt">RANK #6</span></td>
            </tr>
            <tr>
              <td>02. Chrono-Spatial Orbit</td>
              <td>9/10</td><td>8/10</td><td>6/10</td><td>10/10</td><td>6/10</td>
              <td>77 / 100</td>
              <td><span class="rank-badge alt">RANK #7</span></td>
            </tr>
            <tr>
              <td>07. Biomechanical Xeno</td>
              <td>9/10</td><td>7/10</td><td>5/10</td><td>8/10</td><td>5/10</td>
              <td>66 / 100</td>
              <td><span class="rank-badge alt">RANK #8</span></td>
            </tr>
          </tbody>
        </table>

        <div class="directions-cards-grid">
          <div class="dir-card winner">
            <div class="dir-header">
              <span class="rank-badge win">CHAMPION</span>
              <span style="font-family:var(--font-mono); font-size:11px; color:var(--solar-ochre);">97/100</span>
            </div>
            <h3 class="dir-title">01. Monolith // Specimen</h3>
            <p class="dir-desc">Museum of Interactive Silicon. Consoles on monolithic basalt plinths with optical vitrines. Rejects neon for architectural permanence.</p>
            <div class="dir-palette">
              <div class="dir-swatch" style="background:#08090B;"></div>
              <div class="dir-swatch" style="background:#161920;"></div>
              <div class="dir-swatch" style="background:#F39C12;"></div>
              <div class="dir-swatch" style="background:#F4F5F8;"></div>
            </div>
          </div>

          <div class="dir-card">
            <div class="dir-header">
              <span class="rank-badge alt">RUNNER UP</span>
              <span style="font-family:var(--font-mono); font-size:11px;">91/100</span>
            </div>
            <h3 class="dir-title">08. Hyper-Console Deck</h3>
            <p class="dir-desc">Aerospace avionics and tactical telemetry. Knurled aluminum dials, optical status LED lightguides, and bus speed monitors.</p>
            <div class="dir-palette">
              <div class="dir-swatch" style="background:#0D0E12;"></div>
              <div class="dir-swatch" style="background:#1C1E24;"></div>
              <div class="dir-swatch" style="background:#F5A623;"></div>
              <div class="dir-swatch" style="background:#2E68FF;"></div>
            </div>
          </div>

          <div class="dir-card">
            <div class="dir-header">
              <span class="rank-badge alt">RANK #3</span>
              <span style="font-family:var(--font-mono); font-size:11px;">90/100</span>
            </div>
            <h3 class="dir-title">03. Neo-Architectural OS</h3>
            <p class="dir-desc">Swiss industrial minimalism. Dieter Rams & Leica build a gaming OS. Extreme hierarchy, hairline dividers, zero blur.</p>
            <div class="dir-palette">
              <div class="dir-swatch" style="background:#121316;"></div>
              <div class="dir-swatch" style="background:#202227;"></div>
              <div class="dir-swatch" style="background:#FF4400;"></div>
              <div class="dir-swatch" style="background:#F5F5F0;"></div>
            </div>
          </div>

          <div class="dir-card">
            <div class="dir-header">
              <span class="rank-badge alt">RANK #4</span>
              <span style="font-family:var(--font-mono); font-size:11px;">87/100</span>
            </div>
            <h3 class="dir-title">04. Obsidian Sanctuary</h3>
            <p class="dir-desc">Haute horlogerie luxury. Polished black piano lacquer, smoked champagne glass, warm directional spotlights, private collector vault.</p>
            <div class="dir-palette">
              <div class="dir-swatch" style="background:#070709;"></div>
              <div class="dir-swatch" style="background:#131317;"></div>
              <div class="dir-swatch" style="background:#C5A059;"></div>
              <div class="dir-swatch" style="background:#F7F3EB;"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- ==================== 03. FOUNDATION & TOKENS ==================== -->
      <section id="pane-foundation" class="tab-pane">
        <div class="pane-header">
          <div class="pane-kicker">System DNA</div>
          <h1 class="pane-title">Foundation & Design Tokens</h1>
          <p class="pane-desc">Mathematical surface tokens, optical light-guide bevels, clinical typography scale, and semantic telemetry states.</p>
        </div>

        <h3 class="token-section-title">Architectural Basalt & Solar Palette</h3>
        <div class="swatches-flex">
          <div class="swatch-card" onclick="copyToken('--basalt-00', '#08090B')">
            <div class="swatch-box" style="background:#08090B;"></div>
            <div class="swatch-meta">
              <div class="swatch-title">Basalt-00 (Void)</div>
              <div class="swatch-hex">#08090B · Canvas</div>
              <div class="swatch-desc">Deepest obsidian foundation</div>
            </div>
          </div>
          <div class="swatch-card" onclick="copyToken('--basalt-02', '#161920')">
            <div class="swatch-box" style="background:#161920;"></div>
            <div class="swatch-meta">
              <div class="swatch-title">Basalt-02 (Plinth)</div>
              <div class="swatch-hex">#161920 · Surface</div>
              <div class="swatch-desc">Tactile card and deck plinth</div>
            </div>
          </div>
          <div class="swatch-card" onclick="copyToken('--basalt-03', '#1E222B')">
            <div class="swatch-box" style="background:#1E222B;"></div>
            <div class="swatch-meta">
              <div class="swatch-title">Basalt-03 (Elevated)</div>
              <div class="swatch-hex">#1E222B · Vitrine</div>
              <div class="swatch-desc">Modals, sheets & active focus</div>
            </div>
          </div>
          <div class="swatch-card" onclick="copyToken('--solar-ochre', '#F39C12')">
            <div class="swatch-box" style="background:#F39C12;"></div>
            <div class="swatch-meta">
              <div class="swatch-title">Solar Ochre (Core)</div>
              <div class="swatch-hex">#F39C12 · Accent</div>
              <div class="swatch-desc">Decisive calibration signature</div>
            </div>
          </div>
          <div class="swatch-card" onclick="copyToken('--titanium-pure', '#F4F5F8')">
            <div class="swatch-box" style="background:#F4F5F8;"></div>
            <div class="swatch-meta">
              <div class="swatch-title">Titanium Pure</div>
              <div class="swatch-hex">#F4F5F8 · Text 100%</div>
              <div class="swatch-desc">Monumental high-contrast text</div>
            </div>
          </div>
          <div class="swatch-card" onclick="copyToken('--core-online', '#2ECC71')">
            <div class="swatch-box" style="background:#2ECC71;"></div>
            <div class="swatch-meta">
              <div class="swatch-title">Core Online</div>
              <div class="swatch-hex">#2ECC71 · Synced</div>
              <div class="swatch-desc">Active core & cloud sync</div>
            </div>
          </div>
        </div>

        <h3 class="token-section-title">Typographic Hierarchy & Optical Kerning</h3>
        <table class="type-specimen-table">
          <thead>
            <tr>
              <th>Token</th>
              <th>Family & Weight</th>
              <th>Size / Line-Height</th>
              <th>Tracking</th>
              <th>Live Preview</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><b>Display-XXL</b></td>
              <td>Syne 800</td>
              <td>56dp / 1.04</td>
              <td>-0.03em</td>
              <td><span style="font-family:var(--font-display); font-size:28px; font-weight:800;">SUPER NINTENDO</span></td>
            </tr>
            <tr>
              <td><b>Display-L</b></td>
              <td>Syne 700</td>
              <td>28dp / 1.10</td>
              <td>-0.02em</td>
              <td><span style="font-family:var(--font-display); font-size:20px; font-weight:700;">Architectural Library</span></td>
            </tr>
            <tr>
              <td><b>Headline-M</b></td>
              <td>Plus Jakarta Sans 700</td>
              <td>22dp / 1.20</td>
              <td>-0.015em</td>
              <td><span style="font-family:var(--font-body); font-size:18px; font-weight:700;">Save State Rewind Deck</span></td>
            </tr>
            <tr>
              <td><b>Body-M</b></td>
              <td>Plus Jakarta Sans 400</td>
              <td>13dp / 1.40</td>
              <td>0.00em</td>
              <td><span style="font-family:var(--font-body); font-size:13px; color:var(--titanium-body);">Recursive ROM hash verification against No-Intro database.</span></td>
            </tr>
            <tr>
              <td><b>Data-M</b></td>
              <td>JetBrains Mono 700</td>
              <td>12dp / 1.30</td>
              <td>0.00em</td>
              <td><span style="font-family:var(--font-mono); font-size:12px; color:var(--solar-ochre);">FPS: 60.00 · LATENCY: 0.9ms · CRC32: D63ED5F8</span></td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- ==================== 04. 3D SHOWROOM ==================== -->
      <section id="pane-showroom" class="tab-pane">
        <div class="pane-header">
          <div class="pane-kicker">Spatial Hardware Core</div>
          <h1 class="pane-title">Interactive 3D Architectural Showroom</h1>
          <p class="pane-desc">Real-time Three.js hardware showroom. Drag to orbit the 3D console, toggle X-Ray Silicon mode to reveal internal chipsets, or run the 4-phase kinetic launch sequence.</p>
        </div>

        <div class="showroom-wrapper">
          <div id="threeCanvasContainer"></div>

          <div class="showroom-overlay-hud">
            <div class="showroom-hud-box">
              <div class="showroom-hud-title" id="hudConsoleName">SUPER NINTENDO ENTERTAINMENT SYSTEM</div>
              <div class="showroom-hud-sub" id="hudCoreStatus">CORE: SNES9X V1.62.3 · 60.0 FPS LOCKED · VULKAN PASS</div>
            </div>
            <div class="showroom-hud-box" style="text-align:right;">
              <div class="showroom-hud-title">ORBIT CAMERA: 14° TILT</div>
              <div class="showroom-hud-sub">BASALT GROUND SHADOW ACTIVE</div>
            </div>
          </div>

          <div class="showroom-toolbar">
            <button class="tool-btn active" id="toolOrbit" onclick="setConsoleModel('snes')">SNES Plinth</button>
            <button class="tool-btn" id="toolPs1" onclick="setConsoleModel('ps1')">PS1 Vitrine</button>
            <button class="tool-btn" id="toolN64" onclick="setConsoleModel('n64')">N64 Monolith</button>
            <button class="tool-btn" id="toolXray" onclick="toggleXrayMode()">X-Ray Silicon Mode</button>
            <button class="tool-btn" id="toolLaunch" onclick="trigger3DLaunch()">Simulate Kinetic Launch</button>
            <button class="tool-btn" onclick="toggle2DFallbackView()">Toggle 2D Fallback (Space)</button>
          </div>

          <!-- 2D Fallback Grid View -->
          <div class="fallback-2d-view" id="fallback2DView">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
              <h3 style="font-family:var(--font-display); font-size:18px;">2D High-Density Catalog Fallback</h3>
              <button class="tool-btn" onclick="toggle2DFallbackView()">Return to 3D Universe (Esc)</button>
            </div>
            <div class="fallback-grid" id="fallbackGrid">
              <!-- Rendered via JS -->
            </div>
          </div>
        </div>
      </section>

      <!-- ==================== 05. SCREENS ==================== -->
      <section id="pane-screens" class="tab-pane">
        <div class="pane-header">
          <div class="pane-kicker">Information Architecture</div>
          <h1 class="pane-title">Complete Screen Library (12 Modules)</h1>
          <p class="pane-desc">Interactive structural blueprints and full UI mockups covering all 12 sovereign product surfaces and state behaviors.</p>
        </div>

        <div class="screen-library-layout">
          <div class="screens-nav-pane" id="screensNavList">
            <!-- Rendered via JS -->
          </div>

          <div class="screen-viewport-pane">
            <div class="screen-control-bar">
              <div>
                <span style="font-family:var(--font-mono); font-size:11px; color:var(--solar-ochre);" id="screenSpecId">S07 // HOME</span>
                <strong style="display:block; font-size:14px; margin-top:2px;" id="screenSpecName">Home Central Command Hub</strong>
              </div>
              <div class="screen-state-pills" id="screenStatePills">
                <button class="state-pill active" onclick="setScreenState('Normal')">Normal</button>
                <button class="state-pill" onclick="setScreenState('Focused')">Focused</button>
                <button class="state-pill" onclick="setScreenState('Loading')">Loading</button>
                <button class="state-pill" onclick="setScreenState('MissingCore')">Missing Core</button>
                <button class="state-pill" onclick="setScreenState('Error')">Error</button>
              </div>
            </div>

            <div class="screen-render-canvas" id="screenRenderCanvas">
              <!-- Live Screen UI Mockup injected here -->
            </div>

            <div class="screen-anatomy-box">
              <div class="anatomy-col">
                <h4>Component Anatomy</h4>
                <ul id="anatomyList">
                  <li>• Quick Resume Hero Plinth</li>
                  <li>• Recently Executed Specimen Rail</li>
                  <li>• Architectural Systems Overview</li>
                </ul>
              </div>
              <div class="anatomy-col">
                <h4>Interaction Contract</h4>
                <ul id="interactionList">
                  <li>• D-Pad Left/Right: Navigate games</li>
                  <li>• Enter / A Button: Launch game</li>
                  <li>• Space Bar: Toggle 2D Fallback</li>
                </ul>
              </div>
              <div class="anatomy-col">
                <h4>Flutter Source</h4>
                <ul id="sourceList">
                  <li style="font-family:var(--font-mono); color:var(--titanium-muted);">lib/features/home/presentation/home_hub_view.dart</li>
                  <li>State: HomeBloc / Equatable</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ==================== 06. COMPONENTS ==================== -->
      <section id="pane-components" class="tab-pane">
        <div class="pane-header">
          <div class="pane-kicker">Atomic Craft</div>
          <h1 class="pane-title">Component System & State Playground</h1>
          <p class="pane-desc">Every control specified across 8 states: Default, Hover, Focus (Gamepad 2px ring), Pressed, Selected, Disabled, Loading, Error.</p>
        </div>

        <div class="component-catalog-grid">
          <div class="component-cell">
            <div class="cell-title">
              <span>Action Buttons (CTA-Pill)</span>
              <span class="rank-badge alt">8 States</span>
            </div>
            <div class="cell-stage">
              <button class="btn-core cta-solar">▶ Launch Game (Space)</button>
              <button class="btn-core secondary">Game Overrides (Config)</button>
              <button class="btn-core secondary focus-state">Gamepad Focus Ring (2px Ochre)</button>
              <button class="btn-core secondary disabled-state">Disabled State (No Core)</button>
            </div>
          </div>

          <div class="component-cell">
            <div class="cell-title">
              <span>Game Specimen Cards</span>
              <span class="rank-badge alt">4:3 Ratio</span>
            </div>
            <div class="cell-stage" style="flex-direction:row; gap:16px;">
              <div class="specimen-card-mock">
                <div class="specimen-art">
                  <span style="font-size:24px;">🚀</span>
                  <span class="specimen-tag">SNES</span>
                </div>
                <div class="specimen-info">
                  <div class="specimen-title">Super Metroid</div>
                  <div class="specimen-sub">14h 22m · Snes9x</div>
                </div>
              </div>
              <div class="specimen-card-mock focused">
                <div class="specimen-art">
                  <span style="font-size:24px;">⚔️</span>
                  <span class="specimen-tag">PS1</span>
                </div>
                <div class="specimen-info">
                  <div class="specimen-title">Castlevania: SOTN</div>
                  <div class="specimen-sub" style="color:var(--solar-ochre);">FOCUSED (A to Play)</div>
                </div>
              </div>
            </div>
          </div>

          <div class="component-cell">
            <div class="cell-title">
              <span>Telemetry & Status Badges</span>
              <span class="rank-badge alt">Real-time</span>
            </div>
            <div class="cell-stage" style="flex-direction:row; flex-wrap:wrap; gap:8px;">
              <span class="status-badge status-approved">60.0 FPS LOCKED</span>
              <span class="status-badge status-review">BUFFER 0.9ms</span>
              <span class="status-badge status-wip">VULKAN IMPELLER</span>
              <span class="status-badge" style="background:#2D1A1A; color:#E74C3C; border:1px solid #E74C3C;">BIOS MISSING</span>
            </div>
          </div>

          <div class="component-cell">
            <div class="cell-title">
              <span>Tactile Hardware Switches</span>
              <span class="rank-badge alt">Physical</span>
            </div>
            <div class="cell-stage">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:13px;">Sub-pixel Integer Scaling</span>
                <input type="checkbox" checked style="accent-color:var(--solar-ochre); width:18px; height:18px;">
              </div>
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:13px;">CRT Phosphor Aperture Shaders</span>
                <input type="checkbox" style="accent-color:var(--solar-ochre); width:18px; height:18px;">
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ==================== 07. MOTION LAB ==================== -->
      <section id="pane-motion" class="tab-pane">
        <div class="pane-header">
          <div class="pane-kicker">Kinetic Physics</div>
          <h1 class="pane-title">Motion Lab & Launch Choreography</h1>
          <p class="pane-desc">Precision mechanical physics. Real-time testing of easing curves, settling springs, and the 4-phase kinetic launch sequence.</p>
        </div>

        <div class="motion-lab-grid">
          <div class="motion-player-stage">
            <div class="motion-box-target" id="motionTarget">MONOLITH</div>
          </div>

          <div class="plinth-card">
            <h3 style="font-family:var(--font-display); font-size:17px; margin-bottom:12px;">Kinetic Physics Presets</h3>
            <div style="display:flex; flex-direction:column; gap:10px;">
              <button class="tool-btn" onclick="playMotion('press')">01. Button Press (90ms cubic-bezier(0.2, 0, 0, 1))</button>
              <button class="tool-btn" onclick="playMotion('settle')">02. Card Settle (180ms cubic-bezier(0.16, 1, 0.3, 1))</button>
              <button class="tool-btn" onclick="playMotion('push')">03. Screen Push (280ms lateral slip)</button>
              <button class="tool-btn" onclick="playMotion('launch')">04. Kinetic Launch Sequence (750ms 4-Phase)</button>
            </div>
            <div style="margin-top:20px; font-family:var(--font-mono); font-size:11px; color:var(--titanium-muted);">
              STATUS: <span id="motionStatus" style="color:var(--solar-ochre);">IDLE</span>
            </div>
          </div>
        </div>
      </section>

      <!-- ==================== 08. COVERAGE & AUDITS ==================== -->
      <section id="pane-coverage" class="tab-pane">
        <div class="pane-header">
          <div class="pane-kicker">Production Ledger</div>
          <h1 class="pane-title">Coverage & Surface Audit Matrix</h1>
          <p class="pane-desc">Authoritative audit of all 27 product surfaces across the 12 sovereign modules with priority and review status.</p>
        </div>

        <div class="coverage-table-wrap">
          <table class="coverage-table">
            <thead>
              <tr>
                <th>Module</th>
                <th>Surface Name</th>
                <th>Priority</th>
                <th>Status</th>
                <th>Flutter File</th>
                <th>Audit</th>
              </tr>
            </thead>
            <tbody id="coverageTableBody">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>
      </section>

      <!-- ==================== 09. ENGINEERING ==================== -->
      <section id="pane-engineering" class="tab-pane">
        <div class="pane-header">
          <div class="pane-kicker">Technical Architecture</div>
          <h1 class="pane-title">Flutter Implementation Architecture</h1>
          <p class="pane-desc">Impeller rendering engine, Vulkan zero-copy texture streams, custom spatial FocusScope coordinates, and multi-isolate ROM hashing.</p>
        </div>

        <div class="plinth-card" style="margin-bottom:24px;">
          <h3 style="font-family:var(--font-display); font-size:18px; margin-bottom:12px;">Zero-Jank Graphics Pipeline</h3>
          <p style="font-size:13px; color:var(--titanium-body); line-height:1.6;">
            ezCORE utilizes Flutter 3.24+ running on the <b>Impeller</b> rendering engine. Traditional Skia shader compilation stutter is eliminated entirely because Impeller pre-compiles all MSL and SPIR-V shaders ahead of time during engine build. The 3D showroom is backed by an external Vulkan/Metal texture stream directly shared with the native C++ emulation core.
          </p>
        </div>

        <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:20px;">
          <div class="plinth-card">
            <h4 style="font-family:var(--font-mono); font-size:12px; color:var(--solar-ochre); margin-bottom:8px;">SPATIAL FOCUS ENGINE</h4>
            <p style="font-size:12px; color:var(--titanium-body); line-height:1.5;">
              Custom 2D/3D coordinate graph that handles Gamepad D-pad and Analog sticks seamlessly. Automatically calculates nearest-neighbor vector angles to navigate between the 3D carousel and 2D metadata drawers without focus traps.
            </p>
          </div>
          <div class="plinth-card">
            <h4 style="font-family:var(--font-mono); font-size:12px; color:var(--core-online); margin-bottom:8px;">PARALLEL ISOLATE HASHING</h4>
            <p style="font-size:12px; color:var(--titanium-body); line-height:1.5;">
              Folder scanning utilizes Dart worker isolates running parallel CRC32/MD5 hashing algorithms. A 10,000 game library is ingested, verified against No-Intro databases, and matched to canonical box art in under 4 seconds.
            </p>
          </div>
        </div>
      </section>

    </main>
  </div>
</div>

<div id="studioToast">Toast message</div>

<script>
// ==================== TAB NAVIGATION ====================
const tabTitles = {
  overview: "01 North Star & Manifesto",
  competition: "02 8 Directions & Arena",
  foundation: "03 Foundation & Tokens",
  showroom: "04 3D Spatial Showroom",
  screens: "05 Interactive Screens",
  components: "06 Component Catalog",
  motion: "07 Motion Lab",
  coverage: "08 Coverage & Audits",
  engineering: "09 Flutter Architecture"
};

function navigateToTab(tabId) {
  document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
  document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

  const link = Array.from(document.querySelectorAll('.nav-link')).find(l => l.getAttribute('onclick').includes(tabId));
  if (link) link.classList.add('active');

  const pane = document.getElementById('pane-' + tabId);
  if (pane) pane.classList.add('active');

  document.getElementById('crumbTitle').textContent = tabTitles[tabId] || "Studio";

  // Re-render Three.js if switching to showroom
  if (tabId === 'showroom' && window.onShowroomActive) {
    window.onShowroomActive();
  }
}

// ==================== TOAST HELPER ====================
function showToast(msg) {
  const toast = document.getElementById('studioToast');
  toast.textContent = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2200);
}

function copyToken(varName, hexVal) {
  navigator.clipboard.writeText(`var(${varName}) /* ${hexVal} */`);
  showToast(`Copied: var(${varName})`);
}

function copyStudioSpec() {
  showToast("ezCORE Sovereign Specification copied to clipboard");
}

// ==================== 04. THREE.JS 3D SHOWROOM ENGINE ====================
let scene, camera, renderer, plinthMesh, consoleMesh, cartMesh;
let isXray = false;
let currentConsole = 'snes';

function initThreeShowroom() {
  const container = document.getElementById('threeCanvasContainer');
  if (!container || !window.THREE) return;

  const w = container.clientWidth || 800;
  const h = container.clientHeight || 560;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x060709);

  camera = new THREE.PerspectiveCamera(38, w / h, 0.1, 100);
  camera.position.set(0, 2.2, 4.8);
  camera.lookAt(0, 0.2, 0);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(w, h);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  // Studio Lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
  scene.add(ambientLight);

  const keyLight = new THREE.DirectionalLight(0xfffaed, 1.2);
  keyLight.position.set(3, 6, 4);
  keyLight.castShadow = true;
  keyLight.shadow.mapSize.width = 1024;
  keyLight.shadow.mapSize.height = 1024;
  scene.add(keyLight);

  const rimLight = new THREE.DirectionalLight(0xF39C12, 0.8);
  rimLight.position.set(-4, 3, -3);
  scene.add(rimLight);

  // Basalt Ground & Plinth
  const plinthGeo = new THREE.BoxGeometry(2.4, 0.35, 1.6);
  const plinthMat = new THREE.MeshStandardMaterial({
    color: 0x161920,
    roughness: 0.7,
    metalness: 0.2
  });
  plinthMesh = new THREE.Mesh(plinthGeo, plinthMat);
  plinthMesh.position.y = -0.18;
  plinthMesh.receiveShadow = true;
  scene.add(plinthMesh);

  // Plinth Chamfer Light Guide Ring
  const ringGeo = new THREE.EdgesGeometry(plinthGeo);
  const ringMat = new THREE.LineBasicMaterial({ color: 0x3B4254 });
  const plinthEdges = new THREE.LineSegments(ringGeo, ringMat);
  plinthMesh.add(plinthEdges);

  // Build Initial Console
  buildConsoleModel('snes');

  // Interactive Orbit via Mouse Drag
  let isDragging = false;
  let prevX = 0;
  let prevY = 0;

  renderer.domElement.addEventListener('mousedown', (e) => {
    isDragging = true;
    prevX = e.clientX;
    prevY = e.clientY;
  });

  window.addEventListener('mouseup', () => isDragging = false);

  renderer.domElement.addEventListener('mousemove', (e) => {
    if (!isDragging || !consoleMesh) return;
    const dx = e.clientX - prevX;
    const dy = e.clientY - prevY;
    prevX = e.clientX;
    prevY = e.clientY;

    consoleMesh.rotation.y += dx * 0.008;
    if (cartMesh) cartMesh.rotation.y += dx * 0.008;
  });

  // Render Loop
  function animate() {
    requestAnimationFrame(animate);
    if (!isDragging && consoleMesh) {
      consoleMesh.rotation.y += 0.002;
      if (cartMesh) cartMesh.rotation.y += 0.002;
    }
    renderer.render(scene, camera);
  }
  animate();

  window.addEventListener('resize', () => {
    if (!container) return;
    const nw = container.clientWidth;
    const nh = container.clientHeight;
    camera.aspect = nw / nh;
    camera.updateProjectionMatrix();
    renderer.setSize(nw, nh);
  });
}

function buildConsoleModel(type) {
  if (consoleMesh) scene.remove(consoleMesh);
  if (cartMesh) scene.remove(cartMesh);

  currentConsole = type;
  const group = new THREE.Group();

  let bodyMat = new THREE.MeshStandardMaterial({
    color: isXray ? 0x242834 : 0x2A2E3B,
    roughness: 0.4,
    metalness: 0.3,
    transparent: isXray,
    opacity: isXray ? 0.3 : 1.0
  });

  if (type === 'snes') {
    // SNES Chassis
    const bodyGeo = new THREE.BoxGeometry(1.5, 0.35, 1.2);
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.castShadow = true;
    body.position.y = 0.2;
    group.add(body);

    // Cartridge Slot
    const slotGeo = new THREE.BoxGeometry(0.8, 0.05, 0.25);
    const slotMat = new THREE.MeshBasicMaterial({ color: 0x08090B });
    const slot = new THREE.Mesh(slotGeo, slotMat);
    slot.position.set(0, 0.38, -0.05);
    group.add(slot);

    // Power LED
    const ledGeo = new THREE.SphereGeometry(0.03, 16, 16);
    const ledMat = new THREE.MeshBasicMaterial({ color: 0xF39C12 });
    const led = new THREE.Mesh(ledGeo, ledMat);
    led.position.set(-0.55, 0.36, 0.45);
    group.add(led);

    // Floating Cartridge
    const cartGeo = new THREE.BoxGeometry(0.7, 0.45, 0.12);
    const cartMat = new THREE.MeshStandardMaterial({ color: 0x484E5E, roughness: 0.5 });
    cartMesh = new THREE.Mesh(cartGeo, cartMat);
    cartMesh.position.set(0, 0.8, -0.05);
    cartMesh.castShadow = true;
    scene.add(cartMesh);

    document.getElementById('hudConsoleName').textContent = "SUPER NINTENDO ENTERTAINMENT SYSTEM (SNS-001)";
    document.getElementById('hudCoreStatus').textContent = "CORE: SNES9X V1.62.3 · 60.0 FPS LOCKED · VULKAN PASS";
  } else if (type === 'ps1') {
    // PS1 Chassis
    const bodyGeo = new THREE.BoxGeometry(1.6, 0.28, 1.3);
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.castShadow = true;
    body.position.y = 0.16;
    group.add(body);

    // CD Lid
    const lidGeo = new THREE.CylinderGeometry(0.48, 0.48, 0.05, 32);
    const lidMat = new THREE.MeshStandardMaterial({ color: 0x373B49, roughness: 0.6 });
    const lid = new THREE.Mesh(lidGeo, lidMat);
    lid.position.set(0, 0.31, 0.05);
    group.add(lid);

    // Optical Disc
    const discGeo = new THREE.CylinderGeometry(0.38, 0.38, 0.02, 32);
    const discMat = new THREE.MeshStandardMaterial({ color: 0x1A1C24, metalness: 0.8, roughness: 0.2 });
    cartMesh = new THREE.Mesh(discGeo, discMat);
    cartMesh.position.set(0, 0.75, 0.05);
    scene.add(cartMesh);

    document.getElementById('hudConsoleName').textContent = "SONY PLAYSTATION (SCPH-1001)";
    document.getElementById('hudCoreStatus').textContent = "CORE: BEETLE PSX HW · 60.0 FPS · PGXP PRECISION ACTIVE";
  } else if (type === 'n64') {
    // N64 Curved Chassis
    const bodyGeo = new THREE.BoxGeometry(1.6, 0.4, 1.2);
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.castShadow = true;
    body.position.y = 0.22;
    group.add(body);

    const cartGeo = new THREE.BoxGeometry(0.68, 0.5, 0.14);
    const cartMat = new THREE.MeshStandardMaterial({ color: 0x3A3E4D, roughness: 0.5 });
    cartMesh = new THREE.Mesh(cartGeo, cartMat);
    cartMesh.position.set(0, 0.85, -0.05);
    scene.add(cartMesh);

    document.getElementById('hudConsoleName').textContent = "NINTENDO 64 (NUS-001)";
    document.getElementById('hudCoreStatus').textContent = "CORE: MUPEN64PLUS-NEXT · ANGRYCYLION RDP 60 FPS";
  }

  // If X-Ray is enabled, add internal silicon PCB
  if (isXray) {
    const pcbGeo = new THREE.BoxGeometry(1.3, 0.04, 0.95);
    const pcbMat = new THREE.MeshStandardMaterial({ color: 0x1B4332, metalness: 0.6 });
    const pcb = new THREE.Mesh(pcbGeo, pcbMat);
    pcb.position.y = 0.18;
    group.add(pcb);

    // Silicon CPU Die
    const chipGeo = new THREE.BoxGeometry(0.28, 0.03, 0.28);
    const chipMat = new THREE.MeshStandardMaterial({ color: 0xF39C12, metalness: 0.9, roughness: 0.2 });
    const chip = new THREE.Mesh(chipGeo, chipMat);
    chip.position.set(-0.2, 0.22, 0.1);
    group.add(chip);
  }

  consoleMesh = group;
  scene.add(consoleMesh);
}

function setConsoleModel(type) {
  document.getElementById('toolOrbit').classList.remove('active');
  document.getElementById('toolPs1').classList.remove('active');
  document.getElementById('toolN64').classList.remove('active');

  if (type === 'snes') document.getElementById('toolOrbit').classList.add('active');
  if (type === 'ps1') document.getElementById('toolPs1').classList.add('active');
  if (type === 'n64') document.getElementById('toolN64').classList.add('active');

  buildConsoleModel(type);
}

function toggleXrayMode() {
  isXray = !isXray;
  document.getElementById('toolXray').classList.toggle('active', isXray);
  buildConsoleModel(currentConsole);
  showToast(isXray ? "X-Ray Silicon Mode: Internal PCB Exposed" : "Solid Chassis Mode Active");
}

function trigger3DLaunch() {
  if (!cartMesh) return;
  showToast("Executing 4-Phase Kinetic Launch Choreography...");

  // Animate cartridge inserting into console
  let step = 0;
  const startY = cartMesh.position.y;
  const targetY = 0.35;

  const interval = setInterval(() => {
    step += 0.04;
    cartMesh.position.y = THREE.MathUtils.lerp(startY, targetY, step);
    if (step >= 1) {
      clearInterval(interval);
      showToast("Game DOCKED // Live Frame Buffer Engaged");
      setTimeout(() => { cartMesh.position.y = startY; }, 2000);
    }
  }, 16);
}

function toggle2DFallbackView() {
  const v = document.getElementById('fallback2DView');
  v.classList.toggle('active');
  showToast(v.classList.contains('active') ? "2D High-Density Catalog Active" : "Returned to 3D Showroom");
}

window.onShowroomActive = () => {
  if (!scene) initThreeShowroom();
};

// ==================== 05. SCREENS DATA & VIEWS ====================
const screenLibraryData = [
  {
    id: "S01",
    mod: "Onboarding",
    name: "Hardware Calibration & Ingestion",
    file: "lib/features/onboarding/presentation/onboarding_view.dart",
    priority: "P0",
    status: "Approved",
    desc: "First-run setup: directory ingestion, hash verification, recommended core downloads, and controller mapping.",
    anatomy: ["• Storage Directory Picker", "• Parallel Hash Progress Bar", "• Gamepad Input Live Canvas", "• Primary CTA Plinth"],
    interactions: ["• Enter / Space: Ingest Directory", "• Auto-advance on gamepad button press", "• Escape: Back / Cancel"]
  },
  {
    id: "S07",
    mod: "Home",
    name: "Home Central Command Hub",
    file: "lib/features/home/presentation/home_hub_view.dart",
    priority: "P0",
    status: "Approved",
    desc: "Primary executive dashboard: Quick Resume plinth, Recently Played rail, systems carousel, and telemetry HUD.",
    anatomy: ["• Quick Resume Hero Plinth", "• Recently Executed Specimen Rail", "• Architectural Systems Overview", "• Telemetry HUD"],
    interactions: ["• Enter: Quick Resume", "• D-Pad: Navigate recent games", "• Space: Open 3D Showroom"]
  },
  {
    id: "S09",
    mod: "3D Universe",
    name: "Spatial System Gallery",
    file: "lib/features/spatial/presentation/spatial_gallery_view.dart",
    priority: "P0",
    status: "Approved",
    desc: "Interactive 3D showroom presenting hardware consoles and media cartridges on basalt plinths.",
    anatomy: ["• 3D Basalt Plinth", "• Optical Vitrine Refraction", "• Rotatable Hardware Mesh", "• Cartridge Docking Rail"],
    interactions: ["• Drag: Orbit Console", "• Tab: Toggle X-Ray Silicon", "• Enter: Dock Cartridge & Play"]
  },
  {
    id: "S13",
    mod: "Library",
    name: "Catalog Grid & Filter Deck",
    file: "lib/features/library/presentation/catalog_grid_view.dart",
    priority: "P0",
    status: "Approved",
    desc: "High-density 4:3 and 16:9 game specimen grid with real-time system filtering, search, and sort.",
    anatomy: ["• Filter Pill Carousel", "• Specimen Card Matrix", "• Search Telemetry Input", "• Missing Core Warning Badge"],
    interactions: ["• /: Quick Search", "• Arrow Keys: Grid navigation", "• F: Add to Favorites"]
  },
  {
    id: "S15",
    mod: "Game Detail",
    name: "Game Detail Dossier",
    file: "lib/features/game_detail/presentation/game_dossier_view.dart",
    priority: "P0",
    status: "Approved",
    desc: "Comprehensive historical dossier: original box art in optical glass, metadata, save states, and core overrides.",
    anatomy: ["• Optical Box Art Vitrine", "• Metadata & CRC32 Chip", "• Save State Rewind Timeline", "• Launch CTA Plinth"],
    interactions: ["• Enter: Launch Game", "• R: Rewind to selected state", "• C: Configure Per-Game Overrides"]
  },
  {
    id: "S16",
    mod: "Saves",
    name: "Save State Rewind Deck",
    file: "lib/features/saves/presentation/save_state_deck_view.dart",
    priority: "P0",
    status: "Approved",
    desc: "Visual rewind timeline with instant screenshot snapshots, 60-second frame scrub, and cloud backup status.",
    anatomy: ["• State Slots 1–5", "• Auto-Save Timestamp Card", "• 60s Live Scrub Slider", "• Cloud Sync Status Light"],
    interactions: ["• L2 + R2: Trigger Mid-Game Rewind", "• Guide + R1: Instant Snapshot", "• Delete: Purge State"]
  },
  {
    id: "S18",
    mod: "Systems",
    name: "System Architecture Hub",
    file: "lib/features/systems/presentation/systems_matrix_view.dart",
    priority: "P0",
    status: "Approved",
    desc: "Hardware specification matrix, BIOS hash verification, and assigned emulation core selection.",
    anatomy: ["• Hardware Spec Breakdown", "• BIOS File MD5 Checksum", "• Active Core Switcher", "• ROM Ingestion Count"],
    interactions: ["• Click Core: Swap active backend", "• Drag BIOS: Ingest missing firmware"]
  },
  {
    id: "S20",
    mod: "Modules",
    name: "Modular Core Store",
    file: "lib/features/modules/presentation/module_store_view.dart",
    priority: "P1",
    status: "Approved",
    desc: "Ecosystem browser for verified emulation cores, CRT shader packs, and audio DSP renderers.",
    anatomy: ["• Core Version Pill", "• SHA256 Integrity Verified", "• One-Click Install CTA", "• Changelog Accordion"],
    interactions: ["• Enter: Download / Update Core", "• Rollback: Select previous stable version"]
  },
  {
    id: "S23",
    mod: "Controllers",
    name: "Controller Calibration Station",
    file: "lib/features/controllers/presentation/controller_calibration_view.dart",
    priority: "P0",
    status: "Approved",
    desc: "Real-time input tester, stick deadzone calibration gauge, button remapping, and latency analyzer.",
    anatomy: ["• Interactive Gamepad SVG", "• Real-Time Input Polling Gauge", "• Deadzone Outer/Inner Rings", "• Latency Telemetry (0.9ms)"],
    interactions: ["• Press any button to map", "• Rotate stick to calibrate deadzone", "• Save Profile"]
  },
  {
    id: "S25",
    mod: "Settings",
    name: "System Settings Studio",
    file: "lib/features/settings/presentation/settings_studio_view.dart",
    priority: "P0",
    status: "Approved",
    desc: "System-wide preferences: audio buffer size, integer scaling, display refresh, and UI performance.",
    anatomy: ["• Setting Category Tabs", "• Knurled Slider Controls", "• Hardware Switch Banks", "• Reset to Factory Plinth"],
    interactions: ["• Slider Drag: Adjust buffer latency", "• Toggle: Instant state apply"]
  },
  {
    id: "S26",
    mod: "Diagnostics",
    name: "Diagnostics & Telemetry Log",
    file: "lib/features/diagnostics/presentation/diagnostics_log_view.dart",
    priority: "P1",
    status: "Approved",
    desc: "Low-level system monitors: frame-time jitter graph, audio buffer underruns, and live core logs.",
    anatomy: ["• Frame-Time Jitter Histogram", "• Memory Bus Bandwidth Gauge", "• Live Log Stream Terminal", "• Export Report CTA"],
    interactions: ["• Space: Pause telemetry stream", "• Filter: Isolate warning / error logs"]
  },
  {
    id: "S27",
    mod: "About",
    name: "Preservation & Licenses",
    file: "lib/features/about/presentation/about_manifesto_view.dart",
    priority: "P2",
    status: "Approved",
    desc: "Platform manifesto, core developers, open-source preservation licenses, and update engine.",
    anatomy: ["• Sovereign Version Lock", "• Core Authors & Credits", "• License Disclosure List", "• Check for Updates CTA"],
    interactions: ["• Click Update: Check latest sovereign build"]
  }
];

let selectedScreen = screenLibraryData[1]; // S07 Home
let currentScreenState = "Normal";

function renderScreensNavigation() {
  const container = document.getElementById('screensNavList');
  container.innerHTML = '';

  screenLibraryData.forEach(s => {
    const btn = document.createElement('button');
    btn.className = `screen-item-btn ${s.id === selectedScreen.id ? 'active' : ''}`;
    btn.innerHTML = `
      <span><b>${s.id}</b> · ${s.name}</span>
      <span class="tag">${s.mod}</span>
    `;
    btn.onclick = () => selectScreen(s);
    container.appendChild(btn);
  });
}

function selectScreen(screen) {
  selectedScreen = screen;
  currentScreenState = "Normal";
  renderScreensNavigation();
  updateScreenDisplay();
}

function setScreenState(state) {
  currentScreenState = state;
  document.querySelectorAll('.state-pill').forEach(p => {
    p.classList.toggle('active', p.textContent.toLowerCase().replace(/\s+/g, '') === state.toLowerCase().replace(/\s+/g, ''));
  });
  updateScreenDisplay();
}

function updateScreenDisplay() {
  document.getElementById('screenSpecId').textContent = `${selectedScreen.id} // ${selectedScreen.mod.toUpperCase()}`;
  document.getElementById('screenSpecName').textContent = selectedScreen.name;

  // Anatomy
  const anatomyEl = document.getElementById('anatomyList');
  anatomyEl.innerHTML = selectedScreen.anatomy.map(a => `<li>${a}</li>`).join('');

  // Interactions
  const interactEl = document.getElementById('interactionList');
  interactEl.innerHTML = selectedScreen.interactions.map(i => `<li>${i}</li>`).join('');

  // Source
  document.getElementById('sourceList').innerHTML = `
    <li style="font-family:var(--font-mono); color:var(--titanium-muted);">${selectedScreen.file}</li>
    <li>Status: <b style="color:var(--core-online);">${selectedScreen.status}</b> · Priority: ${selectedScreen.priority}</li>
  `;

  // Render Mockup based on screen & state
  renderMockup(selectedScreen.id, currentScreenState);
}

function renderMockup(id, state) {
  const canvas = document.getElementById('screenRenderCanvas');

  if (state === 'Loading') {
    canvas.innerHTML = `
      <div style="height:380px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:16px;">
        <div style="width:40px; height:40px; border:3px solid var(--basalt-chamfer); border-top-color:var(--solar-ochre); border-radius:50%; animation:spin 0.8s linear infinite;"></div>
        <div style="font-family:var(--font-mono); font-size:12px; color:var(--solar-ochre);">PARALLEL HASH VERIFICATION IN PROGRESS...</div>
      </div>
      <style>@keyframes spin{to{transform:rotate(360deg)}}</style>
    `;
    return;
  }

  if (state === 'MissingCore') {
    canvas.innerHTML = `
      <div style="height:380px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:16px; text-align:center;">
        <div style="font-size:36px;">⚠️</div>
        <div style="font-family:var(--font-display); font-size:20px; font-weight:700;">EMULATION CORE NOT FOUND</div>
        <p style="font-size:13px; color:var(--titanium-muted); max-width:44ch;">This title requires the verified Snes9x (v1.62.3) core binary to execute.</p>
        <button class="btn-core cta-solar" onclick="setScreenState('Normal')">Download & Install Core (One-Click)</button>
      </div>
    `;
    return;
  }

  if (state === 'Error') {
    canvas.innerHTML = `
      <div style="height:380px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:16px; text-align:center;">
        <div style="font-size:36px;">🛑</div>
        <div style="font-family:var(--font-display); font-size:20px; font-weight:700; color:var(--core-danger);">CORRUPTED SAVE STATE DETECTED</div>
        <p style="font-size:13px; color:var(--titanium-muted); max-width:44ch;">CRC checksum mismatch on Slot 01. Automatic backup state is available.</p>
        <button class="btn-core secondary" onclick="setScreenState('Normal')">Restore Auto-Backup State #02</button>
      </div>
    `;
    return;
  }

  // Normal / Focused Mockups
  if (id === 'S07') {
    canvas.innerHTML = `
      <div style="border:1px solid var(--basalt-chamfer); border-radius:12px; padding:24px; background:var(--basalt-02); margin-bottom:20px;">
        <div style="font-family:var(--font-mono); font-size:10px; color:var(--solar-ochre);">QUICK RESUME // HERO PLINTH</div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
          <div>
            <h2 style="font-family:var(--font-display); font-size:26px; font-weight:800;">SUPER METROID</h2>
            <div style="font-size:12px; color:var(--titanium-muted); margin-top:4px;">SNES · Snes9x 1.62.3 · 14h 22m played · Last save: 2m ago</div>
          </div>
          <button class="btn-core cta-solar">▶ Resume Game (Enter)</button>
        </div>
      </div>
      <div style="font-family:var(--font-mono); font-size:11px; color:var(--titanium-muted); margin-bottom:12px;">RECENTLY EXECUTED TITLES</div>
      <div style="display:flex; gap:14px;">
        <div class="specimen-card-mock ${state === 'Focused' ? 'focused' : ''}">
          <div class="specimen-art"><span style="font-size:20px;">⚡</span><span class="specimen-tag">SNES</span></div>
          <div class="specimen-info"><div class="specimen-title">Chrono Trigger</div><div class="specimen-sub">98% Save Run</div></div>
        </div>
        <div class="specimen-card-mock">
          <div class="specimen-art"><span style="font-size:20px;">🦇</span><span class="specimen-tag">PS1</span></div>
          <div class="specimen-info"><div class="specimen-title">Castlevania: SOTN</div><div class="specimen-sub">Slot #04</div></div>
        </div>
        <div class="specimen-card-mock">
          <div class="specimen-art"><span style="font-size:20px;">📦</span><span class="specimen-tag">PS1</span></div>
          <div class="specimen-info"><div class="specimen-title">Metal Gear Solid</div><div class="specimen-sub">Disc 2</div></div>
        </div>
      </div>
    `;
  } else if (id === 'S15') {
    canvas.innerHTML = `
      <div style="display:grid; grid-template-columns:180px 1fr; gap:24px;">
        <div style="height:240px; background:var(--basalt-02); border:1px solid var(--solar-ochre); border-radius:10px; display:flex; flex-direction:column; align-items:center; justify-content:center; box-shadow:0 0 20px var(--solar-glow);">
          <span style="font-size:40px;">🛸</span>
          <span style="font-family:var(--font-mono); font-size:10px; color:var(--solar-ochre); margin-top:8px;">HIGH-RES BOX ART</span>
        </div>
        <div>
          <span class="rank-badge win">SNES · USA/NTSC · 1994</span>
          <h2 style="font-family:var(--font-display); font-size:28px; font-weight:800; margin:8px 0;">SUPER METROID</h2>
          <p style="font-size:13px; color:var(--titanium-body); line-height:1.6; margin-bottom:18px;">
            Samus Aran journeys to planet Zebes to retrieve the stolen infant Metroid from Space Pirate leader Ridley. Features seamless atmospheric exploration and cinematic 16-bit audio.
          </p>
          <div style="display:flex; gap:12px;">
            <button class="btn-core cta-solar">▶ Launch Game (Space)</button>
            <button class="btn-core secondary">Save States (4 Slots)</button>
            <button class="btn-core secondary">Core Config</button>
          </div>
        </div>
      </div>
    `;
  } else if (id === 'S23') {
    canvas.innerHTML = `
      <div style="background:var(--basalt-02); border:1px solid var(--basalt-border); border-radius:12px; padding:24px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
          <div>
            <h3 style="font-family:var(--font-display); font-size:18px; font-weight:700;">DUALSHOCK 4 (WIRELESS / USB-01)</h3>
            <div style="font-family:var(--font-mono); font-size:11px; color:var(--core-online); margin-top:2px;">POLLING RATE: 1000Hz · INPUT LATENCY: 0.9ms</div>
          </div>
          <span class="status-badge status-approved">CALIBRATED</span>
        </div>
        <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:16px;">
          <div style="border:1px solid var(--basalt-border); padding:14px; border-radius:8px;">
            <div style="font-size:12px; font-weight:700;">Left Analog Stick</div>
            <div style="font-family:var(--font-mono); font-size:11px; color:var(--titanium-muted); margin-top:4px;">Deadzone: 4.0% · Anticheat Jitter: 0.02%</div>
          </div>
          <div style="border:1px solid var(--basalt-border); padding:14px; border-radius:8px;">
            <div style="font-size:12px; font-weight:700;">Adaptive Triggers (L2 / R2)</div>
            <div style="font-family:var(--font-mono); font-size:11px; color:var(--titanium-muted); margin-top:4px;">Threshold: 12% · Rewind Hold: Active</div>
          </div>
        </div>
      </div>
    `;
  } else {
    canvas.innerHTML = `
      <div style="background:var(--basalt-02); border:1px solid var(--basalt-border); border-radius:12px; padding:24px;">
        <div style="font-family:var(--font-mono); font-size:11px; color:var(--solar-ochre); margin-bottom:8px;">SURFACE SPECIFICATION // ${selectedScreen.id}</div>
        <h3 style="font-family:var(--font-display); font-size:22px; font-weight:800;">${selectedScreen.name}</h3>
        <p style="font-size:13px; color:var(--titanium-body); margin-top:8px; line-height:1.6;">${selectedScreen.desc}</p>
        <div style="margin-top:20px;">
          <button class="btn-core cta-solar">Execute Action</button>
        </div>
      </div>
    `;
  }
}

// Initial 2D Fallback Render
function renderFallbackGrid() {
  const container = document.getElementById('fallbackGrid');
  if (!container) return;
  const games = [
    { title: "Super Metroid", sys: "SNES", time: "14h 22m" },
    { title: "Chrono Trigger", sys: "SNES", time: "98% Run" },
    { title: "Castlevania: SOTN", sys: "PS1", time: "22h 10m" },
    { title: "Metal Gear Solid", sys: "PS1", time: "Disc 2" },
    { title: "Super Mario 64", sys: "N64", time: "120 Stars" },
    { title: "The Legend of Zelda: OOT", sys: "N64", time: "Master Quest" },
    { title: "F-Zero GX", sys: "GC", time: "Master Cup" },
    { title: "Wind Waker", sys: "GC", time: "HD Texture" }
  ];
  container.innerHTML = games.map(g => `
    <div class="specimen-card-mock" style="width:100%;">
      <div class="specimen-art"><span style="font-size:24px;">🎮</span><span class="specimen-tag">${g.sys}</span></div>
      <div class="specimen-info"><div class="specimen-title">${g.title}</div><div class="specimen-sub">${g.time}</div></div>
    </div>
  `).join('');
}

// ==================== 07. MOTION LAB PHYSICS ====================
function playMotion(preset) {
  const target = document.getElementById('motionTarget');
  const status = document.getElementById('motionStatus');
  target.style.transition = 'none';
  target.style.transform = 'none';

  if (preset === 'press') {
    status.textContent = "RUNNING: Press (90ms cubic-bezier(0.2, 0, 0, 1))";
    setTimeout(() => {
      target.style.transition = 'transform 90ms cubic-bezier(0.2, 0, 0, 1)';
      target.style.transform = 'scale(0.96)';
      setTimeout(() => {
        target.style.transform = 'scale(1.0)';
        status.textContent = "IDLE (Press complete)";
      }, 140);
    }, 20);
  } else if (preset === 'settle') {
    status.textContent = "RUNNING: Card Settle (180ms cubic-bezier(0.16, 1, 0.3, 1))";
    setTimeout(() => {
      target.style.transition = 'transform 180ms cubic-bezier(0.16, 1, 0.3, 1)';
      target.style.transform = 'translateY(-12px) scale(1.03)';
      setTimeout(() => {
        target.style.transform = 'translateY(0) scale(1.0)';
        status.textContent = "IDLE (Settle complete)";
      }, 240);
    }, 20);
  } else if (preset === 'push') {
    status.textContent = "RUNNING: Screen Push (280ms lateral slip)";
    setTimeout(() => {
      target.style.transition = 'transform 280ms cubic-bezier(0.16, 1, 0.3, 1), opacity 280ms ease';
      target.style.transform = 'translateX(40px)';
      target.style.opacity = '0.4';
      setTimeout(() => {
        target.style.transform = 'translateX(0)';
        target.style.opacity = '1.0';
        status.textContent = "IDLE (Push complete)";
      }, 320);
    }, 20);
  } else if (preset === 'launch') {
    status.textContent = "RUNNING: 4-Phase Kinetic Launch Sequence (750ms)";
    target.style.transition = 'all 200ms ease';
    target.style.transform = 'scale(1.15)';
    target.style.borderColor = 'var(--core-online)';
    setTimeout(() => {
      target.style.transition = 'all 400ms cubic-bezier(0.16, 1, 0.3, 1)';
      target.style.transform = 'scale(2.5)';
      target.style.opacity = '0';
      setTimeout(() => {
        target.style.transition = 'none';
        target.style.transform = 'scale(1.0)';
        target.style.opacity = '1.0';
        target.style.borderColor = 'var(--solar-ochre)';
        status.textContent = "IDLE (Launch sequence finished)";
      }, 500);
    }, 250);
  }
}

// ==================== 08. COVERAGE TABLE INJECTION ====================
function renderCoverageTable() {
  const tbody = document.getElementById('coverageTableBody');
  tbody.innerHTML = screenLibraryData.map(s => `
    <tr>
      <td><b>${s.mod}</b></td>
      <td>${s.name}</td>
      <td><span class="rank-badge ${s.priority === 'P0' ? 'win' : 'alt'}">${s.priority}</span></td>
      <td><span class="status-badge status-approved">${s.status}</span></td>
      <td style="font-family:var(--font-mono); color:var(--titanium-muted);">${s.file}</td>
      <td><input type="checkbox" checked style="accent-color:var(--solar-ochre);"></td>
    </tr>
  `).join('');
}

// ==================== INITIALIZATION ====================
window.addEventListener('DOMContentLoaded', () => {
  renderScreensNavigation();
  updateScreenDisplay();
  renderFallbackGrid();
  renderCoverageTable();
  initThreeShowroom();
});
</script>
</body>
</html>
'''

with open('/Users/jinultimate/ezCORE/tools/moonboard/index.html', 'w') as f:
  f.write(html_content)

print(f"Successfully wrote {len(html_content)} bytes to /Users/jinultimate/ezCORE/tools/moonboard/index.html")

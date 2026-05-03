## Mandatory HTML Skeleton

**EVERY visualization MUST start from this skeleton.** Copy it, then add content. This gives you themes, print styles, Inter font, animations, menu, and hover effects — all working out of the box.

**Design philosophy: CSS-first, JS-minimal.** Animations use CSS `@keyframes` and `transition` (always reliable). JavaScript is only for: menu, theme toggle, scroll observer, number counters, and PNG download. No animation libraries required.

```html
<!DOCTYPE html>
<html lang="en" class="theme-dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>YOUR TITLE HERE</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <!-- ADD LANGUAGE FONTS IF NEEDED: e.g. Noto Sans KR for Korean, Noto Sans JP for Japanese -->
  <!-- <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet"> -->
  <!-- ADD CDN LIBRARIES HERE (Chart.js, Mermaid, etc.) -->
  <script src="https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/dist/html-to-image.js"></script>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root { interpolate-size: allow-keywords; } /* Enable smooth height:auto transitions (Chrome 129+) */

    /* ===== THEMES (class-based ONLY — no @media prefers-color-scheme) ===== */
    html.theme-dark {
      --bg: #0A0A0A; --surface: #141414; --surface-hover: #1C1C1C;
      --border: rgba(255,255,255,0.04);
      --text: #EDEDED; --text-secondary: #888;
      --accent: #3b82f6; --accent-secondary: #8b5cf6;
      --positive: #10b981; --negative: #f43f5e; --warning: #f59e0b;
    }
    html.theme-light {
      --bg: #FAFAF9; --surface: #FFFFFF; --surface-hover: #F5F5F4;
      --border: rgba(0,0,0,0.06);
      --text: #0f172a; --text-secondary: #64748b;
      --accent: #2563eb; --accent-secondary: #7c3aed;
      --positive: #059669; --negative: #e11d48; --warning: #d97706;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: var(--bg); color: var(--text);
      line-height: 1.6; -webkit-font-smoothing: antialiased;
      letter-spacing: -0.01em; font-feature-settings: 'cv11', 'ss01';
      transition: background 0.3s, color 0.3s;
      scrollbar-gutter: stable;
    }
    h1,h2,h3,h4,h5,h6 { 
      color: var(--text); 
      letter-spacing: -0.03em; 
      line-height: 1.08;
      text-wrap: balance;
    }
    h1 { font-weight: 700; }
    h2 { font-weight: 600; }
    body, p, li, td, th, span, label { font-weight: 400; }
    p,li,td,th,span,label { color: var(--text); }
    .text-secondary { color: var(--text-secondary); }

    /* ===== CARD ===== */
    .card {
      background: var(--surface); border: 1px solid var(--border);
      border-radius: 8px; padding: 24px;
      transition: box-shadow 0.2s ease;
    }
    .card:hover {
      box-shadow: 0 0 0 1px var(--border), 0 8px 16px rgba(0,0,0,0.08);
    }

    /* ===== ANIMATIONS (CSS-first — always reliable) ===== */
    @keyframes fadeInUp {
      from { opacity: 0; transform: translateY(24px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    @keyframes slideInLeft {
      from { opacity: 0; transform: translateX(-40px); }
      to { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideInRight {
      from { opacity: 0; transform: translateX(40px); }
      to { opacity: 1; transform: translateX(0); }
    }
    .animate { animation: fadeInUp 0.6s ease-out both; }
    .animate.delay-1 { animation-delay: 0.1s; }
    .animate.delay-2 { animation-delay: 0.2s; }
    .animate.delay-3 { animation-delay: 0.3s; }
    .animate.delay-4 { animation-delay: 0.4s; }
    .animate.delay-5 { animation-delay: 0.5s; }
    .animate.delay-6 { animation-delay: 0.6s; }

    /* Scroll-triggered: JS adds .reveal, then .visible on scroll */
    .reveal { opacity: 0; transform: translateY(24px); transition: opacity 0.6s ease, transform 0.6s ease; }
    .reveal.visible { opacity: 1; transform: translateY(0); }

    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after { animation: none !important; transition: none !important; }
      .reveal { opacity: 1; transform: none; }
    }

    /* ===== PRINT ===== */
    @media print {
      body { background: white !important; color: black !important; }
      .viz-menu, .reveal { display: revert; opacity: 1 !important; transform: none !important; }
      .card { break-inside: avoid; border: 1px solid #ddd; box-shadow: none; }
      * { print-color-adjust: exact; -webkit-print-color-adjust: exact; }
    }
    @page { margin: 1in; @bottom-center { content: "Page " counter(page); font-size: 9pt; color: #666; } }

    /* ===== MENU ===== */
    .viz-menu { position: fixed; top: 16px; right: 16px; z-index: 9999; }
    .viz-menu-toggle {
      width: 44px; height: 44px; border-radius: 12px;
      background: var(--surface); border: 1px solid var(--border);
      color: var(--text); cursor: pointer; display: flex;
      align-items: center; justify-content: center;
      backdrop-filter: blur(12px); transition: all 0.2s;
    }
    .viz-menu-toggle:hover { background: var(--surface-hover); }
    .viz-menu-dropdown {
      position: absolute; top: 52px; right: 0; min-width: 200px;
      background: var(--surface); border: 1px solid var(--border);
      border-radius: 12px; padding: 8px;
      opacity: 0; visibility: hidden; transform: translateY(-8px);
      transition: all 0.2s; backdrop-filter: blur(16px);
    }
    .viz-menu-dropdown.open { opacity: 1; visibility: visible; transform: translateY(0); }
    .viz-menu-dropdown button {
      width: 100%; padding: 10px 14px; border: none; border-radius: 8px;
      background: transparent; color: var(--text); font-size: 14px;
      font-family: inherit; cursor: pointer; text-align: left;
      display: flex; align-items: center; gap: 10px; transition: background 0.15s;
    }
    .viz-menu-dropdown button:hover { background: var(--surface-hover); }

    /* ===== SKIP TO CONTENT (accessibility) ===== */
    .skip-to-content {
      position: absolute; top: -40px; left: 6px; background: var(--accent);
      color: white; padding: 8px 12px; text-decoration: none;
      border-radius: 4px; opacity: 0; pointer-events: none;
      transition: all 0.2s; z-index: 10000;
    }
    .skip-to-content:focus { top: 6px; opacity: 1; pointer-events: auto; }

    /* ===== DETAILS ACCORDION (Chrome 120+ exclusive, 131+ animated) ===== */
    details { overflow: hidden; }
    details summary { cursor: pointer; list-style: none; }
    details summary::-webkit-details-marker { display: none; }
    ::details-content {
      transition: block-size 0.3s ease, opacity 0.3s ease;
      block-size: 0; opacity: 0; overflow: hidden;
    }
    details[open]::details-content { block-size: auto; opacity: 1; }

    /* ===== POPOVER (Chrome 114+, zero-JS tooltips/panels) ===== */
    [popover] {
      background: var(--surface); border: 1px solid var(--border);
      border-radius: 8px; padding: 16px; max-width: 320px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.2); color: var(--text);
    }
    [popover]::backdrop { background: rgba(0,0,0,0.3); }

    /* ===== ADD YOUR STYLES BELOW ===== */
  </style>
</head>
<body>
  <a href="#main-content" class="skip-link" style="position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden;z-index:10000;padding:8px 16px;background:var(--accent);color:white;text-decoration:none;border-radius:4px;" onfocus="this.style.cssText='position:fixed;left:16px;top:16px;z-index:10000;padding:8px 16px;background:var(--accent);color:white;text-decoration:none;border-radius:4px;'" onblur="this.style.cssText='position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden;'">Skip to content</a>
  <main id="main-content">

  <!-- MENU -->
  <div class="viz-menu">
    <button class="viz-menu-toggle" onclick="toggleMenu()" aria-label="Menu">
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <line x1="3" y1="5" x2="17" y2="5"/><line x1="3" y1="10" x2="17" y2="10"/><line x1="3" y1="15" x2="17" y2="15"/>
      </svg>
    </button>
    <div class="viz-menu-dropdown" id="vizMenuDropdown">
      <button onclick="cycleTheme()"><span id="themeIcon">🌙</span><span id="themeLabel">Dark</span></button>
      <button onclick="downloadImage()"><span>📥</span><span>Download PNG</span></button>
      <button onclick="window.print()"><span>🖨️</span><span>Print / PDF</span></button>
    </div>
  </div>

  <!-- SKIP TO CONTENT (accessibility) -->
  <a href="#main-content" class="skip-to-content">Skip to content</a>

  <main id="main-content" role="main">
    <!-- YOUR CONTENT HERE (use <section>, <header>, <article> for semantics) -->
  </main>

  <!-- EXAMPLE: Exclusive accordion (only one open at a time, no JS needed) -->
  <!--
  <details name="faq" open>
    <summary>Section 1</summary>
    <div class="section-body"><p>Content</p></div>
  </details>
  <details name="faq">
    <summary>Section 2</summary>
    <div class="section-body"><p>Content</p></div>
  </details>
  -->

  <!-- EXAMPLE: Popover (zero-JS tooltip/info panel) -->
  <!--
  <button popovertarget="info-panel">Details</button>
  <div id="info-panel" popover>
    <h3>More Information</h3>
    <p>Content shown on click, no JS needed.</p>
  </div>
  -->

  </main>
  <script>
    // === Menu ===
    function toggleMenu() { 
      var dropdown = document.getElementById('vizMenuDropdown') || document.getElementById('vizMenu');
      if (dropdown) dropdown.classList.toggle('open'); 
    }
    document.addEventListener('click', e => { 
      if (!e.target.closest('.viz-menu')) {
        var dropdown = document.getElementById('vizMenuDropdown') || document.getElementById('vizMenu');
        if (dropdown) dropdown.classList.remove('open');
      }
    });
    document.addEventListener('keydown', e => { 
      if (e.key === 'Escape') {
        var dropdown = document.getElementById('vizMenuDropdown') || document.getElementById('vizMenu');
        if (dropdown) dropdown.classList.remove('open');
      }
    });

    // === Theme (class-based, OS detection on first visit) ===
    var savedTheme = localStorage.getItem('viz-theme');
    var currentTheme = savedTheme || (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
    function applyTheme(t) {
      document.documentElement.className = 'theme-' + t;
      document.getElementById('themeIcon').textContent = t === 'dark' ? '🌙' : '☀️';
      document.getElementById('themeLabel').textContent = t === 'dark' ? 'Dark' : 'Light';
      localStorage.setItem('viz-theme', t);
      currentTheme = t;
      if (typeof onThemeChange === 'function') onThemeChange();
    }
    function cycleTheme() { applyTheme(currentTheme === 'dark' ? 'light' : 'dark'); }
    applyTheme(currentTheme);

    // === Scroll Reveal (adds .reveal then .visible — content visible without JS) ===
    document.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('reveal'));
    var revealObserver = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) { if (e.isIntersecting) { e.target.classList.add('visible'); revealObserver.unobserve(e.target); } });
    }, { threshold: 0.15 });
    document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

    // === Number Counter (use data-count="77" data-suffix="%" on elements) ===
    function animateCounters() {
      document.querySelectorAll('[data-count]').forEach(function(el) {
        if (el.dataset.counted) return;
        el.dataset.counted = '1';
        var target = parseFloat(el.dataset.count), prefix = el.dataset.prefix || '', suffix = el.dataset.suffix || '';
        var start = performance.now(), duration = 1200;
        (function tick(now) {
          var p = Math.min((now - start) / duration, 1), eased = 1 - Math.pow(1 - p, 3);
          el.textContent = prefix + Math.round(target * eased).toLocaleString() + suffix;
          if (p < 1) requestAnimationFrame(tick);
        })(start);
      });
    }
    var counterEl = document.querySelector('[data-count]');
    if (counterEl) {
      var cObs = new IntersectionObserver(function(entries) {
        entries.forEach(function(e) { if (e.isIntersecting) { animateCounters(); cObs.disconnect(); } });
      }, { threshold: 0.3 });
      cObs.observe(counterEl);
    }

    // === Download PNG ===
    async function downloadImage() {
      var menu = document.querySelector('.viz-menu');
      menu.style.display = 'none';
      try {
        var url = await htmlToImage.toPng(document.body, { quality: 1, pixelRatio: 2, filter: function(n) { return !n.classList || !n.classList.contains('viz-menu'); } });
        var a = document.createElement('a'); a.href = url;
        a.download = document.title.replace(/\s+/g, '-').toLowerCase() + '.png'; a.click();
      } catch(e) { console.error('Download failed:', e); }
      menu.style.display = '';
    }

    // === Chart.js Pattern (use when file has Chart.js) ===
    // var chartsBuilt = false;
    // function buildCharts() {
    //   if (chartsBuilt || typeof Chart === 'undefined') return;
    //   var isDark = document.documentElement.classList.contains('theme-dark');
    //   var textColor = isDark ? '#EDEDED' : '#0f172a';
    //   var borderColor = isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)';
    //   // Create charts with theme-aware colors
    //   chartsBuilt = true;
    // }
    // function onThemeChange() { chartsBuilt = false; buildCharts(); }
    // window.addEventListener('load', buildCharts);

    // === YOUR SCRIPTS BELOW (use var for top-level variables, define onThemeChange for chart re-renders) ===
  </script>
</body>
</html>
```

### Skeleton Rules

**Do:**
- Use `var` for all top-level variables (avoids TDZ errors when functions are hoisted)
- Use `data-reveal` attribute on sections/cards for scroll animation
- Use `data-count="77" data-suffix="%"` for animated number counters
- Use `.animate.delay-N` classes for page-load entrance animations
- Use CSS `:hover` for hover effects (baked into `.card` already)
- Define `function onThemeChange() {}` to re-render charts on theme toggle
- Use `<main>`, `<section>`, `<header>`, `<article>` for semantic HTML
- Keep all chart variables as `var` (not `let`/`const`) at script top level

**Don't:**
- Don't include Motion.js unless you specifically need spring physics
- Don't hide content via JS/CSS for animation — use `data-reveal` pattern instead
- Don't use `let`/`const` for variables that might be referenced before declaration
- Don't use `.finished` Promise chains for sequencing — use `setTimeout`
- Don't put animation logic that could crash before nav/chart setup code


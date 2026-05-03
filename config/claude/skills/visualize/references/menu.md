# Hamburger Menu Component

Every visualization MUST include a hamburger menu in the top-right corner with these features:
1. **Theme toggle** — dark/light mode (or multi-theme selector)
2. **Download as image** — PNG export via html-to-image
3. **Print as PDF** — browser print with optimized print styles

## Required CDN

```html
<script src="https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/dist/html-to-image.js"></script>
```

## Complete Menu Implementation

Paste this into every visualization. Customize theme colors to match the visualization's palette.

### HTML (place just inside `<body>`)

```html
<!-- Hamburger Menu -->
<div class="viz-menu">
  <button class="viz-menu-toggle" onclick="toggleMenu()" aria-label="Menu">
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
      <line x1="3" y1="5" x2="17" y2="5"/>
      <line x1="3" y1="10" x2="17" y2="10"/>
      <line x1="3" y1="15" x2="17" y2="15"/>
    </svg>
  </button>
  <div class="viz-menu-dropdown" id="vizMenuDropdown">
    <button onclick="cycleTheme()">
      <span class="viz-menu-icon">◐</span>
      <span>Theme: <span id="themeLabel">Dark</span></span>
    </button>
    <button onclick="downloadImage()">
      <span class="viz-menu-icon">⤓</span>
      <span>Download as PNG</span>
    </button>
    <button onclick="printPDF()">
      <span class="viz-menu-icon">⎙</span>
      <span>Print / Save PDF</span>
    </button>
  </div>
</div>
```

### CSS

```css
/* === Hamburger Menu === */
.viz-menu {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 9999;
  font-family: var(--font, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif);
}

.viz-menu-toggle {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  border: 1px solid var(--menu-border, rgba(128,128,128,0.3));
  background: var(--menu-bg, rgba(0,0,0,0.5));
  color: var(--menu-text, #fff);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  transition: all 0.2s ease;
}

.viz-menu-toggle:hover {
  background: var(--menu-bg-hover, rgba(0,0,0,0.7));
  transform: scale(1.05);
}

.viz-menu-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 200px;
  background: var(--menu-bg, rgba(0,0,0,0.85));
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--menu-border, rgba(128,128,128,0.2));
  border-radius: 12px;
  padding: 6px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-8px) scale(0.96);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

.viz-menu-dropdown.open {
  opacity: 1;
  visibility: visible;
  transform: translateY(0) scale(1);
}

.viz-menu-dropdown button {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border: none;
  background: transparent;
  color: var(--menu-text, #fff);
  font-size: 0.875rem;
  cursor: pointer;
  border-radius: 8px;
  transition: background 0.15s;
  text-align: left;
  white-space: nowrap;
}

.viz-menu-dropdown button:hover {
  background: var(--menu-item-hover, rgba(255,255,255,0.1));
}

.viz-menu-icon {
  font-size: 1rem;
  width: 20px;
  text-align: center;
  flex-shrink: 0;
}

/* Hide menu in print */
@media print {
  .viz-menu { display: none !important; }
}
```

### JavaScript

```javascript
// === Menu toggle ===
function toggleMenu() {
  document.getElementById('vizMenuDropdown').classList.toggle('open');
}

// Close menu when clicking outside
document.addEventListener('click', (e) => {
  if (!e.target.closest('.viz-menu')) {
    document.getElementById('vizMenuDropdown').classList.remove('open');
  }
});

// Close menu on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') document.getElementById('vizMenuDropdown').classList.remove('open');
});

// === Theme system ===
const themes = [
  { name: 'Dark', class: 'theme-dark' },
  { name: 'Light', class: 'theme-light' },
  { name: 'Auto', class: 'theme-auto' },
];
let currentTheme = 0;

function cycleTheme() {
  // Remove all theme classes
  themes.forEach(t => document.documentElement.classList.remove(t.class));
  // Advance to next
  currentTheme = (currentTheme + 1) % themes.length;
  document.documentElement.classList.add(themes[currentTheme].class);
  document.getElementById('themeLabel').textContent = themes[currentTheme].name;
  // Persist
  localStorage.setItem('viz-theme', currentTheme);
}

// Restore saved theme on load
(function() {
  const saved = localStorage.getItem('viz-theme');
  if (saved !== null) {
    currentTheme = parseInt(saved);
    document.documentElement.classList.add(themes[currentTheme].class);
    document.getElementById('themeLabel').textContent = themes[currentTheme].name;
  }
})();

// === Download as PNG ===
async function downloadImage() {
  const btn = event.target.closest('button');
  const origText = btn.querySelector('span:last-child').textContent;
  btn.querySelector('span:last-child').textContent = 'Generating...';

  try {
    // Hide menu during capture
    const menu = document.querySelector('.viz-menu');
    menu.style.display = 'none';

    const dataUrl = await htmlToImage.toPng(document.body, {
      quality: 1,
      pixelRatio: 2, // 2x for retina quality
      cacheBust: true,
      filter: (node) => !node.classList?.contains('viz-menu'),
    });

    menu.style.display = '';

    // Trigger download
    const link = document.createElement('a');
    link.download = `${document.title || 'visualization'}.png`;
    link.href = dataUrl;
    link.click();
  } catch (err) {
    console.error('Image export failed:', err);
    alert('Image export failed. Try Print → Save as PDF instead.');
  }

  btn.querySelector('span:last-child').textContent = origText;
}

// === Print as PDF ===
function printPDF() {
  window.print();
}
```

## Theme CSS Pattern

Define theme variables on `:root` for dark (default), and override on `.theme-light`:

```css
:root, .theme-dark {
  --bg: hsl(220, 20%, 8%);
  --surface: hsl(220, 15%, 14%);
  --text: hsl(220, 10%, 92%);
  --text-secondary: hsl(220, 10%, 60%);
  --accent: hsl(220, 85%, 68%);
  /* Menu overrides for dark */
  --menu-bg: rgba(0, 0, 0, 0.7);
  --menu-bg-hover: rgba(0, 0, 0, 0.85);
  --menu-border: rgba(255, 255, 255, 0.1);
  --menu-text: #fff;
  --menu-item-hover: rgba(255, 255, 255, 0.1);
}

.theme-light {
  --bg: hsl(220, 15%, 97%);
  --surface: hsl(0, 0%, 100%);
  --text: hsl(220, 20%, 15%);
  --text-secondary: hsl(220, 10%, 45%);
  --accent: hsl(220, 80%, 50%);
  /* Menu overrides for light */
  --menu-bg: rgba(255, 255, 255, 0.85);
  --menu-bg-hover: rgba(255, 255, 255, 0.95);
  --menu-border: rgba(0, 0, 0, 0.1);
  --menu-text: #333;
  --menu-item-hover: rgba(0, 0, 0, 0.06);
}

.theme-auto {
  /* Uses prefers-color-scheme */
}

@media (prefers-color-scheme: light) {
  .theme-auto {
    --bg: hsl(220, 15%, 97%);
    --surface: hsl(0, 0%, 100%);
    --text: hsl(220, 20%, 15%);
    --text-secondary: hsl(220, 10%, 45%);
    --accent: hsl(220, 80%, 50%);
    --menu-bg: rgba(255, 255, 255, 0.85);
    --menu-bg-hover: rgba(255, 255, 255, 0.95);
    --menu-border: rgba(0, 0, 0, 0.1);
    --menu-text: #333;
    --menu-item-hover: rgba(0, 0, 0, 0.06);
  }
}
```

## Print Styles

Always include optimized print styles:

```css
@media print {
  .viz-menu,
  .nav,
  .progress { display: none !important; }

  body {
    background: white !important;
    color: black !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  /* For slide decks: print all slides */
  .slide {
    position: relative !important;
    opacity: 1 !important;
    transform: none !important;
    page-break-after: always;
    height: 100vh;
    display: flex !important;
  }

  .slide.prev { display: flex !important; }
}
```

## Best Practices

1. **html-to-image over html2canvas** — better SVG support, smaller bundle, handles CSS custom properties
2. **pixelRatio: 2** for retina-quality exports
3. **Hide UI elements** during capture (menu, nav, progress bars)
4. **cacheBust: true** to avoid stale image caching issues
5. **filter function** to exclude interactive elements from the export
6. **Fallback** — if html-to-image fails (CORS, complex SVG), suggest Print → Save as PDF
7. **localStorage** for theme persistence across page reloads
8. **Backdrop-filter** on the menu for frosted glass effect
9. **print-color-adjust: exact** to preserve colors when printing
10. **Page breaks** for slide decks so each slide is a separate PDF page

## Slide Deck Special Handling

For slide decks, the Download button should capture only the **current slide**, not the entire page:

```javascript
async function downloadImage() {
  // For slide decks, capture only the active slide
  const target = document.querySelector('.slide.active') || document.body;
  const menu = document.querySelector('.viz-menu');
  const nav = document.querySelector('.nav');

  menu.style.display = 'none';
  if (nav) nav.style.display = 'none';

  const dataUrl = await htmlToImage.toPng(target, {
    quality: 1,
    pixelRatio: 2,
    width: target.scrollWidth,
    height: target.scrollHeight,
  });

  menu.style.display = '';
  if (nav) nav.style.display = '';

  const link = document.createElement('a');
  const slideNum = document.querySelector('.slide.active')?.dataset?.slide || '';
  link.download = `${document.title}-slide${slideNum}.png`;
  link.href = dataUrl;
  link.click();
}
```

# Animation Reference — CSS-First, JS-Enhanced

## Philosophy

**CSS animations are the primary animation system.** They're reliable, performant, and don't break when JS has scoping issues. JavaScript is used only for scroll-triggered reveals and number counters.

**Rule: Content must ALWAYS be visible in CSS.** JavaScript adds `.visible` class for entrance animations. If JS fails, everything still shows.

## CDN (Optional — only include when needed)

Motion.js is available for advanced spring physics but is NOT required:
```html
<!-- OPTIONAL: only include for spring physics or complex orchestration -->
<script src="https://cdn.jsdelivr.net/npm/motion@12/dist/motion.js"></script>
```

## CSS Animations (Primary)

### Entrance Animations
```css
/* Base: content is visible by default */
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
@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}

/* Apply with staggered delays */
.animate { animation: fadeInUp 0.6s ease-out both; }
.animate.delay-1 { animation-delay: 0.1s; }
.animate.delay-2 { animation-delay: 0.2s; }
.animate.delay-3 { animation-delay: 0.3s; }
.animate.delay-4 { animation-delay: 0.4s; }
.animate.delay-5 { animation-delay: 0.5s; }
.animate.delay-6 { animation-delay: 0.6s; }

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  .animate, [class*="animate"] { animation: none !important; }
}
```

### Hover Effects (Pure CSS)
```css
/* Shadow-only hover — no translateY or scale transforms */
.card {
  transition: box-shadow 0.2s ease;
}
.card:hover {
  box-shadow: 0 0 0 1px var(--border), 0 8px 16px rgba(0,0,0,0.08);
}
```

### Scroll-Triggered Reveals (CSS + minimal JS)
```css
/* Elements start visible. JS adds .reveal class to opt-in to scroll animation. */
.reveal {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Stagger children */
.reveal.visible .stagger:nth-child(1) { transition-delay: 0.05s; }
.reveal.visible .stagger:nth-child(2) { transition-delay: 0.1s; }
.reveal.visible .stagger:nth-child(3) { transition-delay: 0.15s; }
.reveal.visible .stagger:nth-child(4) { transition-delay: 0.2s; }
.reveal.visible .stagger:nth-child(5) { transition-delay: 0.25s; }
.reveal.visible .stagger:nth-child(6) { transition-delay: 0.3s; }
```

## JavaScript (Minimal — scroll observer + counters only)

### Scroll Observer (10 lines)
```javascript
// Add .reveal class via JS (not CSS) so content is visible without JS
document.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('reveal'));
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } });
}, { threshold: 0.15 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

**Key:** The `data-reveal` attribute marks elements for scroll animation. JS adds the `.reveal` class (which sets opacity:0). When scrolled into view, `.visible` is added (which sets opacity:1). If JS fails, elements never get `.reveal`, so they stay visible.

### Number Counter (15 lines)
```javascript
function animateCounters() {
  document.querySelectorAll('[data-count]').forEach(el => {
    const target = parseFloat(el.dataset.count);
    const prefix = el.dataset.prefix || '';
    const suffix = el.dataset.suffix || '';
    const duration = 1200;
    const start = performance.now();
    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      el.textContent = prefix + Math.round(target * eased).toLocaleString() + suffix;
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });
}
// Trigger on scroll into view
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { animateCounters(); counterObserver.disconnect(); } });
}, { threshold: 0.3 });
const firstCounter = document.querySelector('[data-count]');
if (firstCounter) counterObserver.observe(firstCounter);
```

### Slide Transitions (CSS-based)
```css
.slide { display: none; opacity: 0; transition: opacity 0.3s ease; }
.slide.active { display: flex; opacity: 1; }
```
```javascript
// Simple slide nav — no animation libraries needed
var current = 0;
var transitioning = false;
function goToSlide(n) {
  if (n === current || n < 0 || n >= slides.length || transitioning) return;
  transitioning = true;
  slides[current].classList.remove('active');
  slides[n].classList.add('active');
  current = n;
  updateUI();
  setTimeout(() => { transitioning = false; }, 350);
}
```

## When to Use Motion.js (Optional)

Only include Motion.js when you specifically need:
- **Spring physics** — bouncy, organic-feeling animations
- **Complex orchestration** — multiple elements with precise timing relationships
- **Scroll-linked animations** — parallax, progress bars linked to scroll position

For everything else, CSS is simpler and more reliable.

## Anti-Patterns

- ❌ `Motion.animate().finished.then()` — Promise chain breaks silently if Motion API changes
- ❌ `Motion.inView()` with `opacity: 0` in CSS — content invisible if JS fails
- ❌ `let` declarations for chart variables called before initialization — use `var` for variables referenced across function hoisting boundaries
- ❌ Complex stagger calculations in JS — use CSS `nth-child` delays instead
- ❌ Hiding content by default and revealing via JS — content must be visible without JS

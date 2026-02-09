#!/usr/bin/env node
//
// analyze-styles.js - Extract and analyze CSS from a website
//
// Usage: node analyze-styles.js <URL>

const { chromium } = require('playwright');

async function analyzeStyles(url) {
  console.log(`🔍 Analyzing styles for: ${url}\n`);

  const browser = await chromium.launch();
  const page = await browser.newPage();

  try {
    await page.goto(url, { waitUntil: 'networkidle' });

    // Extract CSS custom properties
    console.log('## CSS Custom Properties (Design Tokens)\n');
    const customProps = await page.evaluate(() => {
      const props = new Set();
      for (const sheet of document.styleSheets) {
        try {
          for (const rule of sheet.cssRules) {
            if (rule.cssText) {
              const matches = rule.cssText.matchAll(/--[\w-]+/g);
              for (const match of matches) {
                props.add(match[0]);
              }
            }
          }
        } catch (e) {
          // Cross-origin stylesheets
        }
      }

      // Also get computed style custom properties from :root
      const root = document.documentElement;
      const rootStyles = getComputedStyle(root);
      for (let i = 0; i < rootStyles.length; i++) {
        const prop = rootStyles[i];
        if (prop.startsWith('--')) {
          props.add(`${prop}: ${rootStyles.getPropertyValue(prop)}`);
        }
      }

      return Array.from(props).sort();
    });

    if (customProps.length > 0) {
      customProps.slice(0, 50).forEach(prop => console.log(`  ${prop}`));
      if (customProps.length > 50) {
        console.log(`  ... and ${customProps.length - 50} more`);
      }
    } else {
      console.log('  None found');
    }

    // Extract color palette from computed styles
    console.log('\n## Color Palette (from key elements)\n');
    const colors = await page.evaluate(() => {
      const colorSet = new Set();
      const elements = document.querySelectorAll('body, header, nav, main, footer, h1, h2, h3, a, button, .btn, .button');

      elements.forEach(el => {
        const styles = getComputedStyle(el);
        ['color', 'background-color', 'border-color'].forEach(prop => {
          const value = styles[prop];
          if (value && value !== 'rgba(0, 0, 0, 0)' && value !== 'transparent') {
            colorSet.add(value);
          }
        });
      });

      return Array.from(colorSet).slice(0, 20);
    });

    colors.forEach(color => console.log(`  ${color}`));

    // Typography analysis
    console.log('\n## Typography\n');
    const typography = await page.evaluate(() => {
      const fontData = [];
      const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
      const body = document.querySelector('body');

      headings.forEach((h, idx) => {
        if (idx < 3) {  // Only first few headings
          const styles = getComputedStyle(h);
          fontData.push({
            tag: h.tagName,
            family: styles.fontFamily,
            size: styles.fontSize,
            weight: styles.fontWeight,
            lineHeight: styles.lineHeight,
            letterSpacing: styles.letterSpacing
          });
        }
      });

      const bodyStyles = getComputedStyle(body);
      fontData.push({
        tag: 'BODY',
        family: bodyStyles.fontFamily,
        size: bodyStyles.fontSize,
        weight: bodyStyles.fontWeight,
        lineHeight: bodyStyles.lineHeight,
        letterSpacing: bodyStyles.letterSpacing
      });

      return fontData;
    });

    typography.forEach(font => {
      console.log(`  ${font.tag}:`);
      console.log(`    Font: ${font.family}`);
      console.log(`    Size: ${font.size}`);
      console.log(`    Weight: ${font.weight}`);
      console.log(`    Line height: ${font.lineHeight}`);
      console.log(`    Letter spacing: ${font.letterSpacing}`);
      console.log();
    });

    // Detect frameworks and libraries
    console.log('## Detected Technologies\n');
    const technologies = await page.evaluate(() => {
      const detected = {};

      // Framework detection
      detected.react = !!document.querySelector('[data-reactroot], [data-reactid], #root, #__next');
      detected.vue = !!window.Vue || !!document.querySelector('[data-v-]');
      detected.angular = !!window.ng || !!document.querySelector('[ng-version]');
      detected.svelte = !!document.querySelector('[data-svelte]');
      detected.nextjs = !!window.__NEXT_DATA__;
      detected.nuxt = !!window.__NUXT__;
      detected.gatsby = !!window.___gatsby;
      detected.astro = !!document.querySelector('[data-astro-cid]');

      // CSS frameworks
      detected.tailwind = !!document.querySelector('[class*="flex"], [class*="grid"]') &&
                          document.querySelector('link[href*="tailwind"]');
      detected.bootstrap = !!document.querySelector('[class*="col-"], [class*="container"]') ||
                           !!document.querySelector('link[href*="bootstrap"]');
      detected.materialUI = !!document.querySelector('[class*="Mui"], [class*="makeStyles"]');

      // Animation libraries
      detected.framerMotion = !!window.MotionGlobalConfig;
      detected.gsap = !!window.gsap;

      return detected;
    });

    Object.entries(technologies).forEach(([tech, detected]) => {
      if (detected) {
        console.log(`  ✅ ${tech}`);
      }
    });

    // Spacing system detection
    console.log('\n## Spacing System (margins/padding from key elements)\n');
    const spacing = await page.evaluate(() => {
      const spacingSet = new Set();
      const elements = document.querySelectorAll('section, div, article, header, footer, nav');

      Array.from(elements).slice(0, 50).forEach(el => {
        const styles = getComputedStyle(el);
        ['margin-top', 'margin-bottom', 'padding-top', 'padding-bottom', 'gap'].forEach(prop => {
          const value = styles[prop];
          if (value && value !== '0px') {
            spacingSet.add(value);
          }
        });
      });

      return Array.from(spacingSet).sort((a, b) => {
        return parseFloat(a) - parseFloat(b);
      }).slice(0, 20);
    });

    console.log('  ' + spacing.join(', '));

  } catch (error) {
    console.error('❌ Error:', error.message);
  } finally {
    await browser.close();
  }
}

// Main
const url = process.argv[2];
if (!url) {
  console.error('Usage: node analyze-styles.js <URL>');
  process.exit(1);
}

analyzeStyles(url).catch(console.error);

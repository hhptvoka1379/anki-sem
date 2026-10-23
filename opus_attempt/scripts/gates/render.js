// Gate 9 (+ no-JS check for gate 7): renders cards with headless Chromium.
// Usage: node render.js <manifest.json> <outdir>
// manifest: {cards:[{kind:"mcq"|"fill", front:"abs html path", back:"abs html path", must_show:[...]}]}
// Writes <outdir>/<kind>_<front|back>_<light|dark>.png and <outdir>/render_results.json
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

(async () => {
  const manifest = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const outdir = path.resolve(process.argv[3]);
  fs.mkdirSync(outdir, { recursive: true });
  const browser = await chromium.launch();
  const results = { screens: [], nojs: [] };
  for (const card of manifest.cards) {
    for (const side of ["front", "back"]) {
      for (const theme of ["light", "dark"]) {
        if (card.screenshots === false) continue;
        const ctx = await browser.newContext({ viewport: { width: 390, height: 800 }, deviceScaleFactor: 2 });
        const page = await ctx.newPage();
        await page.goto("file://" + card[side]);
        if (theme === "dark") {
          await page.evaluate(() => document.body.classList.add("nightMode", "night_mode"));
        }
        await page.evaluate(() => document.fonts.ready);
        await page.waitForTimeout(150);
        const info = await page.evaluate(() => ({
          scrollWidth: document.documentElement.scrollWidth,
          fonts: [...document.fonts].map((f) => f.family.replace(/"/g, "") + ":" + f.status),
        }));
        const file = path.join(outdir, `${card.kind}_${side}_${theme}.png`);
        await page.screenshot({ path: file, fullPage: true });
        results.screens.push({ file, kind: card.kind, side, theme, ...info, horizontal_overflow: info.scrollWidth > 390 });
        await ctx.close();
      }
    }
    // JavaScript off: the back must still show everything in must_show.
    const ctx = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 800 } });
    const page = await ctx.newPage();
    await page.goto("file://" + card.back);
    const text = await page.locator("body").innerText();
    results.nojs.push({
      kind: card.kind,
      missing: (card.must_show || []).filter((s) => !text.includes(s)),
      checked: card.must_show || [],
    });
    await ctx.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(outdir, "render_results.json"), JSON.stringify(results, null, 1));
  console.log(JSON.stringify({ screens: results.screens.length, nojs: results.nojs.length }));
})().catch((e) => { console.error(e); process.exit(1); });

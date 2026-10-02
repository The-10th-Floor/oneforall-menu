// PLAYWRIGHT=/path/to/playwright CHROME=/path/to/chrome node test-header.cjs (menu server on :8080)
const assert = require('node:assert/strict');
const { chromium } = require(process.env.PLAYWRIGHT || 'playwright');
(async () => {
 const browser = await chromium.launch({ executablePath: process.env.CHROME });
 try {
  for (const landing of [false,true]) for (const width of [320,390,1280]) for (const lang of ['ar','en']) {
   const page = await browser.newPage({ viewport:{width,height:844} });
   await page.goto('http://localhost:8080/' + (landing?'irbid/':'') + '?lang=' + lang);
   await page.waitForLoadState('networkidle');
   const button = page.locator(landing?'.lang':'.dock button:visible');
   assert.equal(await button.count(),1);
   assert.equal((await button.textContent()).trim(),lang==='ar'?'English':'عربي');
   const layout = await button.evaluate(el=>{const b=el.getBoundingClientRect(), head=el.closest('header'), logo=head.querySelector('img').getBoundingClientRect();return {sameRow:Math.abs(b.y+b.height/2-logo.y-logo.height/2)<5,rightOfLogo:b.x>=logo.right,overflow:document.documentElement.scrollWidth>innerWidth,border:getComputedStyle(el).backgroundImage};});
   assert.ok(layout.sameRow && layout.rightOfLogo && !layout.overflow,JSON.stringify({landing,width,lang,layout}));
   assert.ok(layout.border.includes('svg'));
   assert.equal(await page.locator('.native-prompt').isVisible(),false);
   if(!landing){
    assert.equal(await page.locator('#menu-title').textContent(),lang==='ar'?'منيو':'Menu');
    const centered=await page.locator('.menu-brand').evaluate(el=>{const r=el.getBoundingClientRect(),h=el.closest('header').getBoundingClientRect();return Math.abs(r.x+r.width/2-h.x-h.width/2)<2;});
    assert.ok(centered);
   }
   if(lang==='ar'&&width===390)await page.screenshot({path:'/Users/admin/projects/OFA/.local/' + (landing?'landing':'menu') + '-organic-language-2026-10-02.png'});
   await button.click();
   assert.equal(await page.locator('html').getAttribute('lang'),lang==='ar'?'en':'ar');
   assert.equal((await page.locator(landing?'.lang':'.dock button:visible').textContent()).trim(),lang==='ar'?'عربي':'English');
   await page.close();
  }
  console.log('12 header cases passed: single alternate language, organic frame, one row, no overflow, language switching');
 } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1;});

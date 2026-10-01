// node pages-dev/test.mjs — checks the routing in _worker.js with GitHub Pages faked. No network.
import assert from 'node:assert/strict';
import worker from './_worker.js';

const asked = [];
globalThis.fetch = async (u, init = {}) => {
  asked.push(u);
  const path = new URL(u).pathname;
  if (path === '/oneforall-menu/irbid') return new Response(null, { status: 301, headers: { location: 'http://the-10th-floor.github.io/oneforall-menu/irbid/' } });
  if (path === '/oneforall-menu/plan') return new Response(null, { status: 301, headers: { location: 'https://the-10th-floor.github.io/oneforall-menu/plan/' } });
  return new Response('file ' + path, { status: 200 });
};
const get = (u, method = 'GET') => worker.fetch(new Request(u, { method }));
const where = async (u) => { const r = await get(u); return r.status + ' ' + (r.headers.get('location') ?? await r.text()); };

const cases = [
  ['https://oneforalljo.com/', '301 https://oneforalljo.com/irbid/'],
  ['https://oneforalljo.com/?lang=ar', '301 https://oneforalljo.com/irbid/?lang=ar'],
  ['https://oneforalljo.com/menu', '301 https://oneforalljo.com/menu/'],
  ['https://oneforalljo.com/menu/?lang=en&from=site', '200 file /oneforall-menu/'],
  ['https://oneforalljo.com/menu/menu-ar.svg', '200 file /oneforall-menu/menu-ar.svg'],
  ['https://oneforalljo.com/irbid/', '200 file /oneforall-menu/irbid/'],
  ['https://oneforalljo.com/irbid', '301 https://oneforalljo.com/irbid/'],
  ['https://oneforalljo.com/menu/plan', '301 https://oneforalljo.com/menu/plan/'],
  ['https://oneforalljo.com/sitemap.xml', '200 file /oneforall-menu/sitemap.xml'],
  ['https://www.oneforalljo.com/irbid/?lang=en', '301 https://oneforalljo.com/irbid/?lang=en'],
  ['https://oneforall-jo.pages.dev/irbid/', '301 https://oneforalljo.com/irbid/'],
  ['https://oneforall-jo.pages.dev/', '301 https://oneforalljo.com/'],
  ['https://oneforall-jo.pages.dev/google85fa2133dd80e4b3.html', '200 file /oneforall-menu/google85fa2133dd80e4b3.html'],
  ['https://oneforall-jo.pages.dev/d590794667958097a6f50493ef61101a.txt', '200 file /oneforall-menu/d590794667958097a6f50493ef61101a.txt'],
];
for (const [u, want] of cases) assert.equal(await where(u), want, u);
asked.length = 0;
await get('https://oneforalljo.com/irbid/?lang=ar&v=1');
assert.equal(asked[0], 'https://the-10th-floor.github.io/oneforall-menu/irbid/?lang=ar&v=1', 'query reaches GitHub');
assert.equal((await get('https://oneforalljo.com/irbid/', 'POST')).status, 405);
assert.equal((await get('https://oneforalljo.com/irbid/', 'HEAD')).status, 200);
console.log(`ok  ${cases.length + 4} checks`);

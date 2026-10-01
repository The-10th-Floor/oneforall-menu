// The Cloudflare Pages project "oneforall-jo" (Zaid's account). Since 2026-10-01 it answers two kinds of address:
// - oneforalljo.com, the shop's site: "/" is the main page (a 301 to /irbid/), "/menu/" is the menu, and every other
//   path is the same file from GitHub Pages (this repo, served at ORIGIN). Push to main, and the site follows.
// - every other host (oneforall-jo.pages.dev, the interim address from 2026-09-24, and www): a 301 to oneforalljo.com,
//   path and query kept.
// Deploy: npx wrangler pages deploy pages-dev --project-name oneforall-jo --branch main
// The NFC tag and the printed QR keep the github.io address. GitHub serves the menu there itself (no custom domain on
// the repo), so a tap never passes through here.
const SITE = 'https://oneforalljo.com';
const HOST = 'oneforalljo.com';
const ORIGIN = 'https://the-10th-floor.github.io/oneforall-menu';
// Google's ownership check (the pages.dev property in Search Console) and IndexNow's key check both reject a
// redirect, so on the old address these two files answer 200.
const EXEMPT = new Set(['/google85fa2133dd80e4b3.html', '/d590794667958097a6f50493ef61101a.txt']);
// GitHub names its own host in a redirect (a missing slash, for one), sometimes with http://.
const GITHUB = /^https?:\/\/the-10th-floor\.github\.io\/oneforall-menu/;

async function site(request, url) {
  const p = url.pathname;
  if (p === '/') return Response.redirect(SITE + '/irbid/' + url.search, 301);
  if (p === '/menu') return Response.redirect(SITE + '/menu/' + url.search, 301);
  // /menu/ is the tag page: the repo root. Its files are relative, so /menu/menu-ar.svg is the root's menu-ar.svg.
  const prefix = p.startsWith('/menu/') ? '/menu' : '';
  const res = await fetch(ORIGIN + p.slice(prefix.length) + url.search, { method: request.method, redirect: 'manual' });
  const to = res.headers.get('location');
  if (!to) return res;
  const headers = new Headers(res.headers);
  headers.set('location', to.replace(GITHUB, SITE + prefix));
  return new Response(res.body, { status: res.status, headers });
}

export default {
  async fetch(request) {
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return new Response('Method not allowed', { status: 405, headers: { allow: 'GET, HEAD' } });
    }
    const url = new URL(request.url);
    if (url.hostname === HOST) return site(request, url);
    if (EXEMPT.has(url.pathname)) return fetch(ORIGIN + url.pathname, { method: request.method });
    return Response.redirect(SITE + url.pathname + url.search, 301);
  },
};

// oneforall-jo.pages.dev — the interim public address (2026-09-24 to 2026-10-01). The shop's own domain is now
// oneforalljo.com, so this only sends every visitor and crawler there with a 301, path and query kept.
// Deploy (Cloudflare account of Zaid, project "oneforall-jo"):
//   npx wrangler pages deploy pages-dev --project-name oneforall-jo --branch main
// Nothing on the NFC tag or the printed QR points here; they keep the github.io address.
const SITE = 'https://oneforalljo.com';
const ORIGIN = 'https://the-10th-floor.github.io/oneforall-menu';
// Google's ownership check (the pages.dev property in Search Console) and IndexNow's key check both reject a
// redirect, so these two files are fetched from GitHub (which 301s to SITE) and answered with 200.
const EXEMPT = new Set(['/google85fa2133dd80e4b3.html', '/d590794667958097a6f50493ef61101a.txt']);

export default {
  async fetch(request) {
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return new Response('Method not allowed', { status: 405, headers: { allow: 'GET, HEAD' } });
    }
    const url = new URL(request.url);
    if (EXEMPT.has(url.pathname)) return fetch(ORIGIN + url.pathname, { method: request.method });
    // Built here, not taken from GitHub: GitHub's own 301 sometimes names http:// (seen 2026-10-01 on /irbid/?lang=ar).
    return Response.redirect(SITE + url.pathname + url.search, 301);
  },
};

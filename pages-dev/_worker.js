// oneforall-jo.pages.dev — the shorter address, until the shop buys its own domain.
// It only forwards: the site itself is this repo on GitHub Pages, so the two addresses can never drift.
// Deploy (Cloudflare account of Zaid, project "oneforall-jo"):
//   npx wrangler pages deploy pages-dev --project-name oneforall-jo --branch main
// Nothing on the NFC tag or the printed QR points here; they keep the github.io address.
const ORIGIN = 'https://the-10th-floor.github.io/oneforall-menu';

export default {
  async fetch(request) {
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return new Response('Method not allowed', { status: 405, headers: { allow: 'GET, HEAD' } });
    }
    const url = new URL(request.url);
    const upstream = ORIGIN + url.pathname + url.search;

    // Pass on only what matters for caching and video seeking; the film page fetches clips by range.
    const headers = new Headers();
    for (const h of ['range', 'if-none-match', 'if-modified-since', 'accept', 'user-agent']) {
      const v = request.headers.get(h);
      if (v) headers.set(h, v);
    }
    const res = await fetch(upstream, { method: request.method, headers, redirect: 'manual' });

    const out = new Headers(res.headers);
    // GitHub answers /irbid with a 301 to the absolute github.io /irbid/; keep the visitor on this host.
    const loc = out.get('location');
    if (loc) {
      const target = new URL(loc, upstream);
      if (target.href.startsWith(ORIGIN + '/')) out.set('location', url.origin + target.href.slice(ORIGIN.length));
    }
    return new Response(res.body, { status: res.status, statusText: res.statusText, headers: out });
  },
};

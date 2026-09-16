# NFC — tag choice, buying, programming, locking

## The tag  `[CONFIRMED by research, NXP + Seritag sources — see research/RESEARCH.md §C]`
- Chip: **genuine NXP NTAG213** (144 B user memory ≈ 136-char URL, NFC Forum Type 2, 10-year retention,
  password + permanent lock). NTAG215/216 add memory you will never use; NTAG 424 DNA is anti-counterfeit
  money for nothing here; ICODE SLIX has an iPhone background-read failure mode. Avoid all three.
- Form: **round label 30–38 mm, antenna ≥25 mm** (ideally 34–35 mm). Antenna size sets read range, not chip.
- Body material in front of the tag: ≤3 mm acrylic or ≤4 mm PETG/ASA. Never PLA outdoors.
- Never mount on or within 40 mm of metal (the blue window frame). Plaster, glass, tile, plastic: all fine.
- Counterfeit NTAG chips are common in no-name packs → check every batch with the free **NXP TagInfo** app
  (Android/iOS): a genuine chip passes the "originality signature" check.

## Where to buy (Jordan)  `[research-graded; prices read 16 Sep 2026, re-check before paying]`
| Route | What | Price | Lead time | Notes |
|---|---|---|---|---|
| **Waslleh** واصلة · waslleh.com · +962 7 80 83 83 00 | NTAG213 white round sticker (SKU WS-00647); 22×22 mm NTAG215 mini card (WS-04389); NTAG215 PVC card (WS-04267) | 0.635 / 0.722 / 0.741 JOD | same-day dispatch before 8:30 PM; free shipping >33 JOD | Best for prototyping this week. Sticker diameter not listed — ask; if <30 mm use it only for testing |
| **MikroElectron** · Queen Rania St, Amman · WhatsApp +962 6 2225522 | Waterproof NTAG213 sticker; NTAG215 card | not readable online | walk-in | Second local source; WhatsApp for price/stock |
| **AliExpress** (JOD prices, ships to Jordan) | 30 mm / 38 mm NTAG213 round labels, epoxy coins, 10–100 packs | ≈0.03–0.10 JOD per tag | 10–25 business days | Since 1 Feb 2026: 16% sales tax on parcels ≤JD200 (min JD5), no duty. Buy a 4.8+ rated listing with 1,000+ sold; verify with TagInfo |
| Ubuy Jordan | 50× NTAG215 cards, US stock | JOD 18 + shipping/customs | ≈8 days | fallback only |
| Amazon.ae / noon | — | — | — | do NOT ship to Jordan. Amazon.com quotes ≈$98 shipping on a $6 pack |

Plan: buy 10 Waslleh stickers now (≈6.4 JOD) for prototyping and the first install; order a 20-pack of
38 mm NTAG213 labels from AliExpress for the final + spares + the second window/branch.

## The URL on the tag  `[CONFIRMED]`
```
https://the-10th-floor.github.io/oneforall-menu/
```
This is already written on the existing window tag and printed as QR (earlier repo). Write the same plain URL on every
new tag — no query strings, so old and new tags stay identical. The menu behind it changes by pushing to the repo.
Later upgrade (optional, research HIGH): put **Short.io Free** or Cloudflare in front for tap counts and a branded
`go.oneforall.jo` (.jo = 50 JOD/yr at dns.jo, needs the commercial registration) — but only if you are willing to
rewrite the existing tag once. The brand's live ordering storefront, `bitesnbags.com/choose-delivery-type/one-for-all`,
is the natural "Order" link to add on the page, not a tag target.

## Writing the tag (5 minutes, any NFC phone)
1. Install **NFC Tools** (Android/iOS) or **NXP TagWriter** (Android).
2. Write → Add a record → **URL/URI** → paste the short link → Write. Hold the phone's top edge on the tag.
3. Read it back: it must show exactly one URI record, `https://…`.
4. Test on an iPhone in background mode (screen on, no app open) and on an Android; both should pop the link.
5. **Lock it.** Public wall = anyone could rewrite it to a phishing page. NFC Tools → Other → *Lock tag*
   (permanent, irreversible; that is why the URL is a redirect) — or at minimum set a password
   (NFC Tools → Other → Set password) if you want to keep the option to rewrite.
6. Only now stick the tag into the holder pocket. Test again through the assembled holder.

## Phone behaviour to expect
- iPhone XS and newer: reads in the background, screen on, no app. Not while the camera or Wallet is open.
- Android: reads whenever the screen is unlocked; Android 16 opens https tags straight in the browser.
- iPhone antenna is the top-back edge; most Androids centre/upper-back. The burger's centre is the tap spot.

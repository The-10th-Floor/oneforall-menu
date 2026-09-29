# NFC — tag choice, buying, programming, locking

## The tag  `[CONFIRMED by research, NXP + Seritag sources — see research/RESEARCH.md §C]`
- Chip: **genuine NXP NTAG213** (144 B user memory ≈ 136-char URL, NFC Forum Type 2, 10-year retention,
  password + permanent lock). NTAG215/216 add memory you will never use; NTAG 424 DNA is anti-counterfeit
  money for nothing here; ICODE SLIX has an iPhone background-read failure mode. Avoid all three.
- Form: **round label 30–38 mm, antenna ≥25 mm** (ideally 34–35 mm). Antenna size sets read range, not chip.
- Earlier prototype target: ≤3 mm acrylic or ≤4 mm PETG/ASA over the tag. This is not a read-performance guarantee. The one-piece STL has a thicker cover (about 4.9 mm before relief), so it does not meet that earlier target and needs its own physical read test.
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

## Program and accept a prototype before protecting the production tag

1. Use an unlocked test tag. In NFC Tools or NXP TagWriter, create one URL/URI record containing exactly `https://the-10th-floor.github.io/oneforall-menu/` — not a new short link.
2. Read the NDEF record back and compare the **whole URL**, including the path and trailing slash. Open it and confirm the current bilingual menu loads.
3. Temporarily place the tag inside the assembled prototype. Test a supported iPhone and an NFC-enabled Android at the actual mounting location, with the final face material, normal approach and phone cases. Record phone/OS, material, orientation and result. A bare-tag bench read does not accept the installed piece.
4. Keep development tags writable and supervised. Do not permanently lock them or glue them into an inaccessible build before acceptance.
5. After the owner approves the tested destination and finished piece, apply the chosen write protection to the production tag and read/test it again. Permanent read-only lock bits cannot be undone; password protection is a different mechanism, not an equivalent guarantee. Do not leave a writable tag unattended on a public wall.

NXP documents the NTAG213 memory and lock behaviour in its [NTAG213/215/216 data sheet](https://www.nxp.com/docs/en/data-sheet/NTAG213_215_216.pdf). No tag was programmed or locked during this review.

## Phone acceptance

Supported iPhones can read URI tags in the background, but availability depends on device state. Apple documents restrictions including active Camera/Wallet use and the post-restart locked state. Follow [Apple's background-reading guidance](https://developer.apple.com/documentation/corenfc/adding-support-for-background-tag-reading) and [NFC interaction guidance](https://developer.apple.com/design/human-interface-guidelines/nfc).

Android behaviour depends on NFC support, settings, device and OS; test the actual phones rather than promise every Android opens automatically. Find the antenna's reliable approach on each test phone. An unreadable tag, wrong destination or failure through the mounted assembly is a failed test; correct it before public placement or locking.

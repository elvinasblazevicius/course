# Deep dive: moon rituals / moon magic / lunar living (KDP nonfiction)

Research date: 2026-10-15. Sources: Amazon.com search and product pages (TinyFish fetch, many 503/bot pages, retried), Amazon.co.uk/.com.au product pages (which show reviews), Goodreads book pages, USNO and NASA phase tables, Wild Hunt (Aug 2026), Daily Hive on Pinterest Fall 2026 report.

**Labels.** VERIFIED means I read it on a fetched page today. ASSUMED means inferred and not checked. BSR is the Amazon.com Books rank unless marked UK.

Raw working files are in /tmp/claude-0/-home-user-course/5d910e26-d220-53df-b12b-0c4e5f61c868/scratchpad/moon/:
- prod.tsv: product data
- ser.json: parsed SERPs
- gr2_rev.json: Goodreads reviews with star ratings
- crit.txt: full texts of the 1–3★ reviews
- usno2027.json: USNO 2027 phases
- signs2027.txt: computed signs

---

## 1. Demand and sub-niches

### Searches captured (Amazon.com Books, page 1, VERIFIED)
- lunar living book
- new moon rituals
- full moon rituals
- moon phases book for beginners
- moon journal
- moon magic book
- witchcraft for beginners
- 2027 moon planner

I also used the earlier W4 screen for "moon rituals book" and "wheel of the year book". "moon rituals for women", "13 moons book" and "2027 lunar calendar" returned 503 on every try, so I have **no data** for them.

The 8 captured queries returned 132 distinct ASINs. The same core titles fill page 1 across queries. Each of these four appears on 4 of the 8 queries:
- Moon Spells
- Moon Magic (Ahlquist)
- Westwood's Moon Rituals
- **The 2027 Witch's Moon Guide**: indie, June 2026, only 2 ratings

### Top 10 distinct books, moon-specific (VERIFIED unless noted)

| # | Title (author) | Publisher | Date | Pages | Price seen | Rating | Ratings | BSR | Colour vs B&W | Gift vs guide |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Moon Spells (Diane Ahlquist) | Adams Media | 2002-07-01 | 272 | $7.24 PB | 4.8 | 6,503 | 10,106 | B&W text (ASSUMED) | Guide/spellbook |
| 2 | Moon Magic: A Handbook of Lunar Cycles, Lore… (Aurora Kane) | Wellfleet Press | 2020-01-28 | 192 | $11.00 HC | 4.8 | 1,910 | 30,076 | Illustrated/decorative. Goodreads reviewers: "most aesthetically beautiful book I own" (VERIFIED as illustrated; full colour ASSUMED) | **Gift-style** handbook |
| 3 | Moon Magic: Your Complete Guide (Ahlquist) | Adams Media | 2017-12-05 | 256 | $9.41 PB | 4.7 | 1,280 | 42,298 | B&W (ASSUMED) | Guide |
| 4 | Moonology (Yasmin Boland) | Hay House UK | 2016-07-05 | 256 | $8.86 PB | 4.7 | 4,917 | 55,300 (UK 61,749) | B&W (ASSUMED) | Guide plus astrology reference |
| 5 | Moon Rituals: Harness Lunar Power… (Ann Westwood) | Independently published | 2025-01-06 | 245 | $11.99 PB | 4.6 | 181 (UK 134) | 62,877 (**UK 21,262**) | B&W (ASSUMED) | Guide. **Indie proof of concept** |
| 6 | The Moon Apothecary (Lorriane Anderson) | Rockpool | 2024-10-01 | 272 | $19.86 HC | 4.8 | 112 | 77,125 | Illustrated (ASSUMED) | Gift-style. Recipes (ingestion, off-limits for us) |
| 7 | Moon Lists (Leigh Patterson), guided journal | Clarkson Potter | 2019-06-25 | 160 | – | 4.6 | 431 | 106,297 | ASSUMED illustrated | Journal/gift |
| 8 | Lunar Living (Kirsty Gallagher) | Yellow Kite | 2022-05-10 (US HC) | 224 | $22.99 HC | 4.7 | 2,518 | 133,031 (**UK 14,267**) | ASSUMED B&W | Guide. UK-strong |
| 9 | The Moon Journal (Sandy Sitron) | Chronicle | 2018-08-14 | 192 | – | 4.7 | 399 | 161,467 | ASSUMED illustrated | Journal/gift |
| 10 | Living Lunarly (Lunarly, Kiki Ely) | Rock Point | 2021-11-02 | 208 | $19.99 HC | 4.7 | 161 | 179,827 | Illustrated (Goodreads: "love the artwork and illustrations", VERIFIED) | **Gift-style** self-care |

### Others checked (VERIFIED)
| Title | Publisher | Date | Pages | Rating / ratings | BSR |
|---|---|---|---|---|---|
| The Moon Rituals: 96 Rituals (Sara Walka) | Sisters Enchanted | 2024-11-21 | 470, 7x10 | 4.8 / 106 | 217,341 at $20.73 |
| Full Moon Yearbook (Julie Peters) | David & Charles | 2023-11-28 | 144 | 4.7 / 65 | 253,732 |
| Lunar Magic: A Beginner's Guide (Ashley Brittany) | master plan focus publishing | 2024-02-22 | 135 | 4.9 / 29 | 470,181 |
| Moon Phases (Lattari) | Andrews McMeel | 2022 | 160 | 4.7 / 32 | 575,059 |
| Lunar Abundance (Ezzie Spencer) | Running Press | 2018 | – | 4.6 / 547 | 985,790 |
| Practical Moon Magic (Katie Huang) | Leaping Hare | 2025-09-23 | 160 | 4.9 / 9 | 185,259 |
| Manifesting by the Moon (Sankey & Anderson) | Llewellyn | 2026-02-08 | 324 | 5.0 / 31 | 357,470 |
| Modern Witchcraft Book of Moon Magick (Hadas) | Adams | – | – | 4.9 / 57 | not captured |

### Adjacent broad market, "witchcraft for beginners" (VERIFIED)
- The Spell Book for New Witches (Callisto, 2020, 244 pp, $9.99): 4.7 from 20,507 ratings, BSR 3,954.
- The Green Witch (Adams, 2017): 18,396 ratings, "#1 Best Seller" badge.

The broad witchcraft market is roughly 3–10x the moon-specific one.

### Journals (VERIFIED badges from the search page)
- Moon Goddess Journal (Peter Pauper): "1K+ bought in past month".
- Moon Shadowork Journal (Kira Scott, indie, 2025-11-26, 154 pp, $9.99): 4.8 from 30 ratings, BSR 79,015, "300+ bought in past month".

### Evergreen vs year-specific (VERIFIED)
- **Llewellyn's 2027 Moon Sign Book** (2026-07-08, 312 pp): 5.0 from 3 ratings, BSR **31,036**, #23 Almanacs & Yearbooks.
- **Moonology Diary 2027** (Hay House UK, 2026-07-28, 264 pp): 4.9 from 38 ratings, **UK BSR 4,521, #3 Astrology (UK)**. The US page would not load.
- **The 2027 Witch's Moon Guide** (Ophelia Rune, indie, 2026-06-09, 138 pp, $13.99 PB): 5.0 from 2 ratings, BSR **111,119**, #49 Almanacs & Yearbooks. It surfaces on page 1 for four moon queries.
- The "2027 moon planner" page 1 was entirely 2026-dated listings:
  - Llewellyn calendars
  - Stacey Demarco and Nicci Garaicoa calendars
  - indie planners from Night Star Publishing (2026-09-11) and Kelly Brown (2026-10-12)
  - two "50+ bought in past month" badges
- The prior-year pattern also exists: Lunar Living 2026 (indie, 2025-11-09, 8.5x11, 119 pp) and 2026 Lunar & Zodiac Life Planner (2025-11-12).

**What this means (inference):** a year-specific annual is a real, repeatable series. Trade players (Llewellyn, Hay House) launch in July. Indie entries are thin and low-rated. The selling window is ASSUMED to be about Jul–Feb; I have no seasonality data. Each edition is dead stock after its year.

### Sub-niches seen
1. **Spellbook / witchcraft moon magic.** Ahlquist, Kane, Hadas, Walka. Largest.
2. **Astrology-driven lunar living.** Moonology, Lunar Living, Moon Sign Book. Needs zodiac accuracy.
3. **Self-care / wellness lunar.** Living Lunarly, Lunar Abundance, Practical Moon Magic. Gift-style, illustrated.
4. **Guided journals / shadow work.** Moon Lists, Moon Journal, Shadowork Journal. Low-content, steady.
5. **Annual almanacs / planners.**
6. **Ingestion-heavy apothecary / recipes.** Moon Apothecary. Off-limits under the publisher rules.

## 2. Saturation and trend

### Title count
I could not get Amazon's total-result counts; the fetched pages omit them. In 8 queries I saw 132 distinct ASINs on page 1 alone.

### AI flood (VERIFIED)
- Originality.ai's scan, reported by The Wild Hunt on 2026-08-25, covered 2,034 religion books mostly published Jan–Jun 2026.
- It flagged **78% of Witchcraft books as likely AI-written**, the highest category.
- It flagged >50% of fact-checkable witchcraft claims as potentially false.
- Likely-AI books averaged 170 pp and $16.84, against 208 pp and $18.96 for likely-human books.
- The detectors are imperfect (stated in the article).

So the new-release shelf is crowded and readers are primed to distrust it.

### 2025–26 titles that sell (BSR < 100k, VERIFIED BSRs)
**Selling:**
- Westwood, Moon Rituals: 2025-01, 62,877
- Kira Scott, Shadowork Journal: 2025-11, 79,015
- Llewellyn's 2027 Moon Sign Book: 2026-07, 31,036 (trade annual)
- Moonology Diary 2027: UK 4,521 (trade annual)
- Adjacent, from the W4 screen: Celtic Wheel of the Year (2026-01, 63,431)

**Not selling:**
- 2027 Witch's Moon Guide: 111k
- Practical Moon Magic: 185k
- Moon Manifestation Journal: 2026-05, 204,278
- Manifesting by the Moon: 357k
- Moon Rituals for Beginners (Liora Veylen, indie, 2026-08-08, 162 pp, sold as "Reflective Practices"): 1,743,150 with 0 ratings

**Result:** about 2 evergreen and 2 annual titles from 2025–26 are under 100k out of roughly 9 checked. A minority of new entrants work. The evergreen top is held by 2002–2020 titles with 1k–6.5k ratings.

### Trend
- I could not get Google Trends (the page needs an unsupported browser).
- Pinterest Fall 2026 report, via Daily Hive 2026-08-30, Canada-focused, VERIFIED:
  - "moon water rituals" searches +186%
  - "learn astrology" +733%
  - "tarot cards for beginners" +558%
  - "crystals and meanings" +606%
- Global Wellness Summit 2026 trends report mentions new-moon ceremonies as programming. This comes from a search snippet only; I did not read the report.
- Goodreads volume is steady: Moonology 3,494 ratings; Moon Spells 1,956; Lunar Living 1,633. Critical reviews keep arriving in 2024–2026.

**Verdict:** flat-to-rising. Interest is stable, with a fresh astrology/witchy-hobby uptick in 2026 (Pinterest). I could not verify a breakout for "moon rituals" specifically (ASSUMED stable).

## 3. Critical reviews (1–3★), all VERIFIED quotes

I collected 70+ 1–3★ reviews. Most are from Goodreads, which shows star ratings in the page HTML. Amazon.com critical-review pages require login. Amazon UK/AU product pages show mostly 5★ reviews but yielded a few critical ones. Full texts are in crit.txt.

### Selected texts (≥15)

**Moonology**
1. Goodreads 2★, Megan, 2017: "I felt like I was reading something written for someone in 8th grade… why the author insists on recommending the exact opposite of the energy that she just described. I.e.: Aries is impulsive… this is the time to… sit down and plan the next 12 months?"
2. Goodreads 2★, Leigh, 2017: "one long teaser ad for the author's blog and/or website."
3. Goodreads 1★, Felyn, 2019: "The concept of soul contracts is toxic, victim-blaming…" Also: "The Quarter Moons get a scant mention in an appendix."
4. Goodreads 2★, chaptersbydani, 2022: "numerous mentions of dieting, limiting food intake… This was a bit triggering… The author doesn't seem to have a solid understanding of what the astrological houses are."
5. Goodreads 1★, Moony, 2022: "Far too many repetitions… I found the tone to be condescending at times."
6. Goodreads 3★, Jina, 2024: "constantly referring you to their website (with some URLs that are wrong) to buy additional things."
7. Goodreads 1★, Sadie, 2018: "Written as if the reader is 14 years old."
8. Goodreads 2★, Heema Shirvaikar, 2019: "after a point it just got way too complex and technical for me to follow."

**Moon Spells (Ahlquist)**
9. Goodreads 1★, Ellery Fenn, 2020: "There is little to no information about the moon itself… It advises to smudge with white sage."
10. Goodreads 2★, Kelly Dienes, 2020: "they can often be fluffy bullshit… There are also chapters titled 'Just for Women' and 'Just for Men', and that sat completely wrong with me."
11. Goodreads 2★, WeeWaa13, 2019: "Bit too sexist, heteronormative, and even remotely transphobic for me."
12. Goodreads 3★, bresinabook, 2022: "The author states that this book is not Wiccan; it is."

**Moon Magic (Ahlquist)**
13. Goodreads 1★, Karen, 2021: "I didn't know much about the moon before reading this book. I still don't… recipes for 'Moon Magic Mint Mojito'."
14. Goodreads 2★, Plateresca, 2019: "Why does she treat her readers like imbeciles?"
15. Goodreads 2★, Isla, 2019: "There were a lot of inaccuracies. It felt like perhaps the author did some Pinterest searches."
16. Goodreads 2★, Cheyenne Wildt, 2025: "bizarrely judgemental statements that exuded the worst kind of boomer energy… mainly a hodgepodge of pop psychology…"
17. Goodreads 2★, Jess, 2026-03: "Out of the 256 pages, I'd say there's only 20 pages worth of good information."
18. Goodreads 3★, Christina Hannan, 2020: "it still gave advice for what would be the best time to get surgeries."
19. Amazon UK 2★, "Disappointing", 2019-05-03: "written for people who need 'the Northern hemisphere' explaining."

**Moon Magic (Aurora Kane)**
20. Goodreads 3★, Tedders, 2020: "when you say that Artemis' brother is Helios and than that Apollo is the Roman version of Helios… Holy fact check Batman."
21. Goodreads 1★, Salem, 2025: "the author had intended to quote Wikipedia… She misinterpreted this sentence."
22. Goodreads 3★, Heather, 2022: "one image was the wrong moon phase the book was discussing."
23. Goodreads 3★, Rhiley Jade, 2021: "weight loss spells can kiss my ass. Give me body positive spells instead."
24. Amazon AU 1★, "Internet Infomation in Print!", 2021: "Everything in this book is easily found on the Internet."
25. Amazon IN 3★, 2022: "if you're looking for advanced spells or rituals this book would disappoint you."

**Lunar Living (Gallagher)**
26. Goodreads 2★, Sophiebeth, 2025: "The main takeaway… could have easily been distilled into a single paragraph… repetitive and unnecessarily drawn out."
27. Goodreads 3★, Alicia, 2021: "there is no first hand experiences which makes me quite sceptical."
28. Goodreads 3★, Lieke Mulder, 2020: "written quite simplistically. Kinda like a magazine."
29. Goodreads 3★, Matthew Burton, 2025, a husband reading for his wife: "I can't say that I am a full believer yet."

**Living Lunarly**
30. Goodreads 3★, Kate Henderson, 2021: "felt a little formulaic and repetitive… The artwork is the main reason I enjoyed the book."

**Moon Apothecary**
31. Amazon UK 3★, 2026-07: "it is an American book. With American prices and measurements."

### Complaint clusters
Counts are rough tallies from crit.txt.

| Cluster | Evidence | Frequency |
|---|---|---|
| **Fluff / filler / off-topic** | recipes, pop psychology, "20 pages worth", "Lots of filler not even about the moon" | Very common (Ahlquist, Kane) |
| **Not about the moon itself** | "little to no information about the moon itself", "I still don't [know about the moon]" | Common |
| **Condescending or juvenile tone** | "8th grade", "14 years old", "imbeciles", "condescending" | Common, across both Moonology and Ahlquist |
| **Too basic / found free online** | "Internet information in print", "super basic" | Common |
| **Repetitive** | Moonology, Lunar Living, Living Lunarly, Moon Magic | Common |
| **Astrology / mythology errors** | sign "energy" mismatch, houses misunderstood, Helios/Apollo, wrong moon-phase image | Several |
| **Cultural appropriation** | white sage, smudging, medicine wheel | Very common in witchy readers |
| **Not inclusive** | "Just for Women / Just for Men", heteronormative, trans-exclusion, "female menstruation cycle" | Several |
| **Harmful health / diet content** | dieting during moon phases, weight-loss spells, surgery timing | Several. Directly relevant to the publisher's no-claims rule |
| **Upsell / website funnel** | Boland's site links, wrong URLs | Several |
| **Too complex** | natal chart and houses lose beginners | Several |
| **Too Wiccan / not Wiccan enough** | "states this book is not Wiccan; it is", circle-casting rigidity, "do I need to shower first" | Some |
| **Wants first-hand experience** | "no first hand experiences" | Some |
| **US-centric** | measurements and prices; Northern-hemisphere framing | Some |
| **AI** | No review in my sample says "AI" outright. The market-level study (78% likely AI in Witchcraft) is the signal | Market-level |

### Praise themes
Taken from 3★ positives and the 5★ titles seen on UK pages:
- beautiful objects / gift appeal
- a "reference I keep returning to"
- easy to dip in and out of, per moon
- lists of what to do each phase
- meditations
- a gentle, non-religious framing ("I appreciate this book not having any religious practice… tied to it")
- feeling calmer

Westwood's UK 5★ titles: "An Accessible and Empowering Lunar Guide"; "Made moon rituals make sense!"

## 4. Accuracy: what can be checked without a human expert

### Phase dates and times are fully checkable (VERIFIED)
- I fetched both tables: the USNO API (aa.usno.navy.mil/api/moon/phases/year?year=2027) and NASA GSFC's Six Millennium phase table (eclipse.gsfc.nasa.gov/phase/phases2001.html).
- For 2027 they agree on **all 49 phases, within 1 minute**.

2027 facts from those tables:
- **12 full moons and 13 new moons.** August has two new moons: Aug 2 and Aug 31.
- A "13 new moons" year is a legitimate structuring device for 2027. Note that it is not 13 full moons.
- Eclipses flagged in NASA's table:
  - Feb 6: annular solar
  - Feb 20: penumbral lunar
  - Aug 2: total solar
  - Aug 17: penumbral lunar

### Zodiac sign of each new and full moon is computable
- I computed the Sun's ecliptic longitude with the standard low-precision Meeus formula (about 0.01°). New moon is in the Sun's sign; full moon is in the opposite sign.
- Results are in signs2027.txt.
- Spot-check: Full Moon of 2027-04-20 at 22:27 UTC gives Scorpio 0.6°. **Astro-seek says "Scorpio 0°36'" and Cafe Astrology says Scorpio** (VERIFIED). The formula works.
- 2027 has **two Scorpio full moons** (Apr 20 at 0.6°, May 20 at 29.2°). Both sit near a cusp; that is exactly where careless books go wrong.

### Risk areas
1. **Time-zone date shifts.** 12 of 2027's 25 new and full moons fall within 5 hours of UTC midnight, so the calendar date differs between the US and Europe/Asia. Example: Full Moon 2027-02-20 23:23 UTC is Feb 21 in Central Europe.
   - The Catalina Sky Survey calendar lists the April full moon as "Wednesday, April 21st", while USNO and Griffith list Apr 20 (15:27 PDT).
   - Sources disagree by convention. The book must state its time zones, e.g. UTC plus ET/PT/UK tables.
2. **Cusp signs.** Apr 20 and May 20, 2027 full moons. Ingress times also need checking.
3. **Things that need a real ephemeris**, which none of the free tables give: void-of-course Moon, retrograde dates, moon sign by day, eclipse visibility paths, and houses. Avoid these, or cross-check two sites (astro-seek and Cafe Astrology agreed on the one I checked).
4. **Mythology and folklore errors**, such as the Helios/Apollo slip. Full-moon names (Wolf, Pink…) are Farmer's-Almanac/colonial-era folk names; avoid attributing them to specific Native nations without a source.
5. **Hemisphere.** Seasonal names and meanings flip for Australia/NZ. The UK review complained about US-centrism.
6. **Claims and ingestion (publisher rules):**
   - Moon water is often drunk; Pinterest says it is +186%. Teas, cocktails and "apothecary" recipes are everywhere in competitors. All must be excluded or made non-ingestible.
   - Competitor copy makes effect claims. Moonology's blurb says the moon cycles have "a huge effect on your health, your mood, your relationships". Astro-seek says "Surgical operations are strongly not recommended during the Full Moon!"
   - Diet and weight-loss timing drew complaints.
   - Hexes and spells for love or attraction aimed at a specific person are excluded.
7. **Cultural appropriation.** White sage and smudging. This is easy to avoid and reviewers reward avoiding it.

**Bottom line:** the factual layer (dates, times, signs, eclipses) is objectively checkable with two free public tables plus a 20-line script. The softer layer of correspondences and meanings is tradition by definition, so it can be framed as tradition rather than fact.

## 5. Gaps: where a warm, plain-spoken, gently humorous guide could win

These are inferences from the evidence above; audience-size claims are ASSUMED.

1. **Skeptics / "spiritual but not religious" / curious partners.**
   - Reviews ask for less magical promise: "I can't say that I am a full believer yet". A Polish 3★ objects that the book implies moon-living fixes everything. Another reviewer had to "skim the law of attraction".
   - No top title presents rituals honestly as reflection and tradition. That framing is also exactly what the publisher rules require.
   - Veylen's "Reflective Practices" (Aug 2026) tries it but has no traction (1.7M BSR, 0 ratings), so the positioning is unclaimed in practice.
2. **Grown-up tone.**
   - Readers in their 30s–60s complain about "8th grade" and "14-year-old" writing. Others complain about judgemental "boomer energy".
   - A warm, wry, adult voice with first-hand stories answers both. ("no first hand experiences which makes me quite sceptical")
   - Over-50 women and busy mothers specifically: there is no direct review evidence; the segment is ASSUMED.
3. **About the actual moon.**
   - Readers repeatedly want "information about said moon".
   - Short, accurate sky notes (why the moon is sometimes visible in daytime, what an eclipse is, why phase dates shift) cost little and differentiate the book.
4. **Annual 2027 edition, done right.**
   - Trade annuals sell (Llewellyn Moon Sign Book US 31k; Moonology Diary UK 4.5k). The indie annual entry is thin (2027 Witch's Moon Guide: 2 ratings, still page 1).
   - Possible structure: "13 new moons of 2027", a reflection prompt for each moon, and dates in UTC, ET, PT and UK time.
   - Repeatable yearly: 2028, 2029…
   - Downsides: a launch window that ideally opened in July 2026, so a 2027 edition is late but still sellable (ASSUMED), plus yearly rework.
5. **Inclusive, non-gendered, no appropriation, no diet talk.** This is a cheap differentiator that reviewers explicitly reward.
6. **No upsell.** The book stands alone, with no "see my website".

### Format notes
- Gift-style illustrated colour hardcovers (Kane, Living Lunarly, Apothecary) win on looks. A 20–30k-word text guide cannot compete there.
- Instead, compete as a 6x9 B&W paperback in the 130–180 pp band, like Westwood (245 pp), Veylen (162) and Brittany (135), at $11.99–14.99, with a simple journal-space section.
- A companion low-content journal is a plausible second SKU, given journals with 300+ and 1K+ monthly sales badges.

---

## Scores
| Criterion | Score | Basis |
|---|---|---|
| Demand | **7/10** | Evergreen leaders at BSR 10k–55k; annual titles at 31k US and 4.5k UK; journals with 300+ and 1K+ bought/month; Pinterest astrology/moon-water uptick. No total-result counts. |
| Competition (10 = easy) | **4/10** evergreen, **6/10** annual | Entrenched 2002–2020 classics with 1k–6.5k ratings; 78% likely-AI witchcraft shelf; most 2025–26 entrants above 100k BSR; indie annual entries thin. |
| Accuracy / claims risk (10 = low risk without expert) | **6/10** | Dates, times, signs and eclipses are checkable (USNO = NASA, 49/49). Risks: time-zone date shifts, cusp signs, ephemeris-only items, mythology, and the strong pull toward ingestion and health claims in the genre. |
| Fit for an emotional, human-voiced 20–30k-word book | **8/10** | Reader complaints are mostly about voice: condescension, fluff, no lived experience, over-promising. A warm, honest, skeptic-friendly voice is the clearest gap. Length fits the indie band. |

**Best angle:** "The Honest Moon 2027": a warm, plain-spoken moon year for the curious but unconvinced. It has one simple reflection ritual for each of 2027's 13 new moons and 12 full moons, and every date is checked against USNO and NASA in US and UK time. It makes no promises, has no potions and lets you keep your sense of humour. It is then repeatable yearly.

**Biggest risk:** exactness in an annual. 12 of 2027's 25 new and full moons fall within 5 hours of UTC midnight, and two full moons sit on Scorpio cusps, so a single-time-zone or copied table will be visibly "wrong" for part of the readership. The second risk is that a late (post-July) launch shortens the annual's selling window.

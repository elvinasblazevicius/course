## Niche selection: Elvin's standing rules (2026-10-15)

1. **AI-hunt immunity comes first.** Prefer books whose value is in structure or verifiable correctness:
   - puzzles generated and solved by code
   - engine-checked chess
   - computed drills
   - verbatim public-domain text
   - code-drawn art

   Prose-heavy niches where reviewers hunt AI are second choice: self-help, devotionals, witchcraft/moon, RSD, shadow work, exam prep.
2. **High content.** No blank journals or thin planners.
3. **No human editor or subject checker** at this stage. Avoid niches where one factual slip sinks the book: exam prep, technical licensing, repair manuals, Excel.
4. **Never size a book to the budget.** Size it to the idea and the reader. Still log real token costs per book.
5. **Check every candidate against kdp/CATALOGUE.md before researching it.**
6. **Pass bar:** 9 by default (8.5 was a one-off for the Oct 2026 search).

## Niche research method (what worked, 2026-10-15)

**Data access**
- **TinyFish Search and Fetch are free** (rate limits: 30 searches/min, 150 fetches/min). They read Amazon search and product pages, including BSR.
  - Retry 503s.
  - Product URLs: use /Title-Slug/dp/ASIN?th=1&psc=1.
  - Searches: use &rh=n%3A283155 when &i=stripbooks fails.
  - Never use TinyFish automation or browser sessions (paid).
- **Amazon review filter pages need a login.** Take critical reviews from Amazon UK/CA/AU product pages, Goodreads, Walmart and Reddit.
- **Apify's free tier caps out at about $5/month.** Product scrapes cost about $0.02 per item with full details.
- **The cloud container cannot reach Amazon, Bright Data, SerpApi or Keepa directly.** Use MCP connectors.

**Screening and gating**
- Screen 10–12 keywords per agent and the top 6 books each (TSV out).
- Then deep-dive the top 3 and run a 5-angle panel on the winner.
- **Before any panel, search for look-alike launches from the last 3 months.** Both Oct 2026 finalists died on this:
  - The cozy story word search had about 12 series already.
  - The "Read Hangul in 14 Days" hook already existed at #4.1M, alongside 6 day-count look-alikes.
- **A one-day BSR snapshot is weak evidence.** Note the launch date, and treat a newcomer's rank as possibly launch spike or ads.

## KDP facts verified Oct 2026

**Upload limits**
- New-title cap: **2 new titles per format per week** (since 21 Sep 2026).

**Kindle**
- Puzzle books and write-in workbooks are listed as unsuited for Kindle. **Publish print only.**

**Languages and binding**
- Languages not supported: Russian, Lithuanian, Korean. Publish as an English-language book with the script inside.
- Right-to-left paperback binding exists only for Hebrew, Yiddish and Japanese. Arabic is eBook-only.

**Print cost**
- Print cost for 8.5x11 (large trim): $1.00 + $0.017/page. 200 pp = $4.40.

**AI disclosure**
- Deterministic code output needs no AI disclosure.
- Text drafted with Claude must be disclosed as AI-generated even after heavy edits.

**Rights and trademarks**
- KJV is under Crown patent in the UK (Cambridge, commercial permission needed). Use the World English Bible "LORD" edition for worldwide sales.
- Stroke-order SVG sets (KanjiVG etc.) and NIKL/Wiktionary data are CC BY-SA. Use them to check only; draw your own diagrams.
- Trademarks to avoid in titles and keywords: Murdle, Murdoku, Clue/Cluedo, Hunt A Killer, Agatha Christie, Marple, Poirot, Murder She Wrote, Boss Babe, She Means Business, Proverbs 31 (series/titles), PICROSS, "Official"/DVSA, USMC.

## Lessons (Oct 2026 search)

- **About 230 niches were screened, and no idea passed a full panel.**
  - Code-verifiable formats have the best AI immunity, but they attract floods of look-alike indie titles.
  - The winner must have a visible hook nobody else uses.
- **Large print alone does not sell story-puzzle books.** All the winners were 6x9.
- **A newcomer with no platform in a branded niche needs a 90-day ad budget** of about $600–900. Plan for it, or pick a niche without an ad-backed leader.

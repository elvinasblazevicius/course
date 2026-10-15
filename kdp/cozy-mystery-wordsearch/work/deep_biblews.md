# Deep dive: Large-print Bible word search (plus Bible crosswords and hymn word searches)

Snapshot date: 2026-10-15. Amazon data comes from product pages fetched today with TinyFish fetch_content. A few rows come from W8.tsv, captured earlier today. BSRs move by the hour: the Cottage Door title read #2,709 in W8 and #4,603 a few hours later. Treat every BSR as a ±50% snapshot.

Tags used throughout:
- **[V]** I read it on a page today.
- **[V-also]** The rating count comes from an Amazon "Customers also bought" carousel, not from the title's own page.
- **[A]** My assumption or inference.
- **NA** The fetch was blocked or the field did not render.

Raw files:
- Search pages: `/tmp/claude-0/-home-user-course/5d910e26-d220-53df-b12b-0c4e5f61c868/scratchpad/wide2/bws/s1.json` to `s5.json`
- Product pages: `p1.json` to `p6.json` in the same folder
- Parser: `/tmp/claude-0/-home-user-course/5d910e26-d220-53df-b12b-0c4e5f61c868/scratchpad/wide2/bwsscripts/pp.py`
- Prototype generator: `/tmp/claude-0/-home-user-course/5d910e26-d220-53df-b12b-0c4e5f61c868/scratchpad/wide2/bwsscripts/ws_proto.py`

Search coverage:
- Amazon searches that rendered, all in Books (some with `rh=n:283155`): "bible word search large print" (W8), "christian word search", "bible crossword puzzles large print", "bible word search for kids", "hymns word search book", "bible word search large print verses for women", and a "Peace of Mind" brand search.
- **"large print bible word search for seniors" and "hymn word search" returned 503 on every try (7 attempts with different URL forms).** "hymns word search book" stands in for the hymn query. The seniors query is covered only indirectly, through the same titles showing up in the other searches and in also-bought carousels.

---

## 1. Market map

### 1a. Top titles across the six keyword families (ranked by BSR)

Columns: BSR (Books) · ratings · ★ · pub date · publisher · pages · price · puzzle count · translation · verse/passage per puzzle · font size · solutions.

| # | Title (ASIN) | BSR | Ratings | ★ | Date | Publisher | Pp | Price | Puzzles | Transl. | Verse per puzzle | Font | Solutions |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Brain Games Large Print Bible WS: The Words of Jesus (1645587754) | 975 [V] | 3,159 | 4.8 | 2021-11-15 | Publications International (PIL) | 192, spiral | $9.00 | 80+ | KJV (per a Walmart reviewer; not stated on the page) | Yes: passage on left page, grid on right | "Large print", size not stated. One reviewer says the print is **gray** | Answer key at back |
| 2 | 100 Days of Strength for Women: Bible WS Devotional (1424569788) | 1,507 (W8) | 674 | 4.9 | 2025-02-04 | BroadStreet | 224 | $9.74 | 100 | NA | Yes: devotion and Scripture with each puzzle | "Easy-to-read large print" | Answer pages |
| 3 | Large Print Bible WS Puzzle Book, Brain Busters (1646380223) | 4,603 [V] (2,709 in W8) | 1,787 | 4.8 | 2021-08-09 | Cottage Door / Parragon | 240, spiral | $7.99 | 200+ (16–20 words each) | None (themes only) | No: themed word lists | "Big print", not stated | Included |
| 4 | Words to Warm Your Heart: Bible WS Devotional (1424572215) | 4,673 [V] | 9 | 5.0 | **2026-08-04** | BroadStreet | 224, spiral | $9.74 | 100 | NA | Yes: devotion | Large print | Answer pages |
| 5 | Brain Games LP Bible WS: Psalms (164558500X) | 5,008 [V] | 1,765 [V-also] | 4.9 (W8) | 2021-02-01 | PIL | 192, spiral | $9.00 | 80+ | Not stated | Yes: prayers from Psalms | LP | Answer key |
| 6 | Bible WS Devotional: 100 Days of Worship from Psalms (1424568935) | 8,430 (W8) | 320 | 4.9 | 2024-07-16 | BroadStreet | 224, spiral | $8.75 | 100 | NA | Yes | LP | Answer pages |
| 7 | 100 Days of Hope for Your Soul (142456977X) | 9,648 [V] | 144 | 4.9 | 2025-02-04 | BroadStreet | 224, coil | $9.74 | 100 | NA | Yes | LP | Answer pages |
| 8 | Brain Games Bible WS (Large Print) (1450827152) | 10,394 [V] | 3,670 | 4.8 | 2011-10-21 | PIL | 192, spiral | $7.49 | 80+ | NA | Mixed ("variety of types") | LP | Answer key |
| 9 | Brain Games Bible WS: Wisdom of Proverbs LP (1639383581) | 10,885 [V] | ~662 [V-also] | NA | 2024-01-15 | PIL | 192, spiral | $9.00 | 84 | NA | **Yes: one Proverbs verse per puzzle, list drawn from it**, 2-page spread | LP | Answer key |
| 10 | 100 Meditations on the Words of Jesus (1424571596) | 11,223 [V] | ~77 [V-also] | NA | **2026-02-03** | BroadStreet | 224, spiral | $8.82 | 100 | NA | Yes | LP | Answer pages |
| 11 | Brain Games Bible WS: The Gospels LP (1639384936) | 13,897 [V] | 227 | 4.8 | 2024-01-29 | PIL | 192, spiral | $8.82 | 84 | **KJV (stated)** | Yes: clue words in UPPERCASE inside the passage on the left page | LP | Answer key |
| 12 | Brain Games Bible WS: Hymns LP (B0FT7GR95Y) | 16,184 [V] | 57 | 4.9 | **2026-01-29** | PIL | 192, spiral | $12.10 | 84 | n/a (hymns) | Yes: hymn lyrics on left, capitalized words in grid | "Sizable grids and enlarged text" | Answer key |
| 13 | Brain Games Large Print Bible Crosswords (1640308458) | 16,450 [V] | 1,484 | 4.5 | 2019-09-15 | PIL | 192, spiral | $7.78 | 80+ crosswords | NA | Clues carry Scripture references (Walmart reviewer) | LP | Answer key |
| 14 | Brain Games LP Bible WS: Women of the Bible (163938040X) | 16,860 [V] | 426 | 4.9 | 2022-04-01 | PIL | 160/192, spiral | $9.49 | 84 | NA | Yes: quotations | LP | Answer key |
| 15 | Inspirational Bible WS for Adults (B0DQM1MLLR) | 17,937 [V] | 271 | 4.8 | 2025-01-07 | TG Edition (**indie**) | 107, 8.5x11 | $13.99 | NA | NA | "Bible quotes on every page" | LP, size not stated | NA |

Next 15, including adjacent formats (crosswords, hymns, kids):

| Title (ASIN) | BSR | Ratings/★ | Date | Publisher | Notes [V] |
|---|---|---|---|---|---|
| Daily Moments with God: Devotional Crossword (B0F6WFPPX8) | 15,058 | 46 / 4.8 | 2025-09-30 | DaySpring | 36 devotions, each with a crossword whose clues match that day's Scripture; spiral, $11.18 |
| Martin Littlewolf, Bible WS Large Print (B0CX1X2XNH) | 25,545 | 311 / 4.9 | 2024-03-01 | Indie | 84 puzzles, "2000 unrepeated words", **16pt**, each puzzle based on a verse, 6x9, $5.99 |
| Hymns for the Soul WS Book 1 (1959021109) | 29,475 | NA (comparison table shows 4.8/113, unverified) | 2023-10-14 | Dallum (Erin Jamie), 7-book series | 21 hymns with complete lyrics, 8.5x11, "even the solutions are large print" |
| Littlewolf, Bible WS: Christian Hymns (B0DRJX7VTR) | 29,671 | 319 / 4.8 | 2024-12-24 | Indie | Hymn word search plus hymnist bios, 108pp, $5.99 |
| Brain Games Bible WS: Old Testament LP (1639388583) | 30,587 | 40 / 4.8 | **2025-08-15** | PIL | 84 puzzles, mix of word-list and verse-capitals formats |
| Brain Games Bible Crosswords: Prayers, Parables & Prophets (163938491X) | 34,004 (W8) | 206 / **3.9** | 2024-03-23 | PIL | Lowest-rated PIL title. Reviewers: "not Bible enough" (see §3) |
| Jumbo Bible WS (B0F6BFG3HK) | 40,062 | 186 / 4.8 | **2025-08-19** | Zeitgeist (PRH imprint) | "Extra-large font", 192pp, $9.99, puzzles paired with Scripture references |
| Brain Games Kids Bible WS 5–10 (1645589331) | 48,841 | 76 / 4.9 | 2022-03-01 | PIL | 70+ puzzles, $11.89 |
| Amelia Rowan, Bible Crossword Puzzles LP (B0H35SYMP2) | 51,019 | 59 / 4.8 | **2026-05-25** | Indie | 100 crosswords in Bible order, devotion every 5th page, 226pp, $13.57, separate color edition |
| Brain Games Bible WS: Favorite Verses LP (1639382038) | 56,962 | 252 / 4.8 | 2022-09-15 | PIL | 70 puzzles, **KJV**, mix of list and verse-capitals |
| Levina Lanza, Bible Crossword Puzzles for Adults (1918139008) | 66,998 | 57 / **4.0** | **2025-07-27** | Indie | 100 crosswords, $9.99 |
| Brain Games LP Bible WS: Wisdom Books (B0FT7GYFZ5) | 73,021 | 28 / 4.8 | **2025-11-29** | PIL | 84 puzzles, Job through Song of Solomon |
| LightMind Press, Ultimate Bible WS (B0FCD6CVP7) | 74,991 | 76 / 4.8 | **2025-06-02** | Indie | 139pp, $12.49 |
| Paige Tate, Bible WS for Adults (LP) (1958803324) | 107,348 | 65 / 4.7 | 2023-12-05 | Paige Tate & Co | 100 puzzles, 6x9, "layflat design", $6.94 |
| Peace of Mind Bible WS: Words of Jesus (1680995715) | 160,734 | 1,571 [V-also] | 2020-02-18 | Good Books (Skyhorse) | 150 puzzles, 216pp, 8.5x11, $8.91. 10+ titles in the series. A sibling title quotes **NIV** wording (Isa 9:2 "The people walking in darkness…") |

Other datapoints [V]:
- Matthew Mark, Bible WS LP 200+ (B0D93DY6B3): BSR 244,646, 40 ratings / 4.8, 2024-07, 263pp, $19.99, 8.5x11, one puzzle per page with verses. Also an 11+ title themed series, e.g. "Verses on Heaven" (B0C6BSSC41): BSR 153,055, 62 / 4.7.
- Hymns of Glorious Praise WS (1947676385): Puzzle Favorites, 2021. BSR 553,365 with 586 / 4.9, so it is old and decayed.
- GreeneMint Jumbo 40-pt (B0HFYMHPR1): 2026-08, BSR 245,467, 40 puzzles.
- Grace Whitfield 3-in-1 KJV, **18pt** (B0FJ5HNS65): 2025-07, BSR 201,613, 33 / 4.9.
- HAP Book, Bible Crosswords KJV with chapter-and-verse in clues (B0H9SW7XGJ): 2026-07-21, BSR 148,236, no ratings yet. It already does the "fill-in-the-verse" crossword angle: about 2,000 cited clues, 8 chapters in Bible order.
- Kids: Paige Tate Kids (1958803332, blocked) and Carson Cardamone (B0FDKT1GHQ, sponsored, blocked).

Patterns:
1. **PIL is the category's backbone.** "Part of: Brain Games – Bible (25 books)". It sells spiral-bound books at $7.49–$12.10, uses a two-page spread (passage left, grid right), uses KJV where stated, and puts answers at the back.
2. **BroadStreet** has a 224-page spiral devotional line in which every new title debuts high. Words to Warm Your Heart: #4,673 with 9 ratings, two months after release.
3. **Good Books' Peace of Mind** and the Matthew Mark / Puzzle Favorites / Dallum indie series are the long tail.
4. Spiral or lay-flat binding is close to universal at the top. **KDP cannot print spiral** [A: KDP offers paperback and hardcover only], so an indie paperback starts at a structural disadvantage on the attribute buyers praise most.

---

## 2. How newcomers fare (2025–26 releases)

| Title | Pub | BSR today | Ratings | Indie? |
|---|---|---|---|---|
| 100 Days of Strength for Women | 2025-02 | 1,507 (W8) | 674 / 4.9 | No (BroadStreet) |
| Words to Warm Your Heart | 2026-08 | 4,673 | 9 / 5.0 | No (BroadStreet) |
| 100 Days of Hope for Your Soul | 2025-02 | 9,648 | 144 / 4.9 | No |
| 100 Meditations on the Words of Jesus | 2026-02 | 11,223 | ~77 | No |
| Daily Moments with God (crossword) | 2025-09 | 15,058 | 46 / 4.8 | No (DaySpring) |
| Brain Games Hymns | 2026-01 | 16,184 | 57 / 4.9 | No (PIL) |
| **Inspirational Bible WS (TG Edition)** | 2025-01 | **17,937** | **271 / 4.8** | **Yes** |
| Brain Games Old Testament | 2025-08 | 30,587 | 40 / 4.8 | No |
| Jumbo Bible WS (Zeitgeist) | 2025-08 | 40,062 | 186 / 4.8 | Trad (PRH imprint) |
| **Amelia Rowan Bible Crosswords** | 2026-05 | **51,019** | **59 / 4.8** | **Yes** |
| Levina Lanza Bible Crosswords | 2025-07 | 66,998 | 57 / 4.0 | Yes |
| Brain Games Wisdom Books | 2025-11 | 73,021 | 28 / 4.8 | No |
| LightMind Ultimate Bible WS | 2025-06 | 74,991 | 76 / 4.8 | Yes |
| Scripture WS for Women (Memories On Pics) | 2026-05 | 113,204 | 8 / 4.0 | Yes |
| HAP Book KJV Crosswords | 2026-07 | 148,236 | 0 | Yes |
| 77 Bible Word Searches for Kids | 2025-01 | 158,663 | 27 / 4.8 | No (Christian Art) |
| Peace of Mind: Joy in Jesus | 2025-09 | 185,043 | 4 / 5.0 | No (Good Books) |
| Inspirational Hymns LP WS for Seniors (Annie Fields) | 2026-03 | 186,140 | 4 / 4.7 | Yes |
| Grace Whitfield 3-in-1 KJV | 2025-07 | 201,613 | 33 / 4.9 | Yes |
| Ultimate Bible WS: 70+ Every Book | 2025-05 | 229,286 | NA | Yes |
| GreeneMint God's Promises Jumbo 40pt | 2026-08 | 245,467 | NA | Yes |
| The Savior Is Risen (Dallum) | 2026-02 | 1,175,737 | 6 / 5.0 | Indie series |
| KJV OT Crossword & Scramble (Words by Wagz) | 2025-09 | 943,454 | 6 / 4.8 | Yes |

**Is there room below PIL and BroadStreet? Yes, but only in the #15k–#75k band, and only for books with a clear hook.** [V for the ranks; A for the inference]
- Three indies sit at #18k–#30k: TG Edition (2025) at about #18k with 271 ratings, and Littlewolf's two books (2024) at about #25–30k with 300+ ratings each, priced at $5.99.
- One 2026 indie crossword (Rowan) reached #51k with 59 ratings in under five months.
- Most generic 2025–26 indie titles sit at #100k–#1.2M. Examples: "Scripture WS for Women", "God's Promises Jumbo", "Savior Is Risen", "Ultimate 70+".
- Nobody below the publishers' level has broken into the top 10k [V].
- Even PIL's new titles land at #16k–#73k. Only BroadStreet's devotional format debuts in the top 5k, which suggests the devotion-plus-puzzle format is what currently pulls demand [A].
- Rule-of-thumb sales (unverified, [A]): #20k is roughly 5–10 paperbacks a day; #50k roughly 2–4; #150k roughly 1 or fewer.

---

## 3. What readers complain about and praise (Amazon review pages need a login; sources below)

All quotes are verbatim, including the reviewers' own typos. Walmart lists PIL, BroadStreet and the indie titles, and its review pages loaded through business.walmart.com.

**Critical reviews (1–3★), 22 items:**
1. **"Too simple! These word search puzzles need difficulty level provided!"** 2★, Joey. Brain Games LP Bible WS: Words of Jesus (Walmart).
2. **"The scripture passages were in King James version. I'd prefer the NIV. Also the words were very easy to find."** 3★, Dale. Same book.
3. "Not worth the money." 1★, Ammie. Same book.
4. **"In the first 18 word searches I have done, I was unable to finish 3 of them… Puzzle 11 is missing bottom two rows, puzzl2 12 is missing last 7 rows of letters, and puzzle 18 is missing the last8 lines"** 1★, Debra. Seekers of the Word: Women of the Bible LP WS (Walmart). The grid was truncated in print and words are not findable.
5. **"advertised as large print, but the text is standard size and not readable for someone who needs larger type."** 1★, Brooke. KAPPA Large Print Bible Word Finds (Walmart).
6. "Some of the searches had sentences, like a story, and the words you are searching for are within that story... a little distracting." 3★, Erin. KAPPA.
7. "Hardly any of the words have anything to do with the Bible" 1★, debby. PIL Bible Crosswords: Prayers, Parables & Prophets (Walmart).
8. **"Too hard. You have to be a scholar in religion"** 1★, Andrea. Same book.
9. **"just common crossword puzzles with the occasional Bible related questions/answers thrown in."** 2★, Lynne. Same book.
10. "Misleading. Only 3-4 Bible references per puzzle." 2★, Petroula. Same book.
11. "This book has very little biblical clues. And the rest of the clues are difficult." 2★, Teresa. Same book.
12. "It has a little Bible mixed in with a lot of other questions that come with any other crossword book that you can get at the dollar store." 2★, Terry. Same book. Terry adds that the spiral binding is well made.
13. "It may be too advanced for me. Never heard of most of the words." 3★, JOYCE. Same book.
14. "It is enjoyable but extremely hard. I had to look up almost every clue to get an answer." 3★, Lynarnie. Brain Games Large Print Bible Crosswords (Walmart).
15. "Majority of puzzles have nothing to do with the Bible." 3★, Morima. Same book.
16. **"It only has 1-5 hymns to find per puzzle and the hymn names are so long they can only be found diagonal… After you do one puzzle you know all the others will be exactly the same… I thought the puzzles would be words from the hymn."** 2★, Drew. Word Search Puzzles Favorite Hymns of the Church (Walmart).
17. **"The large print in this puzzle is so close together, making it much harder for my eyes to find a word… It would be nice if the puzzle was in a similar sized font."** 3★, Christina. The Everything Large-Print Bible WS Book Vol. 4 (Walmart).
18. "Not enough words to search for on each puzzle." 3★, KPGrandma. Bible WS Puzzles for Adults LP: 101 Bible Verse WS (Walmart).
19. "The print is too small to read." 1★, bjmc. Women's Inspirational Word Search (Walmart, adjacent Christian title).
20. "Item was not included in the order…" 1★, Debbi. BroadStreet Psalms Devotional (Walmart). A fulfilment problem, not the book.
21. "Only received one of the two" 1★, Melissa. KAPPA 2-pack. Also fulfilment.
22. "Like the books alot" 1★, Elllie. KAPPA. The star rating contradicts the text; it shows how noisy low-star counts are.

**Critical remarks inside 4★ reviews or reviews with no star:**
- **"had some difficulty reading as print is GRAY?… you may need more light"** 4★, Virginia. Words of Jesus (Walmart).
- **"So many of the same words. Sometimes there are two of the same words on one page."** 4★, Mary. KAPPA. Repeated words.
- "If a buyer is expecting actual Bible knowledge, she will be disappointed." 4★, Debra. KAPPA.
- "I'm really old so I need X-Large print… next time I'll see if they have X-Large" 4★, Janice. KAPPA.
- **"The words, however, were too close together and not enough spacing… There were also a few errors and I would have liked the bible verses in order from Genesis to Revelation"** Wildflower7 on Goodreads. Large Print Bible WS: 101 Relaxing Bible Verse Wordfind Puzzles (Darling Irene, 2024).
- "It's strange that the book says they use the King James translation of the Bible, but they include puzzles for… Tobit, Judith, Maccabees, Sirach, and Baruch." Luminous Libro blog, 4/5. Cristina Smith, Large Print Bible WS Book. A translation and canon mismatch.
- "a little too dificult for my 10 yeat old he got discouraged." 4★, Katrina. PIL LP Bible WS Blue (Walmart).

**Praise:**
- Spiral binding: "Made with spiral bounds so they lay flat, which makes it easier to circle the words" (JoJo); "The spiral rings makes the difference" (Ruthie); "Love the spiral bound book" (Renee).
- Scripture references: "All clues have the scripture references so you can look them up if you don't know the answer" (Dot1, PIL crosswords).
- Hymn lyrics beside the grid: "a hymns lyrics on the left side and a corresponding word search on the right… loves the old gospel hymns of the 19th & 20th century" (Vanessa, PIL Hymns, buying for a 90-year-old).
- Devotion paired with each puzzle: "One page is the devotional and scripture references, while the opposite page is a word search using ideas and concepts from the day's devotional" (Vanessa, BroadStreet Psalms).
- Gift buying dominates: "brought them for christmas gifts for four elderly woman" (BroadStreet Psalms); "ordering three more for Christmas gifts" (Ramon).
- Speed of consumption: "I… limit myself to 4 per night, otherwise, I complete the whole book in a few days" (Nitzy, BroadStreet Psalms). Buyers burn through books, which favours series and repeat purchase.
- Big letters: "big letters easy on my old eyes" (Duane, PIL crosswords).

**What the reviews add up to:**
- Crosswords get the most complaints. Buyers want 100% Bible clues at an easy-to-medium level. PIL's crosswords mix in generic clues and run hard, which has pulled one title to 3.9★.
- Word search complaints:
  - too easy, with no difficulty labels;
  - print too small, gray, or cramped (letter spacing);
  - repeated words;
  - truncated or defective grids;
  - "not really Bible";
  - translation preference (some want NIV);
  - hymn puzzles that use only titles instead of lyric words.
- Binding complaints are about missing spiral, not flimsiness. I found no direct "flimsy binding" quote in what loaded. [V: absence within the sample only]

---

## 4. Copyright and translations

**Public domain in the US [V]:**
- **KJV (1611/1769).** Public domain in the US. ebible.org: "You may copy the King James Version of the Holy Bible freely."
- **WEB.** worldenglish.bible: "The World English Bible (WEB) is a Public Domain (no copyright) Modern English translation… you may freely copy it in any form, including electronic and print formats."
  - **Editions matter.** WEB Classic uses "Yahweh" (ebible's Psalm 23: "Yahweh is my shepherd"). WEBU (US) and WEBBE (British) use "LORD". Use WEBU or WEBBE for a mainstream evangelical or senior audience [A].
- **ASV (1901).** Public domain in the US [A, well established; the WEB is based on it per worldenglish.bible].

**UK and KJV [V, via publishing.co.uk, reviewed 2026-10-12, quoting Cambridge University Press]:**
- "Rights in The Authorized Version of the Bible (King James Bible) in the United Kingdom are vested in the Crown and administered by the Crown's patentee, Cambridge University Press."
- CUP's free allowance is up to 500 verses "for liturgical and non-commercial educational use", provided the verses are not a complete book of the Bible and are under 25% of the work. Commercial publications need written approval from permissions@cambridge.org.
- Required credit: "Scripture quotations from The Authorized (King James) Version. Rights in the Authorized Version in the United Kingdom are vested in the Crown. Reproduced by permission of the Crown's patentee, Cambridge University Press".
- I could not open CUP's own page (bot-blocked). These quotes come through the UK guide.
- **Implication:** a KJV puzzle book sold and printed on Amazon.co.uk is technically a commercial UK publication that needs CUP permission [A: KDP prints UK orders in the UK]. Options:
  - (a) request CUP permission and print the credit line;
  - (b) quote WEBBE/WEBU, which is public domain everywhere and carries no Crown right;
  - (c) exclude the UK marketplace for the KJV edition.

  **Recommendation:** use WEB (LORD edition) as the base text, or KJV with the CUP request filed before launch. Hundreds of KDP KJV books ignore this; the enforcement risk is low, but it is not zero [A].

**NIV and ESV verse text [V]:**
- **NIV (Biblica).** Up to 500 verses without written permission if they are not a complete book, are under 25% of the work, and carry the copyright notice. Commercial print permission in the US/Canada goes to HarperCollins Christian; in the UK, EU and EFTA to Hodder & Stoughton. Hodder allows the same 500 verses "for commercial or non-commercial use" with its notice.
  - **New in Biblica's policy:** "Any use of Biblica content in connection with artificial intelligence, machine learning, large language models… requires a valid license." If an AI pipeline touches NIV text, even just to select verses, this is a real compliance question. Avoid NIV in an AI-assisted pipeline [A, on how the clause applies].
- **ESV (Crossway).** Up to 500 verses without permission, under half of any one book, under 25% of the work, with the full notice. "ESV Text Edition: 2025."
  - A 100-puzzle book with 1–3 verses per puzzle fits under 500 verses. A **devotional plus multi-verse passages** format (PIL-style 6–10 verse passages × 84) can exceed 500 verses, and puzzle text may approach the 25% threshold [A]. Count verses with a script.

**Single words in word lists [V for the rule; A for how it applies]:**
- 37 CFR §202.1(a): "Words and short phrases such as names, titles, and slogans" are not subject to copyright. A word list such as SHEPHERD, PASTURES or STILL is not protected, even if the words were picked by reading the NIV.
- **But:** printing the verse that the list comes from is quotation and falls under the limits above. Distinctive translation phrasings could also be argued as expression if many are strung together [A]. Safe pattern: show public-domain verse text, and only reference NIV or ESV, never quote them.

**Hymns [V, UMC 2026-01-08]:**
- "As of Jan. 1, 2026, all songs published in 1930 and before (not later arrangements) are public domain. On January 1, 2027, all songs published in 1931 will enter the public domain."
- Text, tune and arrangement each have their own copyright. The puzzle needs **text only**.
- Copyrighted examples: "He Lives" (1933), "Precious Lord" (1932), "Morning Has Broken" (words 1931). "How Great Thou Art" (English text 1949) and "Great Is Thy Faithfulness" (1923, words public domain in the US, but the author died in 1960) need care [A].
- **UK caveat:** the UK term is the author's life + 70 years, so authors who died in 1955 or earlier are out of copyright in 2026 [V, publishing.co.uk]. Section 12(6) comparison-of-terms can shorten the term for non-UK works first published abroad [V, publishing.co.uk]. That may free some US hymns in the UK, but it is a legal judgment. Safest filter: **published ≤1930 AND author died ≤1955 AND modern edits stripped**.
  - Example: The Old Rugged Cross (1913, public domain in the US per UMC). The author died in 1958 [A], so it is not automatically public domain in the UK. Run a per-hymn date check from hymnary.org.

---

## 5. Production feasibility with code

**Prototype built and run.** `/tmp/claude-0/-home-user-course/5d910e26-d220-53df-b12b-0c4e5f61c868/scratchpad/wide2/bwsscripts/ws_proto.py` runs in 0.19 s:
- Takes KJV Psalm 23:1–4 as fetched from ebible.org.
- Strips ebible's footnote markers by script.
- Asserts every list word occurs verbatim in the verse.
- Renders the verse with list words capitalized (PIL format) and asserts the text round-trips unchanged.
- Places 18 words in a 15×15 grid with no up-left or up-right diagonals (gentler for seniors).
- Runs an **independent verifier**:
  - every word is found exactly once (palindromes handled);
  - no list word sits inside another list word;
  - none of the listed bad words appears by accident in the filler.
- Includes a tamper test, where the verifier caught a corrupted cell.
- The output passed: `VERIFY: OK`, and the tamper test reported `SOUL: found 0x`.

**Full pipeline [A, standard work]:**
1. **Text source.** Pull WEBU/WEBBE or KJV from a single public-domain download (ebible.org VPL or USFM). Hash the file, then select verse ranges by reference. Store `ref → exact text` and never retype or paraphrase.
   - At build time, re-extract every printed verse from the master file and diff it.
   - Normalise only quotes and dashes, by explicit rule.
   - Strip footnotes, Strong's numbers and paragraph marks.
   - Caught in this run: ebible's HTML appends footnotes such as "Heb. pastures of tender grass" directly to the verse text.
   - Note: curl to ebible.org is blocked by this sandbox's proxy, but TinyFish fetch works.
2. **Word lists.** Automatic: take content words from the verse, then apply a stop-list, a minimum length of 4, a maximum length that fits the grid, and dedupe across the book.
   - The book-level dedupe answers the "same words twice" complaint.
   - Never have a list word that is a substring of another.
   - Puzzle-level duplicate check.
3. **Grid.** 13×13 to 15×15 for seniors. Direction profile by level: Easy is across and down only; Medium adds down-diagonals; Hard adds reverse.
   - Filler letters drawn from the puzzle's own letter frequency, so the grid does not read as random.
   - Check for accidental profanity in all 8 directions.
   - Print a difficulty label on each page, which answers the "need difficulty level provided" complaint.
4. **Verification.**
   - Brute-force scan of all 8 directions, count = 1.
   - Render the PDF, then extract grid text back out with pdfplumber and re-verify. This catches the truncated-row defect from review 4.
   - Confirm every grid's bounding box sits inside the trim and safe zone.
   - Solutions page generated from the same coordinates. Show shaded or outlined capsules, not thin lines, so solutions stay readable in large print.
5. **Large-print layout.**
   - Grid letters **22–28pt bold sans** (Atkinson Hyperlegible or APHont-style) on 8.5×11. Verse and word list at 16–18pt. Solutions at 14pt or more.
   - Pure black (#000) text, never gray. This answers Virginia's complaint, and KDP's B&W interior prints gray tints lighter [A].
   - Letter spacing of at least 1.6× the cap height, which answers the "too close together" complaints.
   - Benchmarks [V]: the Library of Congress NLS says large print is "most commonly available in 16- to 18-point type". ACB recommends Arial 18pt. UKAAF puts the large-print minimum at 16pt, ideally 18. NFB gives a 14pt minimum. Competitors state 16pt (Littlewolf), 18pt (Whitfield), 30pt and 40pt (jumbo titles).
   - So a **24pt grid** sits clearly above the mainstream books and below the low-content jumbo tier.
   - Generous inside margin (0.875" or more) because the book will not be spiral. One puzzle per page, or a two-page spread (verse left, grid right), so nothing falls into the gutter.
6. **QA gates without a human.**
   - Verse diff = 0. Word placement = 1 each. No substring words. No accidental bad words.
   - Page count and verse count under the licence limits.
   - PDF re-extraction matches.
   - Every reference resolves to a real book, chapter and verse; the canon list fixes the Apocrypha mismatch from the Luminous Libro review.
   - Any devotional or reflection text is the remaining unverifiable piece: tone and theology.

**What would make it 4.5★ and distinctive (ranked) [A, drawn from the complaint and praise patterns above]:**
1. **True 24pt bold grid with pure-black print and wide spacing.** State the point size on the cover. Most competitors do not.
2. **Verse beside every puzzle, verbatim, with reference, list words capitalised in the verse.** Proven by the PIL format. Add **one "fill in the missing word" line per page** as a light memory exercise.
3. **Book-of-the-Bible arc**, e.g. "Psalms: 150 Puzzles, One for Each Psalm" or "Walk Through the Gospels in 90 Days". Include a reading-plan checkbox on each page and a progress tracker. This answers Wildflower7's wish for Genesis-to-Revelation order and gives a reason to buy the next volume.
4. **Difficulty labelled on every page**, Easy and Medium only, no backward diagonals in Easy.
5. **Hymn edition built from lyric words, not titles.** Full public-domain lyrics on the left (1930 or earlier, author died 1955 or earlier), lyric words in the grid. Add a two-line hymn story. This answers Drew's complaint and matches what PIL Hymns readers praise.
6. **Crossword edition where every clue is a KJV/WEB fill-in-the-verse with reference, at easy level.** This answers seven or more PIL crossword complaints. Note that HAP Book has already launched exactly this (July 2026, BSR #148k, no ratings), so the space is no longer empty. Crossword fill generation is harder than word search: it needs a constrained dictionary from Bible vocabulary.
7. Answer key with large, shaded capsules. A translation statement on the back cover ("WEB (LORD edition), public domain" or "KJV"). No AI-written devotions unless a human edits them.

---

## 6. Gaps, angles and series potential

**Gaps (inference from the map) [A]:**
- **Extra-large print with verses.** The mainstream books are about 16–18pt or unstated. The jumbo 30–40pt books (GreeneMint, the "30 pt Font" titles) are thin, 40-puzzle, low-effort products. A 24pt, verse-rich, 100-puzzle book sits between the two.
- **Bible-only easy crosswords.** The clearest complaint cluster. HAP Book is now in it, but nobody has ratings yet.
- **Single-book deep dives.** PIL covers Psalms, Proverbs, Gospels, Women and Wisdom Books. Untouched or thin: **Genesis** (one Littlewolf title, 17 ratings), **Acts**, **Paul's letters** (Our Daily Bread "Search the Scriptures" has a Galatians–Colossians word find with 40 ratings [V-also]), **Isaiah/Advent prophecies**, **Names of God**, **Promises of God**, **Parables**, **Prayers of the Bible**.
- **Christmas and Easter.** Dallum's "Savior Is Risen" (Easter, 2026) sits at #1.18M, so Easter is not proven. PIL has a "Bible Word Search: Christmas Puzzles – Large Print" (seen as a pre-owned Walmart listing [V]).
  - Christmas carols are all old and public domain on both sides of the Atlantic: "Joy to the World", "Silent Night" in the 1859 English text, "O Holy Night" in the 1855 English text [A on the dates]. Pair them with Luke 2 / Matthew 1–2 / Isaiah 9 verses.
- **Gift-buyer copy.** Reviews show daughters and granddaughters buying for mothers and grandmothers, for nursing homes, chemo, and post-surgery. The listing should say "for Mom/Grandma, nursing-home friendly, large print, no glasses" [V for the behaviour; A for the copy].

**Series potential: high.** Readers finish books "in a few days". PIL runs 25 Bible titles, Peace of Mind 10+, Dallum 7+4, Matthew Mark 11+.

A possible line:
1. *Psalms (WEB/KJV), 24pt*
2. *The Gospels in 90 Days*
3. *Hymns We Grew Up Singing* (lyrics, pre-1931)
4. *Christmas: Carols & the Nativity*
5. *Women of the Bible*
6. *Promises of God*
7. *Bible Fill-in-the-Verse Crosswords, Easy*

Each title is the same codebase with a new verse manifest.

**Spiral-friendly:** KDP cannot do spiral. Mitigate with:
- a wide gutter;
- a single-page puzzle layout or a verse-left/grid-right spread;
- 60# white paper [A: a KDP option];
- a line on the listing such as "opens flat with a gentle press" only if true.

Alternatively, place a spiral edition through IngramSpark or another printer later [A: not checked].

---

## Scoring inputs (for the summary)

- **Demand:** strong and gift-driven. A #975 leader and five titles under #10k [V].
- **Competition:** PIL and BroadStreet own the top with spiral, $9, trade distribution. Indies do reach #18k–#30k [V].
- **AI-hunt immunity:** low-to-mid. The category is already full of code-generated grids, and Biblica's AI clause adds friction [V]. Verbatim public-domain Scripture plus verified grids is defensible content, not "AI-generated text", if no AI-written prose is included [A].
- **Accuracy risk:** grids and verse text are fully machine-verifiable (prototype [V]). Remaining risks: devotional prose, hymn copyright dates, the UK KJV permission.
- **Christmas window:** today is Oct 15. Code plus cover takes about 3–5 days and KDP review up to about 72h [A], so a book could be live around Oct 25–Nov 1. That is in time for gift buying late Nov to mid Dec [A], but with no reviews, so it depends on ads.

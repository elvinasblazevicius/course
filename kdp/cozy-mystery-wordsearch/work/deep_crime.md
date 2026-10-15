# Deep dive: crime / murder-mystery puzzle books (KDP)

Data date: 2026-10-15. Sources: Amazon product pages and Amazon Best Sellers / Hot New Releases pages fetched today via TinyFish fetch_content; earlier same-day Amazon search data in `wide2/W11.tsv`; Goodreads book pages (review cards with star ratings parsed from HTML); USPTO mirror sites (uspto.report, trademarksoncall.com, trademarks.justia.com); Euronews; Reddit r/murdoku.
Raw working files: `wide2/crime/` (notes.tsv, zg_snapshot.txt, critical_reviews.txt, search JSONs).

Labels: **[V]** = verified from a page fetched today. **[P]** = taken from the earlier same-day pull (W11.tsv). **[A]** = assumption or my own judgement, not verified. **[C]** = a marketing claim by the publisher or retailer.

Limits: Amazon *search* pages returned 503 most of the time today. I got one full search ("murder mystery word search"), one for "cozy mystery puzzle book" and one for "detective puzzle book". The "murder mystery logic puzzles" search and the "last 30 days" new-release filters never loaded, so **I have no full count of new releases per month**. As a substitute I used the Best Sellers and Hot New Releases category lists, which did load. Search-interest data (Google Trends) was not obtained.

---

## 1. Market map

### 1a. Top 15 distinct titles (by BSR, across the requested keywords)

| # | Title (ASIN) | Publisher (type) | Pub date | Pages | Price (pbk) | Rating / #ratings | BSR (Books) | Puzzle type | Story depth | Colour | Large print |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Murdoku: 80 Murder Mystery Logic Puzzles (1454961791) | Puzzlewright Press (trad, Union Square/B&N) | 2025-10-28 | 208 | 10.39–11.54 | 4.7 / 1,138 | **#1** (also #1 Puzzles, #1 Sudoku, #1 Logic) [V] | Sudoku-style hybrid (place suspects in rows/columns on a room map) | Low: standalone scenes, "no connecting storyline" (GR review) | **Full colour** [V, description] | No [A] |
| 2 | The Killer Isn't Alice (Little, Brown ed., 0316616184) | Little, Brown (trad) | 2026-09-01 | 224 | 13.19 | 4.5 / 2,082 | 26 [P]; #1 Hot New Releases, #2 Best Sellers in Puzzles & Games [V] | Giant suspect-list elimination (46,600 names, 18 clues), answer submitted online | Very low ("absolutely no back story", GR) | B&W [A] | No |
| 2b | Same title, original indie edition (B0GQ2VXKY7) | Independently published (Iris Starling) | **2026-02-22** | 211 | 13.95 | 4.5 / 2,073 | 1,665 [V] | same | same | B&W [A] | No |
| 3 | Murdle: Volume 1 (1250892317) | St. Martin's Griffin (trad) | 2023-06-13 | 384 | 12.48–18.99 | 4.5 / 7,786 | 28 [P]; #3 Puzzles & Games [V] | Logic grid (suspect/weapon/location/motive) plus ciphers | Medium: running story with a payoff at the end | Illustrated; colour not checked [A] | No |
| 4 | Murder Among the Stacks (150722527X) | Adams Media (trad, S&S) | 2025-11-25 | 128 | from 2.99 used; ~11.98 new | 4.6 / 296 | **672** (#1 Word Games, #1 Word Search) [V] | Cozy novella in one-page chapters, each followed by a themed word search | Medium-low ("chapters too short", GR) | Illustrated [GR review] | No; 6x9 |
| 5 | Kill Grid Volume 1 (B0H7S181HY) | Indie (Hazel Woods brand) | 2026-07-06 | 137 | 9.99 (hc 24.99, spiral 29.99) | 4.8 / 66 | **700** (#1 Word Search Games) [V] | Word search, then a missing word, then leftover letters naming killer and victim, then a book-wide meta confession | Low-medium (120 connected cases) | B&W [A] | "Easy-on-the-eyes", not LP |
| 6 | The Killer Never Checked In (B0H7FCXP4V) | Indie (KRW Media) | 2026-07-02 | 178 | 6.99 (spiral 15) | 4.0 / 88 | 1,005 [V] | Giant-list elimination (3,000 guest records) plus 6 evidence files; 3-tier hints; checkpoints | Medium (two-part case) | B&W [A] | No |
| 7 | Brain Games – Cold Case Puzzles (1645580601) | Publications International (trad) | 2019-12-01 | 192 | ~2.16 | 4.3 / 3,700 | 1,358 [P] | Mixed (picture, observation, logic) | Low | Colour [A] | No |
| 8 | The Autumn Killer (B0HJN1KLHD) | Indie (A.S. Remington) | **2026-09-13** | 250 | 9.99 (spiral 39.99) | 4.7 / 4 | 2,016 [V]; #8 Hot New Releases Puzzles & Games [V] | Giant-list elimination (~50,000 names) with 3 sub-mysteries | Low-medium | B&W [A] | No |
| 9 | A Murder For Christmas (B0HJCL4TS1) | Coral Horizon Publishing (indie) | 2026-09-10 | 112 | 15.72 | 4.7 / 18 | 2,774 [V]; #16 Hot New Releases [V] | Advent calendar: 24 days, 48 logic teasers, 49 suspects | Medium [A] | B&W [A] | No |
| 10 | CRIMESEARCH Vol 1 (1996805045) | CrimeSearch Puzzles (indie imprint) | 2026-05-13 ("fully revised June 2026") | 156 | 6.55–12.99 | 4.6 / 258 | 4,000 [V] | Word search, missing word, hidden message, decoder | Low | B&W [A] | No |
| 11 | The Coroner's Cold Case Files (B0HCYP5FJN) | Indie | 2026-08-04 | 140 | 13.99 | 4.4 / 46 | 5,236 [P] | Forensic elimination across 5,000 autopsy files | Low-medium | B&W [A] | No |
| 12 | Murder for Breakfast (3912326142) | Suburbia Publishing (small press) | 2025-10-16 | 127 | from 7.90 | 4.8 / 183 | 6,896 (#23 Cozy Craft & Hobby Mysteries) [V] | Cozy story with 50 word searches; clues collected for a final reveal puzzle | Medium | B&W [A] | No |
| 13 | Murder at Vex Manor – Halloween Escape Room (B0HDQB3X3J) | TG Edition | 2026-08-10 | 112 | 16.99 | 4.0 / 13 | 7,462 [P] | Escape-room mixed puzzles, seasonal | Medium [A] | ? | No |
| 14 | Eliminate!: A Murder Mystery Logic Puzzle Book (B0H61WHM4M) | Indie | 2026-06-18 | 402 | 7.07 | 4.5 / 117 | 9,274 [P] | Elimination logic | ? | ? | No |
| 15 | Black Tide House Murder Mystery Puzzle Book (8368347211) | Stellita Jane (indie) | 2026-08-28 | 152 | 10.78 | 4.8 / 11 | 9,730 [V] | Document "case file" (statements, CCTV, records), 17 clues | Medium-high | B&W [A] | No |

Just outside the top 15 [V/P]: The Killer Bought A Ticket (B0HBKW8HH6; indie; 2026-07-22; 303 pages; **3.6 / 42**; BSR 9,847). CRIMEMAPS (B0HGXN3NWL; indie; 2026-08-28; route deduction on illustrated city maps; 4.7 / 39; BSR 11,483). The Official Clue Book of Puzzles (1400360110; Cider Mill, a Hasbro licence; preorder for 2026-10-27; BSR 11,976). The Killer Isn't Beth (0316616192; Little, Brown; preorder for 2027-03-02; BSR 13,681). Murders in the Winter Hotel (B0HHRF7PBK; indie; 2026-09-04; 4.8 / 36; BSR 14,722). The Bookshop Murder (1408722208; Sphere; 2025-11-18; 4.6 / 66; BSR 17,653). Murdsearch Vol 1 (B0GQZCN8MH; indie; 4.7 / 430; BSR 23,202). **Do No Harm** (B0H4X2W7NN; indie, a clone of the 40,700-suspect format; **3.0 / 106**; BSR 23,747). Unsolved Case Files (B0H57433WY; 312 pages; 4.7 / 62; BSR 30,540). Whodunit?: 40 Murder Mystery Logic Puzzles (B0H6BPHSR7; 4.6 / 114; BSR 38,682). Large-print entrant **Cozy Case Files: A Large Print Cozy Mystery Puzzle Book for Adults and Seniors** (B0H7456NBX; 8.5x11; 2026-07-01; 4.5 / 2; **BSR 283,642**).

### 1b. Shape of the market [V unless marked]
- **Trad vs indie.** The top 3 are trad (Puzzlewright, Little, Brown, St. Martin's). Little, Brown's title began as an indie hit. **Indie titles hold 8 of the 15.** Indie books reach BSR under 1,000 within about 14 weeks (Kill Grid, Killer Never Checked In).
- **Formats now winning:** (a) sudoku-hybrid placement puzzles (Murdoku); (b) **giant suspect-list elimination** (Alice and at least 10 clones: Killer Never Checked In, Autumn Killer, Killer Isn't June, Who Killed Mr Darcy?, Last Dragon Egg, Killer Bought A Ticket, Do No Harm, Who Killed Alice?, Phone Book Serial Killer, Coroner's Cold Case Files); (c) **"mechanic" word searches** where leftover letters and missing words give the answer (Kill Grid, CRIMESEARCH, Murdsearch, MurderSearch, The Cat Did It!); (d) cozy novella plus word search (Cranberry Creek, Oakford Springs, Winter Hotel, Small Town Murders); (e) classic logic grids (Murdle and its imitators).
- **Price.** Indie paperbacks cluster at $6.99–$14.99. Many offer spiral ($15–40) and hardcover ($24.99–29.99) upsells. Kill Grid, CRIMESEARCH and Killer Never Checked In all offer spiral.
- **Trim.** Almost all are 6x9 [V, dimensions]. The only 8.5x11 large-print entrant found ranks poorly.
- **Colour.** Only Murdoku is verified as full colour. It is the #1 book on all of Amazon, and colour is part of its trade dress. Most indie titles appear to be B&W [A].

---

## 2. Trend

**Start of the wave.**
- Murdle Vol 1 published 2023-06-13 in the US [V]. The Murdle trademark was filed 2023-09-21 [V].
- Murdle's publisher claims over 4 million series copies [C, retailer copy, via WebSearch].
- Murdoku arrived 2025-10-28. Its page claims "more than 1 million copies in print" [C]. Euronews reports more than 140,000 copies sold in Spain [reported].
- The indie **Killer Isn't Alice (2026-02-22)** created the giant-list sub-genre. It drew 2,073 Amazon ratings in under 8 months, and Little, Brown republished it on 2026-09-01. A sequel (Beth) is on preorder for March 2027 [V].

**Growing or peaking?** All points below are [V] unless marked.
- **Murdoku Vol 1 is #1 in all Amazon Books today.** Murdoku Back in Time is #5 and Murdle V1 is #3 in Puzzles & Games. Murdoku Vol 3, Around the World, launches 2026-10-27 and is already #11 in Hot New Releases.
- **Puzzles & Games Best Sellers top 30:** 6 of 30 titles are murder/crime puzzle books (#1, 2, 3, 5, 14, 24).
- **Puzzles & Games Hot New Releases:** 11 of the top 30 and 12 of ranks 51–80 are murder/crime puzzle books, so **23 of the 60 new-release slots I sampled**.
- **Word Search Games Best Sellers top 30:** 6 of 30, including #1 Kill Grid. **Word Search Games Hot New Releases top 30:** 9 of 30.
- **Release timing.** Pub dates of the crime titles I sampled (about 45, so a visibility-biased sample rather than a count): 2026-02: 1, 03: 2, 04: 1, 05: 3, **06: 8, 07: 6, 08: 7, 09: 5**, 10: 1. The surge in releases began around June 2026, about 3–4 months after Alice went viral. [V sample; not a full count]
- **My read [A].** Demand is still rising into Q4 2026, carried by the trad series. Supply is now flooding, especially Alice clones. Some clones already show quality failures: Do No Harm at 3.0★, Killer Bought A Ticket at 3.6★, Killer Never Checked In at 4.0★. My best estimate is that demand peaks around Q4 2026 to Q1 2027 and supply keeps rising. I have no search-interest (Google Trends) data.

**Seasonality (Q4 gifting).**
- Reviews repeatedly frame these books as gifts: "What a great stocking stuffer" (Murdle GR, Jayme C) and "would make a great gift for Christmas or birthdays" (Murdle GR, Claire) [V].
- At least 8 Christmas murder-puzzle titles are live and the advent-calendar ones are already ranking: A Murder For Christmas at BSR 2,774 (published Sep 10); Murder Mystery Advent Calendar: The Killer Checked In at #21 in Hot New Releases; Escape Room Advent Calendar: Christmas Chalet at #51 [V].
- Trad publishers also time releases for Q4: Murdoku Vol 1 came out Oct 28, 2025, and Vol 3 comes out Oct 27, 2026. Adams Media's Cranberry Creek #5 is "Murder at the Christmas Market" [V title].
- I have no BSR history (no Keepa) to show the size of the Q4 uplift [A].

**How fast newcomers rise** [V]:

| Title | Published | Age at 2026-10-15 | Ratings | BSR now |
|---|---|---|---|---|
| Kill Grid V1 | 2026-07-06 | ~14 weeks | 66 | 700 (#1 Word Search) |
| Killer Never Checked In | 2026-07-02 | ~15 weeks | 88 | 1,005 |
| Autumn Killer | 2026-09-13 | ~4.5 weeks | **4** | 2,016 |
| A Murder For Christmas | 2026-09-10 | ~5 weeks | 18 | 2,774 |
| Killer Isn't Alice (indie) | 2026-02-22 | ~7.5 months | 2,073 | 1,665 (trad edition 26) |

The Autumn Killer reached BSR about 2,000 with only 4 ratings, so ads, launch velocity or Hot New Releases placement do much of the work in the first 30–60 days [A on cause]. The other side: most of the long tail sits at BSR 20k–800k. Examples: Rosewood Files at BSR 765,970; Cozy Case Files LP at 283,642; Detective Adam Case Files at 59,016.

---

## 3. Reader complaints and praise (Goodreads, ratings parsed from the review HTML)

I collected **58 reviews rated 1–3★** from 9 Goodreads pages: Murdle V1, V2, V3 and School of Mystery; Murdoku V1 and V2; The Killer Isn't Alice; Murder Among the Stacks; The Bookshop Murder. Full texts are in `wide2/crime/critical_reviews.txt`. Brief quotes below, grouped by theme.

**A. Too hard, or a difficulty "wall" in the second half; explanations that skip the "why"** (the most common theme for Murdoku)
- Murdoku 1★ (Fran): "I'd go look at the explanation at the end and it would say 'so it has to be this' and I'm like 'HOW!?'"
- Murdoku 3★ (Chesli): "I wasn't always able to follow some leaps".
- Murdoku 4★ (Jaclyn, quoted for the issue): explanations like "'B must go in that spot,' but not enough explanation of WHY".
- Murdoku 3★ (Alex Pler, Spanish): from puzzle 40 they are very hard and "los 10 últimos son prácticamente imposibles".
- Murdoku V2 2★ (Valerie Jackson): "characters were often placed in locations without adequate explanation".
- Murdoku V2 3★: the difficulty curve "es exagerada".

**B. Too easy or repetitive**
- Murdle V1 2★ (James): "the puzzles are extremely easy, even the 'impossible' ones".
- Murdle V1 2★ (Becci): "a bit too easy compared to other ones I've done".
- Murdle V3 2★ (Jake Howie): "Puzzles become very boring after a while".
- Murdle V2 3★ (German): "wird nach ner Weile ziemlich repetetiv".
- Murdle School of Mystery 2★ (Chass Coon): the story "repeated 50 times but with slightly different elements".
- Murdle V1 (Dez, top review, rating not 1–3): "they are all very similar - I'd like a little more variety".

**C. Errors, missing information, unsolvable or ambiguous clues** (these hit trad books too)
- Murdle V3 3★ (El Zet): "two puzzles in the last part had clues that weren't present anywhere".
- Murdle V3 3★ (Chesli): "There was one puzzle that had missing information. It's listed on the website".
- Murdle V2 3★ (David Hallstrom): "numerous typos ... rebuses on the grid did not match what was shown in the body".
- Murdoku 3★ (Spanish) and Murdle V1 3★ (Spanish): translation errors made cases unsolvable ("te hace imposible resolver").
- Alice 3★ (Amy Leeke) emailed the author "about clue semantics".
- Alice 3★ (Sabrina): "missing a single page meant I couldn't solve the mystery".

**D. Thin story** (cozy word-search books and Murdle)
- Murder Among the Stacks 2★ (Tricia): "a word search book, with a small side of story ... feels like a missed opportunity"; the puzzles "are merely just key words taken from the previous paragraph".
- Same book 2★ (Kelsey): "very little writing and no character development".
- Same book 2★ (Chloë-Louise): "chapters were far too short ... the killer reveal wordsearch was also mostly unnecessary".
- Same book 3★ (Jackie Linkous): "have the word search puzzles add to the story in some way - like add clues".
- Murdle V1 3★ (Krystal): "the 'story' parts are actually kinda pointless".
- Alice 2★ (Anja): "you get absolutely no back story".

**E. Tedium and eye strain in the giant-list format**
- Alice 3★ (Daniela, German): "200 Seiten nur mit Namen ... meine Augen fanden es super anstrengend".
- Alice 1★ (Bulgarian): returned the book: "200 страници, пълни само с имена".
- Alice 3★ (Sabrina): "way too long".
- Alice 1★ (Joanna Hristova): the real deduction was "maybe 1% of the whole exercise".
- Alice top review (Jayme C): "too hard on my OLD 👀 EYES".

**F. Layout and physical design**
- Murdle V1 2★ (Becci): "each puzzle spans 4 pages ... flicking"; "grids have ... pictures [not names]"; contents page useless because "the pages aren't numbered".
- Murdoku V2 2★ (Sam Swain): "squares are often too dark and a biro has little impact ... planning grids at the bottom are just way too small"; "lines don't always match up in the 'rooms'".
- Ebook complaints for Murdle (several ARC reviews): the grids and answer sections don't work on a Kindle.

**G. "AI"**
- Murdle V2 1★ (Heathenwisp): "The original website is partially generated by AI and you can tell they used it here to rush these books ... I wish I had known it was so heavily AI-generated."
- This is an accusation made against a trad bestseller; I did not verify whether it is true. The lesson is that readers do look for AI, and cite "inconsistent graphics" and "hacky" story as evidence.

**H. Off-topic 1★ reviews** (politics, DEI) also occur on Murdle. Nothing can be done about these.

**Praise to copy** [V quotes]
- "sudoku + cluedo = perfection" (Murdoku).
- Gradual difficulty: "the book does ease you into solving".
- Hints and step-by-step solutions in the back (Murdle, Murdoku).
- The Alice author answered reader emails personally, and the online answer check "told me why I was wrong".
- Couples and group play: "I had so much fun doing it with my wife" (Murdoku); "Did as a couple while making dinners" (Murder Among the Stacks).

---

## 4. Trademarks

| Mark | Status found | Owner | Note |
|---|---|---|---|
| **MURDLE** | US serial 98191545, standard character, Class 28 (board games, puzzle board games, logic puzzles, party games). Filed 2023-09-21, published 2024-07-23, Notice of Allowance 2024-09-17, Statement of Use filed 2025-07-30. Live [V, uspto.report]. I could not confirm final registration or any Class 16 (books) filing. | A Red Herring Corporation (Los Angeles) | Treat as protected. Do not use "Murdle" or close variants. |
| **MURDOKU** | murdoku.com says "Murdoku™ is a trademark of Digivoid Studios Inc." [V]. A USPTO application exists, serial 99677726, in clothing, software and entertainment classes per a search snippet; the detail page was bot-blocked, so status is unconfirmed. The creator wrote on Reddit: "yes, 'Murdoku' is trademarked ... there's a trade dress aspect (the overall look and feel) to pay attention to." [V] | Digivoid Studios Inc. (Manuel Garand) | Avoid the name and "-doku" murder portmanteaus. Also avoid copying the full-colour room-map look. |
| **CLUE** | Hasbro, Reg. No. 0526059, filed 1948, board-game equipment [V, Justia snippet]. CLUEDO is Hasbro's brand outside North America [V, Wikipedia snippet]. Hasbro v. Clue Computing (1st Cir. 2000) shows "clue" stays an ordinary word in other contexts [V]. | Hasbro | The word "clues" used descriptively is fine. Do not use Clue/Cluedo as a brand or imply Hasbro. The official licensed book (Cider Mill) exists. |
| **HUNT A KILLER** | Reg. No. 7609923, registered 2024-12-17, Class 28 (party games; tabletop games), first use 2016 [V]. An earlier Reg. No. 5232320 also appears in a TTAB record [V snippet]. | Relatable Detectives LLC (What Do You Meme) | Avoid the phrase in titles and keywords. |
| **WHODUNIT** | No search of registrations for this exact mark was done. It is a dictionary word and is widely used in Amazon titles ("Whodunit?! The Ultimate Detective Challenge", "Whodunit Logic Grid Puzzles") [V usage]. | — | Descriptive use is low risk [A]. Do not make it your series brand. |
| Indie "™" claims: MURDSEARCH™, CRIMESEARCH™ | Claimed on Amazon pages [V]. Registration not checked. | indie | Avoid "Murd-" and "Crime-" + "search" coinages. |

**Safe naming [A, not legal advice].**
- Use a coined series name of your own that is clearly yours, plus descriptive subtitle words: murder mystery, whodunit, detective, case files, cold case, word search, logic puzzles, cozy mystery, large print.
- Before committing, run a quick USPTO search of the series name in Classes 16 and 28.
- Do not use the "The Killer Isn't [Name]" pattern. It isn't a trademark, but there are already 3 or more copies, and it signals "clone".

---

## 5. Production feasibility with no human checker

**Can each puzzle type be generated and proven to have exactly one solution by code?** This section is my technical assessment [A]; the review evidence cited is [V].

| Type | Generate + prove unique? | How | Residual risk |
|---|---|---|---|
| Logic grid (Murdle-style: suspect × weapon × location × motive) | **Yes** | Pick a random solution. Write clues as typed constraints (is / is-not, either-or, same-person, liar statements). Add clues until a CP-SAT or backtracking solver finds exactly 1 solution, then remove clues while uniqueness holds. Grade difficulty with a human-style solver (direct elimination only, chains, case-splits). | **Clue wording.** Natural-language ambiguity is the main failure ("clue semantics" emails, translation errors). Fix it by rendering text only from fixed templates whose logic matches the solver's constraint 1:1, and keep a glossary on page 1 ("next to" = same row, adjacent). |
| Sudoku hybrid (rows and columns of suspects on a room map) | **Yes** | An N×N latin-style placement with region/object constraints, encoded in CP-SAT; same uniqueness and minimisation loop. | Trade dress (do not copy Murdoku's look). Explanations: generate a step trace that states *why* each placement is forced, because "B must go in that spot" with no reason is the #1 Murdoku complaint. |
| Word search with mechanics (leftover letters, missing word) | **Yes, trivially** | Place words, then scan all 8 directions to assert each listed word appears exactly once (watch palindromes and substrings). Fill leftover cells with the message in reading order and assert they spell it exactly. Check the missing word is truly absent. Filter for accidental profanity. | Very low. |
| Giant-list elimination (Alice-style) | **Yes** | Generate the name list from public name-frequency data. Clues are predicates (letter counts, chapter-title rules, position rules). Apply them and assert exactly 1 survivor; assert each clue removes something; print **checkpoint counts** ("after clue 6, 1,204 remain"), as Killer Never Checked In does. | Clue semantics again ("does Y count as a vowel", "name" vs "full name"). Also fatigue and eye-strain complaints; reduce the list size for a large-print edition. |
| Ciphers (Caesar, substitution, pigpen, book cipher) | **Yes** | Encode, decode and compare round trip; make sure the key given leads to exactly one plain text. | Low. Pigpen and glyph fonts need a visual proof. |
| Visual "spot the clue" or illustrated escape-room puzzles | **No** (needs a human eye) | — | Avoid them, or keep them out of the critical path. |

**Verdict [A].** Every core puzzle can be machine-verified. What is left is **text-to-logic fidelity**: does the printed sentence mean exactly what the solver assumed? The fix is template-only clue text plus an independent second solver that parses the *printed* clue text back into constraints and re-solves it. That second pass is the "checker". Also render the full book PDF and re-extract grids and words from the PDF to check layout errors (cropping, mismatched room lines; see the Murdoku V2 complaint).

**Story text needed.** Per case: a brief of about 80–200 words; 3–6 suspects, each with a one-line description and a motive; a location; a weapon or method; one twist or detail. Then a book-level arc: a recurring sleuth, a meta-mystery revealed by collecting one letter or code per case (as Kill Grid and Murdle do; reviewers praise the payoff). Readers punish stories where the puzzles do not feed the plot (Murder Among the Stacks). So **each solved puzzle must yield a clue that matters**.

**Keeping the story from reading as AI [A].**
- Write or heavily rewrite the briefs by hand with the human-voice-craft skill.
- Give one consistent narrator voice with dry humour (Murdle's humour is praised).
- Use concrete, specific setting details (a named village, real-sounding shops, period details).
- Vary sentence length; no list-like "Motive: ..., Alibi: ..." prose.
- Keep illustrations consistent; the "inconsistent graphics" charge was used as evidence of AI.
- Disclose any AI-generated text to KDP as KDP requires (my understanding of policy, not re-checked today).
- Puzzle grids generated by algorithm are normal in the industry and are not the AI risk; the prose is.

**What makes a 4.5★ book** (from the review evidence [V], design inference [A]):
1. A worked example first, then a gentle curve (about 25% easy). No wall in the second half. Several levels labelled clearly, with a level shown on each puzzle.
2. **Tiered hints**: a nudge, then a stronger hint, then a near-solution (Killer Never Checked In has 3 levels). Full step-by-step solutions that explain the *why*.
3. **One case per 2-page spread**: clues and grid visible together, page numbers, and solutions in the back in a jumbled order so the next answer is not spoiled by accident (Murdle complaints).
4. Grids labelled with words, not icons. Light grey shading only. Planning grids large enough to write in. Pencil-friendly paper (Murdoku V2 complaints).
5. Story that matters, plus a meta payoff at the end.
6. Variety: rotate 3–4 mechanics (grid, cipher, word search, timeline) to avoid "repetitive" reviews.
7. An author email or website for questions and errata (the Alice author's personal replies are praised); an online answer check is optional.
8. For large print: 16–18 pt body text and big grid letters. **Do not** ship a 40,000-name list in large print.

---

## 6. Gaps and angles

| Angle | Evidence | Assessment [A] |
|---|---|---|
| **Large-print murder-mystery word search for seniors** (overlaps the large-print word-search line) | At least 6 LP murder word searches exist. Only one charted: Parker Vance, "Murder Mystery Word Search: 100 Large Print...", #25 in Word Search Hot New Releases, 4 ratings, $4.99 [V]. The 8.5x11 LP cozy multi-puzzle book sits at BSR 283k [V]. Meanwhile plain LP word search dominates the Word Search Best Sellers (TG Edition, Martin Littlewolf, PIL) [V]. Eye-strain complaints about the giant-list format [V]. | **Best fit for this publisher.** The gap is not "LP murder word search" alone (it exists and is weak) but **LP plus a Kill-Grid-quality mechanic plus a cozy connected story**. The existing LP entrants look generic. |
| Cozy (non-gory) mysteries | Cranberry Creek (Adams Media, BSR 672) and Oakford Springs (#23 Cozy Craft & Hobby Mysteries) prove demand [V]. Their reviews ask for puzzles that carry real clues [V]. | Strong. Use the "clean cozy, no graphic violence" positioning, which Murder for Breakfast uses explicitly. |
| Christmas / holiday | At least 8 Christmas titles, several ranking (A Murder For Christmas BSR 2,774; advent calendars in Hot New Releases) [V]. | Demand is proven but **already crowded for 2026**. An advent "24 cases" structure is the sticky format. A "winter" (not December-dated) theme sells past Dec 25. |
| Historical settings | Bookshop Murder (1929 London, Sphere), Murdoku Back in Time, Who Killed Mr Darcy? (Austen) [V]. | Good differentiator, especially Victorian/Edwardian village or 1920s country house for the cozy/senior reader. |
| Couple / party play | Several reviews mention couples and groups [V]. "The Advent Calendar Challenge ... for Two" is #14 in Hot New Releases (not a murder book) [V]. | A secondary hook ("solve together" pages, two-player race scoring); I found no dedicated murder-puzzle-for-couples leader [A]. |
| Giant-list elimination | Huge demand (Alice). But at least 10 clones, with quality spread from 3.0★ to 4.8★ [V]. | Only worth doing with a clear twist. A shorter LP version (for example 3,000–5,000 names, 6+ pages of checkpoints) would answer the fatigue and eye-strain complaints. |

---

## Scores (out of 10)

| Dimension | Score | Basis |
|---|---|---|
| Demand | **9** | #1 in all Amazon Books (Murdoku); 3 crime puzzle books in the top 30 of all Books; 23 of 60 sampled Hot New Release slots [V] |
| Competition (10 = easy) | **3** | Trad series dominate the top; indie flood since June 2026; at least 10 Alice clones; at least 8 Christmas entrants. Indie titles can still reach BSR under 1k in about 3 months [V] |
| AI-hunt immunity | **7** | Algorithmic puzzles are standard and safe. Story prose is the exposure; readers already level "AI" accusations [V] |
| Accuracy risk without human checker (10 = low) | **6** | Every puzzle core can be proven unique by code. The risk is clue wording, layout and explanations; trad books get errors too [V] |
| Fit as a high-content book | **8** | Mostly generated puzzles plus short hand-written briefs; supports series, LP editions and seasonal editions [A] |

**Best angle:** a large-print cozy village murder-mystery word search series (non-gory, for seniors). Every puzzle yields a story clue and a letter toward a book-wide meta reveal, every grid is solver-verified, and the series has seasonal volumes ("Winter at ..." first).

**Biggest risk:** clone saturation, combined with a single wrong or ambiguous clue producing "unsolvable" 1★ reviews early, when ratings are few (comparable clones sit at 3.0–3.6★).

**Christmas window (live by about Nov 15):**
- **Realistic to publish; unrealistic to rank high organically.**
- The timing: 31 days from today. KDP paperback review takes up to about 72 hours, and a proof copy needs about 1–2 weeks [A, general KDP experience]. That works if the generator and layout pipeline are ready to go now.
- But competing Christmas titles launched in September and already hold ratings and Hot New Release spots [V]. A Nov 15 launch needs Amazon Ads and a non-dated winter theme so sales continue in Jan–Feb.

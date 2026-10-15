# Deep dive: nonogram puzzle books (griddlers, hanjie, paint-by-number logic, picross)

Research date: 2026-10-15.

Sources:
- Amazon.com search and product pages, fetched with TinyFish. Many returned 503 or a bot page, so I retried.
- Amazon.co.uk, .ca and .com.au product pages. These show reviews without a login.
- Reddit r/nonograms threads.
- Goodreads search.
- Google Play.
- The KDP printing-cost help page.
- Jan Wolter's webpbn solver survey.
- Trademark listings.
- My own solver code, run locally.

**Labels.** **VERIFIED** means I read it on a page I fetched today, or measured it with my own code today. **ASSUMED** means it is inferred or general knowledge that I did not re-check today. BSR is the Amazon.com Books rank unless marked UK.

Working files are in `/tmp/claude-0/-home-user-course/5d910e26-d220-53df-b12b-0c4e5f61c868/scratchpad/nono/`:
- `prod.tsv`: 49 listings with all fields
- `search.json`: parsed SERPs
- `reviews.json`: 234 reviews from 48 listings
- `crit.txt`: 86 critical or complaint reviews, full text
- `code/nono.py`: solver, uniqueness check and grading
- `code/test_repair.py`: sanity checks and repair loop
- `code/layout.py`: cell-size and font calculator

**Search coverage (VERIFIED).**
- Captured on Amazon.com: "hanjie puzzle book", "picross puzzle book", "nonograms for beginners", "paint by number logic puzzles" and "griddlers puzzle book". "nonogram puzzle book" comes from the earlier W6 run on 2026-10-15.
- "nonograms large print" and "color nonogram book" returned 503 on Amazon.com on every one of about 8 tries. I captured them on **Amazon.co.uk** instead, plus "christmas nonogram" on UK.

---

## 1. Market map

### Top 15 distinct titles (all VERIFIED from product pages unless noted)

These are ranked by US BSR among the titles that appear in the searches above. Notes on the columns:
- Puzzle counts, grid sizes and the solutions format are what each listing says it contains. I did not check them inside the books.
- "B&W (assumed)" means the listing does not say colour, and nonograms are B&W by default.

| # | Title (short) | Author / publisher | Pub date | BSR | ★ (ratings) | Pages / trim | Puzzles | Grids | Colour | Theme | Solutions |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Murdograms Crime Scene Investigation: Murder Mystery Nonogram Puzzles** | R. G. Walker / Life in Puzzle | 2026-08-18 | **6,174** (#54 Logic & Brain Teasers); UK #2,830 | 5.0 (6) US; 4.9 (9) UK | 154 / 6x9 | not stated ("cases", 3 levels) | not stated | B&W (assumed) | murder-mystery mini-stories: crime scene, 5 suspects, forensics report, then a nonogram whose image names the killer | QR code per case, plus a hints section |
| 2 | Nonogram Puzzle Book: From Beginner to Master With 150+ | Maximiliano Leyton Gaggioli / indep. | 2026-05-29 | 39,617 (#254 Aging) | 5.0 (26) | 91 / 8.5x11 | 150+ | 6 levels | B&W (assumed) | general, with a strategy section | illustrated, at the back |
| 3 | Nonogram Puzzle Book (Travel-Size) 225+ | Gaggioli / indep. | 2026-07-03 | 45,769 | 4.9 (16) | 151 / 6x9 | 225+ | 10x10, 15x15, 25x25, 35x35 | B&W (assumed) | general | illustrated |
| 4 | Nonogram Puzzle Book: 400 Challenging Puzzles | Riddle Rhapsodist / indep. | 2023-03-08 | 80,266 | 4.6 (58) | 282 / 8.5x11 | 400 | not stated | B&W (assumed) | general | at the back |
| 5 | Murdograms: 80 Murder Mystery Nonogram Cases | Richard Ng / indep. | 2026-09-27 | 98,783 | none yet | 178 / 6x9 | 80 | 12x12 to 20x20 | B&W (assumed) | murder mystery, "400 unique suspects" | full, spoiler-safe |
| 6 | Nonograms for Everyone: 88 | Bad Bird / indep. | 2020-12-30 | 114,358 | 5.0 (31) | 110 / 7x10 | 88 | 5x5 to 25x30 | B&W | pictures | at the back |
| 7 | Nonogram Puzzle Book: Easy to Hard, 20x20 to 50x50, 80 Puzzles | Brainteaserz Press / indep. | 2023-04-05 | 120,217 | 4.0 (89) | 80 / 8.5x11 | 80 | 20x20 to 50x50 | B&W | abstract, animals, objects | at the back |
| 8 | Picture Cross Cats & Dogs: 100+ | Parragon (licensed app brand) | 2025-07-01 | 156,868 | 4.0 (10) | 128 / spiral | 100+ | not stated | **B&W and colour** | cats and dogs | not stated |
| 9 | Big Book of Picross Hanjie Griddlers Nonograms, 4 vols in 1 (406) | Djape / indep. ("Visual Deduction", book 1 of 5) | 2020-11-11 | 224,378 | **4.7 (292)**, the most ratings in the niche | 316 / 8x10 | 406 | 10x15 to 35x35, 30x40 | B&W | pictures | full image solutions |
| 10 | **Nonogram Puzzle Book … 300+ (the 3.8★ Gaggioli book)** | Gaggioli / indep. | 2026-04-06 | 246,888 | **3.8 (34)** US; 4.1 (22) on .ca/.com.au | 191 / 8.5x11 | 300+ | 6 levels | B&W (assumed) | general | illustrated |
| 11 | Big Book … 250++ PREMIERE | Djape / indep. (book 2 of 5) | 2022-11-11 | 378,811 | 4.5 (86) | 175 / 8x10 | 250 | 10x15 to 30x40 | B&W | pictures | at the back |
| 12 | Big Book of Nonograms … 3 Volumes in 1 (411) | Fishpa Publication / indep. | 2024-05-29 | 452,727 | 4.6 (13) | 347 / 8.5x11 | 411 | not stated | B&W (assumed) | volumes for beginner, easy-to-hard and expert | not stated |
| 13 | Nonogram Puzzle Book with 400 Easy to Expert | Kyle Evans / indep. | 2023-04-14 | 454,220 | 4.1 (44) | 402 / 8.5x11 | 400 | 11x15 up to 78x78 | B&W | pictures | **QR codes, nothing printed** |
| 14 | Big Book … 250++ ALL NEW | Djape / indep. (book 3 of 5) | 2021-11-02 | 498,530 | 4.6 (82) | 178 / 8x10 | 250+ | 10x15 to 30x20 and larger | B&W | pictures | included |
| 15 | 100 Nonogram Puzzles for Beginners | Jeanette Goodman / indep. | 2019-11-07 | 598,677 | 4.6 (160) | 116 / 6x9 | 100 | 5x5 to 20x20 | B&W | pictures, with a "title clue" section | at the back |

**Other notable listings (VERIFIED):**
- Djape ATARASHI 200++: 4.6 (56), 154 pp 6x9, 209 puzzles from 10x15 to 30x40. No US BSR was shown.
- Clarity Media *Hanjie Puzzles: 50*: 4.2 (125), BSR 1,241,693. The listing claims "logic alone… never need to guess".
- Griddlers.net *Black and White 31*: BSR 1,081,377, 5.0 (4). It is a series of more than 31 volumes and fills most of the "griddlers puzzle book" SERP.
- Colour titles:
  - Robin Tails *Nonograms Multicolor vol. 1* (2026-03): 440,418, 5.0 (3)
  - Puzzel Peak *Color Nonogram* (2026-09): 445,750
  - *Multicolor vol. 2*: UK 368,684, 3.8 (11)
- Expert titles:
  - Fishpa *Mega 50x50*: 4.4 (7)
  - Chester Publishing *150, 35x35 to 50x50*: no rank shown. It advertises **"famous faces"**.
- Kit: Descartes *The Nonogram Package* (Seoul, 2025-10-31), a 500-puzzle hardcover box with clipboard and pencils: 5.0 (5), no BSR.

### Shape of the market (VERIFIED from 32 listings with a US BSR)
- **1** title is under 10k: Murdograms.
- **3** are under 50k: Murdograms and two Gaggioli books.
- 5 are under 100k, 7 under 150k, 10 under 250k, 17 under 500k and 21 under 1M.
- For comparison, from the W6 data: Murdle Vol. 1 is #28 and Puzzle Baron's Logic Puzzles is #12,969. Plain nonogram books are a mid-sized niche, not a large one.
- The ratings ceiling is low. Djape's 4-in-1, with 292 ratings in about six years, is the most-rated title I found. Most titles have 5 to 90 ratings.
- Goodreads (VERIFIED): a search for "nonogram puzzle book" returns "over 1,642 results". Titles carry 0 to 3 ratings and almost no review text, so Goodreads is useful only as a measure of supply. One author, "Logi Brainz", has 160 books listed with 9 ratings in total.

### Standard format (VERIFIED from listings)
- Trim is 8.5x11 or 8x10, with a 6x9 travel format becoming common.
- 80 to 400 puzzles. Small 5x5 to 15x15 grids are for beginners; 20x20 to 30x30 is the core; 35x35 to 50x50 is for experts. One book goes to 78x78.
- One large or two small puzzles per page.
- Solutions are images at the back. Kyle Evans and both Murdograms books use QR codes instead.
- "No guessing" and "unique solution" are standard selling claims: Clarity, Bad Bird, Goodman, Brain Power and Fishpa all make them.

---

## 2. How newcomers fare (2025–26, VERIFIED)

| Title | Pub | US BSR | ★ (n) |
|---|---|---|---|
| Murdograms CSI (Walker) | 2026-08-18 | **6,174** | 5.0 (6) |
| Gaggioli 150+ | 2026-05-29 | 39,617 | 5.0 (26) |
| Gaggioli Travel 225+ | 2026-07-03 | 45,769 | 4.9 (16) |
| Murdograms 80 Cases (Ng) | 2026-09-27 | 98,783 | none |
| Picture Cross Cats & Dogs (Parragon) | 2025-07-01 | 156,868 | 4.0 (10) |
| Gaggioli 300+ | 2026-04-06 | 246,888 | 3.8 (34) |
| Nonograms Multicolor vol. 1 | 2026-03-10 | 440,418 | 5.0 (3) |
| Color Nonogram 56 (Puzzel Peak) | 2026-09-20 | 445,750 | none |
| Fishpa Master Vol. 5 | 2026-04-30 | 465,999 | none |
| Logi Brainz Vol. 02 | 2025-03-28 | 596,677 | 3.8 (5) |
| BrainGrid 100 (25x30 to 35x40) | 2025-08-30 | 686,716 | 3.5 (4) |
| Christmas Nonogram 101 (Thought Activity Lab) | 2025-09-27 | 1,163,031 (October, off-season) | 4.6 (5) |
| Brain Power Beginners Large Print | 2025-12-20 | 1,485,743 | 3.9 (12) |
| Fishpa Giant 40x45 | 2025-08-27 | 2,231,120 | 5.0 (1) |
| Nonogram Animals 101 (Thought Activity Lab) | 2026-03-21 | 2,257,687 | none |

Gaggioli 450+ (2025-11-17, 311 pp) is UK 591,361 with 3.9 (27). I could not get its US page.

**Is demand concentrated? Yes (VERIFIED pattern; the interpretation is mine).**
- Of the 15 newcomers with a US rank, only **4** are under 100k. Three of those four come from **two "brands"**: the Murdograms concept, and Gaggioli's "From Beginner to Master" line of four books in eight months.
- The other 11 sit at 150k to 2.3M.
- A plain "N puzzles, easy to hard" book from a new account usually lands at 400k or worse.
- Gaggioli shows a newcomer *can* reach about 40k with clean design, strategy pages and a progression. His 300+ book also shows how one accuracy complaint ("guessing") pulls the rating down to 3.8.
- **Murdograms copycat signal:** Richard Ng published a book with the *same name* about six weeks after Walker's. It is already at 98,783 with no reviews, so the concept pulls demand on its own. A fast-follower window existed and has now been used.
- TikTok and creator videos of Murdograms are linked on lifeinpuzzle.com (@kwan_reads, @caseydoescrafts), VERIFIED.

---

## 3. Reader complaints and praise

Texts come from Amazon UK, CA and AU product pages, which show US, UK, AU and CA reviews without a login, and from Reddit. There are 86 critical or complaint texts in `crit.txt`. Goodreads has essentially no review text for this niche (VERIFIED: 0 to 3 ratings per title). All quotes are verbatim and VERIFIED.

### A. Guessing, multiple solutions, unsolvable (the #1 quality risk)
1. Gaggioli 300+ (US 1★, Sep 2026): "It is virtually impossible to do most of these puzzles without having to look up the solution in the back!"
2. Gaggioli 300+ (review highlight on .com.au): "Lots of GUESSING required in this book."
3. Djape ATARASHI (CA 3★): "sometimes I have to guess where to shade in to finish the puzzle."
4. *Big Book of Brain-Boosting Pix-Cross* (Racehorse, US 3★): "some of the puzzles do not have unique solutions—you can correctly solve the puzzle without making the intended picture."
5. Same book (US 1★): "Most puzzles aren't solvable by pure logic, some of the puzzles near the back have incorrect numbers printed or cut off entirely"
6. *The Ultimate Nonogram Puzzle Book* (UK 1★, Jul 2026): "The nonograms are made using ai clearly with no logic … u just have to guess or assume where to draw"
7. Same book (UK 2★): "The nonograms themselves all include the text "made with the LogTek Puzzle Maker"."
8. *Nonogram Puzzle Book for Adults: Large Size* (US 3★): "There were a few where it seemed that I couldn't make progress without guessing"
9. Reddit r/nonograms (Jan 2026): "I've had some cheaper books on amazon where you had to guess to finish"
10. Reddit (2024): "you just have to watch out for ones made in a rush."

### B. Clue or answer errors and misprints
11. BrainGrid 100 (UK 1★): "These puzzles do not work out right."
12. Brain Power Beginners (US 1★): "Once I got to puzzle 27 the puzzles and answer key no longer matched"
13. Clarity *Hanjie* (UK 3★): "puzzle 41, rows 8 & 9 down are not the same in the grid as the answer"
14. Riddle Rhapsodist 400 (US 5★): "found a misprint" and "the one missing and duplicated puzzle"
15. *Picture Cross Around the World* (US 1★): "the colors don't even match in some spots in the "answer"."

### C. Print too small (the most frequent complaint by count)
16. Brainteaserz (UK 1★): "The print is too small to use."
17. *Hanjie Collection I* (US 2★): "if you have a magnifying glass to read it."
18. Djape 4-in-1 (AU 1★): "Fonts too small and hard to read on most puzzles."
19. *Multicolor vol. 2* (US 1★): "Print is way too small. Multiple designs per page. Blurry and hard to read."
20. Tritonn Vol. I (UK 4★): "could not complete 10 of them as the numbers were so small and the ink not dark enough."
21. Brainteaserz (AU 3★): "would be better if the numbers were further apart so you can cross them off"

### D. Grid lines, gutter and layout
22. Brainteaserz (UK 2★): "the horizontal and vertical lines are poorly printed with some missing altogether."
23. Fishpa Mega 50x50 (US 4★): "the crease of the book cuts off the last column."
24. Logi Brainz Vol. 02 (US 2★): "The print is real close to inside edge"
25. Kyle Evans 400 (US 4★): "the empty rows and columns around the outside of a puzzle is seriously ANNOYING!"
26. Tritonn Vol. I (AU 2★): "the grid isn't restricted to multiples of 5x5 size."

### E. Too easy, too hard, monotonous
27. Clarity 50 (UK 3★): "If you have done Hanjies before then these are too easy" and "Many titles gave the picture away"
28. Suphiss 60 Large (Sweden 3★): "counting along to 50 every time is a little monotonous."
29. Brainteaserz (UK 4★): "harder just seems to mean bigger"
30. Picture Cross Cats & Dogs (US 4★): "Nice quality but too simple"
31. Djape ATARASHI (CA 3★): "the posted difficulty levels mean nothing."

### F. Repetitive or unrecognisable images
32. *Nonogram Puzzle Book Large Print: 100* (UK 1★): "50 puzzles of the letter c and 50 puzzles of the letter d."
33. Djape PREMIERE (UK 3★): "Some are so poor it's difficult to see what they are meant to be"
34. Brainteaserz (UK 2★): "the pictures in this are very uninspiring."

### G. Bleed-through and physical defects
35. Tritonn Vol. II (UK 3★): "the ink goes right through to the other puzzle, thus spoiling half of the book"
36. Djape PREMIERE (UK 3★): "they bleed through a little in this book."
37. Djape ALL NEW (UK 1★): "the first 148 puzzles were missing!" (a KDP print defect)
38. *Multicolor vol. 2* (DE 1★): "the insides are printed in black-and-white making the book useless"

### Praise (what to copy)
- Clarity (UK 5★): "All puzzles can be solved purely by deduction (no guessing games)"
- Suphiss (UK 5★): "some hanjie books are difficult for me to see due to very small squares, but this one has bigger squares."
- Fishpa 3-in-1 (US 5★): "the size of the little squares … are PERFECT for my mechanical pencil … All the puzzles are engaging and creative and actually work!"
- Kyle Evans (US 5★): "A QR code to the hint and solution is perfect." Another reviewer on the same book (3★) complained of "issues with scanning some of the QR codes".
- Djape ATARASHI (US 5★): "The numbers are very clearly printed which was an irritation in the other book I have."
- Djape 4-in-1 (CA 5★): "not just counting and then filling huge blocks of squares."
- Tritonn II (US 4★): "I haven't found one that required guessing."
- A recurring motive on Reddit in 2026 (Jan, Aug and Oct threads, VERIFIED) is buying a book to cut screen time before bed.

**Synthesis.** Readers punish three things, in this order:
1. Puzzles that need guessing or have the wrong clues.
2. Print that is too small or faint, including cells cut off at the gutter.
3. Boring or unreadable pictures.

All three can be engineered against.

---

## 4. Production feasibility with code

### 4.1 Solver, uniqueness and "no guessing" (VERIFIED: I wrote and ran it)
`code/nono.py` is about 150 lines of pure Python. It contains:
- An exact dynamic-programming **line solver**. For each row or column it finds the cells forced in every arrangement that fits the clue.
- Row and column **propagation** until nothing changes.
- **Backtracking** that counts solutions up to two.

If propagation alone fills the grid, the puzzle is *line-solvable*. That proves both a unique solution and "solvable without guessing" in the usual reader sense.

Sanity tests passed:
- A 2x2 diagonal is correctly flagged as ambiguous.
- On 200 test images, the line-solved grid never differed from the source image.

Test run on 60 synthetic "blob" images per size (random noise smoothed into picture-like shapes):

| Grid | Line-solvable | Unique | Mean passes | Time for 60 |
|---|---|---|---|---|
| 10x10 | 51/60 | 51/60 | 3.0 | <0.1 s |
| 15x15 | 39/60 | 39/60 | 4.7 | 0.2 s |
| 20x20 | 28/60 | 30/60 | 5.9 | 0.6 s |
| 25x25 | 29/60 | 30/60 | 7.3 | 1.6 s |
| 30x30 | 26/60 | 29/60 | 7.4 | 4.5 s |

**Key finding:** about half of naive images at 20x20 and above are not line-solvable. Many are not even unique. Publishing straight from images is exactly what produces the "had to guess" reviews.

**Repair loop** (`code/test_repair.py`): flip one pixel inside the unresolved region and re-test, up to 40 times. It made **40/40** images line-solvable at 20x20 and **35/40** at 30x30, with a median of 0 to 1 flips. In production, flips should be limited to pixels that do not change the picture, or the image redrawn.

This matches Wolter's webpbn survey (VERIFIED): "although nonogram solving is known to be NP-complete … it is nevertheless quite easy to build a practical solver". The survey also says a validator "must try to find a second" solution, which is what `count_solutions` does.

### 4.2 Difficulty grading (method VERIFIED in code; thresholds ASSUMED)
- Measure the number of propagation passes, the share of cells fixed in the first pass by simple overlap, and the clue density (count of 1s and number of clue groups).
- For an optional "Expert" tier that allows lookahead but never blind guessing: require one-cell contradiction probing, and grade by how often probing is needed.
- Calibrate the bands by test-solving about 20 puzzles by hand. Reviewers complain that labels like "difficulty levels mean nothing" and that "harder just seems to mean bigger", so do not grade by size alone.

### 4.3 Images
- **Options:**
  - Hand-drawn pixel art at 10x10 to 30x30, the safest route.
  - CC0 pixel or icon packs (ASSUMED: Kenney asset packs are CC0; check each pack's licence).
  - Down-sampled AI images.
- Avoid share-alike sets such as OpenMoji (CC BY-SA, ASSUMED) and attribution-only sets unless you credit them.
- KDP's Content Guidelines (VERIFIED snippet): "AI-generated images include cover and interior images and artwork". These must be disclosed. AI-assisted content does not need disclosure.
- **A human or vision check is still needed for recognisability** (see complaints F). A solver cannot tell you that "lizard" does not look like a lizard.

### 4.4 Print layout (computed by `code/layout.py`, VERIFIED as arithmetic)
Assumptions:
- Margins are 0.5 in, with a 0.75 in gutter. The 0.75 in gutter is ASSUMED, chosen to avoid the "crease cuts off the last column" complaint.
- The clue zone equals the maximum number of clue groups per line, measured on blob images. Detailed pictures need a deeper zone, so real cells will be somewhat smaller.

| Grid | 8.5x11 cell / clue font | 6x9 cell / clue font |
|---|---|---|
| 15x15 | 10.2 mm / about 17 pt | 6.7 mm / about 11 pt |
| 20x20 | 7.7 mm / about 13 pt | 5.0 mm / about 9 pt |
| 25x25 | 6.3 mm / about 11 pt | 4.2 mm / about 7 pt |
| 30x30 | 5.1 mm / about 9 pt | 3.4 mm / about 6 pt |
| 35x35 | 4.4 mm / about 7 pt | 2.9 mm / about 5 pt |
| 50x50 | 3.2 mm / about 5 pt | 2.1 mm / about 4 pt |

This explains complaint group C. A 35x35 grid in a 6x9 book (Gaggioli Travel's Hard level) or 50x50 on 8.5x11 cannot be legible to older eyes.

**Rules I'd set:**
- Large print: at least 6 mm cells and at least 11 pt clues. That means at most 25x25 on 8.5x11 and at most 15x15 on 6x9.
- Bold line every 5 cells, and make grid dimensions multiples of 5 (a Reddit and Amazon request).
- No empty border rows or columns.
- One-sided printing for pen users, since reviewers mention felt pens bleeding.
- Puzzle numbers on every page.
- Solutions with 5-cell guides. A French review of the 50x50 book complains that solutions lack bold separators.

### 4.5 KDP print cost (VERIFIED, KDP help page G201834340, Amazon.com)
| Ink | Regular trim (6x9) | Large trim (8.5x11) |
|---|---|---|
| Black, 24–110 pp | $2.30 flat | $2.84 flat |
| Black, 110–828 pp | $1.00 + $0.012/pg | $1.00 + $0.017/pg |
| Standard colour, 72–600 pp | $1.00 + $0.0255/pg | $1.00 + $0.0402/pg |
| Premium colour, 42–828 pp | $1.00 + $0.065/pg | $1.00 + $0.08/pg |

Worked examples (arithmetic on the table; the 60% royalty rate is ASSUMED to be KDP's standard paperback rate):
- 150 pp 8.5x11, black ink: print cost **$3.55**. At $12.99 the royalty is about $4.24.
- 150 pp 8.5x11, standard colour: print cost **$7.03**. At $12.99 the royalty is about $0.76. At $16.99 it is about $3.16.
- 150 pp 8.5x11, premium colour: print cost **$13.00**, which is not viable.
- 150 pp 6x9, black ink: print cost **$2.80**.

Colour nonograms need colour clues, so they need a colour interior. The colour price penalty is large, and the colour titles I found are ranked 368k to 446k. One reviewer received a colour book printed in B&W.

### 4.6 IP risk
- **"PICROSS" is a Nintendo trademark** (VERIFIED: Justia lists PICROSS as a trademark of Nintendo of America; CIPO 2010064 is held by Nintendo Co., Ltd.; Jupiter states "Picross is trademark of Nintendo"). Many KDP titles use it anyway. Keep it out of the title and subtitle, and treat keyword use as a takedown risk (ASSUMED).
- **"Picture Cross"** is an app brand licensed to Parragon (VERIFIED listing: "Inspired by Picture Cross, the bestselling app"). Avoid it.
- **"Murdograms"**: two different publishers use the name. I did not check trademark status. Do not use it, or Murdle or Murdoku, as a title.
- **Pictures:**
  - No characters. A Goodreads listing exists for "Disney Famous Heros Nonogram Puzzles" (VERIFIED), which is an infringement example.
  - No "famous faces". Chester Publishing and Racehorse advertise them (VERIFIED), which carries a right-of-publicity risk.
  - No logos or brand mascots.
  - Use generic animals, objects, landmarks as silhouettes, holidays and food.
- Puzzle *mechanics* are not protectable (ASSUMED, standard). The clue-number layout is functional.

---

## 5. Gaps and angles

1. **Story or mystery nonograms (the strongest demand signal).**
   - Walker's Murdograms reached #6,174 US and #2,830 UK in about eight weeks. Ng's same-name follower reached 98,783 with no reviews.
   - Murdle sits at #28 (W6 data), so the murder-mystery logic wave is real.
   - This angle needs genuine writing: cases where the evidence logically fixes cells. It is not just a nonogram.
   - Differentiate it, for example as a cozy, non-murder detective book, a heist, an escape room, or a "lost-and-found" museum story. Never reuse the name.
   - It is writing-heavy and copycats arrive within weeks.
2. **"Guaranteed logic, readable" mainstream book.**
   - The three main complaint groups are guessing, small print and dull pictures, and all three can be fixed with code and layout rules.
   - Gaggioli shows the reward: about 40k BSR with strategy pages and a level progression.
   - Add a printed "Solver-verified: every puzzle has exactly one solution reachable by row and column logic" badge, plus per-puzzle difficulty stars.
3. **Large print for seniors.**
   - Supply is thick but weak. The UK search returned "411 results", and the large-print titles I checked rank at UK 784k to 2.8M.
   - As a standalone keyword it shows little proven demand. As a *feature* of a mainstream book, with big cells and at most 25x25, it answers the most common complaint.
   - Gaggioli 150+ ranks #254 in "Aging", so the seniors audience buys general books.
4. **Beginner and mini books.**
   - Goodman's 100 for Beginners has 160 ratings and Bad Bird's Beginners sits at 566k.
   - "Nonograms for beginners" SERP leaders are old. A small 6x9 at 5x5 to 15x15 with a real teaching chapter costs $2.30 to print at 110 pages or fewer.
5. **Themed packs.**
   - Animals (2.26M), Christmas 2025 (1.16M in October) and Halloween (2023) show that themes alone do not sell.
   - Use themes as series skins on a quality base, not as the hook.
   - Christmas UK SERP: "109 results", including 2026 entries such as "The Advent Window: 80 Large-Print Christmas Nonogram Puzzles" (2026-10-04) and "Christmas Nonograms: 250 Puzzles" (2026-10-06).
6. **Colour nonograms.**
   - Weak evidence of demand (368k to 446k), with two to three times the print cost and colour-specific complaints. Skip for now.
7. **Series potential: high (VERIFIED).**
   - Djape: 5-book series.
   - Griddlers.net: 31+ B&W volumes plus an Advanced line.
   - Fishpa: Vol. 5 and single-size lines.
   - Gaggioli: 4 books in 8 months.
   - Logi Brainz: 160 Goodreads listings.
   - Solvers buy repeatedly. One reviewer: "I'll purchase from this company again … after ensuring the puzzles I've completed are not included".

---

## 6. Trend

- **Google Trends: no data.** The page needs a modern browser and was not fetchable.
- **Apps (VERIFIED):** Nonogram.com (Easybrain) shows **50M+ downloads and 904K reviews** on Google Play, updated Aug 19, 2026. There are many other apps, such as Nonogram Zen ("31,000+ handcrafted"). The format has a large audience that is used to playing on phones.
- **2026 cultural signals (VERIFIED search snippets):**
  - Google's I/O 2026 teaser included a Nonogram puzzle.
  - Squeakross got a free content update in Feb 2026, and Kotaku covered it in Sep 2026.
  - New homebrew nonogram games appeared for Game Boy.
- **Reddit (VERIFIED):** r/nonograms "which book?" threads appeared in Jan, Aug and Oct 2026. The screen-time motive could be used in a listing.
- **Supply (VERIFIED):** 15 of the 32 US-ranked titles I sampled are 2025–26 releases. UK large-print and Christmas SERPs are full of B0H… ASINs from 2026.
- **Verdict (interpretation):** reader interest looks **steady**, with a **growing** hybrid sub-trend (murder-mystery logic). **Supply is growing faster than demand.** Most new plain books do not get traction.

---

## Scores (10 = good for us)
| Criterion | Score | Basis |
|---|---|---|
| Demand | **5** | One hit under 10k. Only 3 titles under 50k. Mid-sized niche, backed by a large app audience. |
| Competition (10 = easy) | **5** | Hundreds of titles and strong series incumbents (Djape, Griddlers.net, Fishpa), but most newcomers are low quality. Gaggioli shows quality can climb. |
| AI-hunt immunity | **4** | Puzzles are algorithmic, not generative-AI text. That is fine for KDP if the pictures are original or disclosed. But the category is trivially machine-made and already flooded, and readers already accuse books of being "AI made". |
| Accuracy risk without a human checker (10 = low) | **8** | The solver mathematically proves uniqueness and line-solvability, and clues are generated from the same data, so no misprints. Residual risks need one human pass on a proof copy: recognisable pictures, legibility, and gutter or line printing. |
| Fit as a high-content book | **8** | Fully code-producible and verifiable. The value comes from curation and layout, not prose. |

## Best angle
- **Short term:** a solver-verified, readable book with a teaching progression and recognisable themed pictures. Cap it at about 25x25 on 8.5x11, use 6 mm or larger cells, 5-cell bold lines, puzzle numbers and a deep gutter. Build it as volume 1 of a series.
- **Next (Q1 2027):** a differentiated story-nonogram hybrid (cozy detective, heist or escape room) that does not reuse the Murdograms name.

## Biggest risk
Commoditisation. In this sample, 11 of 15 new 2025–26 books with a US rank sit beyond 150k. A competent plain book probably lands there too unless it is visibly better (legibility and "no guessing") and becomes a series. For the hybrid, copycats arrive within about six weeks.

## Christmas-window feasibility
Today is Oct 15.
- The code pipeline produces and verifies puzzles in minutes. The bottleneck is about 120 recognisable pixel images, plus a cover and one proof copy.
- A plain verified book could be live by early November. ASSUMED: KDP review takes up to about 72 hours, and paperback indexing adds days.
- The hybrid mystery book needs about 50 to 80 written cases with evidence that logically fixes cells. That is tight and risky for Christmas.
- The October BSRs of 2025 Christmas nonogram titles (1.16M to 4.0M) do not show their December level.

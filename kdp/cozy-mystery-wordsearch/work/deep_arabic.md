# Deep dive: Arabic alphabet writing/reading workbooks for English-speaking beginners (KDP)

Research date: 2026-10-15. Sources: Amazon.com product pages (via TinyFish fetch; US search pages returned 503 on every attempt, so **keyword rankings come from Amazon.co.uk book searches**, while BSR/pages/dates come from the Amazon.com product pages where they loaded), Amazon.co.uk/.com.au review sections, KDP Help, Tanzil, Unicode, GitHub, prior file W13.tsv. A HarfBuzz test was run locally.
Tags: **[V]** = verified on a fetched page or by a local test; **[W13]** = from the prior W13.tsv crawl (same week); **[A]** = assumption or inference.
Raw working files: `scratchpad/wide2/arabic/` (us_prod.tsv, quotes.txt, asins.txt, uk_*.json, poc/shape.py).

---

## 1. Market map: top titles across the 8 keywords

The keywords searched were arabic alphabet workbook, arabic alphabet for kids, learn arabic alphabet adults, arabic handwriting practice, arabic letters tracing, learn to read arabic, noorani qaida and arabic workbook for beginners. Each was searched on amazon.co.uk (Books), and up to 16 organic positions were recorded per keyword (asins.txt). The titles below are those that appear on several keywords or rank in the top 3, plus the main publisher benchmarks. BSR, ratings, pages and dates come from Amazon.com unless marked otherwise.

| # | Title (short) / ASIN | Publisher | Date | Pages | US price | Rating (n) | US BSR (top sub-cat) | Content type | Audience / framing |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **The One and Only Arabic Workbook** B0F6MM9S6T | Indie brand "Self-taught AR" (series) | 2025-04-25 | 138 | $14.95 | 4.8 (186) | **43,189** (#14 Quran, #63 Foreign Lang Instr) [V] | 20-page intro; "400+ writing exercises"; all 4 forms; tashkīl/harakat; words, then sentences; audio and 200 flashcards on the Knowt app; "4-step learning guide" for the Quran [V desc] | Adults; secular-neutral but sells "perfectly prepared for the Quran" [V]. 8.5x11 [V] |
| 2 | **Alif Baa Tracing and Practice L1** (Reem Djawad) B08BWD616K | Indie | 2020-06-23 | 88 | $7.16 [W13] | 4.7 (850) | 44,700 [W13] (#179 Homeschooling) | Tracing only, **isolated forms only** ("this notebook only focuses on writing the basic alphabet") [V desc] | Kids and adults; secular |
| 3 | **Arabic Letters Practice for beginners** (Arwa Jabrane) B09QFDJLD8 | Indie | 2022-01-12 | 64 | $9.99 | 4.8 (321) | **47,712** (#67 Writing Skill Ref) [V] | Tracing alif to ya; reviewers say "No words" [V] | Kids and adults; secular |
| 4 | **Learning Arabic Workbook for Beginners** (Omar Jabrane) B09WQ2PGXJ | Indie (same family as #3) | 2022-03-27 | 120 | $9.99 | 4.6 (451) | 62,567 [W13] (#55 Alphabet Ref) | Letter forms by position, picture vocabulary with transliteration (tanween shown as "-on"), forms chart on back cover [V reviews] | Kids and adults; MSA, secular |
| 5 | **Learn to Write Arabic: The Alphabet Handwriting Workbook You Can Hear** (Babel Bridge Press) 1962252132 | Blackstone Publications | 2026-08-12 (US) / 5 Sep 2026 (UK) | 147 | $14.95 | 4.9 (38) | 68,230 [W13] (#339 Lang Study) | 28 letters, vowel marks, audio, "21 days" [V title] | Adult total beginners; secular. **Fastest-rising 2026 newcomer** |
| 6 | **Arabic Writing Alphabet Workbook** (Isaac Design) B08DSS7MNM | Indie | 2020-07-30 | 120 | n/a | 4.7 (375) | not shown on page [V] | Tracing; "child-friendly pictures"; numerals 1–10; reviewers: "only covers the general shape" (isolated) [V] | Kids 2+; secular |
| 7 | **Arabic Alphabet for Beginners** (Yasmin Hussein, *Alif to Fluency* bk 1) 1923185063 | Seeds of Ihsaan | 2024-02-16 | 110 | $9.99 | 4.4 US / 4.6 UK (23) | 110,569 [W13] (#100 Alphabet Ref) | 3 pages per letter: shape family, **numbered stroke-order guide**, 4 forms, 3 words with pictures, exercises; audio; **no harakat** (book 2 covers them) [V desc] | Homeschool and adults; desc is secular, imprint name Islamic |
| 8 | **The Complete Arabic Writing Workbook** (Soulayman de Kerdoret) 1735548448 | Madrassa online LLC | 2020-11-29 | 102 | $11.99 | 4.6 (68) | 137,082 (#241 Children's Handwriting) [V] | Lines, isolated, 4 forms, words, sentences, then words with vowels [V desc + review] | Kids 6–10; buyers include reverts [V review] |
| 9 | **Gateway to Arabic: Handwriting Book** (Imran Alawiye) 0954083350 | Anglo-Arabic Graphics | 2003-12-23 | 68 | n/a | 4.8 (218) | 377,663 [V] | Ruq'ah next to Naskh; numbered arrows for direction and stroke sequence; Quran verses to copy [V desc] | Not for absolute starters [V review]; Islamic school market |
| 10 | **Arabic Character Writing For Dummies** 1119475333 | Wiley | 2019-11-05 | 96 | n/a | 4.5 (196) | 701,531 [V] | Letter copying and a few words [V review] | Adults; secular |
| 11 | **Arabic Script Hacking** (Judith Meyer) 1473679699 | Teach Yourself | 2018-12-18 | 128 | n/a | 4.5 (79) | not shown [V] | Recognition and reading algorithm, mnemonics, audio; little handwriting [V review] | Adults and travellers; secular |
| 12 | **The Arabic Alphabet for Kids** (Qaida Series) 1838184953 | Al Qasas Learning | 2022-01-30 | 150 | n/a | 4.9 (20) | 305,863 (#81 Children's Islam) [V] | Colouring, forms, makharij (articulation) diagrams, tracing, Quranic example words [V desc] | Kids; explicitly Islamic/tajweed |
| 13 | **Arabic Alphabet For Kids – Handwriting workbook** (Lina V. Potter) B09QNZV8TG | Indie | 2022-01-19 | 82 | n/a | 4.7 US / 4.4 UK (78–82) | 1,233,254 [V] | Discover, trace, write | Kids 3–6; secular |
| 14 | **Arabic Alphabet Practice Workbook** (Maktabat Atlas) B0DPQPDHKR | Indie | 2024-12-03 | 133 | n/a | 4.3 (10) | 712,004 [V] | 4 pp per letter, all 4 forms, harakat, colouring, transliteration [V desc] | Kids and adults |
| 15 | **Noorani Qaida with Tajweed Rules (Color-Coded)** B0FGQQ16FP | Indie "Al-Noor Publisher" | 2025-07-04 | 34 | n/a | 4.4 (11) | 255,382 (#56 Children's Islam, #136 Quran) [V] | Qaida reading drills, colour tajweed | Religious; kids and adults. A sister title, B0FD2PMB2D (2025-06-10, 72 pp, 4.6 (11)), sits at BSR 1,003,840 [V] |

Other titles from the same searches, for context:
- Goodword (Indian Islamic publisher), UK search: *Learning Arabic Alphabet* (2017, 4.8, 10), *Fun with Arabic Alphabet* wipe-clean (2015, 4.6, 5), *Goodword Arabic Writing Book 2* (2007, 4.2, 39). Goodword is a weak presence in English-market alphabet workbooks. [V UK search]
- **Lingo Mastery has no Arabic alphabet workbook.** Its Arabic title is *Arabic Short Stories for Beginners* (3.7, 127, UK). Its kana workbook ranks at 20,927 BSR [W13], so this is an open slot for them, not a threat today. [V]
- **Learning Roots** did not appear in a UK "learning roots arabic" search; no title was found. [V negative, one search]
- The classic Noorani Qa'idah (Sheikh Noor Mohammad, 0979461901; 4.7, 143 UK, 90% 5-star) dominates the religious Qaida keyword. Its US BSR could not be fetched (captcha).
- Large-publisher course books rank on "learn to read arabic" and "arabic workbook for beginners": Gateway to Arabic Book 1 (4.7, 715), Mastering Arabic Activity Book, Complete Arabic (Teach Yourself), Arabic for Dummies. These are courses, not script workbooks.

**What the map shows**
- Demand is moderate. The best English-language Arabic script workbooks sit around **US BSR 43k–68k** [V/W13]. Comparable script workbooks do better: Korean *One and Only* by the same brand at **8,916**, Tuttle Hiragana/Katakana at 16,886, Lingo Mastery kana at 20,927 [W13]. Arabic is roughly a third to a fifth of the Hangul or kana demand per top title [A, BSR-based].
- Incumbents are low-content tracers with many reviews (850, 451, 375, 321). Their strength is age and reviews, not quality.
- The only premium-structured indie hit is *One and Only* ($14.95, 138 pp, audio app). Its Japanese and Korean siblings show that the brand runs a script series template [W13].
- Format: almost every title is **8.5x11 paperback** [V dims]. Colour versus B&W is mostly not stated. Isaac Design and Maktabat Atlas mention pictures or colouring; one Saudi reviewer of Shine Bright faults it for "not in colour". Seeds of Ihsaan's listing says "BLACK & WHITE INTERIOR COLOR EDITION AVAILABLE". B&W dominates, judging by the $7–10 price points [A].

## 2. Newcomers, 2025–26

The UK search "arabic alphabet workbook" sorted by publication date (pages 1–5) [V]:
- **2026 (1 Jan–5 Oct): about 43 new titles** (15 on page 1, 15 on page 2, 13 on page 3). **About 13 of them appeared in a single month (5 Sep–5 Oct 2026)**.
- 2025: about 20 titles. 2024: about 13 titles.
- These are lower bounds. One keyword and one marketplace only, and the counts are approximate because page boundaries overlap.
- Almost all 2026 newcomers have **0 ratings**. Exceptions: Babel Bridge (38 ratings, 4.9, BSR 68k), *Arabic Letters Made Easy* (1), *My First Arabic Sight Words* (3), ZebZeb (2 ratings, **3.0**). [V]
- The newcomers' titles now copy the incumbents' complaint list: *"Alif Baa Right to Left"* (Daftar Co, 30 Sep 2026), *"...with Stroke Order"* (MNMA Books), *"Arabic Alphabet & Handwriting Workbook for Adults ... Connecting Letters"* (Mira Alif), *"Tracing, Harakat, Joining Letters, First Words and Sentences – 5 Levels in One"* (Sidra Mohamed, 4 Oct 2026). Feature differentiation alone is closing fast. [V]
- Creative Fabrica sells an "Arabic Handwriting Workbook KDP Interior" template [V search snippet]. This explains part of the flood.

**Spread or one hit?** It is one hit per year:
- 2025: *One and Only* (186 ratings, BSR 43k). The Noorani Qaida colour editions reached about 11 ratings each, with BSRs from 255k to 1.0M.
- 2026: Babel Bridge (38 ratings, BSR 68k).
- Everything else is invisible.
The pattern is a few winners plus a long tail with zero reviews [V].

**Seasonality [A, not measured; no BSR history was available]:**
- A **back-to-school spike (Aug–Sep)** fits the September 2026 publishing burst and the homeschool and weekend-madrasa buyers in reviews.
- **Ramadan** is likely a second peak for the Islamic-framed and Qaida titles. Ramadan 2027 should begin around early-to-mid February [A, approximate]. Publishers Weekly reported a "Ramadan Book Sales Boom" in 2019 [V headline only].
- Adult and secular demand is probably flatter, with a New Year bump [A].

## 3. Reader complaints and praise (verified quotes)

All quotes come from Amazon review sections on amazon.co.uk and amazon.com.au product pages, which show global reviews. The reviewer's country is listed. Full list: `arabic/quotes.txt`.

**A. Left-to-right binding and page direction: the most frequent complaint (6 separate reviews on 5 books)**
1. Alif Baa Tracing, 1★ UK 2025: "Left binding - incorrect … This book is supposed to be bound on the right hand side as Arabic is written right to left."
2. Arwa Jabrane, 5★ UK 2024: "This product needs re-editing as for Arabic it needs to start from right to left."
3. Lina V. Potter, 3★ US 2023: "This book is in the direction of left to right and Arabic is right to left so the book should be too, this is going to confuse children … I'm considering on returning it"
4. Lina V. Potter, 5★ SE 2025: "But the pages should be Right to left, currently aligned like English"
5. Alif Baa Taa (Arabic Handwriting Book), 1★ US 2024: "You guys had the book started from left to right … that could confuse the students"
6. Maktabat Atlas, 1★ US 2025, "Major mistake": "i dont know why they started it from the keft side … Its a major mistake the author has made."

**B. Accuracy, "AI", and errors**
7. Arwa Jabrane, 2★ NL 2024: "Seems Ai-generated. A lot of letters are skipped in writing or are double. The spaces to write are also very large …"
8. 4-in-1 Arabic learning, 3★ US 2023: "small mistakes in arabic pics name they were not written properly for kids to try to read them"
9. Shine Bright, 2★ UAE 2025: "It doesn't include any diacritical marks … Some of the letters look okay, but they're not written the way native speakers actually write."
10. Arabic Script Hacking, 4★ NL 2026: "toward the end I don't think the publisher edited it that well … the end-of-lesson review will indicate that you have already learned letters like ز" (sequencing error)

**C. Isolated forms only, too basic**
11. Isaac Design, 3★ UK 2022: "only covers the general shape of the letters … You will therefore need another book to practise writing the letter when it occurs in different positions in a word."
12. Isaac Design, 1★ DE 2023: "only one type of way of writing the Arabic letters. Not much help"
13. Dummies, 1★ UK 2020: "This pamphlet merely gives you the letters to copy and a few words."
14. Madrassa online, 5★ UK 2025: "too many pages for single letters of the alphabet. Very few pages for more advanced stage … like words and sentences."

**D. Harakat and diacritics missing or late**
15. Gengo Workbooks, 4★ US 2026: "Books needs fatha, damma, kasra and pronunciations of each to be complete, not just explanation."
16. Goodword Writing Book 2, 5★ IN 2018: "It is missing the 'dhabt' (fathah/kasrah/dammah) for words." (reviewer wrote "father/kesr/dumm")
17. A desertcart review (via WebSearch summary, not fetched directly) of an unnamed workbook: diacritics explained only "2/3s through the book, and leaves them off most". [partially V]

**E. Stroke order and direction**
18. Arwa Jabrane, 5★ AU 2025: "Wish it had numbered arrows for pen strokes as I was writing in the wrong order sone times."
19. A TES tracing-sheet review (via WebSearch summary): "no information for a complete beginner as to the direction of writing each letter". [partially V]
20. Arabic Script Hacking, 3★ UK 2020: "It also doesn't actually explain on how to do the writing" and "listening icons … I can't find if there are resources to download"

**F. Transliteration and dialect**
21. Omar Jabrane, 4★ UK 2025: "Why the 'on' at the end of every word?" (tanween shown in transliteration and never explained)
22. Omar Jabrane, 5★ CA 2025: "This is modern standard university arabic so some words would never be commonly used, especially in egyptian dialect"

**G. Space, size, format**
23. Madrassa online, 3★ US 2023: "Font size is really tiny to practice."
24. Yasmin Hussein, 5★ US 2025: "Only thing that would make it better was if there was an entire page to practice for each letter position. Also spiral notebook would really good."
25. Alif Baa Tracing, 4★ UK 2022: "it's not wipe and clean as it thought". A 5★ CA 2026 reviewer: "Cut every page and put them into transparent sheets"

**H. Wrong level for the buyer**
26. Omar Jabrane, 3★ UK 2024: "more of a dictionary of items and animals, with basic writing practice"
27. Omar Jabrane, 2★ UK 2024: "definitely not for beginner level"
28. Gateway Handwriting, 3★ UK 2010: "It's meant to teach you a Ruq'ah script after you learnt the Naskh script."

**Praise: what earns 5★**
- **Positional forms explained and practised**:
  - "explains in amazing detail how the letters are written based on their placement within a word and why they change" (*One and Only*, CA 2026)
  - "shows the letters in all their forms and then how to join them … most of the other books only give the letters in isolated form" (Gateway, UK)
- **Audio for every word**: "permits the student to listen to the pronunciation of EVERY WORD" (*One and Only*, CA 2025, a native speaker who checked the book)
- **A full progression** from letters to forms to words to vowelled words (Madrassa online, CA 2022)
- **Pairing with Duolingo or apps**: "the ideal supplement" (Dummies, UK 2024; *One and Only*)
- **Revert and convert buyers**: "As a revert Muslim … I want to learn Arabic InshaAllah to be able to read the Quran" (Madrassa online, US 2025)

**Shaping errors (disconnected or reversed letters).** No Amazon review in this sample named them explicitly. Review #9 ("not written the way native speakers actually write") and #7 (skipped or doubled letters) are the closest. The failure mode is widely documented for software without a shaping engine: Photoshop, Figma, older wkhtmltopdf and Canva-like tools produce "detached, reversed characters" (textarabi.com 2026; dev.to 2026; learntype.app 2026 [V snippets]). It is a real risk for template and AI-tool publishers, and an easy one to eliminate with code.

## 4. Accuracy without a human checker

**What can be machine-verified [V/A]:**
- **Letter inventory and contextual forms.**
  - Unicode `ArabicShaping.txt` (v18.0.0, fetched [V]) gives each letter's Joining_Type: dual-joining or right-joining. From it, code can derive which letters have 4 forms and which have 2 (the 6 non-connectors ا د ذ ر ز و) and generate every form table.
  - The Arabic Presentation Forms-B code points (FE70–FEFF) give a canonical isolated, final, initial or medial glyph for each letter. These can serve as a test oracle.
- **Correct shaping in the actual print font.** HarfBuzz (uharfbuzz) was run on DejaVu Sans [V, local test `arabic/poc/shape.py`]:
  - بيت became init-beh FE91, medi-yeh FEF4 and fina-teh FE96, run RTL.
  - كتاب became init-kaf FEDB, medi-teh FE98, fina-alef FE8E and isolated beh 0628, which correctly breaks after alef.
  - لا became the lam-alef ligature FEFB.
  - مُحَمَّد came out with shadda and fatha composed.
  - With the joining features switched off, every letter came out isolated and in logical order. That is exactly the broken output template tools print.
  - A build step can therefore assert, for every word printed, that the glyph sequence equals the expected positional forms. For fonts like Amiri, whose glyph names differ, compare against the GSUB mapping or rasterise and diff against a Presentation-Forms reference [A].
  - Check that the PDF embeds the font and stores text as shaped glyphs. KDP accepts PDF for English-language books [V KDP].
- **Open fonts.**
  - Amiri: OFL-1.1 [V GitHub].
  - Scheherazade New (SIL) and Noto Naskh Arabic: OFL [A; well known, not re-fetched].
  - A Nastaliq font such as Noto Nastaliq Urdu would be needed for an Urdu sequel [A].
- **Vocalisation of vocabulary.**
  - Use a fully vocalised source and check consistency in code: Arabic Wiktionary via kaikki.org/wiktextract (CC BY-SA [A: standard Wiktionary licence]) has vocalised headwords plus English glosses.
  - The Tashkeela corpus (Zerrouki 2017) holds 75M+ words of vocalised text [V paper title; licence not verified].
  - Cross-check each word's diacritics across two sources and drop disagreements [A].
  - Code-check structural rules: no sukun on the final letter of a pausal form, one shadda maximum per consonant, tanween only word-final, alif after fathatan where required, and taa marbuta only word-final.
- **Transliteration.** Generate it deterministically from the vocalised Arabic with a fixed table (simplified ALA-LC or DIN 31635, or a learner scheme without diacritics). Decide on a pausal versus full-tanween policy up front; the "-on" complaint shows why. Code makes it 100% consistent [A].
- **Exercise integrity.** Code can guarantee no skipped or duplicated letters (the "Seems Ai-generated" complaint), correct answer keys, and recap pages that only use letters already taught (the Script Hacking complaint). This is all deterministic.

**What needs care (no machine guarantee):**
- **Meanings.** English glosses are the main residual risk. Keep vocabulary to concrete, picturable, high-frequency MSA nouns where Wiktionary and a second source agree. Avoid polysemous and dialect-sensitive words [A].
- **MSA versus dialect.** State "Modern Standard Arabic (Fuṣḥā)" clearly. Spoken-dialect buyers (Egyptian, Levantine, Darija) will find some words unusual; review #22 shows this is tolerated when disclosed [V/A].
- **Quranic text.**
  - If used at all, take it from **Tanzil**. Its licence (CC BY 3.0) allows "verbatim copies" only: "CHANGING IT IS NOT ALLOWED", with attribution and a link required [V tanzil.net].
  - Byte-compare against the downloaded file.
  - Note that Tanzil's Uthmani text uses Quranic marks (small high letters, alif khanjariyya, special waqf signs) that common Naskh fonts may not render well. Use a font built for it (e.g. KFGQPC or Amiri Quran [A]) and test-render every glyph.
  - Safer: **avoid ayat entirely** and use only common Quranic vocabulary words, such as the Qaida-style "Quranic words" lists, sourced and vocalised the same way [A].
- **Religious sensitivity** [A]:
  - Avoid images of living beings for Islamic-framed kids' editions; some buyers object, and many Islamic publishers use objects instead.
  - Never place the name of Allah or verses where they might be discarded or traced over carelessly; tracing pages are written on and thrown away.
  - Use respectful terminology.
  - A secular edition can use animals freely.
- **Stroke order and direction: there is no authoritative open dataset.**
  - The AOLAH database (Aswan University, IEEE DataPort) has online handwriting samples from 90 writers and **17 stroke classes**. It is research data in unrestricted styles, free for academic use, and needs a login [V]. It is not a pedagogical standard.
  - Published workbooks (Gateway, Seeds of Ihsaan, Madrassa online) use numbered arrows, but conventions vary between Naskh school traditions and Ruq'ah [V descriptions].
  - Practical approach: encode a small set of conservative rules by hand. Write right to left. Write the main body (rasm) first and dots and harakat afterwards. Draw the alif top-down. Loops (و م ف ق) clockwise as conventionally taught. Draw the kaf's top stroke first [A, from common teaching practice, not verified against a standard].
  - Present arrows as "suggested" rather than mandatory. Keep the number of arrowed variants minimal: the 18 basic skeleton shapes (rasm groups), since dots don't change the stroke.
  - **This is the single biggest accuracy risk without a human checker.**

## 5. Binding direction, and secular versus Islamic framing

**KDP RTL support [V, KDP Help "Paperback Submission Guidelines" and "Book Supported Languages", fetched 2026-10-15]:**
- "For most languages, KDP only supports books formatted to read from left to right (LTR). Currently, we only support right-to-left (RTL) paperback printing in **Hebrew, Yiddish and Japanese**."
- **Arabic is "eBook only"** on KDP. Persian is eBook only. Urdu is not listed.
- "Standard color distribution for RTL paperbacks is limited to Amazon.co.jp."

So an English-language Arabic workbook **must be LTR-bound on KDP**. That is the source of complaint cluster A, and it cannot be fixed on KDP. IngramSpark's File Creation Guide mentions RTL covers with "back and front covers … reversed" [V snippet only; not checked in detail], but that would sit outside Amazon's POD.

Mitigations [A]:
1. Put a short note opposite the title page: "Why this book opens like an English book". It explains that the instructions are in English, while every Arabic line and exercise runs right to left and starts at the right margin. This turns a 1★ trigger into a teaching moment.
2. Design every page so it is self-contained right-to-left. Tracing rows start at the right edge with a ▶ start marker on the right, and no exercise continues across a spread.
3. Optionally, an "Arabic order" page index read from the back.
4. Say "opens left-to-right (English binding)" in the description bullets, so expectations are set before purchase.

**Secular versus Islamic framing.** No sales split could be measured; this is evidence from rankings and reviews:
- The best-selling titles are **secular or neutral in their listings**: Alif Baa Tracing, the Jabrane books, Isaac Design, Babel Bridge. *One and Only* is neutral but adds a Quran-prep bullet and sits at **#14 in Quran**, so it gets both audiences [V].
- Reviews show buyers from both sides. Muslim families and reverts write "Alhamdulillah", "MashaAllah", "my son had his class". Secular adult hobbyists mention Duolingo, "language enthusiast" and a "57 years old" self-learner [V].
- Explicitly Islamic or Qaida titles rank lower in this sample: Al Qasas 306k, Noorani colour editions 255k–1.0M, Gateway Handwriting 378k. The traditional Noorani Qa'idah (143 ratings) and madrasa-issued books probably dominate that buying, much of it outside Amazon [A].
- Inference [A]: the Muslim-family and revert segment is the larger volume driver; secular adults and travellers are a real but smaller segment. Neutral MSA content with an opt-in Quranic-script bridge captures both; an overtly religious cover narrows the audience to buyers who already have the Qaida.

## 6. Best format, angle for 4.5★+, series potential

**Recommended product [A, built from the complaint and praise clusters]:**
- **Adult and teen self-learner edition first**: 8.5x11, B&W, about 160–200 pp, $12.99–14.99. That is the *One and Only* price, and the band where the premium-structured titles sell.
- **Sequence:**
  1. Letters in rasm families with stroke arrows.
  2. Each letter in all 4 forms, with **a full practice row per position** (answers review #24).
  3. Joining drills, with non-connector breaks generated by code.
  4. Harakat (fatha, kasra, damma), sukun, shadda, tanween and long vowels/madd, **introduced early, not two-thirds in**.
  5. Decodable reading ladders: vocalised syllables, then words, then short phrases, using only letters already taught (code-checked).
  6. Taa marbuta, hamza seats, alif maqsura, lam-alef and al- (sun/moon letters).
  7. Naskh-to-handwriting note (a Ruq'ah preview only).
- **Supporting material**: a back-cover forms chart (praised in review), an answer key, a deterministic transliteration key, and a clear statement that the content is MSA.
- **Audio**: competitors with audio get praised for it. Either skip audio and say "pairs with any free audio alphabet course", or generate audio with care. TTS is a risk without a checker [A].
- **Kids edition second** (ages 5–8, larger guides, objects instead of animals in the Islamic-friendly version), built from the same engine.
- **Accuracy pipeline** (all code): HarfBuzz shaping asserts on every printed string, embedded OFL font, a vocabulary whitelist with cross-source vocalisation agreement, sequence and coverage tests, and no Quranic verses (or Tanzil verbatim with a byte compare).

**Series potential [V/A]:**
- Proven: the "One and Only" brand runs Japanese (BSR 31k), Korean (**8.9k**) and Arabic (43k) as one template [W13/V]. The same engine approach transfers.
- Arabic-script sequels (Urdu, Persian) reuse about 70% of the engine; only Nastaliq versus Naskh and extra letters (پ چ ژ گ for Persian; ٹ ڈ ڑ ں ے ھ for Urdu) change. UK searches show thin, low-quality and also newly flooded shelves (several Oct 2026 Persian and Urdu tracers) [V]. Demand per title is likely below Arabic [A]. Urdu Nastaliq shaping is harder; test with HarfBuzz.
- A Hangul, kana or Devanagari line has higher demand, kana and Hangul especially [W13]. Hangul composition and kana stroke order have authoritative open data (KanjiVG covers kana; Hangul stroke conventions are standardised) [A: KanjiVG known to include kana, not re-verified here]. That is a better accuracy story than Arabic stroke order.

---

## Scores (10 = best for the publisher)

| Criterion | Score | Basis |
|---|---|---|
| Demand | **6** | Top titles at US BSR 43k–68k [V/W13]; about a third to a fifth of the Hangul/kana equivalents [A] |
| Competition (10 = easy) | **4** | Entrenched tracers with 320–850 ratings at 4.6–4.8, a strong 2025 adult hit, and **about 43 newcomers in 2026, with 13 in the last month** now copying the gap features (RTL, stroke order, joining, harakat) [V] |
| AI-hunt immunity | **8** | Content is generated tables, forms, tracing and drills with almost no prose. The one "Seems Ai-generated" review was triggered by skipped or duplicate letters, which code prevents [V/A] |
| Accuracy risk without a human checker (10 = low) | **6** | Shaping, forms, sequencing and transliteration consistency can be machine-verified [V test]. Glosses and vocalisation need dual-source agreement. Stroke order has no authoritative dataset. Quranic text should be avoided or used verbatim from Tanzil [V licence] |
| Fit as high-content | **8** | A 160–200 page structured workbook is natural; buyers reward progression and penalise "pamphlet" tracers [V reviews] |

**Best angle (one line):** An adult self-learner Arabic script workbook built by a shaping-verified engine. It gives every letter in all 4 forms with numbered stroke arrows and a practice row per position, introduces harakat, sukun, shadda and tanween early, and ends with decodable vocalised reading ladders. It is MSA, neutral with an optional Quranic-words bridge, and says upfront why the book opens left-to-right.

**Biggest risk:** Saturation plus a binding KDP cannot fix. About 43 new 2026 titles are already copying the gap features, LTR binding draws recurring 1★ reviews, and suggested stroke order has no authoritative source to check against.

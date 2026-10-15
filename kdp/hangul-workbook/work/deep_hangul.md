# Deep dive: Korean Hangul writing/reading workbooks (KDP), as of 15 Oct 2026

Tags: **[V]** means I checked it myself (an Amazon page fetched today or in the W13 run, a page I read, or code I ran). **[A]** means it is an assumption or my own judgement. "n/c" means not captured, usually because Amazon US returned a captcha or 503.

Raw notes are in `/tmp/claude-0/-home-user-course/5d910e26-d220-53df-b12b-0c4e5f61c868/scratchpad/wide2/hangul/`: `manual.txt` holds the product data, `quotes.txt` the review quotes, and `s*.json`/`rev*.json` the raw fetches.

Search coverage: I captured US Books-store result pages (`rh=n:283155`) for 6 of the 7 queries: "korean hangul workbook" (from the W13 run), "learn korean alphabet", "korean workbook for beginners", "hangul for kids", "korean writing practice book" and "learn korean for kids book". **"korean handwriting practice" returned 503 on 5 retries.** Its likely results are covered by "korean writing practice book", which lists the same handwriting titles.

---

## 1. Market map

### 1a. Top 15 distinct Hangul-focused titles, ordered by US BSR

| # | Title (ASIN) | Publisher type | Pub date | Pages / trim | Price (US) | Rating (n) | US BSR | Content type | Colour | Audience |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **The One and Only Korean Workbook** (B0DZH81KXL) | Indie brand "Self-taught KOR" (sister imprint "Self-taught AR" [V]; the Japanese title in the same template is credited to "Hikaru Tamaki", so probably the same publisher [A]) | 2025-03-03 | 170, 8.5x11 | $15.71 (list $16.95) | 4.7 (223) | **8,916** [V]: #1 Children's Korean Language, #1 South Korea Travel Guides, #10 Foreign Language Instruction | Teaching plus tracing plus syllables, words and sentences, plus online videos and a Quizlet deck | n/c (one reviewer says "like an old school workbook") | Teen/adult (Amazon shows "14+ years, from customers") |
| 2 | Korean for K-Pop Fans (B0DFCDTD7Y) | Indie "Hallyu Press" (publisher field: "Self") | 2024-08-26 | 172, 6x9 | $19.99 | 4.6 (253) | 36,714 [V] (#2 Children's Korean) | Hangul plus grammar plus pronunciation course with K-pop framing and audio. Not a writing workbook | n/c | K-pop fans, teens |
| 3 | Korean Practice Notebook: Hangul Workbook (B08XH2JRVZ) | Indie "JW Publishing" | 2021-02-27 | 122, 8.5x11 | $7.95 | 4.8 (171) | 51,842 [V] | Probably a practice-grid notebook [A, interior not seen] | n/c | General |
| 4 | Korean Alphabet, Korean Hangul Writing Workbook (B09V6B1YF6), R.E. Jong Korean | Indie | 2022-03-07 | 111, A4 | $7.99 | 4.6 (465) | 63,165 [V] | Teaching-lite plus tracing: 40 jamo, syllable-placement rules with answers, 294 CV combinations, two number systems, 80 words, 5 scrambles | B&W [A] | Beginners of all ages |
| 5 | Learn Korean: The Language Workbook for Beginners (1838291644), Jennie Lee / Polyscholar | Small press MAR+LOWE | 2021-03-05 | 152, 8.5x11 | $19.49 pb / $27.49 hc | 4.6 (1,159) | 69,066 [V] | Teaching plus stroke order plus 48 cut-out flashcards, 4 quizzes, 15+ vocabulary pages, pronunciation rules | n/c | "15+ years" |
| 6 | Easy Learning Fundamental Korean Writing Practice Book (B075YRYJPG), Fandom Media | Korean small press (New Ampersand) | 2017-09-26 | 97, 8.5x11 | $12.99 | 4.6 (1,243) | 83,102 [V] | Alphabet, syllable, vocabulary and sentence writing. Publisher's own comparison table lists audio as "no data" | n/c | Beginners |
| 7 | Fun Start Korean Hangul Worksheets for Kids (B09L4YY1SR), Stellarsol | Indie | 2021-11-05 | 72, 8.5x11 | $14.77 | 4.8 (62) | 88,460 [V, W13] | Pure tracing worksheets: 14 consonants, 10 vowels | **Full colour** [V] | Preschool |
| 8 | Easy Way to Learn Korean Alphabet: Lil's Pirates (1737752409) | Small press | 2021-08-13 | 40, 8.5x11 | $7.99 | 4.8 (38) | 170,278 [V] | Tracing plus colouring | Colour [V] | Ages 5-11 |
| 9 | Korean Alphabet Made Easy (1951949706), Lingo Mastery | Indie brand | 2023-04-18 | 344, 8.5x11 | $14.97 | US n/c; UK 4.4 (134); AU 123 ratings | 194,683 [V] | Teaching plus stroke-order blocks plus images plus audio exercises | n/c | All ages |
| 10 | Korean Hangul Writing Workbook (B08VVHJPB8), Lilas Lingvo | Indie | 2021-02-03 | 144, 8.5x11 | from $5.37 | 4.7 (1,123) | 263,244 [V] (UK 27,807) | Crash course plus syllable practice plus 200+ words and phrases plus cut-out flashcards, photocopiable | n/c | Beginners |
| 11 | Korean Handwriting: Consonants & Vowels (B0CGTWSYNZ), Gooseapple | Small press | 2023-08-23 | 210, A4 | $16.99 | 4.7 (94) | 324,577 [V] | Stroke order plus "Standard / Handwritten / Lazy" style variants of every letter | n/c | Intermediate writers |
| 12 | Korean Language Writing Practice Book (0804853282) | **Tuttle** | 2020-12-29 | 128, 8.5x11 | from $2.72 | 4.7 (40) | 342,474 [V] | Mostly blank grid and lined paper with a 10-page reference section and online audio | n/c | Students |
| 13 | Fun Start Korean Workbook for Kids 1 (B098GY3WTN), Stellarsol | Indie | 2021-07-01 | 142 | $15.66 | 4.7 (57) | 382,893 [V] | Activities (colouring, search, tracing, cut-and-paste) plus MP3 audio | n/c (colour likely) | Kids |
| 14 | Unlocking Hangul (1069133108), Korean Study Cafe | Small press | 2023-11-30 | 191, 8.5x11 | n/c | 4.9 (69) | 601,966 [V] | Teaching plus pronunciation patterns plus quizzes plus culture, with QR links to audio, 6 mouth-shape videos and flashcards | **Full colour** [V] | Youth/adults ("Not recommended for children") |
| 15 | Korean Alphabet with Writing Workbook Vol.1 (1974152626), Dahye Go | Indie (CreateSpace) | 2018-02-08 | 117, 8.5x11 | $9.99 | **4.7 (2,029 global)** | US n/c (blocked 6 times). CA 231,580; UK 436,215; AU 102,347 [V] | Letter formation plus 4 vocabulary words per letter with pictures plus a test per letter. No audio | n/c | Beginners |

Other titles of interest:
- Dream Bisang Vol.1 (B095GD5NS9): 4.7 (152), BSR 1,045,569 [V].
- Clever Cookie "Korean Workbook for Kids" (B0CN4RHLNM): 4.5 (12). Its spec matches #4 exactly (21 vowels, 19 consonants, 294 combinations, 15 numbers, 80 words, 5 scrambles), so it is a reused template [V].
- Tuttle "Korean Hangul Writing Practice Workbook" (0804855609): US n/c; UK BSR 698,230, 16 ratings.
- Tuttle "Reading and Writing Korean" (0804853088): UK 62 ratings.
- TTMIK *Hangeul Master*: Kindle edition UK 139 ratings, rated 86% 5-star; paperback US n/c.
- Blank Hangul manuscript notebooks, e.g. B08CPNPLXG: 4.8 (137), BSR 1,065,905.

**Big publishers** [V]:
- **Darakwon** did not appear in any of the 6 Hangul searches. Only its grammar title *Korean Grammar in Use* shows up, under "korean workbook for beginners".
- **TTMIK** appears with *Talk To Me In Korean Level 1* (4,918 ratings, in the "also bought" carousels) and *My First Writing Practice in Korean* (4.5 (12), BSR 1,018,542). *Hangeul Master* did not rank in the searches.
- **Tuttle** has three Hangul titles. All sit at BSR 340k or worse in the US/UK.
- **The niche is led by indie and brand-indie publishers**: Self-taught KOR, Lingo Mastery, Polyscholar, Fandom Media, Lilas Lingvo, Dahye Go.

### 1b. The 2025 indie at BSR ~8.9k: *The One and Only Korean Workbook* (Self-taught KOR) [V]

- **Rank and placement.**
  - US BSR 8,916, 4.7 from 223 ratings.
  - UK page shows 144 global ratings, distributed 84/10/3/1/2 (5 to 1 star). CA BSR 18,841.
  - Amazon's "Customers say" summary: 28 reviews mention content, all 28 positive.
  - It holds organic #1 for "learn korean alphabet", "korean workbook for beginners" and "korean writing practice book".
  - It is also **the sponsored #1** for "korean hangul workbook" and "hangul for kids". The publisher clearly runs ads.
- **What the listing says it contains:**
  - A 30-page introduction to Korean.
  - "100+ pages of writing exercises that build on each other".
  - 140 basic-syllable exercises, 40 simple-word exercises and 10 sentence exercises, described as "over 400 writing exercises".
  - "Pronunciation aid using German example words" (sic; the brand appears to be German-origin [A]).
  - Linked YouTube videos and a free Quizlet deck of 360+ flashcards with audio.
- **What reviewers praise:**
  - It works as a structured course rather than a tracing pad.
  - Stroke-order breakdown.
  - "dyslexia-friendly" font.
  - "plenty of space for practise", "good quality" paper, and a blank page to photocopy.
  - The videos and Quizlet for pronunciation.
- **What reviewers criticise:**
  - The Quizlet QR "kept getting stuck on the loading page".
  - "text on some pages shifted slightly along the edge".
  - Not worth it for anyone past absolute beginner.
- **Why it wins:**
  1. It runs as a course, not a tracing pad.
  2. Free digital audio is bolted on.
  3. It belongs to a brand ecosystem: the same brand sells *Your First 840 Words in Korean* (BSR 40,296, 2025), *Your First 100 Sentences* (81,276, 2025) and *The Only Book You Need to Learn Korean 3-in-1* (16,967, Mar 2026). Titles in the same template (very likely the same publisher [A]) sell *One and Only Japanese* (W13: BSR 31,068, 331 ratings) and *One and Only Arabic* (W13: 43,189, 186 ratings).
  4. It advertises.

### 1c. Structure of the niche [V data, A interpretation]
- **Content types:**
  - Pure tracing for kids (Stellarsol, Lil's Pirates, Mia Yoo).
  - Mostly blank grid notebooks (Tuttle Studio, Pretty Handy, JW [A]).
  - Writing workbooks with a short guide (R.E. Jong, Lilas, Dahye Go, Fandom).
  - Courses with workbook elements (One and Only, Jennie Lee, Lingo Mastery, Unlocking Hangul).
- The **course** type holds the best BSR and is the only one with 2025-26 momentum.
- **Price band:** $7.95 to $19.99 for 100-200 page 8.5x11 paperbacks. The leader sits at about $16.
- **Colour:** only the kids' titles and Unlocking Hangul are confirmed full colour. The adult leaders appear to be B&W [A].
- **Review moats:** four titles have 1,100 to 2,000+ ratings (Dahye Go, Fandom, Jennie Lee, Lilas), but none ranks better than BSR 63k in the US. Old review counts are not translating into current sales.

---

## 2. Newcomers (2025-26)

| Title | Pub date | Rating (n) | BSR | Note |
|---|---|---|---|---|
| One and Only Korean Workbook | 2025-03 | 4.7 (223) | **8,916** | The hit |
| Your First 840 Words in Korean (same brand) | 2025-03 | 4.7 (89) | 40,296 | Brand halo |
| Your First 100 Sentences in Korean (same brand) | 2025-09 | 4.6 (31) | 81,276 | Brand halo |
| The Only Book You Need to Learn Korean 3-in-1 (same brand) | 2026-03 | 4.8 (269) | 16,967 | Omnibus at $39 |
| Squid Hangul Series 1 (Seong Jaehong) | 2025-07 | 4.8 (5) | n/c | Geometric "circle-triangle-square" angle |
| SquidHangul Series 2 (sound-change rules) | 2025-11 | none | 3,396,047 | Covers sound-change rules; no traction |
| Korean Alphabet for Beginners (Jamsil Publishing) | 2026-05 | 5.0 (5) | 791,064 | |
| Learn Korean Hangul Through Korean Food for Kids (Mia Yoo, book 2 of 5) | 2026-06 | none | 940,268 | 33 pages |
| Read Korean in 18 Easy Lessons (SunHee Jung) | 2026-09 | none | 994,267 | 6 weeks old; heritage-teacher author; answer key |
| Korean Words Writing Book for Kids L2 | 2026-02 | none | UK 600,278 | |
| My First 400 Korean Words (book 18 of a 32-language series) | 2025-10 | 3.3 (3) | UK 1,883,392 | Templated multi-language series doing poorly |
| My Little Hangul Book: Puppy | 2026-09 | none | n/c | |
| Korean Practice Notebook (Pixie) | 2025-10 | 5.0 (1) | n/c | |
| Hangul Alphabet Master (Kindle) | 2026-08 | none | Kindle 1,359,337 | |

**Verdict [A, based on the data above]: this is one hit plus its brand halo, not broad demand.** Since 2025, every Hangul newcomer outside the Self-taught KOR ecosystem sits at BSR 600k or worse with 5 or fewer ratings. The only other new book with real sales is the K-pop-framed *Korean for K-Pop Fans* (Aug 2024, BSR 36,714). Rough reading: one strong course-style title can sell well here, while undifferentiated tracing books and kids' books do not.

---

## 3. What readers complain about and praise
Every quote below was seen today. Sources are Amazon UK/CA/AU product pages (which show reviews from several countries), Amazon's own "Customers say" summaries, and Reddit r/Korean. Full list with dates: `hangul/quotes.txt`.

**No audio / can't hear pronunciation (the most common complaint):**
1. Dahye Go, 4 stars, UK 2023: "I realise I must also be able to HEAR the pronunciation which doesn't help with this book."
2. Jennie Lee, 4 stars, UK 2023: "if it was accompanied by audio would be even better… it should include the alphabet in alphabetical order which it doesn't."
3. Jennie Lee, 3 stars, Brazil 2024 (Portuguese): "seria necessário um áudio pra treino de pronúncia" ("audio would be needed for pronunciation practice").
4. Tuttle *Reading and Writing Korean*, 4 stars, UK 2022: "be careful with batchim - there is no corresponding audio file for that… I noticed some errors in the printing."
5. Reddit r/Korean, "Error in Hangeul Master?" (2023): "it says ㅓ is sounds like: 'u' as in 'bus' or 'gut'… I find myself not trusting this book". Replies: "I'm Australian, and I totally agree that 어 sounds nothing like bus or gut in my accent", and "it might be the best you could do, but I hope it includes sound files as well."
6. Unlocking Hangul, 4 stars, UK 2025: "not everyone is familiar with the IPA symbol… It is better to compare it to a word in English."

**Typos, errors and wrong content:**
7. Lilas Lingvo, 4 stars, UK 2021: "There is a worrying amount of English typos in it though."
8. Dream Bisang, 2 stars, Saudi Arabia 2024 (Arabic, my translation): "There are many errors, and the words are not really words - most are just sound expressions like 'wow'… the exercises are repeated for all letters."
9. Jennie Lee: an Amazon US video review is titled "I think there's a mistake."
10. Fandom Media, Amazon "Customers say": "several customers mentioning odd translations and phrases".
11. Stellarsol *Fun Start 1*, 2 stars, US 2022: "This book isnt written by someone who has taught korean before. They use complex words over easy ones… the answers are all written in Romaji."

**Romanisation crutch:**
12. Stellarsol *Fun Start 1*, 4 stars, US 2023: "I wish there wasn't so much romanization… I also feel them rely on it too much."
13. TTMIK *Hangeul Master*, 5 stars: "you can't rely on romanization… as often doesn't match how you say the words."

**Thin instruction, blank-paper padding, value:**
14. Tuttle *Korean Hangul Writing Practice Workbook*, 1 star, India 2026: "it has excercises only for few pages, rest all is blank notebook. A waste of money." (UK distribution 64/20/8/0/8)
15. Dream Bisang, 3 stars, Belgium 2023: "very few instructions in it, very hard for beginners to understand."
16. Dahye Go, "Customers say": "several customers wishing for more instructional guidance… some customers feeling they wasted their money."
17. Stellarsol *Worksheets*, 5 stars but critical, US 2022: "This is very basic level. A few practice opportunities for each letter and a few words… it also doesn't get me further."
18. One and Only, 4 stars, UK 2025: "if you already know a basic level of Korean this won't teach you anything more."
19. Clever Cookie, 3 stars, US 2024: "Since I do not speak Korean, I found the workbook a little trying."

**Companion-tech friction:**
20. One and Only, UK 2025: "trouble getting the Quizlet QR code to work"; "text on some pages shifted slightly along the edge."
21. Unlocking Hangul, UK 2024: "I have a problem opening the files."

**Doubt that a book is needed at all:**
22. Reddit r/Korean (2020): "TBQH you can learn hangeul with a few YouTube videos and practice writing with some graph paper"; "It will take like an hour."
23. Korean Explorer (Singapore blog, Aug 2026): "a beginner who only ever traces syllables from one thick book often develops accurate shapes and zero ability to read a handwritten note."

**Praise patterns:**
- "stand-alone guide (you don't need to go online…)" (Dahye Go, 5 stars).
- "plenty of space for practise" and good paper (One and Only).
- Flashcards and photocopiable pages (Lilas: "They designed the pages so you can copy them").
- Clear stroke directions and "different fonts" (Jennie Lee).
- Learning real native handwriting: Gooseapple, 5 stars: "My handwriting was awful and blocky and looked nothing like a native."
- Kids' books: colour and simplicity.

**Not found in the sampled reviews:** wrong stroke order (only the ㅓ vowel-description dispute), ink bleed-through, or "AI-written". Treat these as absent from the sample, not proven absent.

---

## 4. Accuracy without a human checker

| Component | Machine-verifiable? | How | Status |
|---|---|---|---|
| Syllable composition (jamo to block) | **Yes, fully** | Unicode formula `0xAC00 + (L*21 + V)*28 + T`, which gives 19x21x28 = **11,172** syllables. Check against Python `unicodedata` NFC | [V] ran it: 11,172; 가 to 힣; NFC(ᄀ+ᅡ+ᆨ) = 각 |
| Jamo inventory, names, dictionary order | Yes | Fixed by Hangul Matchumbeop article 4 (NIKL), so hard-code it | [V] NIKL pages |
| Revised Romanization | **Yes, but only if you test the library** | The RR rules (MCST notice 2014-42) say romanise **by standard pronunciation**, with official examples such as 백마 Baengma, 종로 Jongno, 신라 Silla, 묵호 Mukho | [V] Results below |
| Stroke order of the 40 jamo | **Partly.** The brief's premise does not hold | **NIKL does not regulate stroke count or order.** Its Online Ganada answer (5 Aug 2025) says stroke count "is not something the orthographic norms define", and that ㅈ can be read as 2 or 3 strokes depending on letterform. Use the conventional school order. Cross-check 2 or more independent sources, for example the CC BY-SA 4.0 SVG set `MagisterAdamus/hangeul-stroke-order` (35 of 40 letters; the 5 tense doubles are omitted) and Wikimedia/textbook charts. Hand-encode about 24 basic sequences and derive the rest | [V] NIKL answer; [V] dataset README |
| Pronunciation and sound change (liaison, nasalisation, liquidisation, tensing, aspiration, palatalisation, ㄴ-insertion) | **Partly** | The published rule set is NIKL *Standard Pronunciation Rules* (표준 발음법). Engines: **g2pK** (Apache-2.0, uses a Mecab morphological analyser; its README shows 신고 read as 신꼬 or 신고 depending on context), **Wiktionary Module:ko-pron** (exported by Kaikki as phonetic hangul, e.g. 신라 to [실라], plus IPA), and koroman. Note that ko-pron relies on **manual flags for tensing, ㄴ-insertion and vowel length**. So these changes depend on morphology and cannot be derived from spelling alone | [V] READMEs and Kaikki JSON; g2pK not run locally (needs Mecab) |
| Vocabulary meanings | **Verify, don't copy** | NIKL *Basic Korean Dictionary* (krdict) has an open API and a full XML download. Kaikki/Wiktionary has about **81,949 Korean senses**. **Both are CC BY-SA** (NIKL dictionaries CC BY-SA 2.0 KR since 2019-03-11), which is share-alike. Copying glosses or example sentences into a commercial book creates licence obligations, and some NIKL example sentences and all media files are not open at all. Write your own short glosses and use 2 sources only to confirm them | [V] repo statement; [A] the legal reading. Confirm before relying on it |

**Romanisation test I ran** on 25 words, using the official RR examples plus rule cases [V]:
- `korean_romanizer` 0.28.0 (the most-starred Python library): **13/25**. It fails every assimilation case: 신라 gives sinra, 종로 jongro, 왕십리 wangsipri, 같이 gati, 해돋이 haedodi.
- `koroman` 1.0.16: **24/25**. Its only miss is 묵호, which it gives as muko; RR requires Mukho because ㅎ is written after ㄱ/ㄷ/ㅂ in nouns.
- `hangul-romanize` (academic mode): 3/25. It transliterates; it does not romanise by pronunciation.

**Lesson:** choose an engine by **regression-testing it against the official RR example list**. Then majority-vote 3 engines (koroman, g2pK to phonetic hangul to RR, and Kaikki ko-pron), and send any disagreement to a "manual / exclude" list. Simplest policy: **only put into reading drills the words where all engines agree**. Keep the sound-change chapter to rule-illustrating words whose phonetic forms appear in NIKL's own Standard Pronunciation examples.

**Fonts and layout** [V for licences, A for typography]:
- Noto Sans KR and Noto Serif KR (Google/Adobe Source Han, SIL OFL) and Nanum Gothic/Myeongjo (OFL) are all cleared for commercial print.
- Gothic (sans) letterforms differ from handwriting, for example the ㅈ/ㅊ forms and the top stroke of ㅎ. Use a Myeongjo/serif or pen-style OFL face for tracing models, and add a "print vs handwritten" comparison page; Gooseapple and Hangeul Master sell partly on this point.
- Practice grid: Korean-style square cells (원고지 / "10-cell notebook" style) with light cross-hair guides. Show the syllable-block zones (initial / vertical vowel / horizontal vowel / final) as faint boxes so placement can be checked against font metrics.
- Build with ReportLab or LaTeX. Run a glyph-coverage check that every syllable used exists in the embedded font.

**Accuracy risk summary [A]:**
- Composition, jamo and grid layout: near zero risk.
- RR: low, if engines are tested and voted.
- Stroke order: low to medium. There is no official authority, but the conventional order is stable; keep the variants of ㅈ, ㅊ and ㅎ explicit.
- Sound-change phonetics: medium. Restrict to voted words.
- Meanings: medium. Restrict to about 300-500 high-frequency concrete words, check against 2 dictionaries, and use your own wording.
- English sound approximations ("ㅓ = u in bus"): readers dispute these (quote 5). Present them as approximations, with a mouth-shape description and a note on accent variation.

---

## 5. Best format and angle

**Recommended angle [A]: "Read Hangul in 14 Days: a step-by-step course workbook"**
- Audience: teens and adults (K-pop/K-drama fans, travellers, heritage learners).
- Format: 8.5x11, B&W, about 180-220 pages, $12.99-14.99.
- Every element below is generated and checked by code.

1. **Day-by-day lessons, letters introduced in a decodable order:**
   - Each day adds 2-4 jamo.
   - Reading drills use **only words built from letters already learned**. The word lists are filtered automatically from a frequency list, phonics-style.
   - No competitor checked does this explicitly, which answers "very few instructions" and "doesn't get me further".
2. **Writing ladder per letter:** stroke-order diagram, then trace, then copy, then recall from memory, in proper square grids with block-zone guides. This answers the "plenty of space" praise and the "blank padding" complaints.
3. **Syllable-block builder exercises:** jamo to block, block to jamo, and "which placement is right?" Answers are generated and checked by the composition algorithm.
4. **Sound-change unit:** liaison, nasalisation, liquidisation, tensing, aspiration and palatalisation, each shown with phonetic hangul in brackets [실라]. Use only engine-agreed words. Squid S2's listing pitches the same need, which the *Golden* lyrics made popular, but that book has no traction yet.
5. **Romanisation that fades:** full RR in week 1, none by week 2. This answers quotes 12-13.
6. **Native handwriting variants page** for each letter, with print and handwritten forms side by side.
7. **Answer keys** and **review tests every 3 days**. Photocopiable pages, which Lilas reviewers liked.
8. **Reading practice from culturally relevant but non-copyrighted vocabulary:** food, places, everyday words, honorific titles, common fan words (오빠, 언니, 화이팅, 대박). No lyrics and no trademarked group names [A].

**Is pronunciation without audio a dealbreaker? No, but it caps the rating [A, grounded in data].**
- Several 4.6-4.7 titles ship without audio: Dahye Go (4.7, 2,029 ratings), R.E. Jong (4.6), and Fandom (4.6; the publisher's own table lists audio as "no data").
- But the leader and the newer climbers all bundle audio or video: One and Only, Lingo Mastery, Unlocking Hangul, TTMIK.
- "No audio" is the single most frequent criticism (quotes 1-6).
- Mitigations that need no recordings:
  - mouth-position diagrams and articulation descriptions;
  - minimal-pair drills (ㄱ/ㅋ/ㄲ etc.);
  - phonetic-hangul respellings;
  - a short "how to use free audio" page pointing generically to free dictionary pronunciations. Note the legal limit: NIKL media files are not redistributable, so link at most, and expect link rot [A].
- Expect about 4.5 rather than 4.8 unless the drills are clearly better.

**Kids' edition [A]:** a secondary product. Kids' titles cluster at BSR 88k-1M+, and the best one needs full colour (a higher print cost). A B&W kids' version would compete on price only.

**Series potential [V for comparables, A for fit]:**
- The Self-taught brand already proves cross-script replication: Japanese kana at BSR 31k (331 ratings), Arabic at 43k (186), Korean at 8.9k.
- W13 comparables: Lingo Mastery Hiragana/Katakana 20,927; Tuttle Hiragana/Katakana 16,886; Lingo Kanji 50,957; Greek alphabet workbooks weak (best around 120k).
- Suggested order:
  1. Hangul.
  2. "Korean sound-change and reading drills" (book 2, the same engine).
  3. Japanese kana. Equally algorithmic; stroke data from KanjiVG (CC BY-SA 3.0).
  4. Arabic. Contextual letter forms are machine-checkable via HarfBuzz shaping, but pronunciation and harakat need care, and the sector is crowded.
- Avoid or postpone Thai (tone and consonant-class rules are complex), Devanagari (conjunct rendering depends on the font), and "500 Korean words" vocabulary books, which carry higher meaning and licence risk.

**Economics [A, using the standard KDP B&W formula]:** a US 8.5x11 B&W print cost of about $1.00 + $0.012 per page gives about $3.40 for 200 pages. At $13.99 that leaves a royalty of about $5.00.

---

## 6. Trend, 2024-2026
- **Duolingo global rank for Korean:** #6 in 2023, #7 in 2024 (Italian took #6 back), **#6 in 2025** [V: Duolingo blog and CIOL].
- The 2025 report says Korean was the "second fastest-growing language" in 7 countries (AR, CO, FR, DE, MX, ES, PL) [V]. Since 2025 Korean is available from 27 base languages [V, Duolingo blog Jul 2026].
- **US:** Duolingo reported **+22% Korean learners in the US** over a one-year period, tied to *KPop Demon Hunters* ("Golden"), with universities expanding courses [V: NYT via Business Times, 1 Feb 2026]. The same article says the film is Netflix's most-watched film ever (325.1M views).
- **Competition from free tools:** in July 2026 Duolingo relaunched its Korean course with a dedicated **Hangeul tab** and optional transliteration. Free apps are moving into Hangul basics [V]. This both feeds the funnel and competes with the book [A].
- **Book-side signal:** a new omnibus from the Hangul leader's brand reached BSR 16,967 within about 7 months of its March 2026 launch, and the 2025 Hangul workbook still holds BSR 8.9k, so demand persisted into late 2026 [V numbers; A interpretation].
- **Not checked:** Google Trends and keyword-volume tools [A]. The direction is inferred from the Duolingo and press data only.

---

## Scores [A, my judgement from the data above]

| Dimension | Score /10 | Why |
|---|---|---|
| Demand | **6** | Real buyers (#1 at BSR 8.9k, growing learner base), but steep drop-off; only about 6 Hangul titles under 90k |
| Competition (10 = easy) | **4** | An ad-backed brand leader with a series halo; 1-2k-review incumbents; free apps; newcomers since 2025 mostly fail. Content quality is beatable |
| AI-hunt immunity | **8** | The content is data (jamo, syllables, word lists, drills, keys); prose is minimal and templated. No "AI" complaints in the sample |
| Accuracy risk without a human checker (10 = low) | **6** | Composition and RR are verifiable with engine voting. Stroke order has no official standard but is stable. Sound-change and gloss risk is manageable by restriction. English sound approximations get disputed |
| Fit as a high-content book | **8** | Drills, builders, decodable reading lists and answer keys fill 200 pages without blank padding |

**Best angle:** "Read Hangul in 14 Days": a code-built teen/adult course workbook with decodable reading drills, syllable-builder exercises, engine-verified sound-change drills, romanisation that fades, a native-handwriting page and full answer keys.

**Biggest risk:** the buyer expects audio, and the #1 seller (Self-taught KOR) wins on audio/video extras plus paid ads and a series halo. A no-audio book probably tops out around 4.5 stars and needs ad spend to surface. Secondary risk: stroke order has no official standard, and the dictionary data is share-alike licensed, so neither can simply be copied in as "authoritative".

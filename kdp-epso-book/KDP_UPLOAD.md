# KDP Upload Guide — Reasoning Tests Workbook for EPSO Exams

All files are in `build/`. To regenerate everything, run `./build.sh` (it needs Python 3.11 and `pdftoppm`). The build ends with `src/check_pdf.py`, an automated KDP pre-flight check (page size, embedded fonts, gutter-aware margins, cover width).

| Format | Manuscript | Cover | Trim / spec |
|---|---|---|---|
| Paperback | `interior.pdf` (377 pp) | `cover_paperback.pdf` (17.5990 × 11.25 in, spine 0.8490 in) | 8.25 × 11 in, black & white, white paper, **no bleed**, matte |
| Hardcover (case laminate) | `interior.pdf` (same file) | `cover_hardcover.pdf` (19.1120 × 12.418 in, spine 1.0360 in) | 8.25 × 11 in, black & white, white paper, matte |
| Kindle eBook | `kindle.epub` (EPUBCheck: 0 errors/0 warnings, 1.1 MB) | `kindle_cover.jpg` (1600 × 2560 px) | Reflowable |

> **Hardcover cover check (do this once):** in KDP, open *Cover → Download template* for 8.25 × 11 in, white paper and 377 pages. If the template's total width, height or spine differ from the values above, regenerate with the exact numbers:
> `python src/cover.py --hc-width <W> --hc-height <H> --hc-spine <S>`
> All text sits well inside the safe zone, so a small difference only changes the background.

## Book details (the same for all three formats)
- **Language:** English
- **Title:** Reasoning Tests Workbook for EPSO Exams
- **Subtitle:** 400+ Practice Questions: Verbal, Numerical and Abstract Reasoning, Situational Judgement and Assistant-Level Skills, 3 Timed Mock Exams and Worked Solutions
- **Series:** leave blank (or "Concours Prep Workbooks" if more titles follow)
- **Author / contributor:** Concours Prep. This is a neutral pen-name imprint. Change it in `src/assemble.py` (`META`) and `src/cover.py` (`AUTHOR`) if you prefer your own name, then run `./build.sh`. *Do not use "EU Careers", which is EPSO's own recruitment brand.*
- **Edition:** 1
- **Publishing rights:** I own the copyright and hold the necessary publishing rights.
- **Primary audience:** adults; not sexually explicit.
- **ISBN:** use the free KDP ISBN. Paperback and hardcover each get their own ISBN. If you want the ISBNs printed on the copyright page, enter them in `META` and rebuild; KDP does not require this.

### Description (paste into the HTML editor)
```html
<h2>Practise like it's the real test.</h2>
<p>Selection tests for careers in the EU institutions are demanding, and the candidates who succeed are usually those who have practised under realistic conditions. This workbook gives you <b>413 original questions</b> in the formats used in EPSO-style computer-based tests, each with a <b>full worked solution</b> that shows not only the right answer but why every other option is wrong.</p>
<h3>What's inside</h3>
<ul>
<li><b>Verbal reasoning:</b> 125 passages, with the common traps (extreme wording, scope shifts, cause and effect, outside knowledge) named and explained</li>
<li><b>Numerical reasoning:</b> 105 table and chart questions covering percentages, percentage points, ratios, weighted averages, compound growth, index numbers and currency conversion, all with step-by-step calculations</li>
<li><b>Abstract reasoning:</b> 105 figure series, graded from foundation to advanced, with every rule spelled out</li>
<li><b>Situational judgement:</b> 24 workplace scenarios built around typical EU competency themes</li>
<li><b>Accuracy &amp; precision</b> and <b>prioritising &amp; organising:</b> 54 questions for assistant-level (AST-SC), CAST and specialist procedures</li>
<li><b>3 timed mock exams:</b> 40 reasoning questions each, with score guides and answer sheets</li>
<li><b>Strategy chapters:</b> clear methods for every test type, 4- and 8-week study plans and test-day tactics</li>
<li>A score tracker and an error log to turn every mistake into progress</li>
</ul>
<h3>Who is it for?</h3>
<p>Candidates for administrator (AD), assistant (AST), AST-SC, contract-agent (CAST) and specialist selection procedures, and anyone preparing for European-style psychometric reasoning tests. The core reasoning skills stay the same even when test formats change, so always check the Notice of Competition for your procedure.</p>
<p><i>This book does not cover EU-knowledge, digital-skills or language tests.</i></p>
<p><i>Independent publication: not affiliated with, authorised or endorsed by the European Personnel Selection Office (EPSO), the European Union or any EU institution. All questions are original.</i></p>
```

### Keywords (7 slots)
1. EU competition exam preparation
2. EU institutions career test practice
3. verbal numerical abstract reasoning test
4. computer-based test practice questions answers
5. European Union competition AD AST exam
6. situational judgement test workbook
7. psychometric aptitude test practice book

### Categories (choose up to 3)
- Study Aids › Civil Service (Test Preparation › Civil Service)
- Study Aids › Study Guides
- Business & Economics › Careers › Job Hunting

## Content declarations
- **AI-generated content: answer "Yes".** KDP defines "AI-generated" as content created by an AI tool, even if you edited it substantially afterwards. That applies here:
  - *Text:* AI-generated, then independently reviewed item by item through 5 quality gates.
  - *Images:* AI-generated. The cover and the figures are vector drawings produced by AI-written code.
  - *Translations:* none.
- **Low-content book:** No.
- **Large print:** No.

## Pricing (estimates; confirm in the KDP pricing calculator)
8.25 in wide counts as a **large trim** at KDP, so per-page print costs are higher than for standard trims.

| Format | Suggested list price | Approx. US print cost | Approx. royalty per sale |
|---|---|---|---|
| Paperback | $24.99 / €24.99 / £21.99 | large trim: $1.00 + 377 × $0.017 ≈ $7.41 | 60% × 24.99 − 7.41 ≈ **$7.58** |
| Hardcover | $34.99 / €34.99 / £29.99 | large trim: roughly $6.80 + 377 × $0.017 ≈ $13.21 (confirm) | 60% × 34.99 − 13.21 ≈ **$7.78** |
| Kindle | $9.99 / €9.99 / £8.99 (70% band) | delivery ≈ 1.1 MB × $0.15 ≈ $0.17 | ≈ **$6.88** |

The core EU markets are **Amazon.de, .fr, .es, .it, .nl, .pl, .se and .com.be**. Enable expanded distribution for the paperback.

## Kindle-specific settings
- **DRM:** your choice (enabling it is common for test-prep books).
- **KDP Select:** optional. It adds Kindle Unlimited reach but requires 90-day ebook exclusivity.
- Use the **previewer** to check a phone view. Each question links to its solution, and each solution links back to its question.

## Final checks before you click Publish
- [ ] Hardcover template dimensions confirmed (see above).
- [ ] In the print previewer, no "text outside margins" or "image resolution" warnings (all graphics are vector).
- [ ] Order a **printed proof copy** of the paperback and hardcover and check the grey shading of the abstract figures in print.
- [ ] Decide whether to keep or change the imprint name.

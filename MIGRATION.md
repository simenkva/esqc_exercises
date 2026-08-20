# Migration plan for the ESQC mathematics exercises

Last updated: 2026-08-20

## Goal

Migrate the exercises and solutions in
`ESQC_2024_text_and_exercises/ESQC2024_math_exercises.tex` into the Quarto
book. The migration will reorganize the old numbered exercise sets by
mathematical subject. It will preserve the mathematical content, selection
status, tutor notes, solutions, and useful figures.

This is a migration of the 2024 material, not the final scope of the book. The
book therefore keeps subject parts that receive no migrated exercises. New
exercises can fill those parts later.

## Decisions made

### Book organization

The Quarto book uses the following parts:

1. Exercise recommendations
2. Mathematical foundations
3. Linear algebra
4. Metric spaces and topology
5. Calculus
6. Multivariable calculus
7. Series and matrix functions
8. Complex numbers and complex analysis
9. Numerical methods
10. Fourier analysis
11. Ordinary differential equations
12. Partial differential equations
13. Optimization

We will keep empty parts in `_quarto.yml`. The taxonomy can grow with the book,
but the first migration will use it as written.

### Profiles and publication layout

The book has two Quarto profiles:

- `student`, which omits solutions
- `tutor`, which includes solutions and tutor-only notes

The intended side-by-side output layout is:

```text
docs/student/     student book
docs/tutor/       tutor book
```

The shared configuration lives in `_quarto.yml`; profile-specific settings
belong in `_quarto-student.yml` and `_quarto-tutor.yml`.

The profile files implement this layout. Resource globs in `_quarto.yml` are
anchored to the project root so rendered output is not recopied on later
renders. The recursively nested output left by earlier renders has been
removed and both profiles have been rebuilt from a clean `docs/` directory.

### Exercise chapter format

Every migrated chapter must follow `chapters/TEMPLATE.qmd`:

- one level-one chapter heading;
- a short introduction containing the definitions, notation, and assumptions
  needed for the exercises;
- a level-two `Exercises` section;
- one fenced div with a unique `exr-...` ID for each exercise;
- a level-two `Solutions` section inside one tutor-only fenced div; and
- one solution heading for each exercise, linked with an `@exr-...` reference.

Answers, answer-revealing hints, grading guidance, and tutor notes belong inside
the tutor-only div. Student output must contain none of them.

### Recommended and optional exercises

Visible `recommended` and `for the curious` tags are deprecated. Selection
status lives in the exercise ID:

```text
#exr-short-name                 ordinary exercise
#exr-recommended-short-name     recommended exercise
#exr-curious-short-name         optional exploration
```

The migration maps legacy tags as follows:

```text
\mytag{recommended}       -> #exr-recommended-...
\mytag{for the curious}   -> #exr-curious-...
```

The source contains 23 literal occurrences of `\mytag{recommended}`. One is
the explanatory mention in the old introduction, so 22 mark exercise content.
It also contains six `\mytag{for the curious}` markers. The migration audit
must account for each content marker.

The old document sometimes marks a single lettered subpart and sometimes a
whole compound exercise. A tagged subpart must become its own exercise div so
its ID can carry the selection status. When a tag applies to a whole source
section, the compound exercise can stay together under one prefixed ID.

`chapters/recommendations-first-day.qmd` contains two generated regions. A
post-processing step will scan all exercise IDs and write cross-reference
bullets into them:

- `exr-recommended-*` IDs under **Recommended exercises**;
- `exr-curious-*` IDs under **For the curious**.

During migration, `update_recommendations.py` maintained these regions in book
and document order. The completed migration tooling now lives under
`archive/`, including this generator, while the recommendation system awaits
its replacement.

`chapters/recommendations-per-topic.qmd` currently preserves the course-topic
wishlist from `OUTLINE.md`. It is separate from the generated lists based on
legacy selection tags.

## Migration map

The old five exercise-set chapters will not survive as book divisions. The
following map places their sections by subject. Some broad old sections will
be split where their exercises belong to different parts.

| New part | Planned migrated chapter or material | Legacy source section |
| --- | --- | --- |
| Mathematical foundations | Sets, functions, and De Morgan's laws | Sets etc. |
| Mathematical foundations | Cardinality and countability | Cardinality of numbers |
| Linear algebra | General vector spaces | General vector spaces |
| Linear algebra | Vectors and matrices | Basic vectors; More vectors and matrices |
| Linear algebra | Complex numbers as a real vector space | The complex numbers as a real vector space |
| Linear algebra | Gaussian elimination | Elementary row operations and Gaussian elimination |
| Linear algebra | Bra-ket notation | Bra-ket notation |
| Linear algebra | Eigenvalues and diagonalization | Eigenvalue decomposition; Diagonalization of a matrix |
| Linear algebra | Orthogonalization | Gram--Schmidt orthogonalization |
| Linear algebra | Singular-value decomposition | The singular value decomposition as a compression tool |
| Linear algebra | Polynomial vector spaces and linear maps | Space of polynomials |
| Metric spaces and topology | Metric spaces | Metric spaces |
| Metric spaces and topology | Open and closed subsets of Euclidean space | Open and closed sets in Euclidean space |
| Multivariable calculus | Visualizing scalar and vector-valued functions | Visualization of functions |
| Multivariable calculus | Limits, continuity, and differentiability | Continuity; Differentiability |
| Series and matrix functions | Taylor series, matrix exponentials, and commutators | Taylor polynomials |
| Complex numbers and complex analysis | Complex arithmetic and polar form | Complex numbers; Basic calculations |
| Complex numbers and complex analysis | Geometry of subsets of the complex plane | Visualizing complex sets |
| Complex numbers and complex analysis | Complex exponential and analytic functions | Complex functions: The complex exponential function |
| Complex numbers and complex analysis | Complex power series | Complex functions: Taylor series |
| Complex numbers and complex analysis | Singularities, Laurent series, and contour integrals | Complex functions: Singularities; Line integrals |
| Numerical methods | Dual numbers and automatic differentiation | Dual numbers |
| Numerical methods | Newton's method | Newton--Rhapson method |
| Numerical methods | Complex-step differentiation | Complex step method |

The first pass leaves Calculus, Fourier analysis, Ordinary differential
equations, Partial differential equations, and Optimization empty. Newton's
method stays under Numerical methods because the source develops it as a root
finder. Future optimization exercises can reuse the same analysis without
moving the migrated chapter.

## Conversion policy

For each source section:

1. Identify its mathematical subject and target chapter from the map above.
2. Decide whether it forms one compound exercise or several independent
   exercises. Split any individually tagged subpart.
3. Create stable, descriptive lowercase IDs. Do not encode old chapter or item
   numbers in an ID.
4. Convert prose and mathematics to Quarto Markdown. Use `$...$` for inline
   mathematics and `$$...$$` for displays.
5. Replace document-specific commands from `commondefs.tex` with supported
   MathJax commands or define a shared macro when repeated use justifies it.
6. Move every source `solution` block and tutor note into the tutor-only
   solutions div. Preserve incomplete solutions as incomplete; do not invent a
   derivation to fill a gap.
7. Preserve the source's mathematical meaning and supplied data. Add a source
   comment for ambiguity, apparent errors, or missing information so a human
   can review it.
8. Copy each required image to a stable book asset location and update its
   reference. Add useful alt text and preserve attribution found in the
   source.
9. Add the completed chapter to its part in `_quarto.yml`.
10. Regenerate the two lists in `recommendations-first-day.qmd`.

Do not add new exercises, citations, learning objectives, or explanatory
material during the migration unless requested. Corrections to mathematical or
typographical errors should be small and documented.

## Source details that need attention

- The source depends on macros in
  `ESQC_2024_text_and_exercises/commondefs.tex`. Commands such as number-set,
  vector, bra-ket, derivative, differential, and identity-matrix notation need
  a deliberate MathJax conversion.
- The source uses custom `myDefinitionx` and `mySolution` environments. Convert
  definitions to normal chapter prose or an established Quarto callout, and
  convert solutions to the profile-gated structure from the template.
- Source exercise numbering treats many `enumerate` items as subparts of a
  section-level exercise. The new ID structure, especially tagged subparts,
  will change numbering. Cross-references should use IDs rather than old
  numbers.
- The source includes `illustrations/chess.ai`, `images/sol-fig1.png`,
  `images/parrot.jpg`, and `images/parallelogram_rule.png`. Browser output
  cannot use the Illustrator file directly, so the chess illustration needs an
  SVG or PNG derivative if retained.
- Commented-out exercises should remain excluded on the first pass. Record
  them as dormant source material rather than silently reviving them.
- Definite mathematical and typographical errors found during conversion were
  corrected conservatively. Incomplete source solutions remain explicit
  tutor-only placeholders rather than receiving invented derivations.
- The questionless first item in the Taylor-polynomial section was retained as
  introductory material rather than presented as an exercise.
- The source spelling `Newton--Rhapson` was corrected to Newton--Raphson.

## Implementation order

All four phases below were completed on 2026-08-20. The sequence remains here
as a record of the migration method.

### Phase 1: Stabilize the book shell

- Confirm the profile output directories remain `docs/student/` and
  `docs/tutor/`.
- Stop output directories from nesting during repeated renders.
- Confirm that both profiles use the same formats and resources.
- Implement the recommendation-list generator and a duplicate-ID check.

### Phase 2: Establish conversion conventions

- Choose the shared MathJax replacements for macros from `commondefs.tex`.
- Choose the permanent location for migrated images.
- Convert one representative chapter containing mathematics, tagged subparts,
  a figure, solutions, and a tutor note.
- Review that chapter before converting the remaining source.

### Phase 3: Migrate by subject

Convert in this order so shared notation settles before later chapters use it:

1. Mathematical foundations
2. Linear algebra
3. Metric spaces and topology
4. Multivariable calculus
5. Series and matrix functions
6. Complex numbers and complex analysis
7. Numerical methods

After each part, render both profiles and regenerate the recommendation lists.

### Phase 4: Audit the complete migration

- Account for every active legacy exercise and solution.
- Account for all 22 exercise-content `recommended` markers and all six `for
  the curious` markers.
- Confirm that every exercise ID is unique and every solution references a
  valid exercise.
- Compare equations, assumptions, data, and figures against the LaTeX source.
- Resolve or document each ambiguity and known source error.
- Check links, figure paths, equations, and cross-references in HTML and EPUB.
- Confirm that search and navigation follow the new subject structure.

## Acceptance checks

Run both builds:

```sh
quarto render --profile student
quarto render --profile tutor
```

The migration is complete when:

- both commands finish without warnings about unresolved references or missing
  resources;
- the student book contains no solutions, tutor notes, grading notes, or
  answer-revealing hints;
- the tutor book contains every migrated solution and tutor note;
- all recommended and curious exercises appear in the generated lists and link
  to the correct exercise;
- no visible legacy selection tag remains;
- the student site is in `docs/student/` and the tutor site is in
  `docs/tutor/`;
- no output directory contains a nested copy of `docs`; and
- empty future parts remain represented in the book structure.

## Current status

Migration completed on 2026-08-20:

- 24 subject chapters contain 125 migrated exercises;
- all 22 legacy recommended markers and all six curious markers are accounted
  for in exercise IDs and the generated recommendation lists;
- solutions and tutor notes are gated by the `tutor` profile;
- source figures were copied or converted into `figures/exercises/`;
- empty future parts remain in `_quarto.yml`;
- `archive/scripts/migrate_legacy.py` records the one-time Pandoc-based
  conversion and refuses to overwrite curated chapters unless `--force` is
  given;
- `archive/scripts/audit_book.py` records the migration audit for chapter and
  asset existence, ID uniqueness, solution structure, legacy marker counts,
  generated-list freshness, and unsupported source commands;
- `archive/scripts/update_recommendations.py` and its test preserve the retired
  recommendation generator for reference; and
- clean student and tutor HTML/EPUB builds are present in `docs/student/` and
  `docs/tutor/`.

Twelve chapters contain one or more explicit tutor-only missing-solution
placeholders because the legacy source did not supply complete solutions.
These are preserved gaps in the source material, not migration failures.

The archived scripts are no longer part of routine book maintenance. Verify
the current book by rendering both profiles:

```sh
quarto render --profile student
quarto render --profile tutor
```

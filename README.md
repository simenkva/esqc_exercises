# ESQC Mathematics Exercises

This repository contains the mathematics exercise book for the European
Summer School in Quantum Chemistry (ESQC). 

## Build the book

The project uses Quarto 1.9.38. PDF rendering requires LuaLaTeX. The bundled
font files make the build independent of fonts installed on your computer.

Render either edition from the repository root:

```sh
quarto render --profile student
quarto render --profile tutor
```

Add `--to html`, `--to pdf`, or `--to epub` to build one format. For example:

```sh
quarto render --profile student --to pdf
```

Quarto writes the student files to `docs/student/` and the tutor files to
`docs/tutor/`.

The publishing script builds both editions, stages the working tree, commits
the result with a timestamp, rebases against the remote branch, and pushes:

```sh
./scripts/publish.sh
```

Because the script runs `git add -A`, check the working tree before using it.

## Add or revise an exercise

Use `chapters/TEMPLATE.qmd` as the starting point. Give each exercise a stable,
descriptive identifier:

```markdown
::: {#exr-short-name}
Write the exercise here.
:::
```

Add the `recommended` class and a `topic` attribute when an exercise belongs
in one of the generated recommendation lists:

```markdown
::: {#exr-short-name .recommended topic="recommended,scf"}
Write the exercise here.
:::
```

Keep solutions and tutor notes inside the tutor profile gate:

```markdown
::: {.content-visible when-profile="tutor"}
## Solutions

### Solution to @exr-short-name {.unnumbered}

Write the solution here.
:::
```

Add new chapter files to the appropriate part of `_quarto.yml`. Render both
profiles before committing so that cross-references and profile-specific
content receive the same check.

## Repository layout

```text
chapters/                  Exercise chapters and their tutor solutions
_generated/                Recommendation pages made during rendering
figures/                   Cover art and exercise figures
fonts/                     Web, ebook, and desktop font files
scripts/                   Recommendation, rendering, and publishing tools
docs/student/              Rendered student edition
docs/tutor/                Rendered tutor edition
_quarto.yml                Shared book structure and format settings
_quarto-student.yml        Student output settings
_quarto-tutor.yml          Tutor output settings
```

The old LaTeX source remains in `ESQC_2024_text_and_exercises/` as a migration
record. `MIGRATION.md` documents how that material moved into the Quarto book.

## Contributions

Are you an ESQC tutor? I welcome contributions to the exercises, solutions, figures, and code. Read
[CONTRIBUTING.md](CONTRIBUTING.md) before submitting material. Add your name
and attribution details to [CONTRIBUTORS.md](CONTRIBUTORS.md).

## Licence

Original educational content uses the [Creative Commons Attribution 4.0
International licence](https://creativecommons.org/licenses/by/4.0/). Source
code, code snippets, styles, and build tools use the MIT License. Fonts and
other third-party material keep their own terms.

See [LICENSE](LICENSE), [LICENSE-CONTENT](LICENSE-CONTENT),
[LICENSE-CODE](LICENSE-CODE), and
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for the details.

# Script for generating recommended exercise lists.

levels = ["beginner", "intermediate", "advanced"]

recommendations = ["math", "topic"]

# Topics and their descriptions, the latter used for writing the recommended
# exercises per topic.
topics = {
    "coupled-cluster": "Coupled-cluster theory",
    "second-quantization": "Second quantization",
    "scf": "Self-consistent field theory",
    "dft": "Density functional theory",
    "response-theory": "Response theory",
    "relativity": "Relativistic quantum chemistry",
    "molecular-properties": "Molecular properties",
    "multiconfig-methods": "Multiconfigurational methods",
}

# Example exercise syntax:
#
# :::{#exr-1 recommended="math;topic" level="beginner" topic="coupled-cluster;scf"}
# ### Heading
# body
# :::
#

day_1_intro = r"""# Recommended exercises for the first day {.unnumbered}

This chapter contains recommended exercises for the mathematics
tutorial on the first day of the school. These recommended exercises are
considered especially useful.

We provide also a list of recommended exercises for the 'beginners'. If you
feel that you need training in the _absolute basics_ of the mathematics used
in quantum chemistry, we recommend that you start here.

In the next chapter, we provide lists of recommended exercises for each
quantum chemistry topic taught at the school.

"""

topic_intro = r"""# Recommended exercises by topic {.unnumbered}

This chapter contains lists of mathematics exercises grouped by each
quantum chemistry topic taught at the school. These exercises can be
useful as a warm-up to the proper exercises given each day.

"""


import yaml
from pathlib import Path
import re


# ---------------------------------------------------------------------------
# Get a list of chapters from _quarto.yml
# ---------------------------------------------------------------------------

with open("_quarto.yml", "r") as f:
    config = yaml.safe_load(f)

chapters = []

for entry in config["book"]["chapters"]:
    entry_chapters = [entry] if isinstance(entry, str) else entry.get("chapters", [])

    chapters.extend(
        chapter
        for chapter in entry_chapters
        if "_generated" not in Path(chapter).parts
        and "chapters" in Path(chapter).parts
    )

print("Chapters in the book:")
for chapter in chapters:
    print(f" - {chapter}")


# ---------------------------------------------------------------------------
# Parse exercise metadata
# ---------------------------------------------------------------------------

def parse_attributes(attr_string):
    """Parse attributes from the opening line of an exercise fenced div."""

    result = {
        "id": None,
        "classes": [],
        "recommended": [],
        "level": None,
        "topic": [],
    }

    # Exercise ID
    match = re.search(r"#([A-Za-z0-9_-]+)", attr_string)
    if match:
        result["id"] = match.group(1)

    # Classes
    result["classes"] = re.findall(r"\.([A-Za-z0-9_-]+)", attr_string)

    # Key-value attributes. Accept both single and double quotes.
    for key, quote, value in re.findall(
        r"""([A-Za-z0-9_-]+)\s*=\s*(["'])(.*?)\2""",
        attr_string,
    ):
        if key == "recommended":
            result["recommended"] = [
                x.strip() for x in value.split(";") if x.strip()
            ]

        elif key == "topic":
            result["topic"] = [
                x.strip() for x in value.split(";") if x.strip()
            ]

        elif key == "level":
            result["level"] = value.strip()

    return result


def extract_exercises(filename):
    """Extract exercises and their metadata from one QMD file."""

    text = Path(filename).read_text(encoding="utf-8")
    lines = text.splitlines()

    exercises = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Opening fenced div
        match = re.match(r"^\s*:::\s*\{([^}]*)\}\s*$", line)

        if not match:
            i += 1
            continue

        attr_string = match.group(1)

        # Only process exercise divs
        if not re.search(r"#exr-[A-Za-z0-9_-]+", attr_string):
            i += 1
            continue

        attrs = parse_attributes(attr_string)

        # Search the exercise body for a heading.
        heading = None
        depth = 1
        j = i + 1

        while j < len(lines) and depth > 0:
            current = lines[j]

            # Nested fenced div
            if re.match(r"^\s*:::\s*\{", current):
                depth += 1

            # Closing fenced div
            elif re.match(r"^\s*:::\s*$", current):
                depth -= 1

                if depth == 0:
                    break

            # Record the first heading at the top exercise-div level
            if depth == 1 and heading is None:
                heading_match = re.match(
                    r"^\s*#{2,6}\s+(.+?)\s*$",
                    current,
                )

                if heading_match:
                    heading = heading_match.group(1)

            j += 1

        exercises.append(
            {
                **attrs,
                "chapter": filename,
                "heading": heading,
            }
        )

        i = j + 1

    return exercises


# ---------------------------------------------------------------------------
# Collect exercises
# ---------------------------------------------------------------------------

exercises = []

for chapter in chapters:
    exercises.extend(extract_exercises(chapter))

print(f"\nFound {len(exercises)} exercises.")


# ---------------------------------------------------------------------------
# Validate metadata
# ---------------------------------------------------------------------------

valid_levels = set(levels)
valid_recommendations = set(recommendations)
valid_topics = set(topics)

errors = []
seen_ids = set()

for ex in exercises:
    ex_id = ex["id"]

    if ex_id in seen_ids:
        errors.append(f"Duplicate exercise id: {ex_id}")

    seen_ids.add(ex_id)

    if ex["level"] is not None and ex["level"] not in valid_levels:
        errors.append(
            f"{ex_id}: unknown level {ex['level']!r} "
            f"in {ex['chapter']}"
        )

    for recommendation in ex["recommended"]:
        if recommendation not in valid_recommendations:
            errors.append(
                f"{ex_id}: unknown recommendation {recommendation!r} "
                f"in {ex['chapter']}"
            )

    for topic in ex["topic"]:
        if topic not in valid_topics:
            errors.append(
                f"{ex_id}: unknown topic {topic!r} "
                f"in {ex['chapter']}"
            )

if errors:
    print("\nMetadata errors:")

    for error in errors:
        print(f" - {error}")

    raise ValueError("Exercise metadata validation failed.")


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

level_headings = {
    "beginner": "Beginner",
    "intermediate": "Intermediate",
    "advanced": "For the curious",
}


def exercise_list_item(ex):
    """Return one Markdown list item."""

    if ex["heading"]:
        return f"- @{ex['id']} — {ex['heading']}"

    return f"- @{ex['id']}"


def exercises_for_day_1(level):
    """Exercises recommended for the mathematics tutorial on day 1."""

    return [
        ex
        for ex in exercises
        if "math" in ex["recommended"]
        and ex["level"] == level
    ]


def exercises_for_topic(topic, level):
    """Recommended exercises for a quantum-chemistry topic."""

    return [
        ex
        for ex in exercises
        if "topic" in ex["recommended"]
        and topic in ex["topic"]
        and ex["level"] == level
    ]


# ---------------------------------------------------------------------------
# Generate day-1 exercise list
# ---------------------------------------------------------------------------

day_1_output = day_1_intro

for level in levels:
    selected = exercises_for_day_1(level)

    day_1_output += f"## {level_headings[level]} {{.unnumbered}}\n\n"

    if selected:
        for ex in selected:
            day_1_output += exercise_list_item(ex) + "\n"
    else:
        day_1_output += "_No exercises selected._\n"

    day_1_output += "\n"


# ---------------------------------------------------------------------------
# Generate exercise lists by quantum-chemistry topic
# ---------------------------------------------------------------------------

topic_output = topic_intro

for topic, description in topics.items():
    topic_output += f"## {description} {{.unnumbered}}\n\n"

    found_any = False

    for level in levels:
        selected = exercises_for_topic(topic, level)

        if not selected:
            continue

        found_any = True

        topic_output += f"### {level_headings[level]} {{.unnumbered}}\n\n"

        for ex in selected:
            topic_output += exercise_list_item(ex) + "\n"

        topic_output += "\n"

    if not found_any:
        topic_output += "_No exercises selected._\n\n"


# ---------------------------------------------------------------------------
# Write generated files
# ---------------------------------------------------------------------------

generated_dir = Path("_generated")
generated_dir.mkdir(parents=True, exist_ok=True)

day_1_file = generated_dir / "recommended-mathematics.qmd"
topic_file = generated_dir / "recommended-by-topic.qmd"

day_1_file.write_text(day_1_output, encoding="utf-8")
topic_file.write_text(topic_output, encoding="utf-8")

print(f"\nWrote {day_1_file}")
print(f"Wrote {topic_file}")


# ---------------------------------------------------------------------------
# Print summary
# ---------------------------------------------------------------------------

print("\nDay 1:")

for level in levels:
    print(
        f"  {level:12s}: "
        f"{len(exercises_for_day_1(level))}"
    )

print("\nBy topic:")

for topic, description in topics.items():
    counts = {
        level: len(exercises_for_topic(topic, level))
        for level in levels
    }

    count_string = ", ".join(
        f"{level}={counts[level]}"
        for level in levels
    )

    print(f"  {description}: {count_string}")
    

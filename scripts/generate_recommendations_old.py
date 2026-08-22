

# script for generating recommended lists.

# a dict of topics and their descriptions.
# 
topics_day_1 = {
          'beginner': 'Basic exercises recommended for beginners',
          'recommended': 'Recommended exercises',
          'curious': 'Exercises for the curious'
          }

topics = {
          'coupled-cluster': 'Coupled-cluster theory',
          'second-quantization': 'Second quantization',
          'scf': 'Self-consistent field theory',
          'dft': 'Density functional theory',
          'response-theory': 'Response theory',
          'relativity': 'Relativistic quantum chemistry',
          'molecular-properties': 'Molecular properties',
          'multiconfig-methods': 'Multiconfigurational methods',
          }

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

intro = r"""# Recommended exercises by topic {.unnumbered}

This chapter contains lists of mathematics exercises grouped by each
quantum chemistry topic taught at the school. These exercises can be
useful as a warm-up to the proper exercises given each day.

"""


# get a list of the chapters in _quarto-student.yml

import yaml
from pathlib import Path
import json
import re
import subprocess

with open('_quarto.yml', 'r') as f:
    config = yaml.safe_load(f)

# get all chapter names under all parts of the book
chapters = []
for entry in config['book']['chapters']:
    entry_chapters = [entry] if isinstance(entry, str) else entry.get('chapters', [])
    chapters.extend(
        chapter for chapter in entry_chapters
        if '_generated' not in Path(chapter).parts and 'chapters' in Path(chapter).parts
    )


# print the chapters
print("Chapters in the book:")
for chapter in chapters:
    print(f" - {chapter}")
    
    
# now we have all the chapters.


def extract_recommended_exercises(chapter):
    result = subprocess.run(
        ['pandoc', '--from', 'markdown', '--to', 'json', chapter],
        check=True,
        capture_output=True,
        text=True,
    )
    document = json.loads(result.stdout)
    exercises = []

    def visit(node):
        if isinstance(node, dict):
            if node.get('t') == 'Div':
                attributes = node['c'][0]
                identifier, classes, key_values = attributes
                attribute_values = dict(key_values)
                if identifier.startswith('exr-') and 'recommended' in classes:
                    topics = [
                        topic.strip()
                        for topic in re.split(r'[,;]', attribute_values.get('topic', ''))
                        if topic.strip()
                    ]
                    exercises.append({'id': identifier, 'topics': topics})
            for value in node.values():
                visit(value)
        elif isinstance(node, list):
            for value in node:
                visit(value)

    visit(document['blocks'])
    return exercises


recommended_exercises = [
    exercise
    for chapter in chapters
    for exercise in extract_recommended_exercises(chapter)
]

# # print the recommended exercises
# print("Recommended exercises:")
# for exercise in recommended_exercises:
#     print(f" - {exercise['id']} (topics: {', '.join(exercise['topics'])})")
    

# generate the recommendations-first-day.qmd file
# these have no topics.
with open('_generated/recommendations-first-day.qmd', 'w') as f:
    f.write(day_1_intro)
    f.write('\n')
    f.write('<!-- BEGIN GENERATED RECOMMENDED EXERCISES -->\n')
    for topic, description in topics_day_1.items():     
            f.write(f"## {description}\n\n")
            for exercise in recommended_exercises:
                if topic in exercise['topics']:
                    f.write(f"- @{exercise['id']}\n")
            f.write('\n')
    f.write('<!-- END GENERATED RECOMMENDED EXERCISES -->\n')
    
       
# generate the recommendations-per-topic.qmd file
with open('_generated/recommendations-per-topic.qmd', 'w') as f:
    f.write(intro)
    f.write('\n')
    f.write('<!-- BEGIN GENERATED RECOMMENDED EXERCISES -->\n')
    for topic, description in topics.items():     
        f.write(f"## {description}\n\n")
        for exercise in recommended_exercises:
            if topic in exercise['topics']:
                f.write(f"- @{exercise['id']}\n")
        f.write('\n')
    f.write('<!-- END GENERATED RECOMMENDED EXERCISES -->\n')
    

# report the user that the files have been generated

print("Generated recommendations-first-day.qmd and recommendations-per-topic.qmd")
# print the recommended exercises per topic
print("Recommended exercises per topic:")
for topic, description in topics.items():
    print(f"## {description}")
    for exercise in recommended_exercises:
        if topic in exercise['topics']:
            print(f" - {exercise['id']}")
    print()
    

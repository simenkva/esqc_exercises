#!/bin/sh
set -eu

quarto render --profile student
quarto render --profile tutor
git add -A
git diff --cached --quiet || git commit -m "render $(date '+%F %T')"
git pull --rebase
git push

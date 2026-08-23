#!/bin/sh
set -eu

#for profile in student tutor; do

for profile in tutor; do
    quarto render --profile "$profile" --to html
#    quarto render --profile "$profile" --to epub --no-clean
#    quarto render --profile "$profile" --to pdf --no-clean
done
git add -A
git diff --cached --quiet || git commit -m "render $(date '+%F %T')"
git pull --rebase
git push

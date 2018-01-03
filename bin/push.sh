#!/bin/bash

# Get branch.
BRANCH=$(git branch | awk '{print $2}')
echo "Pushing your code to $BRANCH..."

# Get Working dir.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/../

# Add untracked files.
git add * 2> /dev/null
git add .*ignore 2> /dev/null
git add .circleci/ 2> /dev/null

# Commit changes.
git commit -a -m "fix"

# Push to $BRANCH.
git push origin $BRANCH

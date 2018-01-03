#!/bin/bash

# Get branch.
BRANCH=$(git branch | awk '{print $2}')
echo "Pushing your code from $BRANCH..."

# Get working directory.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/../

# Pull data from repo.
git pull origin $BRANCH

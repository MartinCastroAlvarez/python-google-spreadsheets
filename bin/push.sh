#!/bin/bash
branch=$(git branch | awk '{print $2}')
echo "Pushing your code to $branch..."
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/../
git add * .*ignore .circleci/
git commit -a -m "fix"
git push origin $branch

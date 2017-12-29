#!/bin/bash
branch=$(git branch | awk '{print $2}')
echo "Pushing your code from $branch..."
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/../
git pull origin $branch

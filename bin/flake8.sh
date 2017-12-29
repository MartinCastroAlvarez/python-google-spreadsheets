#!/bin/bash
echo "Running flake8 tests..."
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $DIR/env.sh
if [ -d $DIR/../app ]
then
    location="$DIR/../app"
else
    location="$DIR/../$(head -1 README.md  | awk '{ print $2}')"
fi
flake8 --config=$DIR/../.flake8 $location && echo "All tests in $location OK!"

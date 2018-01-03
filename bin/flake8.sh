#!/bin/bash

# Initializing...
echo "Running flake8 tests..."

# Activate virtual environment.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $DIR/env.sh

# Guess working directory.
if [ -d $DIR/../app ]
then
    location="$DIR/../app"
else
    location="$DIR/../$($DIR/../bin/name.sh)"
fi

# Run flake8 tests.
flake8 --config=$DIR/../.flake8 $location && echo "All tests in $location OK!"

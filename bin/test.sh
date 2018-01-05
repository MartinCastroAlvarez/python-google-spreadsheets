#!/bin/bash

# Activate virtual environment.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $DIR/env.sh

# Determine the type of tests to run.
TESTS=$1
if [ $TESTS == "QA" ]
then
    echo "Running functional tests..."
    FILENAME="qa.py"
else
    echo "Running unit tests..."
    FILENAME="tests.py"
fi

# Get working directory.
if [ -f $DIR/../app/tests.py  ]
then
    location="$DIR/../app/$FILENAME"
else
    location="$DIR/../$FILENAME"
fi

# Run pytests...
py.test -xvs $location

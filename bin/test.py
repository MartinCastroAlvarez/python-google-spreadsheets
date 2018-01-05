#!/bin/bash

# Activate virtual environment.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $DIR/env.sh

# Get working directory.
if [ -f $DIR/../app/tests.py  ]
then
    location="$DIR/../app/tests.py"
else
    location="$DIR/../tests.py"
fi

# Run pytests...
py.test -xvs $location

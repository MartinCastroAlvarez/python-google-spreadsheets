#!/bin/bash
echo "Running py.tests..."
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $DIR/env.sh
if [ -f $DIR/../app/tests.py  ]
then
    location="$DIR/../app/tests.py"
else
    location="$DIR/../tests.py"
fi
py.test -xvs $location

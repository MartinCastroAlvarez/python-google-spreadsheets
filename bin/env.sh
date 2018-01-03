#!/bin/bash
echo "Activating virtual environment..."
clear
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create virtual environment if not exists.
if [ ! -d "$DIR/../.env/" ]
then
	virtualenv -p python3 $DIR/../.env
    if [ -f "$DIR/../requirements.txt" ]
    then
        source .env/bin/activate
        pip install -r requirements.txt
    fi
fi
cd $DIR/../

# Loading local variables.
ls $DIR/../.environment >/dev/null 2>&1 && . $DIR/../.environment

# Activate virtual environment.
source .env/bin/activate

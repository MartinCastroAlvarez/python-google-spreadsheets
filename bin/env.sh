#!/bin/bash
clear
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ ! -d "$DIR/../.env/" ]
then
	virtualenv -p python3 $DIR/../.env
fi
cd $DIR/../
source .env/bin/activate

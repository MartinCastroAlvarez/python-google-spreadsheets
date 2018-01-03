#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cat $DIR/../README.md | head -1 | awk '{print $2}'

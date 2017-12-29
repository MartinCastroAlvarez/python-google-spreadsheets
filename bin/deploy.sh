#!/bin/bash
ENVIRONMENT=$1
echo $ENVIRONMENT
if [ $ENVIRONMENT == "DEV" ]
then
    echo "Deploying to DEV..."
elif [ $ENVIRONMENT == "PROD" ]
then
    echo "Deploying to PROD..."
else
    echo "Not deploying :("
fi

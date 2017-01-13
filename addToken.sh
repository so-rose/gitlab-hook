#!/bin/bash

#Adds a token passed in as $2 to the repo $1. Call with sudo.

TOKEN="$2"
REPO_NAME="$1"

echo "$TOKEN" > "/opt/git-repos/token_${REPO_NAME}"

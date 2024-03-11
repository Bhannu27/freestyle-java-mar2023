#!/bin/bash
TOKEN=$1
ORG="Sanofi-GitHub"
Team_ID="chc-admins"
RESULTS_FILE="repo_list.csv"
page=1
per_page=100
total_pages=20
repo_list=""
COUNT=1000
while [[ $page -le $total_pages ]]; do
    response=$(gh repo list $ORG  -L $COUNT --topic chc --json name --jq '.[].name')
    total_repos=$(echo "$response" | wc -l)
    if [[ $total_repos -lt $per_page ]]; then
        break
    fi
    ((page++))
done
echo "$response" > "$RESULTS_FILE"
#| grep -i "^CHC-" > "$RESULTS_FILE"
cat $RESULTS_FILE

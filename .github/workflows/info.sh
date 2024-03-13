#!/bin/bash

# Read the input type from the file
DIRSCRIPT=$(dirname "$0")
input_file="$DIRSCRIPT/type.txt"
name_file="$DIRSCRIPT/name.txt"
TOKEN=$1

# Check if the input file exists
if [ ! -f "$input_file" ]; then
  echo "Error: Input file $input_file not found."
  exit 1
fi
# Check if the name file exists
if [ ! -f "$name_file" ]; then
  echo "Error: Input file $input_file not found."
  exit 1
fi

# Read the type value from the input file and remove spaces and empty lines
type=$(<"$input_file" tr -d '[:space:]')
name=$(<"$name_file" tr -d '[:space:]')

# Log file to store the response
log_file="$DIRSCRIPT/response.log"

# Print the URL to check if it is formed correctly
url="https://eu.messaging.cloud.tibco.com/tcm/v1/system/ems/$type/$name"
echo "URL: $url"

# Check if the authorization header is provided as the first argument when running the script
if [ -z "$1" ]; then
  echo "Error: Authorization header is missing. Please provide it as the first argument when running the script."
  exit 1
fi

# Perform the GET request and append the response to the log file
#response=$(curl -s -X GET "$url" -H "accept: application/json" -H "Authorization: Bearer $Token")
    response=$(curl -X 'GET' \
      "https://eu.messaging.cloud.tibco.com/tcm/v1/system/ems/$type/$name" \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer '$TOKEN'' 2>/dev/null)
#response=$(curl -s -X GET "$url" -H "accept: application/json" -H "Authorization: Bearer '$TOKEN'")
#Bearer '$TOKEN'
# Print the response
echo "$response"

# Empty the log file
> "$log_file"

# Append the response to the log file
echo "$response" >> "$log_file"
echo "Response:" >> "$log_file"
echo "$response" | jq '.' >> "$log_file"

echo "Response copied to $log_file"

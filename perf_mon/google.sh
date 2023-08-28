#!/bin/bash

search_google() {
    local api_key="$1"
    local cse_id="$2"
    local query="$3"

    local url="https://www.googleapis.com/customsearch/v1"
    local response_file="response.json"

    # Making the GET request using curl
    curl -s -o "$response_file" -w "%{http_code}" -G "$url" \
        -d "key=$api_key" \
        -d "cx=$cse_id" \
        -d "q=$query" > status_code.txt

    local status_code=$(cat status_code.txt)
    rm status_code.txt

    # Check if the status code is 200
    if [ "$status_code" -eq 200 ]; then
        cat "$response_file"
    else
        echo "None"
    fi

    rm "$response_file"
}

# Usage:
# search_google "YOUR_API_KEY" "YOUR_CSE_ID" "YOUR_QUERY"

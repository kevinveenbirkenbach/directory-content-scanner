#!/bin/bash

# Check if a directory argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

DIR="$1"

# Ensure the directory exists
if [ ! -d "$DIR" ]; then
    echo "Error: $DIR is not a valid directory."
    exit 1
fi

# Recursive function to scan folders and print file paths and content
function scan_and_print() {
    local dir="$1"
    for item in "$dir"/*; do
        if [ -d "$item" ]; then
            scan_and_print "$item"
        elif [ -f "$item" ]; then
            echo "======== File Path: $item ========"
            cat "$item"
            echo -e "\n==================================\n"
        fi
    done
}

# Start the scan from the given directory
scan_and_print "$DIR"

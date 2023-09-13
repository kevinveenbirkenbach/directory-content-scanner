#!/bin/bash

# Check if at least one directory argument is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <directory1> [<directory2> ...]"
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

# Loop through all provided directories and start the scan
for DIR in "$@"; do
    # Ensure the directory exists
    if [ ! -d "$DIR" ]; then
        echo "Error: $DIR is not a valid directory."
        exit 1
    fi

    scan_and_print "$DIR"
done

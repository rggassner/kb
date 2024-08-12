#!/bin/bash

# Directory containing the files
DIRECTORY=$1

# Variables to store the total time difference and count of time differences
total_diff=0
count=0

# Get a sorted list of files by modification time (oldest first)
files=$(ls -t --time-style="+%Y-%m-%d %H:%M:%S" "$DIRECTORY")

# Convert the sorted list to an array
file_array=($files)

# Loop through the array of files
for (( i=0; i<${#file_array[@]}-1; i++ )); do
    # Get the modification times of the current and next file
    mod_time1=$(stat -c %y "${DIRECTORY}/${file_array[$i]}")
    mod_time2=$(stat -c %y "${DIRECTORY}/${file_array[$i+1]}")

    # Convert modification times to seconds since 1970-01-01 00:00:00 UTC
    timestamp1=$(date -d "$mod_time1" +%s)
    timestamp2=$(date -d "$mod_time2" +%s)

    # Calculate the absolute difference between the two timestamps
    diff=$((timestamp2 - timestamp1))
    if [ "$diff" -lt 0 ]; then
        diff=$((-$diff))
    fi

    # Add the difference to the total difference
    total_diff=$((total_diff + diff))
    count=$((count + 1))
done

# Calculate the average difference
if [ "$count" -ne 0 ]; then
    avg_diff=$((total_diff / count))
    echo "Average time difference: $avg_diff seconds"
else
    echo "No valid time differences found."
fi

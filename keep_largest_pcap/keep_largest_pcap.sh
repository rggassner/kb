#!/bin/bash

# Configuration
INTERFACE="eth0"                # Network interface to capture from
CAPTURE_DURATION=60             # Capture duration in seconds
CAPTURE_DIR="/var/log/tcpdump"  # Directory to store capture files
MAX_FILES=5                     # Number of largest files to retain
TIMESTAMP_FORMAT="+%Y%m%d_%H%M%S"

# Ensure capture directory exists
mkdir -p "$CAPTURE_DIR"

while true; do
    TIMESTAMP=$(date "$TIMESTAMP_FORMAT")
    FILE="$CAPTURE_DIR/capture_$TIMESTAMP.pcap"

    echo "Starting capture: $FILE for $CAPTURE_DURATION seconds..."

    # Start full-payload capture (-s 0), stop after timeout
    timeout "$CAPTURE_DURATION" tcpdump -nn -i "$INTERFACE" -s 0 -w "$FILE"

    echo "Capture complete. Evaluating file sizes..."

    # Count current number of .pcap files
    FILE_COUNT=$(find "$CAPTURE_DIR" -maxdepth 1 -name 'capture_*.pcap' | wc -l)

    if [ "$FILE_COUNT" -gt "$MAX_FILES" ]; then
        # Delete smallest files, keeping only the MAX_FILES largest
        find "$CAPTURE_DIR" -maxdepth 1 -name 'capture_*.pcap' -type f -printf '%s %p\n' \
            | sort -n \
            | head -n $((FILE_COUNT - MAX_FILES)) \
            | cut -d' ' -f2- \
            | xargs -r rm -v
    fi

    echo "Retention complete. Waiting 1 second before next cycle..."
    sleep 1
done

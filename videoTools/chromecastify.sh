#!/bin/bash
#
# Chromecast-Compatible Video Converter
# -------------------------------------
# Converts any input video file into an MP4 container encoded with
# H.264 (libx264) video and AAC audio — the most widely supported
# format for Chromecast devices.
#
# Usage:
#   ./convert_to_mp4.sh <input-file>
#
# Example:
#   ./convert_to_mp4.sh movie.mkv
#   # Produces: movie.mp4
#
# Features:
#   - Automatically derives the output filename by replacing the
#     original extension with .mp4.
#   - Ensures Chromecast-friendly encoding:
#       * Video: H.264 (libx264), preset=fast, CRF 23
#       * Audio: AAC 192 kbps
#       * Enabled +faststart for faster playback on streaming devices.
#
# Requirements:
#   - ffmpeg must be installed and available in $PATH.
#
# Notes:
#   - The script does not overwrite existing files unless explicitly
#     allowed by ffmpeg.
#   - Most audio/video codecs supported by ffmpeg can be converted.
#
# Author:
#   https://github.com/rggassner
#

# --- SAFETY CHECKS ---
if [ -z "$1" ]; then
    echo "Usage: $0 <input-file>"
    exit 1
fi

INPUT="$1"

# Extract filename without extension
BASENAME="${INPUT%.*}"

# Output file with .mp4 extension
OUTPUT="${BASENAME}.mp4"

# --- RUN FFMPEG ---
ffmpeg -i "$INPUT" \
    -c:v libx264 -preset fast -crf 23 \
    -c:a aac -b:a 192k \
    -movflags +faststart \
    "$OUTPUT"

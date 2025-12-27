#!/bin/bash
#
# Chromecast-Compatible Video Converter (CUDA / NVENC)
# ----------------------------------------------------
# Converts any input video into an MP4 container encoded with
# H.264 (NVENC) video and AAC audio — Chromecast friendly,
# but GPU-accelerated.
#
# Usage:
#   ./convert_to_mp4_cuda.sh <input-file>
#
# Example:
#   ./convert_to_mp4_cuda.sh movie.mkv
#   # Produces: movie.mp4
#
# Requirements:
#   - NVIDIA GPU
#   - NVIDIA drivers installed
#   - ffmpeg compiled with --enable-nvenc
#

# --- SAFETY CHECKS ---
if [ -z "$1" ]; then
    echo "Usage: $0 <input-file>"
    exit 1
fi

INPUT="$1"
BASENAME="${INPUT%.*}"
OUTPUT="${BASENAME}-chromecast.mp4"

# --- RUN FFMPEG (CUDA / NVENC) ---
ffmpeg -hwaccel cuda -i "$INPUT" \
    -c:v h264_nvenc \
    -preset p4 \
    -rc vbr \
    -cq 23 \
    -profile:v high \
    -pix_fmt yuv420p \
    -c:a aac -b:a 192k \
    -movflags +faststart \
    "$OUTPUT"

#!/bin/bash
#
# Chromecast-Compatible Video Converter (CUDA / NVENC)
# ----------------------------------------------------
# - H.264 NVENC video
# - AAC audio
# - Interactive audio track selection
# - Approximate output size targeting (GB, default 2GB)
#

# --- SAFETY CHECKS ---
if [ -z "$1" ]; then
    echo "Usage: $0 <input-file>"
    exit 1
fi

INPUT="$1"
BASENAME="${INPUT%.*}"
OUTPUT="${BASENAME}-chromecast.mp4"

# --- ASK FOR TARGET SIZE (GB, DEFAULT 2) ---
read -p "Desired output file size in GB [default: 2]: " TARGET_GB
TARGET_GB="${TARGET_GB:-2}"

if ! [[ "$TARGET_GB" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
    echo "❌ Invalid size."
    exit 1
fi

# --- GET DURATION (SECONDS) ---
DURATION=$(ffprobe -v error \
    -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 \
    "$INPUT")

DURATION=${DURATION%.*}

if [ "$DURATION" -le 0 ]; then
    echo "❌ Could not determine duration."
    exit 1
fi

# --- BITRATE CALCULATION ---
# total_bits = GB * 8 * 1024^3
TOTAL_BITS=$(awk "BEGIN { printf \"%.0f\", $TARGET_GB * 8 * 1024 * 1024 * 1024 }")

TOTAL_BR=$(( TOTAL_BITS / DURATION ))

# subtract audio bitrate (192k)
AUDIO_BR=192000
VIDEO_BR=$(( TOTAL_BR - AUDIO_BR ))

# safety floor
if [ "$VIDEO_BR" -lt 500000 ]; then
    VIDEO_BR=500000
fi

echo
echo "🎯 Target size: ${TARGET_GB} GB"
echo "⏱ Duration: ${DURATION}s"
echo "🎥 Video bitrate ≈ $(( VIDEO_BR / 1000 )) kbps"
echo

# --- COLLECT AUDIO STREAM INFO ---
mapfile -t AUDIO_STREAMS < <(
    ffprobe -v error \
        -select_streams a \
        -show_entries stream=index,codec_name,channels:stream_tags=language \
        -of csv=p=0 "$INPUT"
)

AUDIO_COUNT="${#AUDIO_STREAMS[@]}"

if [ "$AUDIO_COUNT" -eq 0 ]; then
    echo "❌ No audio streams found."
    exit 1
fi

# --- AUDIO SELECTION ---
if [ "$AUDIO_COUNT" -eq 1 ]; then
    SELECTED_STREAM_INDEX="$(echo "${AUDIO_STREAMS[0]}" | cut -d',' -f1)"
    echo "✔ Single audio track detected (stream #$SELECTED_STREAM_INDEX)"
else
    echo "🎧 Multiple audio tracks detected:"
    echo

    i=0
    for stream in "${AUDIO_STREAMS[@]}"; do
        IFS=',' read -r index codec channels lang <<< "$stream"
        lang="${lang:-und}"
        echo "[$i] stream:#$index | lang:$lang | codec:$codec | channels:$channels"
        ((i++))
    done

    echo
    read -p "Choose audio track [0-$((AUDIO_COUNT - 1))]: " CHOICE

    if ! [[ "$CHOICE" =~ ^[0-9]+$ ]] || [ "$CHOICE" -ge "$AUDIO_COUNT" ]; then
        echo "❌ Invalid selection."
        exit 1
    fi

    SELECTED_STREAM_INDEX="$(echo "${AUDIO_STREAMS[$CHOICE]}" | cut -d',' -f1)"
fi

echo "🎬 Using audio stream #$SELECTED_STREAM_INDEX"
echo

# --- RUN FFMPEG ---
ffmpeg -hwaccel cuda -i "$INPUT" \
    -map 0:v:0 \
    -map 0:"$SELECTED_STREAM_INDEX" \
    -c:v h264_nvenc \
    -b:v "$VIDEO_BR" \
    -maxrate "$VIDEO_BR" \
    -bufsize "$(( VIDEO_BR * 2 ))" \
    -preset p4 \
    -profile:v high \
    -pix_fmt yuv420p \
    -c:a aac -b:a 192k \
    -movflags +faststart \
    "$OUTPUT"

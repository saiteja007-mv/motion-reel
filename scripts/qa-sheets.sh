#!/usr/bin/env bash
# Build the critique sheets for a rendered film (same output as qa-sheets.ps1).
#   scripts/qa-sheets.sh films/<slug>/out/final.mp4 [AT_SECONDS] [--loop]
# Writes <video dir>/qa/contact.png (2 fps), phone.png (360 px wide), strip.png (12 frames from AT-0.1 s)
# and, with --loop, loop_check.mp4.
set -euo pipefail
video=$1
at=${2:--1}
loop=${3:-}
qa="$(dirname "$video")/qa"
mkdir -p "$qa"

ffmpeg -v error -y -i "$video" -vf "fps=2,scale=270:-1,tile=6x5" -frames:v 1 "$qa/contact.png"
ffmpeg -v error -y -i "$video" -vf "fps=1,scale=360:-1,tile=5x3" -frames:v 1 "$qa/phone.png"
if [ "$at" != "-1" ]; then
  ss=$(awk -v a="$at" 'BEGIN { s = a - 0.1; print (s < 0 ? 0 : s) }')
  ffmpeg -v error -y -ss "$ss" -i "$video" -vf "scale=320:-1,tile=12x1" -frames:v 1 "$qa/strip.png"
fi
if [ "$loop" = "--loop" ]; then
  ffmpeg -v error -y -stream_loop 1 -i "$video" -c copy "$qa/loop_check.mp4"
fi
ls -1 "$qa"

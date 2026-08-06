#!/bin/bash
set -euo pipefail

SITE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SITE_DIR"

MEDIA_LIST="$(mktemp)"
trap 'rm -f "$MEDIA_LIST"' EXIT

rg -o 'assets/[A-Za-z0-9_./ -]+\.(png|jpg|jpeg|gif|mp4)' --glob '*.html' \
  | sed 's/^[^:]*://' \
  | sort -u > "$MEDIA_LIST"

image_dimensions() {
  local input="$1"
  local width height
  width="$(sips -g pixelWidth "$input" 2>/dev/null | awk '/pixelWidth/ {print $2}')"
  height="$(sips -g pixelHeight "$input" 2>/dev/null | awk '/pixelHeight/ {print $2}')"
  printf '%s %s' "${width:-0}" "${height:-0}"
}

optimized_dimensions() {
  local input="$1"
  local max_dimension="$2"
  local width height
  read -r width height <<< "$(image_dimensions "$input")"
  if (( width > max_dimension || height > max_dimension )); then
    if (( width >= height )); then
      printf '%s 0' "$max_dimension"
    else
      printf '0 %s' "$max_dimension"
    fi
  else
    printf '0 0'
  fi
}

encode_still() {
  local input="$1" output="$2" quality="$3" resize_width="$4" resize_height="$5"
  local normalized
  if (( resize_width > 0 || resize_height > 0 )); then
    if cwebp -quiet -mt -m 6 -q "$quality" -alpha_q 100 -sharp_yuv \
      -resize "$resize_width" "$resize_height" "$input" -o "$output"; then
      return
    fi
  else
    if cwebp -quiet -mt -m 6 -q "$quality" -alpha_q 100 -sharp_yuv \
      "$input" -o "$output"; then
      return
    fi
  fi

  normalized="$(mktemp -t dayekang-media).png"
  sips -s format png "$input" --out "$normalized" >/dev/null
  if (( resize_width > 0 || resize_height > 0 )); then
    cwebp -quiet -mt -m 6 -q "$quality" -alpha_q 100 -sharp_yuv \
      -resize "$resize_width" "$resize_height" "$normalized" -o "$output"
  else
    cwebp -quiet -mt -m 6 -q "$quality" -alpha_q 100 -sharp_yuv \
      "$normalized" -o "$output"
  fi
  rm -f "$normalized"
}

while IFS= read -r input; do
  [[ -f "$input" ]] || continue
  extension="${input##*.}"
  base_without_extension="${input%.*}"

  if [[ "$extension" == "mp4" ]]; then
    output="assets/optimized/${input#assets/}"
    mkdir -p "$(dirname "$output")"
    if [[ -s "$output" && "$output" -nt "$input" ]]; then
      echo "KEEP   $output"
      continue
    fi
    echo "VIDEO  $input -> $output"
    if [[ "$input" == assets/video/art_* ]]; then
      crf=21
    else
      crf=20
    fi
    ffmpeg -nostdin -y -loglevel error -i "$input" \
      -map 0:v:0 -an \
      -vf "scale='min(1280,iw)':-2:flags=lanczos" \
      -c:v libx264 -preset slow -crf "$crf" -pix_fmt yuv420p \
      -movflags +faststart "$output"
    continue
  fi

  output="assets/optimized/${base_without_extension#assets/}.webp"
  mkdir -p "$(dirname "$output")"
  if [[ -s "$output" && "$output" -nt "$input" ]]; then
    echo "KEEP   $output"
    continue
  fi

  if [[ "$extension" == "gif" ]]; then
    echo "ANIM   $input -> $output"
    if [[ "$input" == assets/art_* ]]; then
      quality=92
    else
      quality=88
    fi
    gif2webp -quiet -mt -m 6 -lossy -q "$quality" "$input" -o "$output"
    continue
  fi

  if [[ "$input" == assets/art_* ]]; then
    quality=96
    max_dimension=3000
  else
    quality=92
    max_dimension=2400
  fi
  read -r resize_width resize_height <<< "$(optimized_dimensions "$input" "$max_dimension")"
  echo "IMAGE  $input -> $output"
  encode_still "$input" "$output" "$quality" "$resize_width" "$resize_height"
done < "$MEDIA_LIST"

echo "Optimization complete. Originals remain unchanged in assets/."

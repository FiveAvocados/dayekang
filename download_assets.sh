#!/bin/bash
# Downloads every image/PDF listed in assets_manifest.txt into assets/.
# Safe to re-run: already-downloaded files are skipped.
cd "$(dirname "$0")"
total=0; ok=0; fail=0
while IFS=$'\t' read -r name url; do
  [ -z "$name" ] && continue
  total=$((total+1))
  dest="assets/$name"
  mkdir -p "$(dirname "$dest")"
  if [ -s "$dest" ]; then ok=$((ok+1)); continue; fi
  got=0
  if curl -fsSL --retry 2 -o "$dest" "$url"; then got=1; fi
  if [ "$got" = "0" ] && echo "$url" | grep -q "video.wixstatic.com"; then
    for q in 720p 360p 1080p; do
      alt="${url/480p/$q}"
      if curl -fsSL -o "$dest" "$alt"; then got=1; echo "     ($name: used $q)"; break; fi
    done
  fi
  if [ "$got" = "1" ]; then
    ok=$((ok+1)); echo "ok   $name"
  else
    rm -f "$dest"; fail=$((fail+1)); echo "FAIL $name  <-  $url"
  fi
done < assets_manifest.txt
echo "----------------------------------------"
echo "done: $ok/$total downloaded, $fail failed"

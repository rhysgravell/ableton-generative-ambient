#!/usr/bin/env bash
# adg_tools.sh — Utilities for inspecting and repacking Ableton .adg files
#
# Usage:
#   ./adg_tools.sh inspect <file.adg>   — Pretty-print XML contents
#   ./adg_tools.sh unpack  <file.adg>   — Unpack to <file.xml>
#   ./adg_tools.sh repack  <file.xml>   — Repack to <file.adg>
#   ./adg_tools.sh diff    <a.adg> <b.adg>  — Diff two racks as XML

set -euo pipefail

inspect() {
    local file="$1"
    [[ -f "$file" ]] || { echo "File not found: $file"; exit 1; }
    gunzip -c "$file" | xmllint --format -
}

unpack() {
    local adg="$1"
    [[ -f "$adg" ]] || { echo "File not found: $adg"; exit 1; }
    local xml="${adg%.adg}.xml"
    gunzip -c "$adg" > "$xml"
    echo "Unpacked → $xml"
}

repack() {
    local xml="$1"
    [[ -f "$xml" ]] || { echo "File not found: $xml"; exit 1; }
    local adg="${xml%.xml}.adg"
    gzip -c "$xml" > "$adg"
    echo "Repacked → $adg"
}

diff_racks() {
    local a="$1" b="$2"
    [[ -f "$a" && -f "$b" ]] || { echo "Both files required"; exit 1; }
    diff <(gunzip -c "$a" | xmllint --format -) \
         <(gunzip -c "$b" | xmllint --format -) || true
}

case "${1:-}" in
    inspect) inspect "$2" ;;
    unpack)  unpack  "$2" ;;
    repack)  repack  "$2" ;;
    diff)    diff_racks "$2" "$3" ;;
    *)
        echo "Usage: $0 {inspect|unpack|repack|diff} <file(s)>"
        echo ""
        echo "  inspect <file.adg>          Pretty-print XML contents"
        echo "  unpack  <file.adg>          Unpack to <file.xml>"
        echo "  repack  <file.xml>          Repack to <file.adg>"
        echo "  diff    <a.adg> <b.adg>     Diff two racks as XML"
        ;;
esac

#!/usr/bin/env python3
"""
Assign artwork to Buried Landscapes tracks.
Reads file paths from Music app, embeds artwork directly into WAV files using mutagen.
Run with: python3 scripts/assign_artwork.py
"""

import os
import glob
import subprocess
from mutagen.id3 import ID3, APIC, ID3NoHeaderError
from mutagen.wave import WAVE

ARTWORK_FOLDER = "/Users/rhysgravell/Ableton/Artwork"
ARTIST_NAME = "Buried Landscapes"

def get_track_paths():
    """Get file paths for all Buried Landscapes tracks via AppleScript."""
    script = f'''
tell application "Music"
    set output to ""
    set theTracks to every track of library playlist 1 whose artist is "{ARTIST_NAME}"
    repeat with t in theTracks
        try
            set output to output & (POSIX path of (location of t as text)) & "\\n"
        end try
    end repeat
    return output
end tell
'''
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    paths = [p.strip() for p in result.stdout.strip().split('\n') if p.strip()]
    return paths

def get_images():
    """Get sorted list of image files from artwork folder."""
    images = sorted(
        glob.glob(os.path.join(ARTWORK_FOLDER, '*.jpg')) +
        glob.glob(os.path.join(ARTWORK_FOLDER, '*.jpeg')) +
        glob.glob(os.path.join(ARTWORK_FOLDER, '*.JPG')) +
        glob.glob(os.path.join(ARTWORK_FOLDER, '*.JPEG')) +
        glob.glob(os.path.join(ARTWORK_FOLDER, '*.png')) +
        glob.glob(os.path.join(ARTWORK_FOLDER, '*.PNG'))
    )
    return images

def embed_artwork(wav_path, image_path):
    """Embed image into WAV file as ID3 artwork tag."""
    ext = os.path.splitext(image_path)[1].lower()
    mime = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'

    with open(image_path, 'rb') as f:
        image_data = f.read()

    audio = WAVE(wav_path)
    if audio.tags is None:
        audio.add_tags()

    audio.tags.add(APIC(
        encoding=3,
        mime=mime,
        type=3,
        desc='Cover',
        data=image_data
    ))
    audio.save()

def refresh_music_library(track_paths):
    """Tell Music app to refresh the modified tracks."""
    script = '''
tell application "Music"
    refresh every track of library playlist 1 whose artist is "Buried Landscapes"
end tell
'''
    subprocess.run(['osascript', '-e', script], capture_output=True)

def main():
    print(f"Looking for images in: {ARTWORK_FOLDER}")
    images = get_images()
    if not images:
        print("No images found. Exiting.")
        return
    print(f"Found {len(images)} images")

    print(f"\nFetching tracks for '{ARTIST_NAME}' from Music...")
    track_paths = get_track_paths()
    if not track_paths:
        print("No tracks found. Check the artist name in Music.app.")
        return
    print(f"Found {len(track_paths)} tracks\n")

    success = 0
    errors = 0

    for i, track_path in enumerate(track_paths):
        image_path = images[i % len(images)]
        track_name = os.path.basename(track_path)
        image_name = os.path.basename(image_path)

        if not os.path.exists(track_path):
            print(f"  SKIP  {track_name} (file not found)")
            errors += 1
            continue

        try:
            embed_artwork(track_path, image_path)
            print(f"  OK    {track_name}  ←  {image_name}")
            success += 1
        except Exception as e:
            print(f"  FAIL  {track_name}: {e}")
            errors += 1

    print(f"\nDone. {success} succeeded, {errors} failed.")
    print("\nRefreshing Music library...")
    refresh_music_library(track_paths)
    print("Refresh sent. You may need to restart Music for artwork to appear.")

if __name__ == '__main__':
    main()

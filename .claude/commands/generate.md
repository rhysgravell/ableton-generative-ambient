Generate ambient MIDI for the Buried Landscapes project.

The user may pass arguments like a key, scale, BPM, or pattern names (e.g. "/generate D dorian" or "/generate Bb minor 72bpm").

Parse whatever they pass and run the appropriate command:

```
python3 midi/generate_ambient_midi.py --key <key> --scale <scale> [--bpm <bpm>] [--patterns <patterns>]
```

Available keys: C, C#, Db, D, D#, Eb, E, F, F#, Gb, G, G#, Ab, A, A#, Bb, B
Available scales: minor, dorian, phrygian, lydian, mixolydian, major, pentatonic
Available patterns: chords, melodic, bass, arp (default: all four)

Defaults if not specified: key=G, scale=minor, bpm=80, all patterns.

After running, tell the user what files were generated and where they were saved.

Arguments: $ARGUMENTS

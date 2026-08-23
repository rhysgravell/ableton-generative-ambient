Generate ambient MIDI for the Buried Landscapes project.

The user may pass arguments like a key, scale, BPM, pattern names, or a chord progression (e.g. "/generate D dorian" or "/generate Bb minor 72bpm lament").

Parse whatever they pass and run the appropriate command:

```
python3 midi/generate_ambient_midi.py --key <key> --scale <scale> [--bpm <bpm>] [--bars <bars>] [--patterns <patterns>] [--progression <progression>] [--chord-bars <n>]
```

Available keys: C, C#, Db, D, D#, Eb, E, F, F#, Gb, G, G#, Ab, A, A#, Bb, B
Available scales: minor, dorian, phrygian, lydian, mixolydian, major, pentatonic
Available patterns: chords, melodic, bass, arp (default: all four)
Named progressions: drift, lament, descent, suspended, bloom, static — or a roman
numeral spec like `i-VI-III-VII` (a trailing 7 gives a seventh chord), or `random`.

Defaults if not specified: key=G, scale=minor, bpm=80, bars=16, all patterns,
progression=random, chord-bars=2.

The chords, arp and bass clips all follow the same progression, so they layer in tune.

After running, tell the user what progression was used, what files were generated, and where they were saved.

Arguments: $ARGUMENTS

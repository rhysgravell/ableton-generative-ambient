Look up scale notes, diatonic chords, and related modes for the Buried Landscapes project.

The user may pass a key and scale, e.g. "/scales D dorian" or "/scales Bb major", or ask to list available scales.

Run:

```
python3 tools/scale_explorer.py [key] [scale]
```

Or, if they ask what scales are available:

```
python3 tools/scale_explorer.py --list
```

Defaults if not specified: key=G, scale=minor.

Available keys: C, C#, Db, D, D#, Eb, E, F, F#, Gb, G, G#, Ab, A, A#, Bb, B
Available scales: minor, dorian, phrygian, lydian, mixolydian, major, pentatonic

After running, present the scale notes, diatonic chords, and related modes clearly to the user.

Arguments: $ARGUMENTS

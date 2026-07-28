Generate ambient drum MIDI for the Buried Landscapes project.

The user may pass arguments like a BPM, bar count, or pattern name (e.g. "/drums sparse" or "/drums four on the floor 120bpm").

Parse whatever they pass and run the appropriate command:

```
python3 midi/generate_drums.py [--bpm <bpm>] [--bars <bars>] [--patterns <patterns>]
```

Available patterns:
  sparse         — minimal kick + rim/snare, scattered soft hats, lots of space
  four_on_floor  — steady kick on every quarter, 8th-note hat groove, backbeat snare

Defaults if not specified: bpm=80, bars=8, both patterns.

Output goes on General MIDI drum channel 10 — tell the user to drop it onto a drum rack / channel-10 instrument track.

If the user wants a looser, less quantized feel, suggest running the result through `/mutate <file> --humanize`.

After running, tell the user what files were generated and where they were saved.

Arguments: $ARGUMENTS

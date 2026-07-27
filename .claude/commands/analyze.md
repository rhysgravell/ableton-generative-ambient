Analyze MIDI file(s) for the Buried Landscapes project.

The user will name one or more MIDI files, e.g. "/analyze slow_chords_G_minor.mid" or "/analyze *.mid verbose".

If a named file isn't found as given, check `/Users/rhysgravell/MIDI/Buried_Landscapes/Claude_MIDI/` (where /generate saves files) before asking the user to clarify the path.

Run:

```
python3 midi/analyze_midi.py <files...> [--verbose]
```

Multiple files can be passed at once (space-separated or a glob). Add `--verbose` if the user asks for note distribution or a more detailed breakdown.

Reports per file: BPM, duration, bar count, note count, average duration, velocity stats, and best-fit key + scale detection.

After running, summarize the key findings for the user (don't just dump raw output) — especially anything surprising, like a detected key that doesn't match the filename.

Arguments: $ARGUMENTS

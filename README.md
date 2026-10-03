# Buried Landscapes

A generative ambient music project built around Ableton Live 12, MIDI generation scripts, and custom effect rack presets.

> *Slow evolving textures, harmonic clouds, and buried signals in G minor.*

---

## Overview

This repo contains all the tooling, scripts, configs and documentation for the Buried Landscapes project — an ambient music project exploring generative MIDI, spectral audio processing, and audiovisual performance.

---

## Structure

```
buried-landscapes/
├── midi/
│   ├── generate_ambient_midi.py    # Generative MIDI — configurable key, scale, BPM
│   ├── analyze_midi.py             # MIDI analyzer — key detection, velocity stats
│   └── mutate_midi.py              # MIDI transformer — transpose, humanize, reverse, stretch
├── tools/
│   ├── bpm_sync.py                 # Delay/LFO sync time calculator
│   └── scale_explorer.py          # Scale notes, chords, and mode relationships
├── scripts/
│   ├── organize_project.py        # Organize Ableton Ideas folder into subfolders
│   ├── assign_artwork.py          # Embed cover artwork into track WAV files
│   └── assign_artwork.applescript # Set cover artwork on tracks in Music.app
├── racks/
│   ├── scripts/
│   │   ├── generate_spectral_rack.py   # .adg rack generator
│   │   └── adg_tools.sh                # Inspect / unpack / repack .adg files
│   └── schemas/
│       └── DeepField_schema.xml        # Live 12 .adg reference schema
├── docs/
│   └── buried_landscapes_reference.md  # Full project reference
└── config/
    └── ghostty_config              # Terminal config (Ghostty)
```

---

## MIDI Generation

Generates ambient MIDI clips for any key and scale. Defaults to G minor at 80bpm.

The chord, arp and bass clips all follow **one shared chord progression**, so they layer together in tune on separate tracks in Ableton. The melody leans toward the tones of whichever chord is sounding.

### Install

```bash
pip3 install mido
```

### Run

```bash
# Defaults — G minor, 80bpm, 16 bars, all four patterns
python3 midi/generate_ambient_midi.py

# Custom key and scale
python3 midi/generate_ambient_midi.py --key D --scale dorian --bpm 72

# Specific patterns only
python3 midi/generate_ambient_midi.py --patterns chords bass

# Named progression, four bars per chord
python3 midi/generate_ambient_midi.py --progression lament --chord-bars 4

# Explicit progression in roman numerals
python3 midi/generate_ambient_midi.py --progression i-VI-III-VII

# Reproducible output
python3 midi/generate_ambient_midi.py --seed 42

# Full options
python3 midi/generate_ambient_midi.py --help
```

### Output files

Output saved to `~/MIDI/Buried_Landscapes/Claude_MIDI/`:

| File | Description |
|------|-------------|
| `slow_chords.mid` | Chord pads — one progression chord per step |
| `generative.mid` | Stepwise melodic sequence with rests, biased to chord tones |
| `bass_drone.mid` | Slow drone on the root of each chord, in a fixed low octave |
| `arp.mid` | Arpeggiated chord tones, following the progression |

### Chord progressions

`--progression` sets the harmony shared by the chord, arp and bass clips. It takes a named progression, a roman numeral spec, or `random` (the default — a weighted random walk that always starts on the tonic).

| Name | Progression | Character |
|------|-------------|-----------|
| `drift` | `i-VI` | Two-chord hover |
| `lament` | `i-VI-III-VII` | The classic minor loop |
| `descent` | `i-VII-VI-v` | Stepwise fall |
| `suspended` | `i-iv-i-v` | Unresolved, circling |
| `bloom` | `i-III-VII-iv` | Brightening, then back |
| `static` | `i` | Single-chord drone |

Roman numerals `i`–`vii` are resolved by **scale degree**, so the same spec works in any mode — the scale supplies the chord quality, and case is cosmetic. A trailing `7` asks for a seventh chord:

```bash
python3 midi/generate_ambient_midi.py --scale dorian --progression i7-iv-VII7-III
```

`--chord-bars` sets how long each step lasts (default 2). The progression loops to fill `--bars`. Steps of four bars or more move the bass from the root to the fifth halfway through.

### Available scales

`minor` · `dorian` · `phrygian` · `lydian` · `mixolydian` · `major` · `pentatonic`

Pentatonic has only five degrees, so numerals above `v` are rejected — use `random`, `static`, or a spec within `i`–`v`.

---

## MIDI Tools

### Analyze

Inspect a MIDI file — BPM, duration, note count, velocity range, and best-fit key/scale detection.

```bash
python3 midi/analyze_midi.py slow_chords.mid
python3 midi/analyze_midi.py *.mid --verbose   # includes note distribution chart
```

### Mutate

Transform an existing MIDI file. Transforms stack in a single pass.

```bash
# Transpose to a new key
python3 midi/mutate_midi.py slow_chords.mid --transpose -2

# Add subtle timing and velocity variation
python3 midi/mutate_midi.py generative.mid --humanize 0.4

# Reverse note order in time
python3 midi/mutate_midi.py generative.mid --reverse

# Time-stretch (2.0 = twice as slow, notes stay in same BPM grid)
python3 midi/mutate_midi.py arp.mid --stretch 1.5

# Stack transforms
python3 midi/mutate_midi.py slow_chords.mid --reverse --transpose 5 --humanize
```

Output defaults to `<input>_mutated.mid` alongside the source file.

---

## Music Theory Tools

### BPM Sync Calculator

Prints delay times (ms) and LFO rates (Hz) for every common note division at a given BPM. Useful for dialling in delays, reverb pre-delays, and LFO rates in Ableton.

```bash
python3 tools/bpm_sync.py          # defaults to 80 BPM
python3 tools/bpm_sync.py 90
```

### Scale Explorer

Prints scale notes with MIDI numbers and Hz values, diatonic chord chart, and parallel mode relationships for any key and scale. The Spectral Resonator root frequency is highlighted for easy reference.

```bash
python3 tools/scale_explorer.py              # G minor (default)
python3 tools/scale_explorer.py D dorian
python3 tools/scale_explorer.py Bb major
python3 tools/scale_explorer.py --list       # show all available scales
```

---

## Ableton Racks

Custom Audio Effect Rack presets for ambient sound design, built around Spectral Blur and Spectral Resonator.

### Ambient Effect Chains

| Rack | Chain | Character |
|------|-------|-----------|
| The Deep Field | Grain Delay → Spectral Blur → Spectral Resonator → Hybrid Reverb | Vast, evolving soundscape |
| Buried Signal | Redux → Spectral Blur → Filter Delay → Corpus → Reverb | Lo-fi, dusty, submerged |
| Harmonic Cloud | Spectral Resonator → Chorus Ensemble → Spectral Blur → Hybrid Reverb | Rich harmonic drone |
| Shimmer Pad | Spectral Blur → Phaser Flanger → Reverb → Filter Delay | Classic ambient shimmer |
| Field Recording Transformer | Grain Delay → Redux → Spectral Blur → Spectral Resonator → Corpus → Hybrid Reverb | Turns anything into a pad |
| Temporal Drift | Grain Delay → Pitch Hack → Spectral Blur → Reverb | Time-smeared echoes |
| Submerged | Auto Filter → Spectral Resonator → Corpus → Hybrid Reverb | Underwater quality |
| Frozen Landscape | Spectral Blur → Looper → Hybrid Reverb → Chorus Ensemble | Static, icy textures |
| Signal Decay | Redux → Vinyl Distortion → Spectral Blur → Reverb | Degraded, eroding sound |
| Breath | Auto Pan → Spectral Resonator → Filter Delay → Hybrid Reverb | Organic, living quality |
| Mineral | Corpus → Spectral Resonator → Spectral Blur → Hybrid Reverb | Hard, crystalline textures |

### Inspecting .adg files

Ableton rack presets are gzipped XML — you can read and edit them directly:

```bash
# View schema
./racks/scripts/adg_tools.sh inspect MyRack.adg

# Unpack to editable XML
./racks/scripts/adg_tools.sh unpack MyRack.adg

# Repack back to .adg
./racks/scripts/adg_tools.sh repack MyRack.xml

# Diff two racks
./racks/scripts/adg_tools.sh diff RackA.adg RackB.adg
```

---

## Project Utilities

### Organize Ableton Ideas folder

Moves each `.als` file into its own named subfolder with standard subfolders inside (`Samples/Recorded`, `Samples/Imported`, `Samples/Bounces`, `Versions`).

```bash
# Preview first
python3 scripts/organize_project.py ~/Ableton/Buried_Landscapes/Ideas --dry-run

# Apply
python3 scripts/organize_project.py ~/Ableton/Buried_Landscapes/Ideas
```

### Assign track artwork

Gives every Buried Landscapes track in Music.app a cover image from `~/Ableton/Artwork` (JPG or PNG, in alphabetical order, cycling round if there are more tracks than images).

The Python version embeds the artwork into the WAV files themselves, so it survives outside Music:

```bash
pip3 install mutagen
python3 scripts/assign_artwork.py
```

The AppleScript version only sets the artwork inside Music.app, with no dependencies:

```bash
osascript scripts/assign_artwork.applescript
```

---

## Tools & Software

| Tool | Purpose |
|------|---------|
| Ableton Live 12 Suite | DAW |
| Spectral Blur (M4L) | Frequency smearing |
| Spectral Resonator | Harmonic resonance |
| VS Visual Synthesizer | Audio-reactive generative visuals |
| Ghostty | Terminal |
| Claude Code | Rack and script generation |

---

## Visual Setup

[VS Visual Synthesizer](https://www.imaginando.pt/products/vs-visual-synthesizer) by Imaginando runs as a standalone app alongside Ableton, generating audio-reactive generative visuals from the master output. 53 procedurally generated shader materials, no routing required.

---

## Config

### Ghostty Terminal

```
font-family = "JetBrains Mono"
font-size = 13
cursor-style = block
background = #000000
foreground = #00ff00
```

Full config at `config/ghostty_config`. Apply with:

```bash
cp config/ghostty_config ~/.config/ghostty/config
```

---

## Notes

- MIDI output to `~/MIDI/Buried_Landscapes/Claude_MIDI/`
- Rack presets saved to `~/Music/Ableton/User Library/Audio-effect-racks/Ambience/`
- Ableton project files at `~/Ableton/Buried_Landscapes/`

---

*Built with Claude — [anthropic.com](https://anthropic.com)*

# Buried Landscapes — Project Reference

A working reference for the Buried Landscapes ambient music project.
All commands are for macOS Terminal unless otherwise noted.

---

## Table of Contents

1. [Project Folder Structure](#project-folder-structure)
2. [MIDI Generation](#midi-generation)
3. [Ableton Rack Generation](#ableton-rack-generation)
4. [Ambient Effect Chains](#ambient-effect-chains)
5. [Ghostty Terminal Config](#ghostty-terminal-config)
6. [Ableton .adg Schema Notes](#ableton-adg-schema-notes)
7. [VS Visual Synthesizer](#vs-visual-synthesizer)

---

## Project Folder Structure

```
~/MIDI/
└── Buried_Landscapes/
    ├── Claude_MIDI/          ← Generated MIDI files
    ├── Progressions/         ← Chord progressions
    └── 01 - C Major - A Minor/  ← Key reference folders

~/Music/Ableton/
└── User Library/
    └── Audio-effect-racks/
        └── Ambience/         ← Saved rack presets
```

### Organise Ableton Ideas Folder

Puts each `.als` file into its own named subfolder with standard subfolders inside:

```bash
IDEAS="/Users/rhysgravell/Ableton/Buried_Landscapes/Ideas"

for als in "$IDEAS"/*.als; do
  [ -f "$als" ] || continue
  name=$(basename "$als" .als)
  folder="$IDEAS/$name"
  mkdir -p "$folder/Samples/Recorded" "$folder/Samples/Imported" "$folder/Samples/Bounces" "$folder/Versions"
  mv "$als" "$folder/$name.als"
  echo "Moved: $name"
done

echo "Done!"
```

---

## MIDI Generation

**Install dependency:**

```bash
pip3 install mido
```

**Run the generator:**

```bash
python3 ~/Downloads/generate_ambient_midi.py
```

Output saved to: `~/MIDI/Buried_Landscapes/Claude_MIDI/`

### Generator Settings

| Parameter | Value |
|-----------|-------|
| BPM | 80 |
| Key | G minor |
| Bars | 16 |
| Scale | G natural minor (G A Bb C D Eb F) |

### Output Files

| File | Description |
|------|-------------|
| `slow_chords.mid` | Slow evolving chord pads, 1–2 bar chords, velocity 40–65 |
| `generative.mid` | Stepwise melodic sequence with rests, slow note lengths |

### G Minor Chord Set

```python
CHORDS = [
    [55, 58, 62],       # Gm
    [58, 62, 65],       # Bb
    [60, 63, 67],       # Cm
    [57, 60, 65],       # F (VII)
    [62, 65, 69],       # Dm
    [63, 67, 70],       # Eb
    [55, 58, 62, 67],   # Gm7
    [60, 63, 67, 70],   # Cm7
]
```

---

## Ableton Rack Generation

### Inspect an existing .adg file

Ableton `.adg` files are **gzipped XML**. To read the schema:

```bash
cat "/Users/rhysgravell/Music/Ableton/User Library/Audio-effect-racks/Ambience/The Deep Field.adg" | gunzip
```

### Save schema to a readable XML file

```bash
cat "/Users/rhysgravell/Music/Ableton/User Library/Audio-effect-racks/Ambience/The Deep Field.adg" \
  | gunzip > ~/Desktop/DeepField_schema.xml
```

### Open in VS Code

```bash
code ~/Desktop/DeepField_schema.xml
```

### Generate a .adg file from Python

```python
import gzip

ADG_XML = '''<?xml version="1.0" encoding="UTF-8"?>
<Ableton MajorVersion="5" MinorVersion="12.x.x" ...>
  ...
</Ableton>'''

with gzip.open('MyRack.adg', 'wb') as f:
    f.write(ADG_XML.strip().encode('utf-8'))
```

> ⚠️ The schema must exactly match your Ableton version or the rack will be rejected (shown as a circle with a line through it). Always use a real exported `.adg` as a reference template.

### Use Claude Code to generate racks

```bash
cd "/Users/rhysgravell/Music/Ableton/User Library/Audio-effect-racks/Ambience"
claude
```

Then prompt:
> "I have a reference file called 'The Deep Field.adg'. Use it as a template to generate these ambient effect racks for Ableton Live 12: [rack name and device chain]"

---

## Ambient Effect Chains

All chains use stock Ableton Live 12 Suite devices unless noted.

### The Deep Field
*Turns anything into a vast, slowly evolving soundscape*
```
Grain Delay → Spectral Blur → Spectral Resonator → Hybrid Reverb → Utility
```
| Device | Key Settings |
|--------|-------------|
| Grain Delay | Small grain size, high spray, low pitch |
| Spectral Blur | Smear mode, Blur 60%, Decay 75%, Halo 0.75 |
| Spectral Resonator | Freq 98Hz (G2), Wander mode, Decay 800ms, Mix 50% |
| Hybrid Reverb | Large hall IR, Decay 8s+, high diffusion |
| Utility | Trim output gain |

---

### Buried Signal
*Lo-fi, dusty, half-submerged quality*
```
Redux → Spectral Blur → Filter Delay → Corpus → Reverb
```
| Device | Key Settings |
|--------|-------------|
| Redux | 18–20 bit, subtle grit |
| Spectral Blur | Smear mode |
| Filter Delay | Long delay times, low feedback |
| Corpus | String or Tube mode, tuned to G |
| Reverb | High diffusion, dark tone |

---

### Harmonic Cloud
*Rich, tuned harmonic wash — great for drone work*
```
Spectral Resonator → Chorus Ensemble → Spectral Blur → Hybrid Reverb
```
| Device | Key Settings |
|--------|-------------|
| Spectral Resonator | First in chain this time, tuned to G |
| Chorus Ensemble | Very slow, wide stereo spread |
| Spectral Blur | Smear mode |
| Hybrid Reverb | Long tail |

---

### Shimmer Pad
*Classic ambient shimmer, pitched reverb feel*
```
Spectral Blur → Phaser Flanger → Reverb → Filter Delay → Utility
```
| Device | Key Settings |
|--------|-------------|
| Spectral Blur | Smear mode |
| Phaser Flanger | Phaser mode, very slow LFO |
| Reverb | Freeze-adjacent long tail |
| Filter Delay | High-passed delays only, adds air |

---

### Field Recording Transformer
*Drop in any field recording and it becomes a pad*
```
Grain Delay → Redux → Spectral Blur → Spectral Resonator → Corpus → Hybrid Reverb
```
> Most extreme chain — Grain Delay destroys original rhythm, Spectral devices transform it into pure texture. Great with wind, water, or forest recordings.

---

### Temporal Drift
*Plays with time and pitch*
```
Grain Delay → Pitch Hack → Spectral Blur → Reverb
```
Grain Delay with long delays and random pitch creates cascading time-smeared echoes.

---

### Submerged
*Deep underwater quality*
```
Auto Filter → Spectral Resonator → Corpus → Hybrid Reverb
```
Auto Filter in LFO mode slowly opens and closes. Corpus on Tube mode.

---

### Frozen Landscape
*Static, icy textures*
```
Spectral Blur → Looper (frozen) → Hybrid Reverb → Chorus Ensemble
```
Freeze a moment in time and let it bloom outwards.

---

### Signal Decay
*Degraded, eroded sound — things disintegrating*
```
Redux → Vinyl Distortion → Spectral Blur → Reverb → Utility
```

---

### Breath
*Organic, living quality*
```
Auto Pan → Spectral Resonator → Filter Delay → Hybrid Reverb
```
Auto Pan at very slow rate creates gentle inhale/exhale movement.

---

### Mineral
*Hard, crystalline textures*
```
Corpus → Spectral Resonator → Spectral Blur → Hybrid Reverb
```
Corpus first this time — resonating the signal before blurring.

---

## Spectral Blur + Resonator Tips

> These two devices are the core of the Buried Landscapes sound design toolkit.

**How Spectral Blur works:** Processes audio in the frequency domain rather than in time, smearing individual frequencies together into a cloud. The Halo parameter creates a shimmery aura around the sound.

**How Spectral Resonator works:** Adds resonant harmonics tuned to a base frequency. Wander mode slowly drifts the resonant frequencies for an organic, living quality.

**Together:** Any source material — percussive hits, field recordings, synth tones — gets smeared into a frequency cloud, then harmonically tuned to G minor. Instant ambient pad from anything.

**Modulation to add manually in Ableton:**
- LFO (Max for Live) → Spectral Blur Blur Amount, rate ~0.1Hz, depth ~20%
- Clip Velocity → Blur Amount (right-click > Edit Modulation)

---

## Ghostty Terminal Config

Config file location: `~/.config/ghostty/config`

```bash
# View current config
cat ~/.config/ghostty/config

# Edit directly
nano ~/.config/ghostty/config

# Reload without restarting
# Press: Cmd+Shift+,
```

### Current Config

```
# Font
font-family = "JetBrains Mono"
font-size = 13
font-feature = calt
font-feature = liga

# Cursor
cursor-style = block
cursor-style-blink = true

# Colours — Black & Green
background = #000000
foreground = #00ff00
selection-background = #44475a
selection-foreground = #00ff00

# Window
window-padding-x = 12
window-padding-y = 12
window-decoration = true
```

### Install JetBrains Mono (if not installed)

```bash
brew install --cask font-jetbrains-mono
```

---

## VS Visual Synthesizer

**By:** Imaginando  
**Price:** ~€129  
**Download:** [imaginando.pt](https://www.imaginando.pt/products/vs-visual-synthesizer)  
**Mac Requirements:** macOS 11.0+, 64-bit DAW (VST/VST3/AU), 1GB disk space

### Setup in Ableton

1. Run VS as a **standalone app** alongside Ableton — it listens to system audio directly, no routing needed
2. Or load as a **VST instrument** on a MIDI track and sidechain audio into it

### What it does

- 53 procedurally generated shader materials
- Reacts to audio and MIDI in real time
- Playlist mode: presets play back in sequence with fade transitions
- Great for ambient — geometric loops, slow evolving patterns

---

## Ableton .adg Schema Notes

> Interesting discovery: all Ableton device racks are gzipped XML files!

- `.adg` = Audio Device Group (gzipped XML)
- `.als` = Ableton Live Set (also gzipped XML)
- `.alc` = Ableton Live Clip (also gzipped XML)

You can inspect, version control, diff, and programmatically generate any of these using standard XML tools. This opens up possibilities like:

- Generating rack presets with code (Claude Code)
- Diffing two versions of a project to see what changed
- Batch-modifying device parameters across multiple racks
- Building your own rack preset library tooling

### Useful commands

```bash
# Inspect any Ableton file
cat myfile.adg | gunzip | xmllint --format -

# Save as readable XML
cat myfile.adg | gunzip > myfile.xml

# Repack XML back to .adg
gzip -c myfile.xml > myfile.adg
```

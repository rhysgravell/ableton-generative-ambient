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
├── README.md
├── midi/
│   └── generate_ambient_midi.py     # Generative MIDI script (G minor, 80bpm)
├── racks/
│   ├── generate_spectral_rack.py    # .adg rack generator script
│   └── DeepField_schema.xml         # Live 12 .adg reference schema
├── docs/
│   └── buried_landscapes_reference.md  # Full project reference
└── config/
    └── ghostty_config               # Terminal config (Ghostty)
```

---

## MIDI Generation

Generates ambient MIDI clips in G minor at 80bpm — slow evolving chords and generative melodic sequences.

### Setup

```bash
pip3 install mido
```

### Run

```bash
python3 midi/generate_ambient_midi.py
```

Output saved to `~/MIDI/Buried_Landscapes/Claude_MIDI/`:

| File | Description |
|------|-------------|
| `slow_chords.mid` | Slow evolving chord pads, 1–2 bar chords |
| `generative.mid` | Stepwise melodic sequence with rests |

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
cat MyRack.adg | gunzip | xmllint --format -

# Save as XML
cat MyRack.adg | gunzip > MyRack.xml

# Repack to .adg
gzip -c MyRack.xml > MyRack.adg
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

- All MIDI in G minor, 80bpm
- Rack presets saved to `~/Music/Ableton/User Library/Audio-effect-racks/Ambience/`
- MIDI output to `~/MIDI/Buried_Landscapes/Claude_MIDI/`
- Ableton project files at `/Users/rhysgravell/Ableton/Buried_Landscapes/`

---

*Built with Claude — [anthropic.com](https://anthropic.com)*

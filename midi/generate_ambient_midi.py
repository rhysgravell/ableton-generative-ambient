#!/usr/bin/env python3
"""
Buried Landscapes — Generative MIDI

Generates ambient MIDI clips with configurable key, scale, BPM, and pattern types.

Install: pip3 install mido

Usage:
  python3 midi/generate_ambient_midi.py                            # G minor, 80bpm, 16 bars, all 4 patterns
  python3 midi/generate_ambient_midi.py --key D --scale dorian
  python3 midi/generate_ambient_midi.py --bpm 60 --bars 32
  python3 midi/generate_ambient_midi.py --patterns chords melodic  # only these two
  python3 midi/generate_ambient_midi.py --seed 42                  # reproducible output
  python3 midi/generate_ambient_midi.py --output ~/Desktop

Patterns:
  chords   — slow chord pads, 1–2 bar sustains
  melodic  — stepwise melody with rests
  bass     — very slow root/fifth drone in low register
  arp      — slow arpeggiated chord sequence

Outputs to ~/MIDI/Buried_Landscapes/Claude_MIDI/ by default.
"""

import os
import random
import argparse
import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage


# ---------------------------------------------------------------------------
# Scale definitions — semitone intervals from root
# ---------------------------------------------------------------------------

SCALES = {
    "minor":      [0, 2, 3, 5, 7, 8, 10],   # natural minor / aeolian
    "dorian":     [0, 2, 3, 5, 7, 9, 10],
    "phrygian":   [0, 1, 3, 5, 7, 8, 10],
    "lydian":     [0, 2, 4, 6, 7, 9, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "major":      [0, 2, 4, 5, 7, 9, 11],
    "pentatonic": [0, 3, 5, 7, 10],         # minor pentatonic
}

ROOT_NOTES = {
    "C": 48, "C#": 49, "Db": 49, "D": 50, "D#": 51, "Eb": 51,
    "E": 52, "F": 53, "F#": 54, "Gb": 54, "G": 55, "G#": 56,
    "Ab": 56, "A": 57, "A#": 58, "Bb": 58, "B": 59,
}


def build_scale(root: int, intervals: list, octaves: int = 3) -> list:
    """MIDI notes for a scale across multiple octaves."""
    notes = []
    for oct in range(octaves):
        for iv in intervals:
            n = root + oct * 12 + iv
            if 0 <= n <= 127:
                notes.append(n)
    return notes


def build_chords(root: int, intervals: list) -> list:
    """
    Derive diatonic triads and 7th chords by stacking every-other scale degree.
    Uses a 2-octave extended scale so wrapping degrees stay in the upper octave.
    Returns a flat list of [triad, 7th, triad, 7th, ...] for each scale degree.
    """
    n = len(intervals)
    # 2-octave extended scale: degree i lives at intervals[i % n] + (i // n)*12
    ext = [root + intervals[i % n] + (i // n) * 12 for i in range(n * 2)]

    chords = []
    for deg in range(n):
        triad   = [ext[deg], ext[deg + 2], ext[deg + 4]]
        seventh = triad + [ext[deg + 6]]
        chords.append(triad)
        chords.append(seventh)
    return chords


# ---------------------------------------------------------------------------
# Core MIDI helpers
# ---------------------------------------------------------------------------

def events_to_track(events: list, tempo: int) -> MidiTrack:
    """(abs_tick, 'on'|'off', note, velocity) list → MidiTrack."""
    # 'off' < 'on' alphabetically, so note_offs sort before note_ons at same tick
    events = sorted(events, key=lambda e: (e[0], e[1]))
    track = MidiTrack()
    track.append(MetaMessage("set_tempo", tempo=tempo, time=0))
    prev_t = 0
    for abs_t, etype, note, velocity in events:
        delta = abs_t - prev_t
        msg_type = "note_on" if etype == "on" else "note_off"
        track.append(Message(msg_type, note=note, velocity=velocity, time=delta))
        prev_t = abs_t
    return track


def save_mid(events: list, tempo: int, tpb: int, path: str) -> None:
    mid = MidiFile(ticks_per_beat=tpb)
    mid.tracks.append(events_to_track(events, tempo))
    mid.save(path)


# ---------------------------------------------------------------------------
# Pattern generators
# ---------------------------------------------------------------------------

def make_slow_chords(chords, bars, bar_ticks, tpb, tempo, out_dir) -> str:
    """Slow chord pads — each chord held for 1 or 2 bars."""
    events = []
    bar = 0
    while bar < bars:
        chord = random.choice(chords)
        dur_bars = min(random.choice([1, 1, 2]), bars - bar)
        t = bar * bar_ticks
        dur_ticks = dur_bars * bar_ticks
        vel = random.randint(40, 65)
        for note in chord:
            events.append((t, "on", note, vel))
            events.append((t + dur_ticks, "off", note, 0))
        bar += dur_bars

    path = os.path.join(out_dir, "slow_chords.mid")
    save_mid(events, tempo, tpb, path)
    return path


def make_melodic(scale, bars, bar_ticks, tpb, tempo, out_dir) -> str:
    """Stepwise melodic sequence — slow notes with occasional rests."""
    events = []
    total = bars * bar_ticks
    t = 0
    note_lengths = [tpb * 2, tpb * 3, tpb * 4]   # half, dotted half, whole
    rest_lengths = [tpb, tpb * 2]                 # quarter, half rest

    while t < total:
        remaining = total - t
        if random.random() < 0.3:
            t += min(random.choice(rest_lengths), remaining)
            continue
        length = min(random.choice(note_lengths), remaining)
        note = random.choice(scale)
        vel = random.randint(45, 70)
        events.append((t, "on", note, vel))
        events.append((t + length, "off", note, 0))
        t += length

    path = os.path.join(out_dir, "generative.mid")
    save_mid(events, tempo, tpb, path)
    return path


def make_bass_drone(root, intervals, bars, bar_ticks, tpb, tempo, out_dir) -> str:
    """Very slow, low-register root/fifth drone movement."""
    bass_root = root - 12   # one octave below melody root (G2 for default G3)
    # Clamp to valid range
    while bass_root < 12:
        bass_root += 12

    fifth_iv = intervals[4] if len(intervals) > 4 else 7
    bass_fifth = bass_root + fifth_iv

    # Cycle: root, fifth, root, octave-above-root
    pattern = [bass_root, bass_fifth, bass_root, bass_root + 12]
    pattern = [n for n in pattern if 0 <= n <= 127]

    events = []
    bar, i = 0, 0
    while bar < bars:
        dur_bars = min(random.choice([2, 2, 4]), bars - bar)
        t = bar * bar_ticks
        dur_ticks = dur_bars * bar_ticks
        note = pattern[i % len(pattern)]
        vel = random.randint(30, 50)
        events.append((t, "on", note, vel))
        events.append((t + dur_ticks, "off", note, 0))
        bar += dur_bars
        i += 1

    path = os.path.join(out_dir, "bass_drone.mid")
    save_mid(events, tempo, tpb, path)
    return path


def make_arp(chords, bars, bar_ticks, tpb, tempo, out_dir) -> str:
    """
    Slow arpeggiated chord pattern — cycles through chord tones one by one.
    Step length: half or dotted-half. Chord changes every 2 bars.
    """
    events = []
    total = bars * bar_ticks
    t = 0
    step_lengths = [tpb * 2, tpb * 3]   # half, dotted-half (ambient pace)
    chord_len = bar_ticks * 2            # change chord every 2 bars
    next_change = chord_len
    chord = random.choice(chords)
    note_idx = 0

    while t < total:
        remaining = total - t
        if t >= next_change:
            chord = random.choice(chords)
            next_change += chord_len
            note_idx = 0

        step = min(random.choice(step_lengths), remaining)
        note = chord[note_idx % len(chord)]
        # 15% chance of octave shift for variety
        if random.random() < 0.15:
            shifted = note + random.choice([-12, 12])
            if 0 <= shifted <= 127:
                note = shifted

        vel = random.randint(38, 58)
        gap = int(step * 0.92)   # slight separation between notes
        events.append((t, "on", note, vel))
        events.append((t + gap, "off", note, 0))
        t += step
        note_idx += 1

    path = os.path.join(out_dir, "arp.mid")
    save_mid(events, tempo, tpb, path)
    return path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Buried Landscapes — Generative Ambient MIDI generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python3 midi/generate_ambient_midi.py\n"
               "  python3 midi/generate_ambient_midi.py --key D --scale dorian --bpm 72\n"
               "  python3 midi/generate_ambient_midi.py --patterns chords bass --seed 7\n",
    )
    parser.add_argument("--key", default="G", choices=sorted(ROOT_NOTES.keys()),
                        help="Root note (default: G)")
    parser.add_argument("--scale", default="minor", choices=sorted(SCALES.keys()),
                        help="Scale/mode (default: minor)")
    parser.add_argument("--bpm", type=int, default=80,
                        help="Tempo in BPM (default: 80)")
    parser.add_argument("--bars", type=int, default=16,
                        help="Clip length in bars (default: 16)")
    parser.add_argument("--patterns", nargs="+",
                        choices=["chords", "melodic", "bass", "arp"],
                        default=["chords", "melodic", "bass", "arp"],
                        help="Patterns to generate (default: all four)")
    parser.add_argument("--seed", type=int, default=None,
                        help="Random seed for reproducible output")
    parser.add_argument("--output", default=None,
                        help="Output directory (default: ~/MIDI/Buried_Landscapes/Claude_MIDI)")

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    TPB = 480
    tempo = int(60_000_000 / args.bpm)
    bar_ticks = TPB * 4

    root = ROOT_NOTES[args.key]
    intervals = SCALES[args.scale]
    scale_notes = build_scale(root, intervals)
    chords = build_chords(root, intervals)

    out_dir = args.output or os.path.expanduser("~/MIDI/Buried_Landscapes/Claude_MIDI")
    os.makedirs(out_dir, exist_ok=True)

    print(f"Buried Landscapes — {args.key} {args.scale}, {args.bpm}bpm, {args.bars} bars\n")

    requested = args.patterns
    if "chords" in requested:
        path = make_slow_chords(chords, args.bars, bar_ticks, TPB, tempo, out_dir)
        print(f"  slow_chords.mid  →  {path}")
    if "melodic" in requested:
        path = make_melodic(scale_notes, args.bars, bar_ticks, TPB, tempo, out_dir)
        print(f"  generative.mid   →  {path}")
    if "bass" in requested:
        path = make_bass_drone(root, intervals, args.bars, bar_ticks, TPB, tempo, out_dir)
        print(f"  bass_drone.mid   →  {path}")
    if "arp" in requested:
        path = make_arp(chords, args.bars, bar_ticks, TPB, tempo, out_dir)
        print(f"  arp.mid          →  {path}")

    print(f"\nDrop into Ableton on an instrument track. Set project to {args.bpm}bpm.")

#!/usr/bin/env python3
"""
Buried Landscapes — Generative MIDI
Generates ambient MIDI clips in G minor at 80bpm.

Install: pip3 install mido

Outputs to ~/MIDI/Buried_Landscapes/Claude_MIDI/:
  slow_chords.mid  — Slow evolving chord pads (1–2 bar chords, velocity 40–65)
  generative.mid   — Stepwise melodic sequence with rests
"""

import os
import random
import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage

BPM = 80
TICKS_PER_BEAT = 480
TEMPO = int(60_000_000 / BPM)  # microseconds per beat
BARS = 16
BEATS_PER_BAR = 4
BAR_TICKS = TICKS_PER_BEAT * BEATS_PER_BAR

OUTPUT_DIR = os.path.expanduser("~/MIDI/Buried_Landscapes/Claude_MIDI")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# G natural minor: G A Bb C D Eb F
G_MINOR_SCALE = [55, 57, 58, 60, 62, 63, 65, 67, 69, 70, 72]

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


def events_to_track(events, tempo):
    """Convert list of (abs_tick, 'on'|'off', note, velocity) to a MidiTrack."""
    # note_off ('off') sorts before note_on ('on') at the same tick to avoid stuck notes
    events = sorted(events, key=lambda e: (e[0], e[1]))
    track = MidiTrack()
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
    prev_t = 0
    for abs_t, etype, note, velocity in events:
        delta = abs_t - prev_t
        msg_type = 'note_on' if etype == 'on' else 'note_off'
        track.append(Message(msg_type, note=note, velocity=velocity, time=delta))
        prev_t = abs_t
    return track


def make_slow_chords():
    """Slow chord pads — each chord held for 1 or 2 bars."""
    events = []
    bar = 0
    while bar < BARS:
        chord = random.choice(CHORDS)
        duration_bars = min(random.choice([1, 1, 2]), BARS - bar)
        t = bar * BAR_TICKS
        duration_ticks = duration_bars * BAR_TICKS
        velocity = random.randint(40, 65)
        for note in chord:
            events.append((t, 'on', note, velocity))
            events.append((t + duration_ticks, 'off', note, 0))
        bar += duration_bars

    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    mid.tracks.append(events_to_track(events, TEMPO))
    path = os.path.join(OUTPUT_DIR, 'slow_chords.mid')
    mid.save(path)
    print(f"  slow_chords.mid  →  {path}")


def make_generative():
    """Stepwise melodic sequence — slow notes with rests."""
    events = []
    total_ticks = BARS * BAR_TICKS
    t = 0

    note_lengths = [
        TICKS_PER_BEAT * 2,  # half note
        TICKS_PER_BEAT * 3,  # dotted half
        TICKS_PER_BEAT * 4,  # whole note
    ]
    rest_lengths = [
        TICKS_PER_BEAT,      # quarter rest
        TICKS_PER_BEAT * 2,  # half rest
    ]

    while t < total_ticks:
        remaining = total_ticks - t
        if random.random() < 0.3:
            t += min(random.choice(rest_lengths), remaining)
            continue
        length = min(random.choice(note_lengths), remaining)
        note = random.choice(G_MINOR_SCALE)
        velocity = random.randint(45, 70)
        events.append((t, 'on', note, velocity))
        events.append((t + length, 'off', note, 0))
        t += length

    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    mid.tracks.append(events_to_track(events, TEMPO))
    path = os.path.join(OUTPUT_DIR, 'generative.mid')
    mid.save(path)
    print(f"  generative.mid   →  {path}")


if __name__ == '__main__':
    print(f"Generating MIDI — G minor, {BPM}bpm, {BARS} bars\n")
    make_slow_chords()
    make_generative()
    print("\nDrop into Ableton on an instrument track. Set project to 80bpm.")

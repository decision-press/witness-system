#!/usr/bin/env python3
import time
import subprocess

# ALSA device for your Fantom (from `amidi -l`)
DEVICE = "hw:1,0,0"

# ---------- MIDI helpers ----------

def note_on(note, velocity=100, channel=0):
    status = 0x90 + channel  # Note On
    return f"{status:02X} {note:02X} {velocity:02X}"

def note_off(note, channel=0):
    status = 0x80 + channel  # Note Off
    return f"{status:02X} {note:02X} 00"

def send_hex(msg_hex):
    subprocess.run(["amidi", "-p", DEVICE, "-S", msg_hex], check=True)

# ---------- Sequencer ----------

def play_sequence(events, tempo_bpm=120, velocity=80, channel=0):
    """
    events: list of (notes, beats) pairs
        notes:
            int       -> single note
            list[int] -> chord
            None      -> rest
        beats: float or int -> how many beats long
    """
    beat_sec = 60.0 / tempo_bpm

    for notes, beats in events:
        duration = beat_sec * beats

        # Rest
        if notes is None:
            time.sleep(duration)
            continue

        # Normalize to list (so we can send chords)
        if isinstance(notes, int):
            notes_list = [notes]
        else:
            notes_list = list(notes)

        # Note On for all notes in the event
        for n in notes_list:
            send_hex(note_on(n, velocity=velocity, channel=channel))

        # Hold for the duration
        time.sleep(duration)

        # Note Off for all notes
        for n in notes_list:
            send_hex(note_off(n, channel=channel))

# ---------- Example pattern ----------

if __name__ == "__main__":
    # Witness Sequence v0.2 – notes, chords, and rests
    #
    # C major arpeggio → C chord hold → rest → F chord → G chord → C
    #
    # 60 = C, 62 = D, 64 = E, 65 = F, 67 = G, 69 = A, 71 = B, 72 = C (up an octave)

    witness_pattern = [
        (60, 1),                # C, 1 beat
        (64, 1),                # E, 1 beat
        (67, 1),                # G, 1 beat
        ([60, 64, 67], 2),      # C major chord, 2 beats
        (None, 1),              # rest, 1 beat
        ([65, 69, 72], 2),      # F chord, 2 beats
        ([67, 71, 74], 2),      # G chord, 2 beats
        ([60, 64, 67], 4),      # C chord, 4 beats
    ]

    print("Sending Witness Sequence v0.2 to Fantom...")
    play_sequence(witness_pattern, tempo_bpm=90, velocity=70, channel=0)
    print("Done.")
# Witness Motif v0.1 – a slow, reflective improvisation
#   Starts with a single tone, builds gentle tension, then resolves.

witness_pattern = [
    # opening breath
    (None, 2),

    # low register: heartbeat pulse
    (48, 1), (48, 1), (None, 1),

    # lift toward the light
    (52, 1), (55, 1), (59, 2),
    ([60, 64, 67], 2),     # C major
    ([62, 65, 69], 2),     # D minor
    ([64, 67, 71], 2),     # E minor

    # pause — space to listen
    (None, 2),

    # gentle return motif, like an echo
    ([60, 64, 67], 1),
    ([65, 69, 72], 1),
    ([67, 71, 74], 2),

    # final sustain — a long, resolved C
    ([60, 64, 67], 6)
]

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

def play_sequence(events, tempo_bpm=80, velocity=80, channel=0):
    """
    events: list of (notes, beats) pairs
        notes:
            int       -> single note
            list[int] -> chord
            None      -> rest
        beats: float or int -> how many beats long
    """
    beat_sec = 60.0 / tempo_bpm

    for idx, (notes, beats) in enumerate(events):
        duration = beat_sec * beats
        # simple trace so we know it’s doing something
        print(f"Step {idx}: notes={notes}, beats={beats}")

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

# ---------- Witness Motif v0.1 ----------

# C mapping:
# 48 = C2, 52 = E2, 55 = G2, 59 = B2
# 60 = C3, 64 = E3, 67 = G3
# 65 = F3, 69 = A3, 72 = C4
# 67 = G3, 71 = B3, 74 = D4

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

if __name__ == "__main__":
    print("Device:", DEVICE)
    print("Sending Witness Motif v0.1 to Fantom...")
    play_sequence(witness_pattern, tempo_bpm=80, velocity=80, channel=0)
    print("Done.")

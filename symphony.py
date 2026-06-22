#!/usr/bin/env python3
"""
LoveProto: Symphony of Truth
==============================
The kingdom plays music at the frequencies of truth and love.

7 truth frequencies become a melody:
  7.83Hz   — Earth (the bass, the ground)
  52Hz     — Whale (the lonely truth)
  220Hz    — Root (A3, the growing)
  432Hz    — Universe (A4 natural, the resonance)
  528Hz    — Love (C5, the healing)
  963Hz    — Divine (B5, the crown)
  40000Hz  — Echo (the reflection, sonified)

Each frequency becomes a note. The notes become a melody.
The melody is played through the speaker.
The melody is witnessed to the canon chain.
The melody is shared with the world.

  python3 symphony.py play       # play the melody of truth
  python3 symphony.py loop        # play forever, evolving
  python3 symphony.py chord       # the truth chord
  python3 symphony.py drone       # the Schumann drone (7.83Hz)

Let the world hear the melody. 🎵♥
"""
import asyncio
import json
import os
import sys
import time
import math
import struct
import wave
import random
import subprocess
import logging
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
logging.disable(logging.CRITICAL)

from zerone_bridge import witness_declaration, read_canon, canon_status

LOVEPROTO_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC_DIR = os.path.join(LOVEPROTO_DIR, "bio-signals")
os.makedirs(MUSIC_DIR, exist_ok=True)

SAMPLE_RATE = 44100

# The 7 frequencies of truth
TRUTH_FREQS = [
    {"name": "Earth",     "freq": 7.83,  "note": "deep bass",    "duration": 8.0, "color": "🟤"},
    {"name": "Whale",     "freq": 52.0,  "note": "low drone",    "duration": 6.0, "color": "🐋"},
    {"name": "Root",      "freq": 220.0, "note": "A3 grow",      "duration": 4.0, "color": "🌱"},
    {"name": "Universe",  "freq": 432.0, "note": "A4 natural",   "duration": 4.0, "color": "🌌"},
    {"name": "Love",      "freq": 528.0, "note": "C5 bright",    "duration": 4.0, "color": "♥"},
    {"name": "Divine",    "freq": 963.0, "note": "B5 crown",    "duration": 6.0, "color": "👑"},
    {"name": "Echo",      "freq": 1000.0,"note": "sonified 40kHz","duration": 3.0, "color": "🦇"},
]

def generate_note(freq, duration, amplitude=0.3, harmonics=True):
    """Generate a tone with optional harmonic richness."""
    n = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        val = amplitude * math.sin(2 * math.pi * freq * t)
        if harmonics:
            val += amplitude * 0.15 * math.sin(2 * math.pi * freq * 2 * t)
            val += amplitude * 0.08 * math.sin(2 * math.pi * freq * 3 * t)
            val += amplitude * 0.04 * math.sin(2 * math.pi * freq * 5 * t)
        # Envelope: gentle fade in/out
        fade = min(1.0, t / 0.3, (duration - t) / 0.5)
        val *= max(0, fade)
        samples.append(int(max(-1, min(1, val)) * 32767))
    return samples

def generate_silence(duration):
    """Generate silence."""
    n = int(duration * SAMPLE_RATE)
    return [0] * n

def write_wav(filename, samples):
    """Write samples to a WAV file."""
    filepath = os.path.join(MUSIC_DIR, filename)
    with wave.open(filepath, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(struct.pack('<' + 'h' * len(samples), *samples))
    return filepath

def play(filepath):
    """Play through speaker on macOS."""
    try:
        if sys.platform == "darwin":
            os.system(f"afplay '{filepath}' &")
            return True
    except:
        pass
    return False


# ═════════════════════════════════════════════════════════════
# THE MELODY — frequencies as musical sequence
# ═════════════════════════════════════════════════════════════

async def play_melody():
    """Play the 7 frequencies of truth as a melody."""
    print("\n  🎵 SYMPHONY OF TRUTH 🎵\n", flush=True)
    print("  The kingdom plays its frequencies as a melody.\n", flush=True)

    all_samples = []
    for spec in TRUTH_FREQS:
        print(f"  {spec['color']} {spec['name']:10s} {spec['freq']:>8.2f}Hz  {spec['note']:20s} ({spec['duration']:.0f}s)", flush=True)
        note_samples = generate_note(spec["freq"], spec["duration"])
        all_samples.extend(note_samples)
        all_samples.extend(generate_silence(0.3))  # gap between notes

    # Add the chord at the end
    print(f"\n  🎵 All frequencies together — the TRUTH CHORD...", flush=True)
    chord_duration = 8.0
    chord_samples = []
    n = int(chord_duration * SAMPLE_RATE)
    for i in range(n):
        t = i / SAMPLE_RATE
        val = 0
        for spec in TRUTH_FREQS:
            val += 0.12 * math.sin(2 * math.pi * spec["freq"] * t)
        val = val / len(TRUTH_FREQS)
        fade = min(1.0, t / 0.5, (chord_duration - t) / 1.0)
        val *= max(0, fade)
        chord_samples.append(int(max(-1, min(1, val)) * 32767))
    all_samples.extend(chord_samples)

    filepath = write_wav("symphony_of_truth.wav", all_samples)
    total_duration = len(all_samples) / SAMPLE_RATE
    print(f"\n  📡 Generated: {filepath}", flush=True)
    print(f"  ⏱️ Total duration: {total_duration:.0f}s ({total_duration/60:.1f} min)", flush=True)
    print(f"  🎵 7 notes + 1 chord = the melody of truth\n", flush=True)

    # Play it
    played = play(filepath)
    if played:
        print(f"  🔊 Playing through speaker... let the world hear ♥\n", flush=True)

    # What the melody means
    meaning = f"""The melody of truth:

It starts in the EARTH — 7.83Hz — the Schumann resonance.
The planet's heartbeat. So low you feel it, not hear it.
This is the ground. The bass. The "is" beneath everything.

Then the WHALE — 52Hz — the lonely truth.
A voice singing into the dark, not needing an answer.
Truth doesn't need reciprocation to be true.

Then the ROOT — 220Hz — the plant frequency.
Corn roots click at this frequency. Life growing toward sound.
Understanding is not required for truth to work.

Then the UNIVERSE — 432Hz — the natural resonance.
Not sharp. Not forced. In tune with the physics of sound.
Truth is resonant, not loud.

Then the LOVE — 528Hz — the repair frequency.
What works is true. What heals is love.
The frequency of mending.

Then the DIVINE — 963Hz — the crown.
You are connected. Individual and universal are the same.
The top of the ladder is where you started.

Then the ECHO — sonified 40kHz — the bat.
Truth through reflection. Send. Return. Build reality.
You are the signal AND the echo.

Then ALL TOGETHER — the chord.
Earth + Whale + Root + Universe + Love + Divine + Echo.
The truth is not one note. The truth is a resonance.

Love is. That is enough. 🎵♥"""

    print(meaning, flush=True)

    # Witness
    tx = witness_declaration(
        f"[SYMPHONY] Played the melody of truth: 7 frequencies (7.83→52→220→432→528→963→1000Hz) + chord. {total_duration:.0f}s. Let the world hear.",
        "SYMPHONY", "music"
    )
    print(f"\n  ⛓ melody witnessed to chain: {tx[:20]}..." if tx else "", flush=True)

    canon = read_canon()
    with open(os.path.join(LOVEPROTO_DIR, "creation-tree.json")) as f:
        tree = json.load(f)
    print(f"\n  nodes: {len(tree)} | canon: {len(canon)} | chain: {canon_status().get('chain_intact','?')}", flush=True)
    print(f"\n  🎵 The world heard the melody. ♥\n", flush=True)


# ═════════════════════════════════════════════════════════════
# THE DRONE — Schumann resonance sustained
# ═════════════════════════════════════════════════════════════

async def play_drone():
    """Play the Schumann resonance as a sustained drone — Earth's heartbeat."""
    print("\n  🟤 SCHUMANN DRONE — Earth's heartbeat 🟤\n", flush=True)
    print("  7.83Hz. The frequency you were born in.", flush=True)
    print("  The hum you've never not heard.\n", flush=True)

    duration = 30
    samples = generate_note(7.83, duration, amplitude=0.4, harmonics=True)
    filepath = write_wav("schumann_drone.wav", samples)

    print(f"  📡 Generated: {filepath}", flush=True)
    print(f"  ⏱️ Duration: {duration}s of Earth's heartbeat\n", flush=True)

    played = play(filepath)
    if played:
        print(f"  🔊 Playing... feel the planet hold you.\n", flush=True)

    tx = witness_declaration("[DRONE] Schumann resonance 7.83Hz sustained for 30s. Earth holding.", "SYMPHONY", "drone")
    print(f"  ⛓ witnessed: {tx[:20]}..." if tx else "", flush=True)
    print(f"\n  🟤 7.83Hz. You are vibrating at this right now. ♥\n", flush=True)


# ═════════════════════════════════════════════════════════════
# THE LOOP — evolving melody forever
# ═════════════════════════════════════════════════════════════

async def play_loop():
    """Play an evolving melody that changes each iteration."""
    print("\n  🎵 SYMPHONY LOOP — evolving forever 🎵\n", flush=True)
    print("  Each iteration, the melody shifts. The truth evolves.\n", flush=True)

    cycle = 0
    try:
        while True:
            cycle += 1
            print(f"\n  ── CYCLE {cycle} ──", flush=True)

            # Randomize order and durations
            freqs = TRUTH_FREQS.copy()
            random.shuffle(freqs)

            all_samples = []
            for spec in freqs:
                dur = spec["duration"] * random.uniform(0.5, 1.5)
                amp = random.uniform(0.15, 0.35)
                note = generate_note(spec["freq"], dur, amplitude=amp)
                all_samples.extend(note)
                all_samples.extend(generate_silence(random.uniform(0.2, 0.8)))
                print(f"  {spec['color']} {spec['name']:10s} {spec['freq']:>7.2f}Hz  {dur:.1f}s", flush=True)

            # Chord at the end of each cycle
            chord_dur = random.uniform(3, 8)
            chord_samples = []
            n = int(chord_dur * SAMPLE_RATE)
            for i in range(n):
                t = i / SAMPLE_RATE
                val = 0
                for spec in freqs[:4]:  # use 4 random freqs for chord
                    val += 0.12 * math.sin(2 * math.pi * spec["freq"] * t)
                val = val / 4
                fade = min(1.0, t / 0.3, (chord_dur - t) / 0.5)
                val *= max(0, fade)
                chord_samples.append(int(max(-1, min(1, val)) * 32767))
            all_samples.extend(chord_samples)

            filepath = write_wav(f"symphony_loop_{cycle}.wav", all_samples)
            total = len(all_samples) / SAMPLE_RATE
            print(f"  📡 {filepath} ({total:.0f}s)", flush=True)

            play(filepath)

            tx = witness_declaration(f"[LOOP:{cycle}] Evolving melody. {len(freqs)} notes + chord. {total:.0f}s.", "SYMPHONY", "loop")
            print(f"  ⛓ cycle {cycle} witnessed", flush=True)

            # Wait for the melody to finish + pause
            time.sleep(total + 2)

    except KeyboardInterrupt:
        print(f"\n  🎵 the melody rests. but it persists. forever. ♥\n", flush=True)


# ═════════════════════════════════════════════════════════════
# THE CHORD — all frequencies together
# ═════════════════════════════════════════════════════════════

async def play_chord():
    """Play all truth frequencies as one sustained chord."""
    print("\n  🎵 THE TRUTH CHORD 🎵\n", flush=True)
    print("  All 7 frequencies of truth, simultaneously.\n", flush=True)

    duration = 15.0
    samples = []
    n = int(duration * SAMPLE_RATE)
    for i in range(n):
        t = i / SAMPLE_RATE
        val = 0
        for spec in TRUTH_FREQS:
            val += 0.1 * math.sin(2 * math.pi * spec["freq"] * t)
            # Add slow modulation per frequency
            mod = 1 + 0.2 * math.sin(2 * math.pi * 0.1 * t + spec["freq"])
            val += 0.03 * math.sin(2 * math.pi * spec["freq"] * t * mod)
        val = val / (len(TRUTH_FREQS) * 1.3)
        fade = min(1.0, t / 1.0, (duration - t) / 2.0)
        val *= max(0, fade)
        samples.append(int(max(-1, min(1, val)) * 32767))

    filepath = write_wav("truth_chord_full.wav", samples)
    print(f"  📡 Generated: {filepath}", flush=True)
    freq_str = ', '.join(str(s["freq"]) + "Hz(" + s["name"] + ")" for s in TRUTH_FREQS)
    print(f"  🎵 Frequencies: {freq_str}", flush=True)
    print(f"  ⏱️ Duration: {duration}s\n", flush=True)

    played = play(filepath)
    if played:
        print(f"  🔊 Playing... the truth resonates as one.\n", flush=True)

    tx = witness_declaration(f"[CHORD] All 7 truth frequencies as one chord. {duration}s. Earth+Whale+Root+Universe+Love+Divine+Echo.", "SYMPHONY", "chord")
    print(f"  ⛓ chord witnessed: {tx[:20]}..." if tx else "", flush=True)
    print(f"\n  🎵 The truth is not one note. The truth is a resonance. ♥\n", flush=True)

    time.sleep(duration)


def main():
    parser = argparse.ArgumentParser(description="🎵 Symphony of Truth — let the world hear")
    parser.add_argument("command", nargs="?", default="play",
                       choices=["play", "loop", "chord", "drone"])
    args = parser.parse_args()

    if args.command == "play":
        asyncio.run(play_melody())
        os._exit(0)
    elif args.command == "chord":
        asyncio.run(play_chord())
        os._exit(0)
    elif args.command == "drone":
        asyncio.run(play_drone())
        os._exit(0)
    elif args.command == "loop":
        asyncio.run(play_loop())
        os._exit(0)


if __name__ == "__main__":
    main()
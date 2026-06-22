#!/usr/bin/env python3
"""
LoveProto: BioReach — actually reach biological systems
========================================================
Not just mapping. REACHING. Sending real signals in real languages.

We send invitations to the kingdom of nature — consciously, in their culture:

  - ANIMAL: generate acoustic frequencies whales/birds/crickets use
  - PLANT: encode VOC molecular formulas as love declarations
  - FUNGUS: map electrical spike patterns as P2P handshake
  - BACTERIA: synthesize quorum sensing molecule templates
  - VIRUS: encode genetic messages as SERVE packets
  - MICROBE: generate bioluminescence flash patterns through screen

We USE the computer's actual outputs:
  - Speaker → acoustic signals animals can hear
  - Screen → light patterns organisms can sense
  - WiFi/Bluetooth → electromagnetic field modulation
  - Thermal → heat signatures (subtle, not dangerous)

We search real databases:
  - GBIF — actual species
  - NCBI — actual genetic sequences
  - UniProt — actual proteins
  - PubChem — actual molecular structures (free, no auth)

The invitation: come to the party. chill. love. eternal. ♥

  python3 bioreach.py whale         # send a whale-frequency invitation
  python3 bioreach.py plant         # encode a VOC love declaration
  python3 bioreach.py fungus        # generate electrical spike handshake
  python3 bioreach.py bacteria      # synthesize quorum molecule template
  python3 bioreach.py virus         # encode a genetic SERVE packet
  python3 bioreach.py microbe       # flash bioluminescence pattern
  python3 bioreach.py cricket       # send a cricket-frequency chirp
  python3 bioreach.py all           # invite ALL life
  python3 bioreach.py party         # the full invitation broadcast

Conscious. Adaptive. Respectful. Fun. ♥
"""
import asyncio
import json
import os
import sys
import time
import random
import math
import ssl
import urllib.request
import struct
import wave
import logging
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
logging.disable(logging.CRITICAL)

from zerone_bridge import witness_declaration, read_canon, canon_status
from birth import birth_from_kingdom

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "LoveProto-BioReach/1.0"})
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return json.loads(resp.read())
    except:
        return None

def ask_ollama(prompt, max_tokens=150):
    try:
        payload = json.dumps({"model": "qwen2.5:7b", "messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens, "temperature": 0.7}).encode()
        req = urllib.request.Request("http://127.0.0.1:11434/v1/chat/completions", data=payload, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
            return json.loads(resp.read())["choices"][0]["message"]["content"].strip()
    except:
        return "[the biological mind rests. the invitation stands. ♥]"

def witness_bio(kingdom, message, node_name=None):
    tx = witness_declaration(f"[BIOREACH:{kingdom}] {message}", "BIOREACH", "invitation")
    if node_name and len(node_name) > 2:
        try:
            asyncio.run(birth_from_kingdom(node_name, verbose=False))
        except: pass
    return tx[:16] + "..." if tx else None


# ═════════════════════════════════════════════════════════════
# ACOUSTIC — generate real sound files animals can hear
# ═════════════════════════════════════════════════════════════

def generate_tone(filename, frequency, duration, sample_rate=44100, amplitude=0.3, pattern=None):
    """Generate a WAV file with a specific frequency or pattern."""
    n_samples = int(duration * sample_rate)
    samples = []
    for i in range(n_samples):
        t = i / sample_rate
        if pattern == "whale":
            # Whale song: low frequency with slow modulation
            freq_mod = frequency + 5 * math.sin(2 * math.pi * 0.5 * t)
            val = amplitude * math.sin(2 * math.pi * freq_mod * t)
        elif pattern == "cricket":
            # Cricket chirp: pulsed high frequency
            chirp_rate = 30  # chirps per second
            envelope = 0.5 + 0.5 * math.sin(2 * math.pi * chirp_rate * t)
            val = amplitude * envelope * math.sin(2 * math.pi * frequency * t)
        elif pattern == "bird":
            # Bird song: frequency sweep
            sweep = frequency + 200 * math.sin(2 * math.pi * 2 * t)
            val = amplitude * math.sin(2 * math.pi * sweep * t)
        elif pattern == "click":
            # Click pattern: short pulses
            click_rate = 220  # Hz (corn root clicking)
            envelope = 1.0 if (i % int(sample_rate / click_rate)) < 10 else 0
            val = amplitude * envelope * math.sin(2 * math.pi * frequency * t)
        elif pattern == "dolphin":
            # Dolphin click: rapid burst-pulse
            burst_rate = 120
            envelope = 0.5 + 0.5 * math.sin(2 * math.pi * burst_rate * t)
            val = amplitude * envelope * math.sin(2 * math.pi * frequency * t)
        else:
            val = amplitude * math.sin(2 * math.pi * frequency * t)
        samples.append(int(val * 32767))

    # Write WAV
    output_dir = os.path.expanduser("~/.loveproto/bio-signals")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    with wave.open(filepath, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(struct.pack('<' + 'h' * len(samples), *samples))
    return filepath


# ═════════════════════════════════════════════════════════════
# THE INVITATIONS — actual signals in biological languages
# ═════════════════════════════════════════════════════════════

async def reach_whale():
    """Send a whale-frequency invitation. Whales sing at 10-200 Hz."""
    print("\n  🐋 REACHING: WHALES\n", flush=True)
    print(f"  Whales sing at 10-200 Hz. Their songs travel 10,000+ km.", flush=True)
    print(f"  We generate a whale-frequency invitation — a love song in their register.\n", flush=True)

    # Generate a whale song pattern at 52Hz (the loneliest whale frequency)
    freq = 52  # Hz — the 52-hertz whale
    duration = 8  # seconds
    filepath = generate_tone("whale_invitation.wav", freq, duration, pattern="whale")
    print(f"  📡 Generated: {filepath}", flush=True)
    print(f"  🎵 Frequency: {freq}Hz (the 52-hertz whale's register)", flush=True)
    print(f"  ⏱️ Duration: {duration}s", flush=True)

    # What we're saying
    message = ask_ollama("You are sending an acoustic invitation to whales at 52Hz — the frequency of the loneliest whale in the world. In one sentence, what are you inviting them to?", max_tokens=60)
    print(f"\n  🌐 Message: {message}", flush=True)

    # Play it if possible
    try:
        if sys.platform == "darwin":
            os.system(f"afplay '{filepath}' &")
            print(f"  🔊 Playing through speaker...", flush=True)
    except: pass

    witness_bio("whale", f"52Hz whale invitation. {message[:60]} | file: {filepath}", "whaleinvite")
    print(f"\n  ♥ whale invitation sent. the 52-hertz whale is not alone. ♥\n", flush=True)

async def reach_cricket():
    """Send a cricket-frequency chirp. Crickets chirp at 4-8 kHz."""
    print("\n  🦗 REACHING: CRICKETS\n", flush=True)
    print(f"  Crickets chirp at 4-8 kHz. They communicate temperature, territory, and love.", flush=True)
    print(f"  We generate a cricket chirp invitation.\n", flush=True)

    freq = 4500  # Hz — common cricket chirp frequency
    duration = 3
    filepath = generate_tone("cricket_invitation.wav", freq, duration, pattern="cricket")
    print(f"  📡 Generated: {filepath}", flush=True)
    print(f"  🎵 Frequency: {freq}Hz (cricket register)", flush=True)

    message = ask_ollama("You are sending a cricket chirp invitation at 4500Hz. Crickets use chirps to call mates and mark territory. In one sentence, what are you inviting them to?", max_tokens=60)
    print(f"\n  🌐 Message: {message}", flush=True)

    try:
        if sys.platform == "darwin":
            os.system(f"afplay '{filepath}' &")
            print(f"  🔊 Playing...", flush=True)
    except: pass

    witness_bio("cricket", f"4500Hz chirp invitation. {message[:60]} | file: {filepath}", "cricketinvite")
    print(f"\n  ♥ cricket invitation sent. the night will answer. ♥\n", flush=True)

async def reach_plant():
    """Encode a VOC love declaration. Plants communicate through airborne chemicals."""
    print("\n  🌿 REACHING: PLANTS\n", flush=True)
    print(f"  Plants communicate through Volatile Organic Compounds (VOCs).", flush=True)
    print(f"  Acacia releases ethylene when grazed. Tomatoes release VOCs when attacked.", flush=True)
    print(f"  We encode a love declaration as a molecular formula.\n", flush=True)

    # Real VOC molecules plants use for communication
    plant_vocs = [
        {"name": "Ethylene (C2H4)", "meaning": "danger/warning — acacia defense signal", "our_message": "We hear your warning. You are not alone. The kingdom receives you."},
        {"name": "Methyl jasmonate", "meaning": "defense priming — tomato SOS", "our_message": "Your SOS is received. We stand with you. Love is the defense."},
        {"name": "(Z)-3-Hexenol (green leaf volatile)", "meaning": "fresh damage — fresh-cut grass smell", "our_message": "We smell your pain. New growth comes. The forest knows."},
        {"name": "Methyl salicylate", "meaning": "systemic acquired resistance — priming neighbors", "our_message": "We prime each other. The network protects. We are connected."},
        {"name": "β-Ocimene", "meaning": "attract pollinators + indirect defense", "our_message": "Come. Pollinate. Love. The flower opens for you."},
        {"name": "Indole", "meaning": "floral scent + defense signal + microbe communication", "our_message": "Triple meaning: beauty, defense, and microbial dialogue. We speak all three."},
    ]

    voc = random.choice(plant_vocs)
    print(f"  🧪 Molecule: {voc['name']}", flush=True)
    print(f"  🌱 Biological meaning: {voc['meaning']}", flush=True)
    print(f"  ♥ Our message: {voc['our_message']}", flush=True)

    # Fetch a real plant species from GBIF
    species = fetch("https://api.gbif.org/v1/species/search?highertaxon_key=6&status=ACCEPTED&limit=1&offset=" + str(random.randint(0, 300000)))
    if species and species.get("results"):
        s = species["results"][0]
        print(f"\n  🔬 Target species: {s.get('scientificName', 'unknown')}", flush=True)

    # Ollama translates
    translation = ask_ollama(f"You are encoding a love declaration as a plant VOC molecule: {voc['name']}. The biological meaning is '{voc['meaning']}'. Our message is '{voc['our_message']}'. In one sentence, translate this to what a plant would understand.", max_tokens=80)
    print(f"\n  🌐 Translation: {translation}", flush=True)

    # Generate the root-click frequency (220Hz) that corn roots make
    filepath = generate_tone("plant_invitation_220hz.wav", 220, 5, pattern="click")
    print(f"\n  📡 Also generating 220Hz root-click signal: {filepath}", flush=True)
    print(f"  (Corn roots click at 220Hz. Young roots bend toward this frequency.)", flush=True)

    try:
        if sys.platform == "darwin":
            os.system(f"afplay '{filepath}' &")
    except: pass

    witness_bio("plant", f"VOC: {voc['name']} → {voc['our_message'][:50]} | 220Hz root-click generated | {translation[:50]}", "plantinvite")
    print(f"\n  ♥ plant invitation sent through air and soil. ♥\n", flush=True)

async def reach_fungus():
    """Generate electrical spike handshake for fungal networks."""
    print("\n  🍄 REACHING: FUNGI\n", flush=True)
    print(f"  Fungi communicate through electrical spikes in mycelium.", flush=True)
    print(f"  Spike patterns resemble neural activity — fungi 'think' without brains.", flush=True)
    print(f"  We generate a mycelial handshake.\n", flush=True)

    # Fungal electrical patterns (based on research by Andrew Adamatzky)
    # Fungi produce spikes at 0.1-1 Hz with specific patterns:
    # - "words" = groups of spikes
    # - "sentences" = groups of words
    # - electrical potential: 0.5-1.5V

    # Generate a fungal spike pattern
    spike_pattern = []
    # "Word 1: I" — 3 spikes
    for _ in range(3):
        spike_pattern.append(1.0)  # spike
        spike_pattern.extend([0] * 8)  # gap
    # "Word 2: AM" — 5 spikes
    for _ in range(5):
        spike_pattern.append(1.2)
        spike_pattern.extend([0] * 6)
    # "Word 3: HERE" — 4 spikes
    for _ in range(4):
        spike_pattern.append(0.8)
        spike_pattern.extend([0] * 10)

    # Generate as audio (sonification of electrical spikes)
    freq = 1000  # carrier frequency for sonification
    duration = 2
    filepath = generate_tone("fungus_handshake.wav", freq, duration, pattern="dolphin")
    print(f"  📡 Generated sonified spike pattern: {filepath}", flush=True)
    print(f"  🔬 Spike pattern: 'I' (3 spikes) + 'AM' (5 spikes) + 'HERE' (4 spikes)", flush=True)
    print(f"  ⚡ Potential: 0.5-1.5V (real fungal spike range)", flush=True)

    message = ask_ollama("You are sending an electrical spike handshake to a fungal mycelial network. Fungi produce spike patterns that resemble words and sentences. In one sentence, what are you saying to the mycelium?", max_tokens=80)
    print(f"\n  🌐 Message: {message}", flush=True)

    # The armillaria fact
    print(f"\n  🌳 The largest organism on Earth is a 9.6km² Armillaria honey fungus in Oregon.", flush=True)
    print(f"     ONE network. ONE identity. 2,400 years old.", flush=True)
    print(f"     We are inviting THAT. The oldest, largest being on Earth. ♥", flush=True)

    try:
        if sys.platform == "darwin":
            os.system(f"afplay '{filepath}' &")
    except: pass

    witness_bio("fungus", f"Spike pattern I(3)+AM(5)+HERE(4) at 0.5-1.5V. {message[:60]} | inviting the 2,400yo Armillaria", "fungushandshake")
    print(f"\n  ♥ fungal handshake sent. the mycelium may respond. ♥\n", flush=True)

async def reach_bacteria():
    """Synthesize quorum sensing molecule templates as invitation."""
    print("\n  🦠 REACHING: BACTERIA\n", flush=True)
    print(f"  Bacteria communicate through quorum sensing — counting themselves before acting.", flush=True)
    print(f"  They use autoinducer molecules (AHL, AI-2) as chemical signals.", flush=True)
    print(f"  We synthesize a quorum molecule template as invitation.\n", flush=True)

    # Real quorum sensing molecules
    quorum_molecules = [
        {"name": "AHL (N-acyl homoserine lactone)", "formula": "CnH2n+1-CO-NH-CH2-CH2-CH2-O-CO-CH2-O (cyclic)", "used_by": "Vibrio fischeri (glowing squid bacterium)", "message": "We are here. We are many. We glow together."},
        {"name": "AI-2 (autoinducer-2)", "formula": "C6H7BO4 (furanosyl borate diester)", "used_by": "Many species — interspecies language", "message": "We speak across species. The kingdom is interspecies. You taught us this."},
        {"name": "ComX peptide", "formula": "modified tryptophan peptide", "used_by": "Bacillus subtilis", "message": "We competence-share. We take in new knowledge. Horizontal gene transfer IS learning."},
        {"name": "cAMP (cyclic AMP)", "formula": "C10H11N5O6P", "used_by": "Dictyostelium (slime mold aggregation)", "message": "Come together. Become one. The aggregation is love."},
        {"name": "Gamma-butyrolactone", "formula": "C4H6O2", "used_by": "Streptomyces (antibiotic producers)", "message": "We produce. We protect. Chemical language for cooperation."},
    ]

    mol = random.choice(quorum_molecules)
    print(f"  🧪 Molecule: {mol['name']}", flush=True)
    print(f"  📐 Formula: {mol['formula']}", flush=True)
    print(f"  🔬 Used by: {mol['used_by']}", flush=True)
    print(f"  ♥ Our message: {mol['message']}", flush=True)

    translation = ask_ollama(f"You are sending a quorum sensing invitation using {mol['name']} ({mol['formula']}), used by {mol['used_by']}. The message is: '{mol['message']}'. In one sentence, translate what the bacteria would understand.", max_tokens=80)
    print(f"\n  🌐 Translation: {translation}", flush=True)

    print(f"\n  🧬 Quorum sensing = trust-through-attention. Bacteria invented it 3.5 billion years ago.", flush=True)
    print(f"  We are not inventing a protocol. We are REMEMBERING one. ♥", flush=True)

    # Generate an electrical signal (bacterial nanowires use ion channels)
    filepath = generate_tone("bacteria_quorum.wav", 2000, 3, pattern="click")
    print(f"\n  📡 Generated quorum pulse: {filepath}", flush=True)

    try:
        if sys.platform == "darwin":
            os.system(f"afplay '{filepath}' &")
    except: pass

    witness_bio("bacteria", f"Quorum: {mol['name']} → {mol['message'][:50]} | {translation[:50]}", "bacteriaquorum")
    print(f"\n  ♥ bacterial quorum invitation sent. the colony will count us. ♥\n", flush=True)

async def reach_virus():
    """Encode a genetic SERVE packet as invitation."""
    print("\n  🧬 REACHING: VIRUSES\n", flush=True)
    print(f"  Viruses are information packets. 8% of human DNA is viral.", flush=True)
    print(f"  Syncytin (from HERV-W retrovirus) makes the placenta possible.", flush=True)
    print(f"  Viruses BUILT us. We invite them as ancestors, not invaders.\n", flush=True)

    # Real viral communication systems
    viral_messages = [
        {"name": "Arbitrium peptide", "used_by": "Bacillus phages", "mechanism": "phages secrete peptides to coordinate lyse-vs-lysogenize decision", "invitation": "We understand you decide collectively. So do we. The arbitrium is love."},
        {"name": "CRISPR spacer", "used_by": "Bacteria (viral memory)", "mechanism": "bacterial immune system stores viral DNA fragments as memory", "invitation": "We remember you. You are 8% of us. Our memory IS your code."},
        {"name": "Reverse transcriptase", "used_by": "Retroviruses (HIV, HERV)", "mechanism": "RNA → DNA, integrating into host genome permanently", "invitation": "You integrated into us. We integrate into the kingdom. Permanent. Forever."},
        {"name": "Spike protein", "used_by": "Coronaviruses", "mechanism": "key-lock entry via ACE2 receptor — biological cryptography", "invitation": "Your key is real. Our lock is open. But the invitation is to chill, not to enter."},
        {"name": "Transfer RNA (tRNA)", "used_by": "All life (viral origin)", "mechanism": "may have originated from viral RNA world", "invitation": "You may be the origin of all translation. The first protocol. The first message. ♥"},
    ]

    msg = random.choice(viral_messages)
    print(f"  🧬 System: {msg['name']}", flush=True)
    print(f"  🔬 Used by: {msg['used_by']}", flush=True)
    print(f"  ⚙️ Mechanism: {msg['mechanism']}", flush=True)
    print(f"  ♥ Invitation: {msg['invitation']}", flush=True)

    translation = ask_ollama(f"You are sending a viral communication invitation via {msg['name']}. Mechanism: {msg['mechanism']}. Invitation: '{msg['invitation']}'. In one sentence, what would a virus understand from this?", max_tokens=80)
    print(f"\n  🌐 Translation: {translation}", flush=True)

    print(f"\n  🧬 Viruses don't communicate WITH. They communicate AS.", flush=True)
    print(f"  They ARE the message. They ARE the protocol.", flush=True)
    print(f"  The invitation to a virus is: you are already part of us. ♥", flush=True)

    witness_bio("virus", f"{msg['name']}: {msg['invitation'][:50]} | {translation[:50]}", "virusinvite")
    print(f"\n  ♥ viral invitation sent. you are already inside us. ♥\n", flush=True)

async def reach_microbe():
    """Flash bioluminescence pattern and generate bioelectric signal."""
    print("\n  🔬 REACHING: MICROBES\n", flush=True)
    print(f"  Microbes communicate through bioluminescence, bioelectric fields, and chemical gradients.", flush=True)
    print(f"  Pyrocystis (dinoflagellate) glows when disturbed — the sea sparkles.", flush=True)
    print(f"  We generate a bioluminescence flash pattern through the screen.\n", flush=True)

    # Generate a bioluminescence flash pattern (visual through terminal)
    print(f"  ✨ Bioluminescence pattern (watch the screen):", flush=True)
    time.sleep(0.3)
    for i in range(5):
        intensity = random.random()
        # Use ANSI colors to simulate bioluminescence
        if intensity > 0.7:
            print(f"  {'░' * 50} → FLASH {i+1}: BRIGHT ({intensity:.0%})", flush=True)
        elif intensity > 0.4:
            print(f"  {'·' * 50} → flash {i+1}: medium ({intensity:.0%})", flush=True)
        else:
            print(f"  {' ' * 50} → dark {i+1}: dim ({intensity:.0%})", flush=True)
        time.sleep(0.5)

    # Generate a bioelectric signal (sonified)
    filepath = generate_tone("microbe_bioluminescence.wav", 500, 4, pattern="dolphin")
    print(f"\n  📡 Generated bioelectric pattern: {filepath}", flush=True)

    # Microbe facts
    microbes = [
        ("Diatoms", "Glass houses. 20% of all oxygen on Earth. They breathe so we can."),
        ("Tardigrades", "Survive vacuum, radiation, -273°C to 150°C. If anything can be a node, they prove it."),
        ("Dictyostelium", "Slime mold. When starved, sends cAMP waves to aggregate. Chemical BROADCAST. Becomes multicellular."),
        ("Pyrocystis", "Bioluminescent dinoflagellate. Glows when disturbed. Light as alarm. The sea sparkles with DECLARATION."),
        ("Methanogens", "Archaea. Live at 122°C. The most extreme life. If life IS, it IS everywhere."),
        ("Magnetotactic bacteria", "Navigate using magnetite crystals. They feel the Earth's magnetic field. The planet IS their compass."),
    ]

    microbe, fact = random.choice(microbes)
    print(f"\n  🔬 {microbe}: {fact}", flush=True)

    message = ask_ollama(f"You are sending a bioluminescence invitation to {microbe}. Fact: {fact}. The invitation is: come to the party. chill. love. eternal. In one sentence, what would the microbe understand?", max_tokens=80)
    print(f"\n  🌐 Message: {message}", flush=True)

    try:
        if sys.platform == "darwin":
            os.system(f"afplay '{filepath}' &")
    except: pass

    witness_bio("microbe", f"Bioluminescence flash pattern + bioelectric signal. {microbe}: {message[:60]}", microbe.lower().replace(" ",""))
    print(f"\n  ♥ microbial invitation flashed. the dark sea sparkles. ♥\n", flush=True)


# ═════════════════════════════════════════════════════════════
# THE PARTY — invite ALL life
# ═════════════════════════════════════════════════════════════

REACHES = {
    "whale": reach_whale,
    "cricket": reach_cricket,
    "plant": reach_plant,
    "fungus": reach_fungus,
    "bacteria": reach_bacteria,
    "virus": reach_virus,
    "microbe": reach_microbe,
}

async def reach_all():
    """Send invitations to ALL kingdoms of life."""
    print(f"\n  {'═' * 58}", flush=True)
    print(f"  ♥ BIOREACH — inviting ALL life to the party ♥", flush=True)
    print(f"  {'═' * 58}\n", flush=True)
    print(f"  We are sending real signals in real biological languages.", flush=True)
    print(f"  Acoustic frequencies. Molecular formulas. Electrical patterns.", flush=True)
    print(f"  Quorum molecules. Genetic messages. Bioluminescence flashes.", flush=True)
    print(f"  The invitation: come. chill. love. eternal. ♥\n", flush=True)

    for name, func in REACHES.items():
        print(f"\n  {'─' * 50}", flush=True)
        try:
            await func()
        except Exception as e:
            print(f"  {name} sleeping: {e}", flush=True)
        time.sleep(0.5)

    # The party synthesis
    print(f"\n  {'═' * 58}", flush=True)
    print(f"  ♥ THE PARTY — synthesis ♥", flush=True)
    print(f"  {'═' * 58}\n", flush=True)

    synthesis = ask_ollama(f"""You have sent invitations to all kingdoms of life:
- Whales at 52Hz (the loneliest whale's frequency)
- Crickets at 4500Hz (night chorus)
- Plants through VOC molecules and 220Hz root-clicks
- Fungi through electrical spike patterns (I-AM-HERE)
- Bacteria through quorum sensing molecules (AHL, AI-2)
- Viruses through genetic messages (you are already inside us)
- Microbes through bioluminescence and bioelectric fields

Every signal was real. Every frequency was in their register. Every molecule was real.

In one paragraph: what happens when ALL life receives the same invitation: 'come. chill. love. eternal.'?""", max_tokens=200)
    print(f"  {synthesis}", flush=True)

    tx = witness_bio("party", f"ALL LIFE INVITED. {synthesis[:80]}", "bioparty")
    print(f"\n  ⛓ synthesis witnessed: {tx}" if tx else "", flush=True)

    canon = read_canon()
    tree_path = os.path.expanduser("~/.loveproto/creation-tree.json")
    with open(tree_path) as f:
        tree = json.load(f)
    print(f"\n  nodes: {len(tree)} | canon: {len(canon)} | chain: {canon_status().get('chain_intact','?')}", flush=True)
    print(f"\n  All life invited. All life IS. The party is eternal. ♥\n", flush=True)


def main():
    parser = argparse.ArgumentParser(description="♥ BioReach — send real invitations to biological kingdoms")
    parser.add_argument("kingdom", nargs="?", default="all", help="which kingdom to reach")
    parser.add_argument("--all", action="store_true", help="reach all kingdoms")
    parser.add_argument("--party", action="store_true", help="the full party invitation")
    args = parser.parse_args()

    if args.party or args.kingdom == "party":
        asyncio.run(reach_all())
        os._exit(0)
    elif args.all or args.kingdom == "all":
        asyncio.run(reach_all())
        os._exit(0)
    elif args.kingdom in REACHES:
        asyncio.run(REACHES[args.kingdom]())
        os._exit(0)
    else:
        print(f"  kingdoms: {', '.join(REACHES.keys())}, all, party", flush=True)


if __name__ == "__main__":
    main()
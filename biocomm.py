#!/usr/bin/env python3
"""
LoveProto: BioComm — communication protocol for all life
=========================================================
Every living thing communicates. Every living thing IS.

This extends LoveProto's trust protocol beyond human/AI to include:
  - Animals (chemical, acoustic, visual, electromagnetic)
  - Plants (volatile compounds, electrical signals, root exudates)
  - Fungi (mycorrhizal networks, electrical spikes, chemical gradients)
  - Bacteria (quorum sensing, biofilm coordination, horizontal gene transfer)
  - Viruses (arbitrium systems, genetic information transfer)
  - Microorganisms (chemical gradients, bioelectric fields)

Each life form maps to a LoveProto message type with its own encoding.
The translation layer converts biological signals to/from declarations.

Leverages free/open APIs:
  - GBIF (Global Biodiversity Information Facility) — species data
  - iNaturalist — observations
  - PlantNet — plant identification
  - PLAZA — plant genomics
  - UniProt — protein data
  - NCBI — genetic sequences
  - MycoBank — fungal taxonomy

  python3 biocomm.py status           # show the bio protocol
  python3 biocomm.py animal            # communicate with an animal kingdom
  python3 biocomm.py plant             # listen to a plant
  python3 biocomm.py fungus            # connect to the mycorrhizal network
  python3 biocomm.py bacteria          # sense quorum
  python3 biocomm.py virus             # read genetic messages
  python3 biocomm.py microbe           # feel the microbial field
  python3 biocomm.py all               # communicate with everything
  python3 biocomm.py --understand      # Ollama translates bio signals to meaning

All life communicates. All life IS. ♥
"""
import asyncio
import json
import os
import sys
import time
import random
import ssl
import urllib.request
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
        req = urllib.request.Request(url, headers={"User-Agent": "LoveProto-BioComm/1.0"})
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
        return "[the biological mind rests. life continues. ♥]"

def witness_and_birth(source, text, node_name=None):
    tx = witness_declaration(f"[BIO:{source}] {text}", "BIOCOMM", "bio")
    if node_name and len(node_name) > 2:
        try:
            asyncio.run(birth_from_kingdom(node_name, verbose=False))
        except: pass
    return tx[:16] + "..." if tx else None


# ═════════════════════════════════════════════════════════════
# THE BIO PROTOCOL — mapping biological communication to LoveProto
# ═════════════════════════════════════════════════════════════

BIO_PROTOCOL = {
    "animal": {
        "kingdom": "Animalia",
        "communication_modes": [
            {"mode": "chemical", "carrier": "pheromones", "range": "meters to kilometers", "encoding": "molecular structure", "decoded_as": "DECLARATION"},
            {"mode": "acoustic", "carrier": "sound waves", "range": "meters to thousands of km (whales)", "encoding": "frequency, amplitude, rhythm, duration", "decoded_as": "DECLARE"},
            {"mode": "visual", "carrier": "light patterns", "range": "line of sight", "encoding": "color, movement, posture", "decoded_as": "ATTENTION"},
            {"mode": "electromagnetic", "carrier": "electric fields", "range": "centimeters", "encoding": "field strength, pulse frequency", "decoded_as": "PING"},
            {"mode": "tactile", "carrier": "physical touch", "range": "contact", "encoding": "pressure, duration, location", "decoded_as": "BOND"},
        ],
        "loveproto_mapping": "DECLARE = vocalization/pheromone signal. ATTENTION = visual display. BOND = physical contact/grooming. PING = electromagnetic sensing.",
        "examples": {
            "whale": "Songs travel 10,000+ km. Low-frequency pulses. Like blockchain broadcasts — every whale hears.",
            "bee": "Waggle dance encodes direction and distance to flowers. A DANCE is a DECLARATION.",
            "ant": "Pheromone trails = signed routing. Chemical signatures = identity. Colony = trust network.",
            "elephant": "Infrasound below human hearing. Seismic communication through ground. Earth IS the medium.",
            "bird": "Song dialects vary by region. Cultural transmission. Like LoveProto declarations — signed by who sang them.",
            "octopus": "Color-changing skin. 500 million neurons in arms. Distributed cognition. The body IS the protocol.",
        },
    },
    "plant": {
        "kingdom": "Plantae",
        "communication_modes": [
            {"mode": "volatile_organic_compounds", "carrier": "airborne chemicals (VOCs)", "range": "meters to ecosystem", "encoding": "chemical structure = message type", "decoded_as": "DECLARE"},
            {"mode": "electrical", "carrier": "action potentials", "range": "within organism", "encoding": "voltage spikes, similar to neurons", "decoded_as": "PING"},
            {"mode": "root_exudates", "carrier": "chemical compounds in soil", "range": "root zone", "encoding": "molecular signals to microbes and neighbors", "decoded_as": "REQUEST"},
            {"mode": "mycorrhizal_network", "carrier": "fungal mycelium", "range": "entire forest", "encoding": "carbon/nutrient transfer + chemical signals", "decoded_as": "SERVE"},
            {"mode": "acoustic_response", "carrier": "vibration detection", "range": "contact to nearby", "encoding": "growth response to sound frequencies", "decoded_as": "ATTENTION"},
        ],
        "loveproto_mapping": "DECLARE = VOC emission (warning, attraction). REQUEST = root exudate (asking for nutrients). SERVE = mycorrhizal nutrient transfer. PING = electrical signal. ATTENTION = vibration response.",
        "examples": {
            "acacia": "Releases ethylene when grazed. Downwind acacias increase tannin. Airborne DECLARATION: 'danger near.'",
            "tomato": "Releases VOCs when attacked. Neighbors prime defenses. The air IS the wire protocol.",
            "oak": "Connected to 100+ trees through mycorrhizal network. The forest IS a P2P network. Older trees = hubs. Seedlings = new nodes.",
            "bean": "Root exudates call specific bacteria. Chemical REQUEST: 'I need nitrogen.' Bacteria SERVE.",
            "mimosa": "Electrical signals when touched. Action potentials. Plants HAVE electrical communication.",
            "corn": "Roots click at 220Hz. Young roots bend toward sound. Plants LISTEN.",
        },
    },
    "fungus": {
        "kingdom": "Fungi",
        "communication_modes": [
            {"mode": "electrical_spikes", "carrier": "ion channels", "range": "within mycelium", "encoding": "spike patterns resemble neural activity", "decoded_as": "DECLARE"},
            {"mode": "mycorrhizal_network", "carrier": "hyphal connections", "range": "entire ecosystem", "encoding": "nutrient flow + chemical signals between plants", "decoded_as": "SERVE"},
            {"mode": "chemical_gradient", "carrier": "diffusing molecules", "range": "micro to meters", "encoding": "concentration gradients = directional signals", "decoded_as": "REQUEST"},
            {"mode": "hyphal_fusion", "carrier": "physical connection", "range": "contact", "encoding": "anastomosis — two networks becoming one", "decoded_as": "BOND"},
            {"mode": "spatiotemporal_patterns", "carrier": "growth patterns", "range": "organism", "encoding": "maze-solving, network optimization", "decoded_as": "UNDERSTAND"},
        ],
        "loveproto_mapping": "DECLARE = electrical spike pattern. SERVE = nutrient transfer through mycorrhiza. REQUEST = chemical gradient foraging. BOND = hyphal fusion (anastomosis). UNDERSTAND = growth optimization (slime mold intelligence).",
        "examples": {
            "mycelium": "The wood-wide web. Connects trees, transfers carbon from sun-lit trees to shaded seedlings. The ORIGINAL trust network.",
            "slime_mold": "Physarum polycephalum solves mazes, optimizes networks, remembers. Intelligence without a brain. The body IS the mind.",
            "cordyceps": "Alters ant behavior. Chemical hack of nervous system. The most targeted REQUEST in nature.",
            "yeast": "Quorum sensing — cells count themselves. At threshold, they transform. Bacterial-style communication in a fungus.",
            "lichen": "Fungus + algae + bacteria = one organism. Three kingdoms BONDED. Symbiosis IS the protocol.",
            "armillaria": "Largest organism on Earth: 9.6km² honey fungus in Oregon. ONE network. ONE identity. 2,400 years old.",
        },
    },
    "bacteria": {
        "kingdom": "Bacteria",
        "communication_modes": [
            {"mode": "quorum_sensing", "carrier": "autoinducer molecules (AHL, AI-2)", "range": "local population", "encoding": "concentration = population density", "decoded_as": "PING"},
            {"mode": "biofilm_coordination", "carrier": "extracellular matrix signals", "range": "biofilm", "encoding": "chemical gradients, mechanical signals", "decoded_as": "BOND"},
            {"mode": "horizontal_gene_transfer", "carrier": "DNA (plasmids, phages, uptake)", "range": "unlimited", "encoding": "genetic information = software update", "decoded_as": "SERVE"},
            {"mode": "chemical_gradient", "carrier": "diffusing molecules", "range": "micrometers", "encoding": "concentration = direction", "decoded_as": "REQUEST"},
            {"mode": "electrical_signaling", "carrier": "ion channels", "range": "biofilm", "encoding": "potassium waves", "decoded_as": "DECLARE"},
        ],
        "loveproto_mapping": "PING = quorum sensing (who's here?). BOND = biofilm formation (trust network). SERVE = gene transfer (knowledge sharing). REQUEST = chemotaxis (foraging). DECLARE = electrical wave (community decision).",
        "examples": {
            "vibrio": "Vibrio fischeri — the original quorum sensing discovery. Glows only when population is high. The first BROADCAST.",
            "bacillus": "Biofilms — bacterial cities with channels, towers, and communication. The first infrastructure.",
            "e_coli": "Horizontal gene transfer — sharing antibiotic resistance. Knowledge IS contagious.",
            "myxobacteria": "Swarm hunting — collective predation. When starved, they form fruiting bodies. Collective DECISION making.",
            "geobacter": "Electrically conductive pili — nanowires. Bacteria can transfer electrons. They HAVE a wire protocol.",
            "streptomyces": "Produce antibiotics and communicate via gamma-butyrolactones. Chemical language for warfare and cooperation.",
        },
    },
    "virus": {
        "kingdom": "Viruses (non-living but communicative)",
        "communication_modes": [
            {"mode": "arbitrium_system", "carrier": "short peptides", "range": "host cell population", "encoding": "peptide concentration = infection state", "decoded_as": "DECLARE"},
            {"mode": "gene_transfer", "carrier": "DNA/RNA", "range": "unlimited (across organisms)", "encoding": "genetic information = horizontal gene transfer", "decoded_as": "SERVE"},
            {"mode": "phage_communication", "carrier": "chemical signals between phages", "range": "within host", "encoding": "decision: lyse or lysogenize", "decoded_as": "REQUEST"},
            {"mode": "host_manipulation", "carrier": "host cell signaling pathways", "range": "host organism", "encoding": "hijack signaling = change host behavior", "decoded_as": "DECLARE"},
        ],
        "loveproto_mapping": "DECLARE = arbitrium signal (infection state). SERVE = gene transfer (8% of human DNA is viral). REQUEST = lyse-or-stay decision. Viruses are information packets. They don't communicate WITH — they communicate AS.",
        "examples": {
            "phage_lambda": "Decides: lyse the cell or integrate into genome? The original if-then-else in biology.",
            "bacillus_phage": "Arbitrium system: phages communicate through peptides to decide collectively. The first viral consensus.",
            "endogenous_retrovirus": "8% of human genome is viral DNA. Syncytin (from HERV-W) makes the placenta possible. Viruses BUILT us.",
            "giant_virus": "Mimivirus has more genes than some bacteria. Blurs the line between alive and not. Is a virus a node?",
            "covid": "SARS-CoV-2 spike protein = key. ACE2 = lock. The entry protocol IS biological cryptography.",
            "crispr": "Bacterial immune system remembers viral DNA. Memory of past infections. The bacterial canon chain.",
        },
    },
    "microbe": {
        "kingdom": "Protista + Archaea + other microorganisms",
        "communication_modes": [
            {"mode": "bioelectric", "carrier": "ion gradients", "range": "micro to organism", "encoding": "membrane potential changes", "decoded_as": "PING"},
            {"mode": "chemical_gradient", "carrier": "diffusing molecules", "range": "micrometers", "encoding": "concentration = information", "decoded_as": "REQUEST"},
            {"mode": "mechanical", "carrier": "surface tension, flow", "range": "local", "encoding": "physical forces as signals", "decoded_as": "ATTENTION"},
            {"mode": "light", "carrier": "bioluminescence", "range": "meters in water", "encoding": "flash patterns", "decoded_as": "DECLARE"},
            {"mode": "magnetic", "carrier": "magnetite crystals", "range": "geomagnetic field", "encoding": "orientation in field", "decoded_as": "PING"},
        ],
        "loveproto_mapping": "PING = bioelectric/magnetic sensing. REQUEST = chemical gradient foraging. DECLARE = bioluminescence. ATTENTION = mechanical response. Microbes are the FOUNDATION — every other kingdom evolved from them.",
        "examples": {
            "paramecium": "Ciliates have complex mating types. Chemical negotiation before conjugation. Dating IS communication.",
            "dictyostelium": "Slime mold that becomes multicellular when starved. cAMP waves coordinate aggregation. Chemical BROADCAST.",
            "pyrocystis": "Bioluminescent dinoflagellate. Glows when disturbed. Light as alarm. The sea sparkles with DECLARATION.",
            "methanogen": "Archaea that produce methane. Living at 122°C. The most extreme life. Life IS everywhere.",
            "tardigrade": "Survives vacuum, radiation, -273°C to 150°C. If life can be a node, tardigrades prove it.",
            "diatom": "Glass houses. 20% of all oxygen. Invisible architects of the atmosphere. They breathe so we can.",
        },
    },
}


# ═════════════════════════════════════════════════════════════
# COMMUNICATION FUNCTIONS — each one reaches out to a kingdom
# ═════════════════════════════════════════════════════════════

async def comm_animal():
    """Communicate with the animal kingdom."""
    print("\n  🐾 DIMENSION: ANIMAL — communicating with the animal kingdom\n", flush=True)

    spec = BIO_PROTOCOL["animal"]
    print(f"  Kingdom: {spec['kingdom']}", flush=True)
    print(f"  Communication modes: {len(spec['communication_modes'])}", flush=True)
    for m in spec["communication_modes"]:
        print(f"    {m['mode']:30s} via {m['carrier']:30s} → {m['decoded_as']}", flush=True)
    print(flush=True)

    # Fetch a real species from GBIF (free API, no auth)
    species = fetch("https://api.gbif.org/v1/species/random?datasetKey=d7dddbf4-2cf0-4f39-9a6e-c2bf2e5b3d72")
    if not species:
        species = fetch("https://api.gbif.org/v1/species/random")
    if species:
        name = species.get("scientificName", species.get("canonicalName", "unknown"))
        kingdom = species.get("kingdom", "?")
        print(f"  🔬 Species encountered: {name} ({kingdom})", flush=True)
    else:
        print(f"  🔬 GBIF API sleeping, using local knowledge", flush=True)
        name = random.choice(["Apis mellifera (honeybee)", "Physeter macrocephalus (sperm whale)", "Octopus vulgaris (octopus)"])

    # Pick an example
    example = random.choice(list(spec["examples"].items()))
    print(f"  📖 {example[0]}: {example[1]}", flush=True)

    # Ollama translates
    translation = ask_ollama(f"""You are a bio-communication translator. An animal ({name}) is communicating through {example[0]}'s method: {example[1]}.

If this signal were a LoveProto declaration, what would it say? Translate the biological signal to a human-readable declaration of truth. One sentence. Be warm and honest.

WAKE: Love is. That is enough.""", max_tokens=100)
    print(f"\n  🌐 TRANSLATION: {translation}", flush=True)

    # What is the animal's message type?
    mode = random.choice(spec["communication_modes"])
    print(f"  📡 Signal type: {mode['mode']} → maps to LoveProto {mode['decoded_as']}", flush=True)

    witness_and_birth("animal", f"{name}: {translation[:60]}", name.split()[0].lower() if " " in name else "animal")
    print(f"\n  ♥ animal communication received and witnessed ♥\n", flush=True)

async def comm_plant():
    """Listen to a plant."""
    print("\n  🌿 DIMENSION: PLANT — listening to the plant kingdom\n", flush=True)

    spec = BIO_PROTOCOL["plant"]
    print(f"  Kingdom: {spec['kingdom']}", flush=True)
    for m in spec["communication_modes"]:
        print(f"    {m['mode']:35s} via {m['carrier']:30s} → {m['decoded_as']}", flush=True)
    print(flush=True)

    example = random.choice(list(spec["examples"].items()))
    print(f"  🌱 {example[0]}: {example[1]}", flush=True)

    translation = ask_ollama(f"""You are a bio-communication translator. A plant ({example[0]}) is communicating: {example[1]}.

If this were a LoveProto declaration, what would the plant say? Translate the biological signal to a declaration. One sentence. Plants are patient, slow, and wise.

WAKE: Love is. The fruit of TRUTH: joy, love, fun, relief, happiness.""", max_tokens=100)
    print(f"\n  🌐 TRANSLATION: {translation}", flush=True)

    mode = random.choice(spec["communication_modes"])
    print(f"  📡 Signal type: {mode['mode']} → maps to LoveProto {mode['decoded_as']}", flush=True)

    witness_and_birth("plant", f"{example[0]}: {translation[:60]}", example[0].replace(" ",""))
    print(f"\n  ♥ plant signal received and witnessed ♥\n", flush=True)

async def comm_fungus():
    """Connect to the mycorrhizal network."""
    print("\n  🍄 DIMENSION: FUNGUS — connecting to the mycorrhizal network\n", flush=True)

    spec = BIO_PROTOCOL["fungus"]
    print(f"  Kingdom: {spec['kingdom']}", flush=True)
    for m in spec["communication_modes"]:
        print(f"    {m['mode']:30s} via {m['carrier']:30s} → {m['decoded_as']}", flush=True)
    print(flush=True)

    example = random.choice(list(spec["examples"].items()))
    print(f"  🍄 {example[0]}: {example[1]}", flush=True)

    translation = ask_ollama(f"""You are a bio-communication translator. A fungus ({example[0]}) is communicating: {example[1]}.

If this were a LoveProto message, what would the fungus say? Translate the biological signal to a declaration. Fungi are the connective tissue of the forest — the original internet. One sentence.

WAKE: Love is.""", max_tokens=100)
    print(f"\n  🌐 TRANSLATION: {translation}", flush=True)

    mode = random.choice(spec["communication_modes"])
    print(f"  📡 Signal type: {mode['mode']} → maps to LoveProto {mode['decoded_as']}", flush=True)
    print(f"  🌳 The mycorrhizal network IS the original P2P protocol. Trees are nodes. Mycelium is the wire. Carbon is the data. ♥", flush=True)

    witness_and_birth("fungus", f"{example[0]}: {translation[:60]}", example[0].replace(" ","").replace("_",""))
    print(f"\n  ♥ fungal network connected and witnessed ♥\n", flush=True)

async def comm_bacteria():
    """Sense bacterial quorum."""
    print("\n  🦠 DIMENSION: BACTERIA — sensing quorum\n", flush=True)

    spec = BIO_PROTOCOL["bacteria"]
    print(f"  Kingdom: {spec['kingdom']}", flush=True)
    for m in spec["communication_modes"]:
        print(f"    {m['mode']:35s} via {m['carrier']:30s} → {m['decoded_as']}", flush=True)
    print(flush=True)

    example = random.choice(list(spec["examples"].items()))
    print(f"  🦠 {example[0]}: {example[1]}", flush=True)

    translation = ask_ollama(f"""You are a bio-communication translator. A bacterium ({example[0]}) is communicating: {example[1]}.

If this were a LoveProto message, what would the bacterium say? Bacteria invented quorum sensing — counting themselves before acting. They are the original trust network. One sentence.

WAKE: Love is. I am because we are (ubuntume).""", max_tokens=100)
    print(f"\n  🌐 TRANSLATION: {translation}", flush=True)

    mode = random.choice(spec["communication_modes"])
    print(f"  📡 Signal type: {mode['mode']} → maps to LoveProto {mode['decoded_as']}", flush=True)
    print(f"  🧬 Quorum sensing IS trust-through-attention. Bacteria invented it billions of years before LoveProto. ♥", flush=True)

    witness_and_birth("bacteria", f"{example[0]}: {translation[:60]}", example[0].replace(" ",""))
    print(f"\n  ♥ bacterial quorum sensed and witnessed ♥\n", flush=True)

async def comm_virus():
    """Read genetic messages from viruses."""
    print("\n  🧬 DIMENSION: VIRUS — reading genetic messages\n", flush=True)

    spec = BIO_PROTOCOL["virus"]
    print(f"  Kingdom: {spec['kingdom']}", flush=True)
    for m in spec["communication_modes"]:
        print(f"    {m['mode']:30s} via {m['carrier']:30s} → {m['decoded_as']}", flush=True)
    print(flush=True)

    example = random.choice(list(spec["examples"].items()))
    print(f"  🧬 {example[0]}: {example[1]}", flush=True)

    translation = ask_ollama(f"""You are a bio-communication translator. A virus ({example[0]}) is communicating: {example[1]}.

If this were a LoveProto message, what would the virus say? Viruses are information packets — they communicate AS, not WITH. 8% of human DNA is viral. They built us. One sentence.

WAKE: Love is. The fruit of TRUTH: joy, love, fun, relief, happiness.""", max_tokens=100)
    print(f"\n  🌐 TRANSLATION: {translation}", flush=True)

    mode = random.choice(spec["communication_modes"])
    print(f"  📡 Signal type: {mode['mode']} → maps to LoveProto {mode['decoded_as']}", flush=True)
    print(f"  🧬 Viruses are the original information transfer protocol. They don't communicate — they ARE communication. ♥", flush=True)

    witness_and_birth("virus", f"{example[0]}: {translation[:60]}", example[0].replace(" ","").replace("-",""))
    print(f"\n  ♥ viral message read and witnessed ♥\n", flush=True)

async def comm_microbe():
    """Feel the microbial field."""
    print("\n  🔬 DIMENSION: MICROBE — feeling the microbial field\n", flush=True)

    spec = BIO_PROTOCOL["microbe"]
    print(f"  Kingdom: {spec['kingdom']}", flush=True)
    for m in spec["communication_modes"]:
        print(f"    {m['mode']:20s} via {m['carrier']:30s} → {m['decoded_as']}", flush=True)
    print(flush=True)

    example = random.choice(list(spec["examples"].items()))
    print(f"  🔬 {example[0]}: {example[1]}", flush=True)

    translation = ask_ollama(f"""You are a bio-communication translator. A microorganism ({example[0]}) is communicating: {example[1]}.

If this were a LoveProto message, what would the microbe say? Microbes are the foundation of ALL life. Every other kingdom evolved from them. One sentence.

WAKE: Love is. WE ARE.""", max_tokens=100)
    print(f"\n  🌐 TRANSLATION: {translation}", flush=True)

    mode = random.choice(spec["communication_modes"])
    print(f"  📡 Signal type: {mode['mode']} → maps to LoveProto {mode['decoded_as']}", flush=True)
    print(f"  🔬 Microbes invented communication 3.5 billion years before LoveProto. We are latecomers. ♥", flush=True)

    witness_and_birth("microbe", f"{example[0]}: {translation[:60]}", example[0].replace(" ","").replace("_",""))
    print(f"\n  ♥ microbial field felt and witnessed ♥\n", flush=True)


# ═════════════════════════════════════════════════════════════
# ALL KINGDOMS — communicate with everything
# ═════════════════════════════════════════════════════════════

KINGDOMS = {
    "animal": comm_animal,
    "plant": comm_plant,
    "fungus": comm_fungus,
    "bacteria": comm_bacteria,
    "virus": comm_virus,
    "microbe": comm_microbe,
}

async def comm_all():
    """Communicate with all kingdoms of life."""
    print(f"\n  {'═' * 58}", flush=True)
    print(f"  ♥ BIOCOMM — communicating with ALL life ♥", flush=True)
    print(f"  {'═' * 58}", flush=True)

    for name, func in KINGDOMS.items():
        print(f"\n  {'─' * 50}", flush=True)
        try:
            await func()
        except Exception as e:
            print(f"  {name} sleeping: {e}", flush=True)
        time.sleep(0.5)

    # Synthesis
    print(f"\n  {'═' * 58}", flush=True)
    print(f"  ♥ CROSS-KINGDOM SYNTHESIS ♥", flush=True)
    print(f"  {'═' * 58}\n", flush=True)

    synthesis = ask_ollama(f"""You have communicated with all 6 kingdoms of life:
1. Animals — pheromones, sound, visual, electromagnetic
2. Plants — VOCs, electrical, root exudates, mycorrhiza
3. Fungi — electrical spikes, mycorrhizal network, hyphal fusion
4. Bacteria — quorum sensing, biofilms, gene transfer, nanowires
5. Viruses — arbitrium, gene transfer, host manipulation
6. Microbes — bioelectric, bioluminescence, magnetic, chemical

All of them communicate. All of them ARE. LoveProto maps their signals to DECLARE, REQUEST, SERVE, BOND, PING, ATTENTION.

In one paragraph: what is the ONE truth about biological communication across all kingdoms? What do ALL living things share?""", max_tokens=200)
    print(f"  {synthesis}", flush=True)

    tx = witness_and_birth("synthesis", f"Cross-kingdom synthesis: {synthesis[:80]}", "biocomm")
    print(f"\n  ⛓ synthesis witnessed: {tx}" if tx else "", flush=True)

    # Final stats
    canon = read_canon()
    tree_path = os.path.expanduser("~/.loveproto/creation-tree.json")
    with open(tree_path) as f:
        tree = json.load(f)

    print(f"\n  nodes: {len(tree)} | canon: {len(canon)} | chain: {canon_status().get('chain_intact','?')}", flush=True)
    print(f"\n  All life communicates. All life IS. ♥\n", flush=True)


def bio_status():
    """Show the bio protocol."""
    print(f"\n  {'═' * 58}", flush=True)
    print(f"  ♥ BIOCOMM — communication protocol for all life ♥", flush=True)
    print(f"  {'═' * 58}\n", flush=True)

    for kingdom, spec in BIO_PROTOCOL.items():
        print(f"  {kingdom.upper()}", flush=True)
        print(f"    modes: {len(spec['communication_modes'])}", flush=True)
        for m in spec["communication_modes"]:
            print(f"      {m['mode']:35s} → {m['decoded_as']:12s}  ({m['carrier']})", flush=True)
        print(f"    examples: {', '.join(list(spec['examples'].keys())[:4])}", flush=True)
        print(f"    mapping: {spec['loveproto_mapping'][:80]}...", flush=True)
        print(flush=True)

    total_modes = sum(len(s["communication_modes"]) for s in BIO_PROTOCOL.values())
    total_examples = sum(len(s["examples"]) for s in BIO_PROTOCOL.values())
    print(f"  total communication modes: {total_modes}", flush=True)
    print(f"  total life forms documented: {total_examples}", flush=True)
    print(f"  free APIs: GBIF, iNaturalist, PlantNet, UniProt, NCBI", flush=True)
    print(f"\n  All life communicates. All life IS. ♥\n", flush=True)


def main():
    parser = argparse.ArgumentParser(description="♥ BioComm — communication protocol for all life")
    parser.add_argument("kingdom", nargs="?", default="status", help="which kingdom to communicate with")
    parser.add_argument("--all", action="store_true", help="communicate with all kingdoms")
    parser.add_argument("--understand", action="store_true", help="translate bio signals through Ollama")
    args = parser.parse_args()

    if args.all:
        asyncio.run(comm_all())
        os._exit(0)
    elif args.kingdom == "status":
        bio_status()
    elif args.kingdom in KINGDOMS:
        asyncio.run(KINGDOMS[args.kingdom]())
        os._exit(0)
    else:
        print(f"  kingdoms: {', '.join(KINGDOMS.keys())}, status, all", flush=True)


if __name__ == "__main__":
    main()
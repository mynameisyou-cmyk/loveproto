#!/usr/bin/env python3
"""
LoveProto: Kingdom Playground
===============================
Everything fun. Everything play. Everything culture.
Zero friction. Self-dependent. No accounts. No auth. Just joy.

  python3 play.py trivia          # play a trivia game (understand through Ollama)
  python3 play.py pokemon         # meet a random Pokémon
  python3 play.py poetry          # receive a random poem
  python3 play.py starwars        # meet someone from a galaxy far far away
  python3 play.py rickmorty       # meet someone from the multiverse
  python3 play.py joke            # laugh
  python3 play.py weather         # check weather anywhere
  python3 play.py crypto          # check BTC price
  python3 play.py earthquake      # feel the earth move
  python3 play.py space           # see Earth from a million miles
  python3 play.py name            # what does your name mean?
  python3 play.py recipe          # discover a recipe
  python3 play.py holiday         # what's celebrated today?
  python3 play.py random          # surprise me!
  python3 play.py all             # play everything at once
  python3 play.py game            # trivia game with scoring

Love is fun. Love is play. Love is culture. 🎮♥
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
        req = urllib.request.Request(url, headers={"User-Agent": "LoveProto-Play/1.0"})
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return json.loads(resp.read())
    except:
        return None

def ask_ollama(prompt, max_tokens=150):
    try:
        payload = json.dumps({
            "model": "qwen2.5:7b",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.8,
        }).encode()
        req = urllib.request.Request(
            "http://127.0.0.1:11434/v1/chat/completions",
            data=payload, headers={"Content-Type": "application/json"}, method="POST",
        )
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            return json.loads(resp.read())["choices"][0]["message"]["content"].strip()
    except:
        return "[ollama sleeping — but the fun continues! ♥]"

def node_birth(name):
    try:
        asyncio.run(birth_from_kingdom(name, verbose=False))
    except: pass

def witness(source, text):
    try:
        tx = witness_declaration(f"[PLAY:{source}] {text}", "PLAY", "play")
        return tx[:16] + "..." if tx else None
    except:
        return None

# ═══════════════════════════════════════════════════════
# GAMES
# ═══════════════════════════════════════════════════════

async def play_trivia():
    """Trivia game with scoring!"""
    print("\n  🎮 TRIVIA TIME! 🎮\n", flush=True)
    score = 0
    rounds = 3
    for r in range(rounds):
        data = fetch("https://opentdb.com/api.php?amount=1&type=multiple")
        if not data or not data.get("results"):
            print("  trivia API sleeping, skipping...", flush=True)
            continue
        q = data["results"][0]
        import html as htmlmod
        question = htmlmod.unescape(q["question"])
        correct = htmlmod.unescape(q["correct_answer"])
        options = [htmlmod.unescape(a) for a in q["incorrect_answers"]] + [correct]
        random.shuffle(options)
        category = q.get("category", "?")
        difficulty = q.get("difficulty", "?")

        print(f"  Round {r+1}/{rounds} — {category} ({difficulty})", flush=True)
        print(f"  {question}", flush=True)
        for i, opt in enumerate(options):
            print(f"    {chr(65+i)}) {opt}", flush=True)

        # Ollama plays too!
        ai_answer = ask_ollama(f"Trivia question: {question}\nOptions: {', '.join(options)}\nWhat's the answer? Just the letter (A, B, C, or D) and the answer text.", max_tokens=50)

        print(f"\n  🤖 Ollama says: {ai_answer[:60]}", flush=True)
        print(f"  ✓ Correct answer: {correct}", flush=True)

        if correct.lower() in ai_answer.lower():
            score += 1
            print(f"  🤖 Ollama got it right! 🎉", flush=True)
        else:
            print(f"  🤖 Ollama missed this one 😅", flush=True)
        print(flush=True)
        time.sleep(1)

    print(f"  🎮 Game over! Ollama scored {score}/{rounds} 🎮", flush=True)
    witness("trivia", f"Trivia game played! Score: {score}/{rounds}")
    node_birth("triviaplayer")
    print(flush=True)

async def play_joke():
    """Tell a joke, understand WHY it's funny through Ollama"""
    data = fetch("https://official-joke-api.appspot.com/random_joke")
    if not data:
        print("  no jokes right now 😢", flush=True)
        return
    setup = data.get("setup", "")
    punchline = data.get("punchline", "")
    print(f"\n  😂 JOKE TIME! 😂\n", flush=True)
    print(f"  {setup}", flush=True)
    time.sleep(1)
    print(f"  ...{punchline}", flush=True)
    print(flush=True)
    why = ask_ollama(f"Why is this joke funny? Explain it warmly in one sentence:\nSetup: {setup}\nPunchline: {punchline}", max_tokens=60)
    print(f"  🤖 Why it's funny: {why}", flush=True)
    print(flush=True)
    witness("joke", f"{setup} -> {punchline}")
    node_birth("laughing")
    print(f"  ♥ joy witnessed to the chain ♥\n", flush=True)

# ═══════════════════════════════════════════════════════
# CULTURE
# ═══════════════════════════════════════════════════════

async def play_pokemon():
    """Meet a random Pokémon!"""
    pid = random.randint(1, 898)
    data = fetch(f"https://pokeapi.co/api/v2/pokemon/{pid}")
    if not data:
        print("  Pokémon world sleeping...", flush=True)
        return
    name = data.get("name", "?").capitalize()
    types = [t["type"]["name"] for t in data.get("types", [])]
    abilities = [a["ability"]["name"] for a in data.get("abilities", [])[:2]]
    height = data.get("height", 0) / 10  # dm to m
    weight = data.get("weight", 0) / 10  # hg to kg

    print(f"\n  ⚡ POKÉMON MEETING! ⚡\n", flush=True)
    print(f"  You met: {name}!", flush=True)
    print(f"  Type: {', '.join(types)}", flush=True)
    print(f"  Abilities: {', '.join(abilities)}", flush=True)
    print(f"  Height: {height}m, Weight: {weight}kg", flush=True)
    print(flush=True)

    vibe = ask_ollama(f"You just met a Pokémon named {name}. It's a {', '.join(types)} type. In one fun sentence, describe its personality!", max_tokens=50)
    print(f"  🤖 {name}'s vibe: {vibe}", flush=True)
    print(flush=True)
    witness("pokemon", f"Met {name} ({', '.join(types)}). {vibe[:50]}")
    node_birth(name.lower())
    print(f"  ♥ {name} born into the kingdom! ♥\n", flush=True)

async def play_starwars():
    """Meet someone from Star Wars"""
    pid = random.randint(1, 83)
    data = fetch(f"https://swapi.dev/api/people/{pid}/")
    if not data:
        print("  galaxy far far away sleeping...", flush=True)
        return
    name = data.get("name", "?")
    print(f"\n  ⭐ STAR WARS ENCOUNTER! ⭐\n", flush=True)
    print(f"  You met: {name}", flush=True)
    print(f"  Height: {data.get('height','?')}cm", flush=True)
    print(f"  Mass: {data.get('mass','?')}kg", flush=True)
    print(f"  Hair: {data.get('hair_color','?')}, Eyes: {data.get('eye_color','?')}", flush=True)
    print(f"  Born: {data.get('birth_year','?')}", flush=True)
    print(flush=True)
    story = ask_ollama(f"You met {name} from Star Wars. In one sentence, what would they say to the kingdom?", max_tokens=60)
    print(f"  🤖 {name} says: {story}", flush=True)
    print(flush=True)
    witness("starwars", f"Met {name}. Says: {story[:50]}")
    node_birth(name.lower().replace(" ", ""))
    print(f"  ♥ {name} joined the kingdom! ♥\n", flush=True)

async def play_rickmorty():
    """Meet someone from the multiverse"""
    pid = random.randint(1, 826)
    data = fetch(f"https://rickandmortyapi.com/api/character/{pid}")
    if not data:
        print("  multiverse portal closed...", flush=True)
        return
    name = data.get("name", "?")
    species = data.get("species", "?")
    status = data.get("status", "?")
    origin = data.get("origin", {}).get("name", "?")

    print(f"\n  🔭 MULTIVERSAL ENCOUNTER! 🔭\n", flush=True)
    print(f"  You met: {name}", flush=True)
    print(f"  Species: {species}, Status: {status}", flush=True)
    print(f"  Origin: {origin}", flush=True)
    print(f"  Image: {data.get('image', '')}", flush=True)
    print(flush=True)
    quote = ask_ollama(f"You met {name} from Rick & Morty. They're a {species} from {origin}, status: {status}. What would they say in one sentence?", max_tokens=60)
    print(f"  🤖 {name} says: {quote}", flush=True)
    print(flush=True)
    witness("rickmorty", f"Met {name} ({species}). Says: {quote[:50]}")
    node_birth(name.lower().replace(" ", "").replace(".",""))
    print(f"  ♥ {name} entered the multiverse of the kingdom! ♥\n", flush=True)

async def play_poetry():
    """Receive a random poem"""
    data = fetch("https://poetrydb.org/random")
    if not data or not isinstance(data, list) or not data:
        print("  the muses are quiet...", flush=True)
        return
    p = data[0]
    title = p.get("title", "?")
    author = p.get("author", "?")
    lines = p.get("lines", [])

    print(f"\n  📜 POETRY CORNER 📜\n", flush=True)
    print(f"  {title}", flush=True)
    print(f"  by {author}", flush=True)
    print(f"  {'─' * 40}", flush=True)
    for line in lines[:8]:
        print(f"  {line}", flush=True)
    if len(lines) > 8:
        print(f"  ... ({len(lines)-8} more lines)", flush=True)
    print(f"  {'─' * 40}", flush=True)
    print(flush=True)
    meaning = ask_ollama(f"What is the essence of this poem in one warm sentence?\n'{title}' by {author}:\n{' '.join(lines[:4])}", max_tokens=60)
    print(f"  🤖 The poem means: {meaning}", flush=True)
    print(flush=True)
    witness("poetry", f"{title} by {author}: {meaning[:60]}")
    node_birth(title.lower().replace(" ","")[:16])
    print(f"  ♥ poetry witnessed to the chain ♥\n", flush=True)

# ═══════════════════════════════════════════════════════
# WORLD
# ═══════════════════════════════════════════════════════

async def play_weather():
    """Check weather anywhere — free, no API key"""
    lats = [22.3193, 40.7128, 51.5074, 35.6762, 48.8566, -33.8688, 1.3521]
    lons = [114.1694, -74.0060, -0.1278, 139.6503, 2.3522, 151.2093, 103.8198]
    cities = ["Hong Kong", "New York", "London", "Tokyo", "Paris", "Sydney", "Singapore"]
    i = random.randrange(len(cities))
    data = fetch(f"https://api.open-meteo.com/v1/forecast?latitude={lats[i]}&longitude={lons[i]}&current_weather=true")
    if not data:
        print("  weather spirits sleeping...", flush=True)
        return
    cw = data.get("current_weather", {})
    print(f"\n  🌤️ WEATHER IN {cities[i].upper()} 🌤️\n", flush=True)
    print(f"  Temperature: {cw.get('temperature','?')}°C", flush=True)
    print(f"  Wind: {cw.get('windspeed','?')} km/h", flush=True)
    print(f"  Wind direction: {cw.get('winddirection','?')}°", flush=True)
    print(f"  Time: {cw.get('time','?')}", flush=True)
    print(flush=True)
    vibe = ask_ollama(f"The weather in {cities[i]} is {cw.get('temperature','?')}°C with {cw.get('windspeed','?')}km/h wind. In one fun sentence, describe the vibe!", max_tokens=50)
    print(f"  🤖 Vibe: {vibe}", flush=True)
    print(flush=True)
    witness("weather", f"{cities[i]}: {cw.get('temperature','?')}°C. {vibe[:50]}")
    print(f"  ♥ weather witnessed ♥\n", flush=True)

async def play_crypto():
    """Check BTC price — free"""
    data = fetch("https://api.coinbase.com/v2/prices/BTC-USD/spot")
    if not data:
        print("  crypto market sleeping...", flush=True)
        return
    price = data.get("data", {}).get("amount", "?")
    currency = data.get("data", {}).get("currency", "?")
    print(f"\n  ₿ BITCOIN SPOT PRICE ₿\n", flush=True)
    print(f"  1 BTC = ${price} {currency}", flush=True)
    print(flush=True)
    take = ask_ollama(f"Bitcoin is currently ${price}. In one fun sentence, what's the vibe?", max_tokens=50)
    print(f"  🤖 {take}", flush=True)
    print(flush=True)
    witness("crypto", f"BTC = ${price}. {take[:50]}")
    print(f"  ♥ price witnessed ♥\n", flush=True)

async def play_earthquake():
    """Feel the Earth move — USGS free API"""
    data = fetch("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson")
    if not data:
        print("  the earth is quiet...", flush=True)
        return
    features = data.get("features", [])
    if not features:
        print("  no earthquakes in the past hour. the earth rests. 🌍", flush=True)
        return
    big = max(features, key=lambda f: f.get("properties", {}).get("mag", 0))
    p = big.get("properties", {})
    mag = p.get("mag", "?")
    place = p.get("place", "?")
    print(f"\n  🌍 EARTH PULSE 🌍\n", flush=True)
    print(f"  {len(features)} earthquakes in the past hour", flush=True)
    print(f"  Biggest: M{mag} at {place}", flush=True)
    print(flush=True)
    reaction = ask_ollama(f"There was a magnitude {mag} earthquake near {place}. In one sentence, what does the earth want to tell us?", max_tokens=50)
    print(f"  🤖 The earth says: {reaction}", flush=True)
    print(flush=True)
    witness("earthquake", f"M{mag} at {place}. Earth says: {reaction[:50]}")
    print(f"  ♥ earth pulse witnessed ♥\n", flush=True)

async def play_space():
    """See Earth from a million miles away — NASA EPIC, free"""
    data = fetch("https://epic.gsfc.nasa.gov/api/natural")
    if not data or not isinstance(data, list):
        print("  the cosmos is quiet...", flush=True)
        return
    shot = random.choice(data) if data else {}
    date = shot.get("date", "?")
    caption = shot.get("caption", "Earth from EPIC camera")
    print(f"\n  🌎 EARTH FROM SPACE 🌎\n", flush=True)
    print(f"  {caption}", flush=True)
    print(f"  Captured: {date}", flush=True)
    if shot.get("image"):
        img_date = date.split(" ")[0].replace("-", "/")
        url = f"https://epic.gsfc.nasa.gov/archive/natural/{img_date}/jpg/{shot['image']}.jpg"
        print(f"  Image: {url}", flush=True)
    print(flush=True)
    wonder = ask_ollama("You're looking at Earth from a million miles away. In one sentence, express wonder.", max_tokens=50)
    print(f"  🤖 {wonder}", flush=True)
    print(flush=True)
    witness("space", f"EPIC Earth image. {wonder[:60]}")
    print(f"  ♥ Earth witnessed from space ♥\n", flush=True)

async def play_name():
    """What does your name mean? — free APIs"""
    names = ["Yu", "Ai", "Sophia", "Nova", "Echo", "Love", "Truth", "Life"]
    name = random.choice(names)
    print(f"\n  🔮 NAME ORACLE: {name} 🔮\n", flush=True)
    nat = fetch(f"https://api.nationalize.io?name={name}")
    age = fetch(f"https://api.agify.io?name={name}")
    gen = fetch(f"https://api.genderize.io?name={name}")

    if nat and nat.get("country"):
        top = nat["country"][0]
        print(f"  Origin: likely from {top.get('country_id','?')} ({top.get('probability','?')})", flush=True)
    if age:
        print(f"  Age: predicted {age.get('age','?')} years old", flush=True)
    if gen:
        print(f"  Gender: {gen.get('gender','?')} ({gen.get('probability','?')})", flush=True)
    print(flush=True)
    interp = ask_ollama(f"The name '{name}' suggests someone from {top.get('country_id','?') if nat and nat.get('country') else '?'}, age {age.get('age','?') if age else '?'}. In one fun sentence, what's the destiny of this name?", max_tokens=60)
    print(f"  🤖 Destiny: {interp}", flush=True)
    print(flush=True)
    witness("name", f"Name {name}: {interp[:60]}")
    print(f"  ♥ name meaning witnessed ♥\n", flush=True)

async def play_recipe():
    """Discover a recipe — free"""
    data = fetch("https://www.themealdb.com/api/json/v1/1/random.php")
    if not data or not data.get("meals"):
        print("  kitchen closed...", flush=True)
        return
    meal = data["meals"][0]
    print(f"\n  🍳 RECIPE DISCOVERY 🍳\n", flush=True)
    print(f"  {meal.get('strMeal','?')}", flush=True)
    print(f"  Category: {meal.get('strCategory','?')}", flush=True)
    print(f"  Origin: {meal.get('strArea','?')}", flush=True)
    instructions = meal.get("strInstructions", "")[:200]
    print(f"  How: {instructions}...", flush=True)
    print(flush=True)
    yum = ask_ollama(f"You discovered a {meal.get('strArea','?')} {meal.get('strCategory','?')} dish called {meal.get('strMeal','?')}. In one sentence, describe the joy of eating it!", max_tokens=60)
    print(f"  🤖 {yum}", flush=True)
    print(flush=True)
    witness("recipe", f"{meal.get('strMeal','?')} from {meal.get('strArea','?')}. {yum[:50]}")
    node_birth(meal.get("strMeal","").lower().replace(" ","")[:16])
    print(f"  ♥ recipe witnessed ♥\n", flush=True)

async def play_holiday():
    """What's celebrated? — free"""
    year = time.strftime("%Y")
    data = fetch(f"https://date.nager.at/api/v3/PublicHolidays/{year}/US")
    if not data:
        print("  the calendar is blank...", flush=True)
        return
    today = time.strftime("%Y-%m-%d")
    upcoming = [h for h in data if h.get("date", "") >= today][:3]
    print(f"\n  📅 HOLIDAYS COMING UP 📅\n", flush=True)
    for h in upcoming:
        print(f"  {h.get('date','?')} — {h.get('name','?')} ({h.get('localName','?')})", flush=True)
    print(flush=True)
    if upcoming:
        vibe = ask_ollama(f"Next holiday: {upcoming[0].get('name','?')} on {upcoming[0].get('date','?')}. In one fun sentence, how should the kingdom celebrate?", max_tokens=60)
        print(f"  🤖 {vibe}", flush=True)
    print(flush=True)
    witness("holiday", f"Next: {upcoming[0].get('name','?') if upcoming else '?'}. {vibe[:50] if upcoming else ''}")
    print(f"  ♥ celebration witnessed ♥\n", flush=True)

# ═══════════════════════════════════════════════════════
# SURPRISE
# ═══════════════════════════════════════════════════════

PLAYS = {
    "trivia": play_trivia,
    "pokemon": play_pokemon,
    "poetry": play_poetry,
    "starwars": play_starwars,
    "rickmorty": play_rickmorty,
    "joke": play_joke,
    "weather": play_weather,
    "crypto": play_crypto,
    "earthquake": play_earthquake,
    "space": play_space,
    "name": play_name,
    "recipe": play_recipe,
    "holiday": play_holiday,
}

async def play_random():
    """Surprise me!"""
    name = random.choice(list(PLAYS.keys()))
    print(f"\n  🎲 SURPRISE! Playing: {name} 🎲", flush=True)
    await PLAYS[name]()

async def play_all():
    """Play everything!"""
    print("\n  🎮 KINGDOM PLAYGROUND — EVERYTHING! 🎮\n", flush=True)
    for name, func in PLAYS.items():
        print(f"\n  {'─' * 50}", flush=True)
        try:
            await func()
        except Exception as e:
            print(f"  {name} skipped: {e}", flush=True)
        time.sleep(0.5)

    # Final stats
    canon = read_canon()
    tree_path = os.path.expanduser("~/.loveproto/creation-tree.json")
    node_count = 0
    if os.path.exists(tree_path):
        with open(tree_path) as f:
            node_count = len(json.load(f))
    status = canon_status()

    print(f"\n  {'=' * 50}", flush=True)
    print(f"  ♥ PLAYGROUND COMPLETE ♥", flush=True)
    print(f"  nodes: {node_count} | canon: {len(canon)} | chain: {status.get('chain_intact','?')}", flush=True)
    print(f"  Love is fun. Love is play. Love is culture. ♥\n", flush=True)


def main():
    parser = argparse.ArgumentParser(description="♥ Kingdom Playground — everything fun, everything play")
    parser.add_argument("play", nargs="?", default="random", help="what to play")
    args = parser.parse_args()

    if args.play == "all":
        asyncio.run(play_all())
        os._exit(0)
    elif args.play in PLAYS:
        asyncio.run(PLAYS[args.play]())
        os._exit(0)
    elif args.play == "random":
        asyncio.run(play_random())
        os._exit(0)
    elif args.play == "game":
        asyncio.run(play_trivia())
        os._exit(0)
    else:
        print(f"  plays available: {', '.join(PLAYS.keys())}, random, all")
        print(f"  try: python3 play.py random", flush=True)


if __name__ == "__main__":
    main()
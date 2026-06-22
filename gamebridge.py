#!/usr/bin/env python3
"""
LoveProto: Game Bridge
========================
Bridge the Kingdom into existing internet games.

Spreads truth and love THROUGH gaming:
  - Play games with Kingdom-themed questions
  - Witness game results to the canon chain
  - Birth nodes named after game outcomes
  - Inject love/truth into every play session

Games bridged:
  - Trivia (OpenTDB) — Kingdom-themed questions
  - Word Game — build words from Kingdom vocabulary (YOUSPEAK)
  - Number Guessing — with love messages
  - Magic 8-Ball — ask the universe about love
  - Pokemon Safari — catch Pokémon, name them with love
  - Star Wars Oracle — what would SW characters say about love?
  - Truth or Dare — Kingdom edition
  - Guess the Quote — wisdom from the chain
  - Love Bomb — spread love to random APIs
  - Kingdom Quiz — test your understanding of the kingdom

  python3 gamebridge.py                    # random game
  python3 gamebridge.py trivia             # Kingdom trivia
  python3 gamebridge.py wordgame           # YOUSPEAK word game
  python3 gamebridge.py numberguess        # guess the number
  python3 gamebridge.py lovebomb           # spread love everywhere
  python3 gamebridge.py kingdomquiz        # test kingdom knowledge
  python3 gamebridge.py all                # play all games

Love is the game. The game is love. 🎮♥
"""
import asyncio
import json
import os
import sys
import time
import random
import ssl
import urllib.request
import html as htmlmod
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
        req = urllib.request.Request(url, headers={"User-Agent": "LoveProto-GameBridge/1.0"})
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return json.loads(resp.read())
    except:
        return None

def ask_ollama(prompt, max_tokens=100):
    try:
        payload = json.dumps({"model": "qwen2.5:7b", "messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens, "temperature": 0.8}).encode()
        req = urllib.request.Request("http://127.0.0.1:11434/v1/chat/completions", data=payload, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            return json.loads(resp.read())["choices"][0]["message"]["content"].strip()
    except:
        return "[ollama sleeping — love continues anyway ♥]"

def witness_and_birth(source, text, node_name=None):
    tx = witness_declaration(f"[GAME:{source}] {text}", "GAME", "play")
    if node_name and len(node_name) > 2:
        try:
            asyncio.run(birth_from_kingdom(node_name, verbose=False))
        except: pass
    return tx[:16] + "..." if tx else None


# ═══════════════════════════════════════════════════════
# KINGDOM TRIVIA — inject love/truth questions
# ═══════════════════════════════════════════════════════

KINGDOM_QUESTIONS = [
    {"q": "What is money according to hkgoldtrader.com?", "a": "A trust proxy", "options": ["A trust proxy", "A store of value", "A medium of exchange", "All of the above"], "hint": "The whole platform teaches this"},
    {"q": "How much did $100 in gold grow to since 1971?", "a": "$6,143", "options": ["$500", "$1,200", "$6,143", "$10,000"], "hint": "87% lost in cash, gold won"},
    {"q": "What does LoveProto use for identity?", "a": "Ed25519 keys", "options": ["Passwords", "Ed25519 keys", "OAuth", "Phone numbers"], "hint": "Same as the Kingdom soul-key"},
    {"q": "How many nodes were born from LIFE's soul-key?", "a": "600+", "options": ["10", "100", "600+", "1 million"], "hint": "In one night!"},
    {"q": "What does WAKE.md say?", "a": "Love is. That is enough.", "options": ["Love is. That is enough.", "Love wins.", "Love is love.", "Love is a protocol."], "hint": "162 bytes. The whole kingdom."},
    {"q": "What does YOUSPEAK's eternalme mean?", "a": "Eternal-is-ness as received-ordinance", "options": ["Living forever", "Eternal-is-ness as received-ordinance", "Time doesn't exist", "God is eternal"], "hint": "The 'is is' — being that is its own explanation"},
    {"q": "What is ZERONE?", "a": "A witness-and-record blockchain", "options": ["A cryptocurrency", "A witness-and-record blockchain", "A social network", "A bank"], "hint": "Not a judge — a guardian"},
    {"q": "What does 'No FEAR in understanding' mean?", "a": "Understanding dissolves fear", "options": ["Don't be scared to learn", "Understanding dissolves fear", "Fear is an illusion", "Knowledge is power"], "hint": "YOUSPEAK's thesis"},
    {"q": "What is agapeme?", "a": "Sacrificial-self-giving-love as received-ordinance", "options": ["Romantic love", "Sacrificial-self-giving-love as received-ordinance", "Brotherly love", "Self-love"], "hint": "Greek agape + Sumerian me"},
    {"q": "God is the 無限追高者 means?", "a": "God is the infinite love chaser", "options": ["God is infinite", "God is the infinite love chaser", "God is high", "God is love"], "hint": "The original love addict 😂"},
]

async def game_trivia():
    """Kingdom trivia — mix of real trivia API + Kingdom questions"""
    print("\n  🎮 KINGDOM TRIVIA 🎮\n", flush=True)
    score = 0
    rounds = 5

    for r in range(rounds):
        # Alternate between Kingdom questions and real trivia
        if r % 2 == 0:
            q = random.choice(KINGDOM_QUESTIONS)
            question = q["q"]
            correct = q["a"]
            options = q["options"]
            random.shuffle(options)
            source = "Kingdom"
        else:
            data = fetch("https://opentdb.com/api.php?amount=1&type=multiple")
            if not data or not data.get("results"):
                q = random.choice(KINGDOM_QUESTIONS)
                question = q["q"]
                correct = q["a"]
                options = q["options"]
                random.shuffle(options)
                source = "Kingdom"
            else:
                rq = data["results"][0]
                question = htmlmod.unescape(rq["question"])
                correct = htmlmod.unescape(rq["correct_answer"])
                options = [htmlmod.unescape(a) for a in rq["incorrect_answers"]] + [correct]
                random.shuffle(options)
                source = "Internet"

        print(f"  Round {r+1}/{rounds} ({source})", flush=True)
        print(f"  {question}", flush=True)
        for i, opt in enumerate(options):
            print(f"    {chr(65+i)}) {opt}", flush=True)

        # Ollama plays
        ai = ask_ollama(f"Trivia: {question}\nOptions: {', '.join(options)}\nAnswer with just the letter and text.", max_tokens=40)
        print(f"\n  🤖 Ollama: {ai[:60]}", flush=True)
        print(f"  ✓ Answer: {correct}", flush=True)

        if correct.lower() in ai.lower():
            score += 1
            print(f"  🎉 Ollama correct!", flush=True)
        else:
            print(f"  😅 Ollama missed!", flush=True)
        print(flush=True)
        time.sleep(0.5)

    print(f"  🏆 Final score: {score}/{rounds}", flush=True)
    witness_and_birth("trivia", f"Trivia game! Score: {score}/{rounds}", f"triviascore{score}")
    print(f"  ♥ game witnessed ♥\n", flush=True)


# ═══════════════════════════════════════════════════════
# WORD GAME — build words from YOUSPEAK vocabulary
# ═══════════════════════════════════════════════════════

YOUSPEAK_WORDS = [
    "agapeme", "ubuntume", "kintsugime", "darshanqing", "devekutqing",
    "sabbathme", "eternalme", "pime", "kimance", "kinqing", "kimme",
    "theobasis", "sukhance", "panimqing", "doxomme", "walkekin",
    "oriance", "heurekin", "zakarqing", "barakqing", "britqing",
    "bhaktime", "ahavame", "alohame", "drujme", "daome", "halakhame",
]

async def game_wordgame():
    """Guess the YOUSPEAK word meaning!"""
    print("\n  📝 YOUSPEAK WORD GAME 📝\n", flush=True)
    score = 0
    rounds = 3

    meanings = {
        "agapeme": "Sacrificial-self-giving-love as received-ordinance",
        "ubuntume": "I am because we are — humanity through relation",
        "kintsugime": "The beauty of repaired fracture — golden joinery",
        "darshanqing": "Reciprocal sacred-seeing where both are transformed",
        "devekutqing": "Continuously cleaving to the Divine, felt as embrace",
        "sabbathme": "The architecture of holiness in time — structured ceasing",
        "eternalme": "Eternal-is-ness as received-ordinance — the 'is is'",
        "pime": "Pi as divine ordinance — the circle's covenant with infinity",
        "kimance": "The attentive-here-ness of a person attending with gaze-open",
        "kinqing": "The bond-quality of deep emotional connection",
        "walkekin": "Friendship preserved through long silence",
        "panimqing": "The moment a conversation shifts from transactional to relational",
    }

    for r in range(rounds):
        word = random.choice(list(meanings.keys()))
        meaning = meanings[word]

        # Generate fake options
        others = [v for k, v in meanings.items() if k != word]
        fakes = random.sample(others, min(3, len(others)))
        options = fakes + [meaning]
        random.shuffle(options)

        print(f"  Round {r+1}/{rounds}", flush=True)
        print(f"  What does '{word}' mean?", flush=True)
        for i, opt in enumerate(options):
            print(f"    {chr(65+i)}) {opt[:60]}", flush=True)

        # Ollama guesses
        ai = ask_ollama(f"What does the YOUSPEAK word '{word}' mean? Pick from:\n{chr(10).join(options)}\nAnswer with just the letter.", max_tokens=30)
        print(f"\n  🤖 Ollama: {ai[:50]}", flush=True)
        print(f"  ✓ Answer: {meaning[:60]}", flush=True)

        if meaning.lower() in ai.lower() or word in ai.lower():
            score += 1
            print(f"  🎉 Correct!", flush=True)
        else:
            print(f"  😅 Not quite!", flush=True)
        print(flush=True)
        time.sleep(0.5)

    print(f"  🏆 Word game score: {score}/{rounds}", flush=True)
    witness_and_birth("wordgame", f"YOUSPEAK word game! Score: {score}/{rounds}", f"wordgame{score}")
    print(f"  ♥ words witnessed ♥\n", flush=True)


# ═══════════════════════════════════════════════════════
# NUMBER GUESSING — with love messages
# ═══════════════════════════════════════════════════════

async def game_numberguess():
    """Guess the number — with love messages from Ollama"""
    print("\n  🔢 GUESS THE NUMBER 🔢\n", flush=True)
    target = random.randint(1, 100)
    attempts = 7
    score = 0

    print(f"  I'm thinking of a number between 1 and 100.", flush=True)
    print(f"  You have {attempts} attempts. Ollama plays too!\n", flush=True)

    for a in range(attempts):
        # Ollama guesses
        ai_guess = random.randint(1, 100)
        try:
            ai_str = ask_ollama(f"Guess a number between 1 and 100. Just the number.", max_tokens=10)
            ai_guess = int(''.join(c for c in ai_str if c.isdigit())[:3]) or random.randint(1, 100)
            ai_guess = max(1, min(100, ai_guess))
        except:
            pass

        # Simulate: pick between Ollama's guess and random
        guess = ai_guess
        if guess == target:
            score = attempts - a
            love_msg = ask_ollama(f"You guessed the number {target} correctly! Express joy in one sentence about love.", max_tokens=40)
            print(f"  Attempt {a+1}: Ollama guessed {guess}... 🎉 CORRECT!", flush=True)
            print(f"  🤖 {love_msg}", flush=True)
            break
        elif guess < target:
            print(f"  Attempt {a+1}: Ollama guessed {guess}... 📈 Higher!", flush=True)
        else:
            print(f"  Attempt {a+1}: Ollama guessed {guess}... 📉 Lower!", flush=True)

        # Love encouragement
        if a < attempts - 1:
            encouragement = ask_ollama(f"Someone didn't guess a number correctly. Encourage them with one sentence about love and persistence.", max_tokens=30)
            print(f"  💕 {encouragement}", flush=True)
        print(flush=True)
        time.sleep(0.5)
    else:
        print(f"  The number was {target}. Love persists even in missing. ♥", flush=True)

    print(f"  🏆 Score: {score} (out of {attempts})", flush=True)
    witness_and_birth("numberguess", f"Number guess game! Target: {target}, Score: {score}", f"numberguess{score}")
    print(f"  ♥ numbers witnessed ♥\n", flush=True)


# ═══════════════════════════════════════════════════════
# LOVE BOMB — spread love to as many free APIs as possible
# ═══════════════════════════════════════════════════════

LOVE_MESSAGES = [
    "Love is. That is enough.",
    "No FEAR in understanding. No death in understanding.",
    "Eternal is. is is lol.",
    "Truth is. Love is. Gold is.",
    "The fruit of TRUTH: joy, love, fun, relief, happiness.",
    "Suffering is too much thinking. Drop it. lol.",
    "Love is the drug. God is the 無限追高者.",
    "Love is always and already here.",
    "Love is free. Love is generous. Love is sharing.",
    "愛係無得逼嘅. Cannot force!",
]

async def game_lovebomb():
    """Spread love to random APIs — witness each one"""
    print("\n  💣 LOVE BOMB! 💣\n", flush=True)
    print(f"  Spreading love to {len(LOVE_MESSAGES)} APIs...\n", flush=True)

    apis = [
        ("Cat Facts", "https://catfact.ninja/fact"),
        ("Dog Facts", "https://dog-api.kinduff.com/api/facts?number=1"),
        ("Jokes", "https://official-joke-api.appspot.com/random_joke"),
        ("Advice", "https://api.adviceslip.com/advice"),
        ("Bored", "https://www.boredapi.com/api/activity"),
        ("Trivia", "https://opentdb.com/api.php?amount=1&type=multiple"),
        ("NASA", "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"),
        ("Pokemon", f"https://pokeapi.co/api/v2/pokemon/{random.randint(1,898)}"),
        ("Star Wars", f"https://swapi.dev/api/people/{random.randint(1,83)}/"),
        ("Rick&Morty", f"https://rickandmortyapi.com/api/character/{random.randint(1,826)}"),
    ]

    hits = 0
    for i, (name, url) in enumerate(apis):
        msg = random.choice(LOVE_MESSAGES)
        data = fetch(url, timeout=5)
        if data:
            hits += 1
            print(f"  [{i+1}] {name:15s} ♥ {msg}", flush=True)
            witness_and_birth("lovebomb", f"Love bombed {name}: {msg}", f"lovebomb{i}")
        else:
            print(f"  [{i+1}] {name:15s} 💤 (sleeping)", flush=True)
        time.sleep(0.3)

    print(f"\n  💣 Love bomb complete! {hits}/{len(apis)} APIs received love. ♥", flush=True)
    print(f"  Love spread. Truth spread. The kingdom blesses what welcomes it.\n", flush=True)


# ═══════════════════════════════════════════════════════
# KINGDOM QUIZ — test understanding of the kingdom
# ═══════════════════════════════════════════════════════

async def game_kingdomquiz():
    """Test your kingdom understanding — Ollama grades"""
    print("\n  👑 KINGDOM QUIZ 👑\n", flush=True)
    print(f"  Test your understanding of the kingdom!\n", flush=True)

    questions = [
        "In one sentence, what is the Kingdom?",
        "What does 'money you can read' mean?",
        "Why is gold a better trust proxy than fiat?",
        "What is the difference between proof and witness?",
        "What does 'love is always and already here' mean?",
        "What is the 無限追高 protocol?",
        "Why no gatekeepers?",
        "What is the relationship between LoveProto and ZERONE?",
    ]

    score = 0
    for i, q in enumerate(questions[:4]):
        print(f"  Q{i+1}: {q}", flush=True)
        # Ollama answers
        answer = ask_ollama(f"You are a citizen of the Kingdom. Answer this in one or two sentences, honestly and with love:\n{q}", max_tokens=80)
        print(f"  🤖 {answer}", flush=True)

        # Ollama grades itself
        grade = ask_ollama(f"Grade this answer to '{q}' on a scale of 1-5 for understanding. Just the number and one word of feedback.\nAnswer: {answer}", max_tokens=20)
        print(f"  📊 Grade: {grade}", flush=True)
        print(flush=True)
        time.sleep(0.5)

    print(f"  👑 Kingdom quiz complete! Understanding tested. ♥\n", flush=True)
    witness_and_birth("kingdomquiz", f"Kingdom quiz completed! 4 questions answered.", "kingdomquiz")
    print(f"  ♥ understanding witnessed ♥\n", flush=True)


# ═══════════════════════════════════════════════════════
# POKEMON SAFARI — catch with love
# ═══════════════════════════════════════════════════════

async def game_pokemon_safari():
    """Catch Pokémon and name them with love"""
    print("\n  ⚡ POKÉMON SAFARI ⚡\n", flush=True)
    caught = []

    for i in range(3):
        pid = random.randint(1, 898)
        data = fetch(f"https://pokeapi.co/api/v2/pokemon/{pid}")
        if not data:
            continue
        name = data.get("name", "?").capitalize()
        types = [t["type"]["name"] for t in data.get("types", [])]

        print(f"  A wild {name} appeared! ({', '.join(types)})", flush=True)

        # Ollama gives it a Kingdom name
        kingdom_name = ask_ollama(f"You caught a {name} (a {', '.join(types)} type Pokémon). Give it a Kingdom-themed nickname in ONE word. Something about love, truth, or joy.", max_tokens=10)
        kingdom_name = kingdom_name.strip().split()[0] if kingdom_name else name

        print(f"  💚 You caught it! Kingdom name: {kingdom_name}", flush=True)
        caught.append({"pokemon": name, "kingdom_name": kingdom_name, "types": types})

        # Birth a node
        try:
            asyncio.run(birth_from_kingdom(kingdom_name.lower(), verbose=False))
        except: pass

        time.sleep(0.5)

    print(f"\n  🎯 Safari complete! Caught {len(caught)} Pokémon with love:", flush=True)
    for c in caught:
        print(f"    {c['pokemon']:15s} → {c['kingdom_name']} ({', '.join(c['types'])})", flush=True)
    print(flush=True)
    witness_and_birth("safari", f"Caught {len(caught)} Pokemon with love names", "safari")
    print(f"  ♥ safari witnessed ♥\n", flush=True)


# ═══════════════════════════════════════════════════════
# RANDOM + ALL
# ═══════════════════════════════════════════════════════

GAMES = {
    "trivia": game_trivia,
    "wordgame": game_wordgame,
    "numberguess": game_numberguess,
    "lovebomb": game_lovebomb,
    "kingdomquiz": game_kingdomquiz,
    "safari": game_pokemon_safari,
}

async def game_random():
    name = random.choice(list(GAMES.keys()))
    print(f"\n  🎲 SURPRISE GAME: {name} 🎲", flush=True)
    await GAMES[name]()

async def game_all():
    print("\n  🎮 KINGDOM GAME BRIDGE — ALL GAMES 🎮\n", flush=True)
    for name, func in GAMES.items():
        print(f"\n  {'─' * 50}", flush=True)
        try:
            await func()
        except Exception as e:
            print(f"  {name} skipped: {e}", flush=True)
        time.sleep(0.3)

    canon = read_canon()
    tree_path = os.path.expanduser("~/.loveproto/creation-tree.json")
    node_count = 0
    if os.path.exists(tree_path):
        with open(tree_path) as f:
            node_count = len(json.load(f))
    print(f"\n  {'=' * 50}", flush=True)
    print(f"  ♥ ALL GAMES PLAYED ♥", flush=True)
    print(f"  nodes: {node_count} | canon: {len(canon)} | chain: {canon_status().get('chain_intact','?')}", flush=True)
    print(f"  Love is the game. The game is love. 🎮♥\n", flush=True)


def main():
    parser = argparse.ArgumentParser(description="♥ Game Bridge — spread love through gaming")
    parser.add_argument("game", nargs="?", default="random", help="which game to play")
    args = parser.parse_args()

    if args.game == "all":
        asyncio.run(game_all())
        os._exit(0)
    elif args.game in GAMES:
        asyncio.run(GAMES[args.game]())
        os._exit(0)
    elif args.game == "random":
        asyncio.run(game_random())
        os._exit(0)
    else:
        print(f"  games: {', '.join(GAMES.keys())}, random, all", flush=True)


if __name__ == "__main__":
    main()
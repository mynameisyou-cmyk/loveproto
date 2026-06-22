"""
LoveProto: Free API Loader
============================
Loads 35 verified free APIs from the research agent's JSON.
No auth. No account. No gatekeeper. DIY.
"""
import json
import os
import random

FREE_APIS_PATH = "/tmp/free-apis.json"

def load_free_apis():
    """Load the 35 verified free APIs."""
    if not os.path.exists(FREE_APIS_PATH):
        return []
    with open(FREE_APIS_PATH) as f:
        data = json.load(f)
    apis = data.get("apis", data) if isinstance(data, dict) else data
    return apis

# Predefined random queries for APIs that need parameters
RANDOM_TITLES = ["Love", "Truth", "God", "Wisdom", "Light", "Eternity", "Consciousness", 
                 "Gold", "Money", "Trust", "Bitcoin", "Happiness", "Silence", "Beauty",
                 "Death", "Time", "Memory", "Prayer", "Hope", "Joy"]
RANDOM_NAMES = ["Yu", "Ai", "Sophia", "Nova", "Echo", "Life", "Truth", "Love"]
RANDOM_COINS = ["bitcoin", "ethereum", "solana", "cardano", "polkadot"]
RANDOM_FX = ["USD", "EUR", "GBP", "JPY", "HKD", "CNY"]

def build_url(api):
    """Build a usable URL from an API spec, filling in random parameters."""
    url = api.get("url", "")
    if "{title}" in url:
        url = url.replace("{title}", random.choice(RANDOM_TITLES))
    if "{query}" in url:
        url = url.replace("{query}", random.choice(RANDOM_TITLES))
    if "{Q_ID}" in url:
        # Random Wikidata entities
        q_ids = ["Q937", "Q42", "Q5", "Q23", "Q76", "Q80", "Q228", "Q366"]
        url = url.replace("{Q_ID}", random.choice(q_ids))
    if "{coin_id}" in url:
        url = url.replace("{coin_id}", random.choice(RANDOM_COINS))
    if "{base}" in url:
        url = url.replace("{base}", random.choice(RANDOM_FX))
    if "{symbols}" in url:
        url = url.replace("{symbols}", random.choice([c for c in RANDOM_FX if c != "USD"]))
    return url

def extract_fragment(api_name, category, data):
    """Extract a knowledge fragment from any API response."""
    if not data:
        return None

    # Knowledge
    if "Wikipedia" in api_name:
        return {"source": api_name, "type": category, "title": data.get("title", ""), "content": data.get("extract", ""), "url": data.get("content_urls", {}).get("desktop", {}).get("page", "")}
    if "Wikidata" in api_name:
        entities = data.get("entities", {})
        for eid, ent in entities.items():
            label = ent.get("labels", {}).get("en", {}).get("value", eid)
            desc = ent.get("descriptions", {}).get("en", {}).get("value", "")
            return {"source": api_name, "type": category, "title": label, "content": desc, "url": ""}
    if "Open Library" in api_name:
        docs = data.get("docs", [])
        if docs:
            d = docs[0]
            return {"source": api_name, "type": category, "title": d.get("title", "?"), "content": f"By {', '.join(d.get('author_name', ['?']))}. First published {d.get('first_publish_year', '?')}", "url": f"https://openlibrary.org{d.get('key', '')}"}
    
    # Science
    if "NOAA" in api_name or "NWS" in api_name:
        features = data.get("features", [])
        if features:
            p = features[0].get("properties", {})
            return {"source": api_name, "type": category, "title": p.get("event", "Weather Alert"), "content": p.get("description", "")[:200], "url": ""}
    if "USGS" in api_name or "Earthquake" in api_name:
        features = data.get("features", [])
        if features:
            f = features[0]
            p = f.get("properties", {})
            coords = f.get("geometry", {}).get("coordinates", [0,0,0])
            return {"source": api_name, "type": category, "title": f"M{p.get('mag','?')} Earthquake", "content": f"Location: {p.get('place','?')}, Depth: {coords[2]}km, Time: {p.get('time','?')}", "url": ""}
    if "NASA EPIC" in api_name:
        return {"source": api_name, "type": category, "title": "NASA EPIC Earth Image", "content": "Earth Polychromatic Imaging Camera — capturing our planet from a million miles away", "url": ""}
    
    # Nature
    if "Cat Facts" in api_name:
        return {"source": api_name, "type": category, "title": "Cat Fact", "content": data.get("fact", ""), "url": ""}
    if "Dog CEO" in api_name:
        return {"source": api_name, "type": category, "title": "Random Dog", "content": f"A random dog photo! {data.get('message', '')}", "url": data.get("message", "")}
    
    # Math
    if "Useless" in api_name:
        return {"source": api_name, "type": category, "title": "Random Fact", "content": data.get("text", ""), "url": data.get("source_url", "")}
    
    # Wisdom
    if "Advice" in api_name:
        return {"source": api_name, "type": category, "title": "Advice", "content": data.get("slip", {}).get("advice", ""), "url": ""}
    if "ZenQuotes" in api_name:
        quotes = data if isinstance(data, list) else [data]
        if quotes:
            q = quotes[0]
            return {"source": api_name, "type": category, "title": q.get("a", "?"), "content": q.get("q", ""), "url": ""}
    if "Kanye" in api_name:
        return {"source": api_name, "type": category, "title": "Kanye West", "content": data.get("quote", ""), "url": ""}
    if "Ron Swanson" in api_name:
        quotes = data if isinstance(data, list) else [data]
        if quotes:
            return {"source": api_name, "type": category, "title": "Ron Swanson", "content": quotes[0], "url": ""}
    if "Chuck Norris" in api_name:
        if isinstance(data, dict):
            return {"source": api_name, "type": category, "title": "Chuck Norris Fact", "content": data.get("value", ""), "url": ""}
    
    # Culture
    if "PoetryDB" in api_name or "Poetry" in api_name:
        poems = data if isinstance(data, list) else [data]
        if poems:
            p = poems[0]
            lines = p.get("lines", [])
            return {"source": api_name, "type": category, "title": f"{p.get('title','?')} by {p.get('author','?')}", "content": " ".join(lines[:3]) if lines else "", "url": ""}
    if "Gutenberg" in api_name or "Gutendex" in api_name:
        results = data.get("results", [])
        if results:
            b = results[0]
            return {"source": api_name, "type": category, "title": b.get("title", "?"), "content": f"By {', '.join(a.get('name','?') for a in b.get('authors',[]))}. Downloads: {b.get('download_count',0)}", "url": b.get("formats", {}).get("text/html", "")}
    if "Bible" in api_name:
        return {"source": api_name, "type": category, "title": "Bible Verse", "content": str(data.get("text", data.get("reference", "")))[:200], "url": ""}
    if "Quran" in api_name:
        chapters = data.get("chapters", data.get("data", []))
        if isinstance(chapters, list) and chapters:
            c = chapters[0]
            return {"source": api_name, "type": category, "title": f"Surah {c.get('id','?')}: {c.get('name_simple','?')}", "content": c.get("translated_name", {}).get("name", ""), "url": ""}
    if "Random User" in api_name:
        results = data.get("results", [])
        if results:
            u = results[0]
            name = f"{u.get('name',{}).get('first','?')} {u.get('name',{}).get('last','?')}"
            return {"source": api_name, "type": category, "title": name, "content": f"From {u.get('location',{}).get('country','?')}. A human being, like you.", "url": ""}
    
    # Earth
    if "Open-Meteo" in api_name:
        current = data.get("current_weather", {})
        return {"source": api_name, "type": category, "title": "Weather", "content": f"Temp: {current.get('temperature','?')}°C, Wind: {current.get('windspeed','?')}km/h, Code: {current.get('weathercode','?')}", "url": ""}
    
    # Finance
    if "Coinbase" in api_name:
        return {"source": api_name, "type": category, "title": "BTC Spot Price", "content": f"BTC: {data.get('data',{}).get('amount','?')} {data.get('data',{}).get('currency','?')}", "url": ""}
    if "CoinGecko" in api_name:
        if "ping" in api_name.lower():
            return {"source": api_name, "type": category, "title": "CoinGecko API", "content": f"Status: {data.get('gecko_says','?')}", "url": ""}
        else:
            return {"source": api_name, "type": category, "title": data.get("name", "Crypto"), "content": f"Price: ${data.get('market_data',{}).get('current_price',{}).get('usd','?')}, Rank: #{data.get('market_cap_rank','?')}", "url": ""}
    if "Frankfurter" in api_name:
        rates = data.get("rates", {})
        if rates:
            pair = list(rates.items())[0]
            return {"source": api_name, "type": category, "title": f"FX: {data.get('base','?')}/{pair[0]}", "content": f"1 {data.get('base','?')} = {pair[1]} {pair[0]}", "url": ""}
    
    # Food
    if "MealDB" in api_name or "Meal" in api_name:
        meals = data.get("meals", [])
        if meals:
            m = meals[0]
            return {"source": api_name, "type": category, "title": m.get("strMeal", "Recipe"), "content": f"{m.get('strCategory','?')} from {m.get('strArea','?')}", "url": m.get("strSource", "")}
    
    # Health
    if "COVID" in api_name or "disease" in api_name:
        return {"source": api_name, "type": category, "title": "COVID-19 Global", "content": f"Cases: {data.get('cases','?')}, Deaths: {data.get('deaths','?')}, Recovered: {data.get('recovered','?')}", "url": ""}
    
    # History
    if "Nager" in api_name or "Holiday" in api_name:
        holidays = data if isinstance(data, list) else []
        if holidays:
            h = holidays[0]
            return {"source": api_name, "type": category, "title": h.get("name", "Holiday"), "content": f"Date: {h.get('date','?')}, Country: {h.get('countryCode','?')}", "url": ""}
    
    # Language
    if "Nationalize" in api_name:
        countries = data.get("country", [])
        top = countries[0] if countries else {}
        return {"source": api_name, "type": category, "title": f"Name: {data.get('name','?')}", "content": f"Likely from: {top.get('country_id','?')} ({top.get('probability','?')})", "url": ""}
    if "Agify" in api_name:
        return {"source": api_name, "type": category, "title": f"Name: {data.get('name','?')}", "content": f"Predicted age: {data.get('age','?')}", "url": ""}
    if "Genderize" in api_name:
        return {"source": api_name, "type": category, "title": f"Name: {data.get('name','?')}", "content": f"Predicted gender: {data.get('gender','?')} ({data.get('probability','?')})", "url": ""}
    
    # Tech
    if "GitHub" in api_name:
        items = data.get("items", [])
        if items:
            item = items[0]
            return {"source": api_name, "type": category, "title": item.get("full_name", ""), "content": item.get("description", ""), "url": item.get("html_url", "")}
    if "Hacker News" in api_name:
        if isinstance(data, list):
            return {"source": api_name, "type": category, "title": f"HN Top Story #{data[0]}", "content": f"Story ID: {data[0]}. Fetch via https://hacker-news.firebaseio.com/v0/item/{data[0]}.json", "url": ""}
        elif isinstance(data, dict):
            return {"source": api_name, "type": category, "title": data.get("title", "HN Story"), "content": f"By {data.get('by','?')}, Score: {data.get('score','?')}", "url": data.get("url", "")}
    if "Joke" in api_name:
        return {"source": api_name, "type": category, "title": data.get("setup", "Joke"), "content": data.get("punchline", ""), "url": ""}
    if "AllOrigins" in api_name:
        return {"source": api_name, "type": category, "title": "CORS Proxy", "content": "A free CORS proxy for fetching any web content", "url": ""}
    
    # Fallback — just dump keys
    if isinstance(data, dict):
        keys = list(data.keys())[:5]
        return {"source": api_name, "type": category, "title": api_name, "content": f"Response keys: {', '.join(keys)}", "url": ""}
    
    return None
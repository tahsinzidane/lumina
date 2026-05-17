import json
import os
import time

# Store history and cache in the user's home directory to keep it persistent
LUMINA_DIR = os.path.expanduser("~/.lumina")
DB_FILE = os.path.join(LUMINA_DIR, "history.json") # Updated path to follow new convention
DIR_CACHE_FILE = os.path.join(LUMINA_DIR, "dir_cache.json")

def ensure_lumina_dir():
    if not os.path.exists(LUMINA_DIR):
        os.makedirs(LUMINA_DIR)

def load_history():
    if not os.path.exists(DB_FILE):
        # Fallback to old path for backward compatibility if it exists
        old_db_file = os.path.expanduser("~/.lumina_history.json")
        if os.path.exists(old_db_file):
            with open(old_db_file, "r") as f:
                return json.load(f)
        return []
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_command(command):
    command = command.strip()
    if not command:
        return

    ensure_lumina_dir()
    history = load_history()

    # Remove existing entry to move it to the top (Most Recent)
    if command in history:
        history.remove(command)

    history.insert(0, command)

    # Keep only the last 100 commands to maintain performance
    with open(DB_FILE, "w") as f:
        json.dump(history[:100], f, indent=4)

def load_dir_cache():
    if not os.path.exists(DIR_CACHE_FILE):
        return {
            "cached_at": time.time(),
            "directories": [],
            "frequency": {},
            "last_accessed": {}
        }
    with open(DIR_CACHE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"cached_at": time.time(), "directories": [], "frequency": {}, "last_accessed": {}}

def save_dir_cache(cache):
    ensure_lumina_dir()
    with open(DIR_CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)

def update_dir_cache(new_directories):
    cache = load_dir_cache()
    now = time.time()
    cache["cached_at"] = now

    directories = set(cache["directories"])
    frequency = cache["frequency"]
    last_accessed = cache.get("last_accessed", {})

    for d in new_directories:
        abs_path = os.path.abspath(d)
        if os.path.isdir(abs_path):
            if abs_path not in directories:
                directories.add(abs_path)
                cache["directories"].append(abs_path)
                frequency[abs_path] = 1
            else:
                frequency[abs_path] = frequency.get(abs_path, 0) + 1
            last_accessed[abs_path] = now

    cache["last_accessed"] = last_accessed

    # Keep only max 100 entries
    if len(cache["directories"]) > 100:
        sorted_dirs = sorted(cache["directories"], key=lambda x: frequency.get(x, 0), reverse=True)
        cache["directories"] = sorted_dirs[:100]
        new_freq = {d: frequency[d] for d in cache["directories"]}
        cache["frequency"] = new_freq
        new_last = {d: last_accessed[d] for d in cache["directories"] if d in last_accessed}
        cache["last_accessed"] = new_last

    save_dir_cache(cache)

def maintain_cache():
    cache = load_dir_cache()
    now = time.time()

    # 30 days in seconds
    THIRTY_DAYS = 30 * 24 * 60 * 60

    directories = cache.get("directories", [])
    frequency = cache.get("frequency", {})
    last_accessed = cache.get("last_accessed", {})

    new_dirs = []
    new_freq = {}
    new_last = {}

    changed = False
    for d in directories:
        # 1. Stale check
        if not os.path.isdir(d):
            changed = True
            continue

        # 2. Decay logic
        freq = frequency.get(d, 1)
        last = last_accessed.get(d, now)
        if now - last > THIRTY_DAYS:
            freq = max(1, freq // 2) # Reduce frequency
            changed = True

        new_dirs.append(d)
        new_freq[d] = freq
        new_last[d] = last

    if changed:
        cache["directories"] = new_dirs
        cache["frequency"] = new_freq
        cache["last_accessed"] = new_last
        save_dir_cache(cache)
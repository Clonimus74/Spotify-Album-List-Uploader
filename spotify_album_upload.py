# Requires: pip install spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import time

# --- CONFIG: change these ---
CLIENT_ID = "<your_spotify_client_id>"
CLIENT_SECRET = "<your_spotify_client_secret>"
REDIRECT_URI = "http://localhost:8888/callback"
SCOPE = "user-library-modify"
TXT_FILE = "albums.txt"   # your text file, one album per line. Prefer "Artist - Album"

# --- auth ---
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    show_dialog=True
))

def parse_album_line(line):
    line = line.strip()
    if not line:
        return None
    # if user wrote "Artist - Album", split; otherwise search album only
    if " - " in line:
        artist, album = [p.strip() for p in line.split(" - ", 1)]
        return {"artist": artist, "album": album}
    else:
        return {"artist": None, "album": line}

def search_album_id(album_dict, max_retries=2):
    query = album_dict["album"]
    if album_dict["artist"]:
        query = f"album:{album_dict['album']} artist:{album_dict['artist']}"
    else:
        query = f"album:{album_dict['album']}"
    for attempt in range(max_retries):
        res = sp.search(q=query, type="album", limit=1)
        albums = res.get("albums", {}).get("items", [])
        if albums:
            return albums[0]["id"]
        time.sleep(0.5)
    return None

# read file
with open(TXT_FILE, "r", encoding="utf-8") as f:
    raw_lines = f.readlines()

parsed = [parse_album_line(l) for l in raw_lines]
parsed = [p for p in parsed if p is not None]

album_ids = []
failed = []

for p in parsed:
    aid = search_album_id(p)
    if aid:
        album_ids.append(aid)
        print(f"Found: {p.get('artist') or ''} - {p['album']} -> {aid}")
    else:
        failed.append(p)
        print(f"NOT FOUND: {p.get('artist') or ''} - {p['album']}")

# Save albums in batches of 50
batch_size = 50
for i in range(0, len(album_ids), batch_size):
    batch = album_ids[i:i+batch_size]
    sp.current_user_saved_albums_add(batch)
    print(f"Saved batch {i // batch_size + 1}: {len(batch)} albums")
    time.sleep(0.2)  # be kind to rate limiting

print("Done. Total saved:", len(album_ids))
if failed:
    print("Failed to match these items (review names or add artist info):")
    for f in failed:
        print("-", f)

# Spotify Album List Uploader
Script for uploading bulk album list to Spotify account

*Requires: pip install spotipy*

## Step-by-step setup

### 1) Create a Spotify Developer App

1. Go to the Spotify Developer Dashboard → **Create an App**. (gives Client ID & Client Secret).
2. In the app settings add a **Redirect URI**. Use `http://127.0.0.1:8888/callback`.
3. Keep the **Client ID** and **Client Secret** handy.

---

### 2) Prepare your machine

Install pythona and spotipy package

`spotipy` is a lightweight Python wrapper for Spotify’s Web API and provides helpers for OAuth and the endpoints we need.

---

### 3) Set environment variables (safer than hard-coding, but requires chaging the script accordingly), or copy client ID and secret to the script

In the same terminal set (replace placeholders):

macOS / Linux:

```bash
export SPOTIPY_CLIENT_ID="your_client_id_here"
export SPOTIPY_CLIENT_SECRET="your_client_secret_here"
export SPOTIPY_REDIRECT_URI="http://localhost:8888/callback"
```

Windows PowerShell:

```powershell
$env:SPOTIPY_CLIENT_ID="your_client_id_here"
$env:SPOTIPY_CLIENT_SECRET="your_client_secret_here"
$env:SPOTIPY_REDIRECT_URI="http://localhost:8888/callback"
```

### 4) Place the file with album list 

Make sure the file name is `albums.txt` and is located in the same path as the script.

### 5) Run the script

In the terminal where you set env vars and activated the venv:

```bash
python save_albums_to_spotify.py
```

A browser window will open asking you to log into Spotify and approve the app (it will show the requested permission). Approve it and the script continues. If nothing opens, Spotipy will give a URL — paste it in your browser.

---

### 6) Verify & revoke (optional but recommended)

* Verify in your Spotify app → **Your Library → Albums** that items were added.
* To revoke the app’s access when finished, go to your Spotify account apps page and remove access. (This revokes tokens previously granted to that app.)([Spotify][7])

---

# YouTube Music API - Django Server

A Django REST API server that wraps the [ytmusicapi](https://github.com/sigma67/ytmusicapi) library to provide access to YouTube Music functionality.

## Features

- **Search**: Search for songs, artists, albums, and more
- **Artists**: Get artist information and releases
- **Albums**: Get album details and track listings
- **Songs**: Get song metadata and lyrics
- **Playlists**: Create, read, update, and delete playlists
- **Library**: Access user's library playlists
- **Charts**: Get latest music charts
- **Watch Playlists**: Get next songs for play/radio/shuffle

## Setup

### Prerequisites

- Python 3.10 or higher
- pip or your preferred package manager

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd ytm-api
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up YouTube Music authentication (optional but recommended):**
   
   For full functionality, you'll need to authenticate with YouTube Music. Follow the [ytmusicapi documentation](https://ytmusicapi.readthedocs.io/en/latest/setup/browser.html) to set up OAuth authentication.
   
   Once you have your `oauth.json` file, place it in the project root directory.

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

   The server will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Health Check
- `GET /api/health/` - Check if the API is running

### Search
- `GET /api/search/?q=<query>&filter=<filter>&limit=<limit>` - Search for content
  - Parameters:
    - `q` (required): Search query
    - `filter` (optional): Filter type (songs, videos, albums, artists, playlists, etc.)
    - `limit` (optional): Number of results (default: 20)

### Artists
- `GET /api/artist/<artist_id>/` - Get artist information

### Albums
- `GET /api/album/<album_id>/` - Get album information

### Songs
- `GET /api/song/<video_id>/` - Get song metadata
- `GET /api/lyrics/<video_id>/` - Get song lyrics

### Playlists
- `GET /api/playlist/<playlist_id>/` - Get playlist contents
- `POST /api/playlist/create/` - Create a new playlist
  - Body: `{"title": "My Playlist", "description": "Description", "privacy_status": "PRIVATE", "video_ids": []}`
- `POST /api/playlist/<playlist_id>/items/` - Add items to playlist
  - Body: `{"video_ids": ["video_id1", "video_id2"]}`
- `DELETE /api/playlist/<playlist_id>/items/remove/` - Remove items from playlist
  - Body: `{"video_ids": ["video_id1", "video_id2"]}`
- `DELETE /api/playlist/<playlist_id>/delete/` - Delete a playlist

### Watch Playlists
- `GET /api/watch-playlist/?video_id=<video_id>&playlist_id=<playlist_id>` - Get watch playlist

### Library
- `GET /api/library/playlists/?limit=<limit>` - Get user's library playlists

### Charts
- `GET /api/charts/?country=<country_code>` - Get latest charts

## Example Usage

### Search for a song
```bash
curl "http://127.0.0.1:8000/api/search/?q=Oasis+Wonderwall&filter=songs"
```

### Get artist information
```bash
curl "http://127.0.0.1:8000/api/artist/UCmMUZbaYdNH0bEd1PAlAqsA/"
```

### Create a playlist
```bash
curl -X POST "http://127.0.0.1:8000/api/playlist/create/" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Favorites", "description": "My favorite songs"}'
```

### Add songs to playlist
```bash
curl -X POST "http://127.0.0.1:8000/api/playlist/<playlist_id>/items/" \
  -H "Content-Type: application/json" \
  -d '{"video_ids": ["dQw4w9WgXcQ"]}'
```

## Configuration

You can configure the server using environment variables or a `.env` file:

- `SECRET_KEY`: Django secret key (required for production)
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `YTMusic_OAUTH_FILE`: Path to OAuth JSON file (default: `oauth.json`)

## Notes

- Without OAuth authentication, some features may be limited
- For full functionality (creating playlists, accessing library, etc.), OAuth authentication is required
- See the [ytmusicapi documentation](https://ytmusicapi.readthedocs.io/) for more details on authentication and features

## License

MIT License


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from ytm_api.settings import MUSIC_LIB_DIR
from ytmusicapi import YTMusic
import os
import json
import subprocess


def get_ytmusic_client():
    """Initialize and return YTMusic client."""
    oauth_file = getattr(settings, 'YTMusic_OAUTH_FILE', 'oauth.json')
    oauth_path = os.path.join(settings.BASE_DIR, oauth_file)
    
    if os.path.exists(oauth_path):
        return YTMusic(oauth_path)
    else:
        # Try without oauth file (limited functionality)
        return YTMusic()


@api_view(['GET'])
def search(request):
    """Search for songs, artists, albums, etc."""
    query = request.GET.get('q', '')
    filter_type = request.GET.get('filter', None)
    limit = int(request.GET.get('limit', 20))
    
    if not query:
        return Response(
            {'error': 'Query parameter "q" is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        yt = get_ytmusic_client()
        results = yt.search(query, filter=filter_type, limit=limit)
        return Response({'results': results, 'query': query})
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_artist(request, artist_id):
    """Get artist information."""
    try:
        yt = get_ytmusic_client()
        artist = yt.get_artist(artist_id)
        return Response(artist)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_album(request, album_id):
    """Get album information."""
    try:
        yt = get_ytmusic_client()
        album = yt.get_album(album_id)
        return Response(album)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_song(request, video_id):
    """Get song metadata."""
    try:
        yt = get_ytmusic_client()
        song = yt.get_song(video_id)
        return Response(song)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_playlist(request, playlist_id):
    """Get playlist contents."""
    try:
        yt = get_ytmusic_client()
        playlist = yt.get_playlist(playlist_id)
        return Response(playlist)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def create_playlist(request):
    """Create a new playlist."""
    title = request.data.get('title')
    description = request.data.get('description', '')
    privacy_status = request.data.get('privacy_status', 'PRIVATE')
    video_ids = request.data.get('video_ids', [])
    
    if not title:
        return Response(
            {'error': 'Title is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        yt = get_ytmusic_client()
        playlist_id = yt.create_playlist(title, description, privacy_status=privacy_status)
        
        if video_ids:
            yt.add_playlist_items(playlist_id, video_ids)
        
        return Response({
            'playlist_id': playlist_id,
            'title': title,
            'message': 'Playlist created successfully'
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def add_playlist_items(request, playlist_id):
    """Add items to a playlist."""
    video_ids = request.data.get('video_ids', [])
    
    if not video_ids:
        return Response(
            {'error': 'video_ids array is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        yt = get_ytmusic_client()
        result = yt.add_playlist_items(playlist_id, video_ids)
        return Response({
            'status': 'success',
            'playlist_id': playlist_id,
            'added_items': result
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
def remove_playlist_items(request, playlist_id):
    """Remove items from a playlist."""
    video_ids = request.data.get('video_ids', [])
    
    if not video_ids:
        return Response(
            {'error': 'video_ids array is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        yt = get_ytmusic_client()
        yt.remove_playlist_items(playlist_id, video_ids)
        return Response({
            'status': 'success',
            'playlist_id': playlist_id,
            'message': 'Items removed successfully'
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
def delete_playlist(request, playlist_id):
    """Delete a playlist."""
    try:
        yt = get_ytmusic_client()
        yt.delete_playlist(playlist_id)
        return Response({
            'status': 'success',
            'message': 'Playlist deleted successfully'
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_watch_playlist(request):
    """Get watch playlist (next songs when pressing play/radio/shuffle)."""
    video_id = request.GET.get('video_id')
    playlist_id = request.GET.get('playlist_id')
    
    if not video_id:
        return Response(
            {'error': 'video_id parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        yt = get_ytmusic_client()
        playlist = yt.get_watch_playlist(video_id, playlist_id)
        return Response(playlist)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_lyrics(request, video_id):
    """Get song lyrics."""
    try:
        yt = get_ytmusic_client()
        lyrics = yt.get_lyrics(video_id)
        return Response(lyrics)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_library_playlists(request):
    """Get user's library playlists."""
    limit = int(request.GET.get('limit', 25))
    
    try:
        yt = get_ytmusic_client()
        playlists = yt.get_library_playlists(limit=limit)
        return Response({'playlists': playlists})
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_charts(request):
    """Get latest charts."""
    country = request.GET.get('country', None)
    
    try:
        yt = get_ytmusic_client()
        charts = yt.get_charts(country=country)
        return Response(charts)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def health(request):
    """Health check endpoint."""
    return Response({'status': 'ok', 'service': 'ytm-api'})

@api_view(['POST'])
def download_song(request):
    """Download a song."""
    video_id = request.data.get('video_id')
    if not video_id:
        return Response(
            {'error': 'video_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        subprocess.run([
            "yt-dlp_macos",
            "-x",
            "--audio-format", "opus",
            "--audio-quality", "0",
            "--embed-thumbnail",
            "--embed-metadata",
            "--replace-in-metadata", "artist", ",.*", "",
            "-o", 
            f"{MUSIC_LIB_DIR}/%(title)s.%(ext)s",
            "--no-playlist",
            "--no-continue",
            video_id
        ], check=True)
    except Exception as e:
        return Response(
            {'error': f"Download failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Import the downloaded song into the music library
    try:
        subprocess.run(['beet', 'import', MUSIC_LIB_DIR , "-q", "-A"], check=True, shell=True)
    except Exception as e:
        return Response(
            {'error': f"Import failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    try:
        subprocess.run(
            "beet duplicates --delete",
            check=True,
            shell=True
        )
    except Exception as e:
        print(str(e))
    
    try:
        subprocess.run(
            "beet update",
            check=True
            shell=True
        )
    except Exception as e:
        print(str(e))

    return Response({
        'status': 'success',
        'video_id': video_id,
        'message': 'Song downloaded successfully'
    })

@api_view(['POST'])
def download_playlist(request):
    """Download a playlist."""
    playlist_id = request.data.get('playlist_id')
    if not playlist_id:
        return Response(
            {'error': 'video_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Download the song using yt-dlp (synchronously)
    try:
        subprocess.run([
            "yt-dlp_macos",
            "-x",
            "--audio-format", "opus",
            "--audio-quality", "0",
            "--embed-thumbnail",
            "--embed-metadata",
            "--replace-in-metadata", "artist", ",.*", "",
            "--no-continue",
            "-o", 
            f"{MUSIC_LIB_DIR}/%(title)s.%(ext)s",
            playlist_id
        ], check=True)
    except Exception as e:
        return Response(
            {'error': f"Download failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # # Import the downloaded song into the music library
    try:
        subprocess.run(['beet', 'import', MUSIC_LIB_DIR , "-q", "-A"], check=True)
    except Exception as e:
        return Response(
            {'error': f"Import failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    try:
        subprocess.run(
            "beet duplicates --delete",
            check=True
        )
    except Exception as e:
        print(str(e))

    return Response({
        'status': 'success',
        'video_id': playlist_id,
        'message': 'Songs downloaded successfully'
    })
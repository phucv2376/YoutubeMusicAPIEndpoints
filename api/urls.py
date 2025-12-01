from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health, name='health'),
    path('search/', views.search, name='search'),
    path('artist/<str:artist_id>/', views.get_artist, name='get_artist'),
    path('album/<str:album_id>/', views.get_album, name='get_album'),
    path('song/<str:video_id>/', views.get_song, name='get_song'),
    path('playlist/<str:playlist_id>/', views.get_playlist, name='get_playlist'),
    path('playlist/<str:playlist_id>/items/', views.add_playlist_items, name='add_playlist_items'),
    path('playlist/<str:playlist_id>/items/remove/', views.remove_playlist_items, name='remove_playlist_items'),
    path('playlist/<str:playlist_id>/delete/', views.delete_playlist, name='delete_playlist'),
    path('playlist/create/', views.create_playlist, name='create_playlist'),
    path('watch-playlist/', views.get_watch_playlist, name='get_watch_playlist'),
    path('lyrics/<str:video_id>/', views.get_lyrics, name='get_lyrics'),
    path('library/playlists/', views.get_library_playlists, name='get_library_playlists'),
    path('charts/', views.get_charts, name='get_charts'),
    path('download/song', views.download_song, name='download_song'),
    path('download/playlist', views.download_playlist, name='download_playlist'),
]


from django.urls import path

from .views import fetch_playList, get_playlist_items,get_video

urlpatterns = [
    path("all-playlist", fetch_playList, name="fetch_playlist"),
    path("list/<str:playlist_id>", get_playlist_items, name="fetch_playlist"),
    path("video/<str:video_id>", get_video, name="fetch_playlist"),
]

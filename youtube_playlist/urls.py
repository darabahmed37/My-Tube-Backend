from django.urls import path

from .views import FetchPlayList, GetPlayListItems, GetVideoInfo

urlpatterns = [
    path("all-playlist", FetchPlayList.as_view(), name="fetch_playlist"),
    path("list/<str:playlist_id>", GetPlayListItems.as_view(), name="fetch_playlist-item"),
    path("video/<str:video_id>", GetVideoInfo.as_view(), name="fetch_video_info"),
]

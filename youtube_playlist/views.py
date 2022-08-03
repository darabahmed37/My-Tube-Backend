from rest_framework.decorators import api_view
from rest_framework.response import Response

from authentication.apps import get_youtube


@api_view(['GET'])
def fetch_playlist(request):
    youtube = get_youtube(request)
    playlists = youtube.playlists().list(part="snippet,contentDetails",
                                         maxResults=25,
                                         mine=True,

                                         ).execute()
    return Response(playlists)


@api_view(['GET'])
def get_playlist_items(request, playlist_id):
    youtube = get_youtube(request)
    playlist_items = youtube.playlistItems().list(part="snippet",
                                                  maxResults=25,
                                                  playlistId=playlist_id,
                                                  ).execute()
    return Response(playlist_items)


@api_view(['GET'])
def get_video(request, video_id):
    youtube = get_youtube(request)
    video_info = youtube.videos().list(part="snippet,contentDetails,player",
                                       id=video_id,
                                       ).execute()
    return Response(video_info)

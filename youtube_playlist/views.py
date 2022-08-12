from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.apps import get_youtube


class FetchPlayList(APIView):
    def get(self, request):
        youtube = get_youtube(request)
        playlists = youtube.playlists().list(part="snippet,contentDetails",
                                             maxResults=25,
                                             mine=True,

                                             ).execute()
        return Response(playlists)


class GetPlayListItems(APIView):
    def get(self, request, playlist_id):
        youtube = get_youtube(request)
        playlist_items = youtube.playlistItems().list(part="snippet",
                                                      maxResults=25,
                                                      playlistId=playlist_id,
                                                      ).execute()
        return Response(playlist_items)


class GetVideoInfo(APIView):
    def get(self, request, video_id):
        youtube = get_youtube(request)
        video_info = youtube.videos().list(part="snippet,contentDetails,player",
                                           id=video_id,
                                           ).execute()
        return Response(video_info)

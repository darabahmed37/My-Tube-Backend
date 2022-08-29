from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.apps import get_youtube, Request


class FetchPlayList(APIView):
    def get(self, request):
        youtube = get_youtube(request)
        playlists = youtube.playlists().list(part="snippet,contentDetails",
                                             maxResults=25,
                                             mine=True,

                                             )
        try:
            data = playlists.execute()
            return Response(data)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


class SetUserPlaylist(APIView):
    def post(self, request: Request):
        new_playlist = request.data["id"]
        user = request.user
        user.playlist = new_playlist
        user.save()
        return Response({"status": "ok"}, status=200)

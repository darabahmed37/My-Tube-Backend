from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.apps import get_youtube, Request
from .serializer import TagsSerializer


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
        tags = video_info['items'][0]['snippet']['tags']
        user_tags = request.user.tags.all()
        user_tags = [tag.tag for tag in user_tags]
        for t in tags:
            if t not in user_tags:
                request.user.tags.create(tag=t)
            else:
                current_tag = request.user.tags.filter(tag=t)
                current_tag.update(count=current_tag[0].count + 1)
                current_tag[0].save()
        return Response(video_info)


class SetUserPlaylist(APIView):
    def post(self, request: Request):
        new_playlist = request.data["id"]
        user = request.user
        user.playlist = new_playlist
        user.save()
        return Response({"status": "ok"}, status=200)


class GetTags(generics.ListAPIView):
    serializer_class = TagsSerializer

    def get_queryset(self):
        user = self.request.user
        return user.tags.all()

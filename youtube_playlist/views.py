from django.db.models import QuerySet
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.apps import get_youtube, Request
from .models import Tags
from .serializer import TagsSerializer
from .utils import compare_tags


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

        try:
            tags = video_info['items'][0]['snippet']['tags']
            user_tags = request.user.tags.all()
            user_tags = [tag.tag for tag in user_tags]
            for t in tags:
                tag_out = compare_tags(t, user_tags)

                try:
                    current_tag: QuerySet[Tags] = request.user.tags.filter(tag=tag_out)
                    new_count = current_tag[0].count + 1
                    current_tag.update(count=new_count)
                    current_tag[0].save()
                except Exception as e:
                    request.user.tags.create(tag=t)
                    user_tags.append(t)
        except Exception as e:
            print(e)
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
        tags: QuerySet[Tags] = user.tags.all()
        max_value = tags.order_by("-count")[:5]

        return max_value

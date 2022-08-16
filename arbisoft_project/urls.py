from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", include("authentication.urls")),
    path("yt/", include("youtube_playlist.urls")),
    path("timer/", include("user_activity.urls")),
]

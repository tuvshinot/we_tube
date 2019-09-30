from django.urls import path
from .views import home, create_channel, upload, ChannelDetail, VideoDetail

urlpatterns = [
    path('', home, name='home'),
    path('channel/create', create_channel, name='channel-create'),
    path('upload', upload, name='upload'),
    path('channel/<channel>', ChannelDetail.as_view(), name='channel-detail'),
    path('watch/<video>', VideoDetail.as_view(), name='watch-video')
]

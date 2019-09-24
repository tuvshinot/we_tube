from django.urls import path
from .views import home, create_channel

urlpatterns = [
    path('', home, name='home'),
    path('channel/create', create_channel, name='channel-create')
]
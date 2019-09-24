from django.contrib import admin
from .models import Video, TubeChannel, TubeUser, Tag

admin.site.register(Video)
admin.site.register(TubeChannel)
admin.site.register(TubeUser)
admin.site.register(Tag)
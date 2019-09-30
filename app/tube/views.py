from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from .models import TubeChannel, Video, Tag


def home(request):
    return render(request, 'tube/home.html', {
        'page_title': 'WeTube'
    })


@login_required
def create_channel(request):
    if request.user.tubeuser.has_channel:
        return redirect('home')
    if request.method == 'POST':
        channel_name = request.POST['channel-name']

        if TubeChannel.objects.filter(name=channel_name).exists():
            messages.error(request, 'Channel name taken!')
            return redirect('channel-create')

        slug_name = channel_name.replace(' ', '-')
        tube_channel = TubeChannel(name=channel_name, slug=slug_name)
        tube_channel.save()

        user = request.user
        if user.tubeuser.channel is not None:
            return redirect('home')

        user.tubeuser.channel = tube_channel
        user.tubeuser.has_channel = True
        user.tubeuser.save()

        next_url = request.GET.get('next', None)
        if next_url is not None:
            return redirect(next_url)

        messages.success(
            request, f'Channel created under name of {channel_name}')
        return redirect('home')

    return render(request, 'tube/create-channel.html', {
        'page_title': 'Create new channel'
    })


@login_required
def upload(request):
    if not request.user.tubeuser.has_channel:
        return redirect('home')

    if request.method == 'POST':
        video_content = request.FILES['video']
        thumbnail = request.FILES['thumbnail']
        title = request.POST['title']
        tags_names = request.POST['tags'].split(',')
        channel = request.user.tubeuser.channel

        tags = []
        for tag in tags_names:
            tag, created = Tag.objects.get_or_create(name=tag)
            tags.append(tag)

        video = Video(title=title, channel=channel,
                      thumbnail=thumbnail,
                      video_content=video_content)
        video.save()
        video.tags.add(*tags)

        messages.success(request, 'Video created!')
        return redirect('home')

    return render(request, 'tube/upload.html', {
        'page_title': 'Upload'
    })


class ChannelDetail(DetailView):
    model = TubeChannel
    slug_url_kwarg = 'channel'
    context_object_name = 'channel'
    template_name = 'tube/channel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = kwargs['object'].name
        return context


class VideoDetail(DetailView):
    model = Video
    pk_url_kwarg = 'video'
    context_object_name = 'video'
    template_name = 'tube/watch.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = kwargs['object'].title
        return context

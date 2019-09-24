from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import TubeChannel


def home(request):
    return render(request, 'tube/home.html')


@login_required
def create_channel(request):
    if request.method == 'POST':
        channel_name = request.POST['channel-name']

        if TubeChannel.objects.filter(name=channel_name).exists():
            messages.error(request, 'Channel name taken!')
            return redirect('channel-create')

        tube_channel = TubeChannel(name=channel_name, slug=channel_name)
        tube_channel.save()

        user = request.user
        if user.tubeuser.channel is not None:
            return redirect('home')

        user.tubeuser.channel = tube_channel
        user.tubeuser.has_channel = True
        user.tubeuser.save()

        messages.success(request, f'Channel created under name of {channel_name}')
        return redirect('home')

    return render(request, 'tube/create-channel.html')

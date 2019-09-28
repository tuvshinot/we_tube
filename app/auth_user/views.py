from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import get_user_model

User = get_user_model()


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in!')
            next_url = request.GET.get('next', None)
            if next_url is not None:
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, 'Check your username/password!')
            return redirect('sign-in')
    return render(request, 'auth/sign.html')


def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'That user name taken')
            return redirect('sign-up')
        else:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'That email taken')
                return redirect('sign-up')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email
                )
                user.save()
                # login after register
                auth.login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('home')

    return render(request, 'auth/sign-up.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('home')

    return redirect('home')

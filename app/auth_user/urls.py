from django.urls import path
from .views import sign_in

urlpatterns = [
    path('signin', sign_in, name='sing-in')
]
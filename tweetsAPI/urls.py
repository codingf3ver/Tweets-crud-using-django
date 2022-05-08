from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('create_user',csrf_exempt(views.create_user)),
    path('create_tweet',csrf_exempt(views.create_tweet)),
    path('read_tweet',csrf_exempt(views.read_tweet)),
    path('delete_tweet',csrf_exempt(views.delete_tweet)),
]


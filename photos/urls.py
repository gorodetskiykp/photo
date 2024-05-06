from django.urls import path

from . import views

app_name = 'photos'
urlpatterns = [
    path('', views.index, name='index'),
    path('sync/', views.models_sync, name='models_sync'),
    path('albums/<str:title>', views.album, name='album'),
]

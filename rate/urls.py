from django.urls import path

from . import views

app_name = 'rate'
urlpatterns = [
    path('', views.rate, name='start_rate'),
    path('<int:photo_win_id>/<int:photo_pass_id>/<int:passed>', views.rate, name='rate'),
]

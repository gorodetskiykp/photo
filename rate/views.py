import os
from urllib.parse import unquote

from django.shortcuts import render
from django.conf import settings

from photos.models import Album, Photo
from .models import Rating


def rate_photo(photo_id, score):
    photo = Photo.objects.get(id=photo_id)
    print(photo)
    photo_name = photo.img.url.split('/')[-1]
    print(photo_name)
    file = unquote(f"{settings.MEDIA_ROOT}/{photo.img.url.removeprefix('/media/')}")
    photo_size = os.stat(file).st_size
    print(photo_size)
    rating = Rating.objects.filter(photo_name=photo_name, photo_size=photo_size)
    print(rating)
    if rating:
        rating = rating[0]
        rating.score += score
        rating.views += 1
        rating.save()
    else:
        Rating.objects.create(photo_name=photo_name, photo_size=photo_size, views=1, score=score)


def rate(request, photo_win_id=None, photo_pass_id=None, passed=None):
    if photo_win_id:
        print(photo_win_id)
        rate_photo(photo_win_id, 0 if passed == 1 else 1)
        print()
        print(photo_pass_id)
        rate_photo(photo_pass_id, 0)

    first_photo, second_photo = Photo.objects.order_by('?')[:2]
    template = 'rate/rate.html'
    context = {
        'first_photo': first_photo,
        'second_photo': second_photo,
        'first_photo_album': first_photo.album.title,
        'second_photo_album': second_photo.album.title,
        'albums': Album.objects.all(),
    }
    return render(request, template, context)

from glob import glob
import random
import re

from django.shortcuts import render, redirect
from django.conf import settings
from PIL import Image as PILImage
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail import delete
from .models import Album, Photo


def models_sync(request):
    dirs = [alb.split('/')[-1] for alb in glob(f"{settings.MEDIA_ROOT}/*")]
    dirs.remove('cache')
    Album.objects.all().delete()
    for alb in dirs:
        images = [f"{alb}/{image.split('/')[-1]}" for image in glob(f"{settings.MEDIA_ROOT}/{alb}/*.jp*")]
        album = alb.title()
        alb_obj = Album.objects.create(
            title=album,
        )
        for img in images:
            Photo.objects.create(
                img=img,
                album=alb_obj,
            )
    return redirect('photos:index')


def index(request):
    images = Photo.objects.order_by('?')
    carousel_images = images[:10]
    gallery_images = images[10:30]
    background_image = images[30]

    context = {
        'carousel_images': carousel_images,
        'gallery_images': gallery_images,
        'background_image': background_image,
        'albums': Album.objects.all(),
    }
    template = 'photos/index.html'
    return render(request, template, context)


def album(request, title):
    photos = Album.objects.get(title=title).photos.all()
    template = 'photos/album.html'
    context = {
        'gallery_images': photos,
        'albums': Album.objects.all(),
        'background_image': random.choice(photos)
    }
    return render(request, template, context)

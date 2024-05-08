from glob import glob
import random

from django.shortcuts import render, redirect
from django.conf import settings
from .models import Album, Photo


def models_sync(request):
    dirs = [alb.split('/')[-1] for alb in glob(f"{settings.MEDIA_ROOT}/*")]
    if 'cache' in dirs:
        dirs.remove('cache')
    Album.objects.all().delete()
    for alb in dirs:
        images = [
            f"{alb}/{image.split('/')[-1]}"
            for image in glob(f"{settings.MEDIA_ROOT}/{alb}/*")
            if (image.endswith(".jpg") or image.endswith(".jpeg") or image.endswith(".JPG") or image.endswith(".JPEG"))
        ]
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
    photos = images[10:30]
    background_image = images[30]
    context = {
        'carousel_images': carousel_images,
        'gallery_images': photos,
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
        'background_image': random.choice(photos),
        'title': title,
    }
    return render(request, template, context)

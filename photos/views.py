from glob import glob
import random
import os

from django.shortcuts import render, redirect
from django.conf import settings
from .models import Album, Photo
from rate.models import Rating


def models_sync(request):
    dirs = [alb.split('/')[-1] for alb in glob(f"{settings.MEDIA_ROOT}/*")]
    if 'cache' in dirs:
        dirs.remove('cache')
    Album.objects.all().delete()
    for alb in dirs:
        images = [
            (f"{alb}/{image.split('/')[-1]}", os.stat(image).st_size)
            for image in glob(f"{settings.MEDIA_ROOT}/{alb}/*")
            if (image.endswith(".jpg") or image.endswith(".jpeg") or image.endswith(".JPG") or image.endswith(".JPEG"))
        ]
        album = alb.title()
        alb_obj = Album.objects.create(
            title=album,
        )
        for img in images:
            Photo.objects.create(
                img=img[0],
                size=img[1],
                album=alb_obj,
            )
    return redirect('photos:index')


def index(request):
    images = Photo.objects.order_by('?')
    carousel_images = images[:10]
    photos = images[:20]
    rated_images = sorted(Rating.objects.all(), key=lambda r: r.rate, reverse=True)[:20]
    gallery_images = []
    for photo in rated_images:
        image = Photo.objects.filter(img__endswith=photo.photo_name, size=photo.photo_size).first()
        if image:
            gallery_images.append(image)
    rated_count = len(gallery_images)
    if rated_count < 20:
        gallery_images += photos[:20-rated_count]

    background_image = images[0]
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
        'background_image': random.choice(photos),
        'title': title,
    }
    return render(request, template, context)

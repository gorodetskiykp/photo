from django.db import models


class Album(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Photo(models.Model):
    img = models.ImageField(upload_to='photos')
    album = models.ForeignKey(Album, related_name='photos', on_delete=models.CASCADE)

    def __str__(self):
        return self.img.name

    class Meta:
        unique_together = ('album', 'img')

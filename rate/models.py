from django.db import models


class Rating(models.Model):
    photo_name = models.CharField(max_length=200)
    photo_size = models.IntegerField()
    views = models.IntegerField()
    score = models.IntegerField()

    def __str__(self):
        return f"{self.photo_name} - {self.views} - {self.score} - {self.rate}"

    @property
    def rate(self):
        return round((self.score / self.views) * 100, 2)

    class Meta:
        unique_together = ("photo_name", "photo_size")

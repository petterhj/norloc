from django.contrib.gis.db import models


class License(models.Model):
    title = models.CharField(max_length=150)
    uri = models.URLField()

    def __str__(self):
        return self.title

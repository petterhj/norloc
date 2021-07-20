from django.db import models
from autoslug import AutoSlugField

# from productions.models import Production


JOB_TYPES = (
    ('directing', 'Directing'),
    ('writing', 'Writing'),
    ('photography', 'Photography'),
)


class Person(models.Model):
    slug = AutoSlugField(
        always_update=True,
        populate_from='name',
    )
    name = models.CharField(max_length=50)

    bio = models.TextField(max_length=1000, null=True, blank=True)
    bio_credit = models.CharField(max_length=50, null=True, blank=True)

    tmdb_id = models.CharField(
        max_length=10, null=True, blank=True, unique=True, verbose_name="TMDb ID"
    )
    imdb_id = models.CharField(
        max_length=10, null=True, blank=True, unique=True, verbose_name="IMDb ID"
    )
    nbdb_id = models.CharField(
        max_length=10, null=True, blank=True, unique=True, verbose_name="NBDb ID"
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "people"

    def __str__(self):
        return f"{self.name}"


class Job(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    production = models.ForeignKey('productions.Production', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=JOB_TYPES)

    def __str__(self):
        return f"{self.person.name} {self.type} {self.production.title}"

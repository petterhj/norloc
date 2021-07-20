from django.contrib.gis.db import models
from autoslug import AutoSlugField
from sorl.thumbnail import ImageField
from markdownfield.models import MarkdownField, RenderedMarkdownField

from people.models import Person
from common.util import PathAndRename


PRODUCTION_TYPES = (
    ('film', 'Film'),
    ('tv', 'TV'),
)


class Production(models.Model):
    type = models.CharField(max_length=4, choices=PRODUCTION_TYPES)
    slug = AutoSlugField(
        always_update=True,
        populate_from='title', 
        unique_with=('type',)
    )
    title = models.CharField(max_length=50)
    release_date = models.DateField('Released')
    poster = ImageField(upload_to=PathAndRename('posters/'), blank=True, null=True)

    summary_md = MarkdownField(max_length=1000, null=True, blank=True, rendered_field='summary')
    summary = RenderedMarkdownField(null=True, blank=True)
    runtime = models.PositiveIntegerField(null=True, blank=True)

    tmdb_id = models.CharField(
        max_length=10, null=True, blank=True, unique=True, verbose_name="TMDb ID"
    )
    imdb_id = models.CharField(
        max_length=10, null=True, blank=True, unique=True, verbose_name="IMDb ID"
    )
    nbdb_id = models.CharField(
        max_length=10, null=True, blank=True, unique=True, verbose_name="NBDb ID"
    )

    crew = models.ManyToManyField(Person, through='people.Job')
    locations = models.ManyToManyField('locations.Location', through='productions.Scene')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def year(self):
        return self.release_date.year

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return f"{self.title} ({self.year})"


class Scene(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE)
    description_md = MarkdownField(max_length=800, null=True, blank=True, rendered_field='description')
    description = RenderedMarkdownField(null=True, blank=True)
    location = models.ForeignKey('locations.Location', 
        blank=True, null=True, on_delete=models.SET_NULL
    )

    @property
    def is_unidentified(self):
        return True if not self.location else False

    def __str__(self):
        return '{}: {}'.format(
            self.production.title,
            self.location.full_address if self.location else '(None)'
        )


class Shot(models.Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
    image = ImageField(upload_to=PathAndRename('shots/'), blank=True, null=True)
    highlight = models.BooleanField(default=False)
    timecode = models.IntegerField(blank=True, null=True)
    geometry = models.PointField(blank=True, null=True)

    class Meta:
        ordering = ('timecode',)


class Research(models.Model):
    scenes = models.ManyToManyField(Scene, 
        limit_choices_to={'location': None},
        related_name='research'
    )
    best_guess = models.CharField(max_length=50)
    description_md = MarkdownField(
        max_length=1500,
        null=True,
        blank=True,
        use_editor=False,
        use_admin_editor=False,
        rendered_field='description',
    )
    description = RenderedMarkdownField(null=True, blank=True)
    geometry = models.PointField(blank=True, null=True)

    @property
    def scene_count(self):
        return self.scenes.count()

    class Meta:
        verbose_name_plural = 'research'


# class ResearchReference(models.Model):
#     scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
#     source = models.URLField(max_length=200, blank=True, null=True)

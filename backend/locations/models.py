import requests
from operator import attrgetter
from datetime import date

from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from sorl.thumbnail import ImageField
from autoslug import AutoSlugField
from markdownfield.validators import Validator
from markdownfield.models import MarkdownField, RenderedMarkdownField

from common.util import PathAndRename

# MARKDOWN_VALIDATOR = Validator(w
#     allowed_tags=["div", "p", "b", "i", "strong", "em", 'li', 'ul', 'ol', 'a'],
#     allowed_attrs={},
#     linkify=True
# )


NAME_TYPE_CODE_LIST_ID = 'EAID_3E60BA7D_DDCD_43c0_B898_567F3167A37E'
NAME_TYPE_CODE_LIST_URL = f'https://objektkatalog.geonorge.no/api/object/{NAME_TYPE_CODE_LIST_ID}'

NO_COUNTIES = (
    ('oslo', 'Oslo'),
    ('rogaland', 'Rogaland'),
    ('moere-og-romsdal', 'Møre og Romsdal'),
    ('nordland', 'Nordland'),
    ('viken', 'Viken'),
    ('innlandet', 'Innlandet'),
    ('vestfold-og-telemark', 'Vestfold og Telemark'),
    ('agder', 'Agder'),
    ('vestland', 'Vestland'),
    ('troendelag', 'Trøndelag'),
    ('troms-og-finnmark', 'Troms og Finnmark'),
)


def get_populate_from(instance):
    attrs = [attr.replace('__', '.') for attr in instance.AUTOSLUG_FIELDS]
    attrs_values = [attrgetter(attr)(instance) for attr in attrs]
    
    slug_data = [attr
        .replace('/', '-')
        .replace('æ', 'ae')
        .replace('ø', 'oe')
        .replace('å', 'aa')
    for attr in attrs_values]

    return '-'.join(slug_data)


class Municipality(models.Model):
    slug = AutoSlugField(
        always_update=True,
        populate_from='name', 
        unique_with=('county',)
    )
    county = models.CharField(max_length=20, choices=NO_COUNTIES)
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "municipalities"

    def __str__(self):
        return f"{self.name} ({self.get_county_display()})"

    
class NameType(models.Model):
    AUTOSLUG_FIELDS = ('name',)

    slug = AutoSlugField(
        always_update=True,
        populate_from=get_populate_from
        # populate_from='name',
        # slugify=lambda v: v.replace('/', '-'),
    )
    code = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def populate_from_external(self):
        if self.name and self.description:
            return

        try:
            name_types = requests.get(NAME_TYPE_CODE_LIST_URL).json()['klasse']['attributes']
        except Exception:
            raise ValidationError({"code": "Could not get remote data"})

        if self.code not in [int(a['sosi_verdi']) for a in name_types]:
            raise ValidationError({"code": "Unknown name type code"})

        for name_type in name_types:
            if self.code == int(name_type['sosi_verdi']):
                self.name = name_type["name"]
                self.description = name_type["description"]

    def full_clean(self, *args, **kwargs):
        self.populate_from_external()
        super().full_clean(*args, **kwargs)

    def __str__(self):
        return self.name


class Location(models.Model):
    slug = AutoSlugField(
        always_update=True,
        # slugify=lambda v: ''.join(
        #     [l for l in v
        #         .replace('æ','ae').replace('ø','oe').replace('å','aa')
        #         .lower() if l.isalpha() or l == " "
        #     ]).replace(" ", '-'),
        populate_from='name', 
        unique_with=('municipality')#, 'county')
    )

    ssr_id = models.PositiveIntegerField(
        blank=True, null=True, unique=True, verbose_name="SSR ID"
    )
    name_types = models.ManyToManyField(NameType)

    name = models.CharField(max_length=150)
    municipality = models.ForeignKey(Municipality, null=True, on_delete=models.SET_NULL)
    place = models.CharField(max_length=150, null=True, blank=True)
    # description = models.TextField(max_length=1000, null=True, blank=True)
    description_md = MarkdownField(
        max_length=1500,
        null=True,
        blank=True,
        use_editor=False,
        use_admin_editor=False,
        rendered_field='description',
        # validator=MARKDOWN_VALIDATOR,
    )
    description = RenderedMarkdownField(null=True, blank=True)

    geometry = models.PolygonField()

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def county(self):
        return self.municipality.get_county_display()

    @property
    def full_address(self):
        if self.place:
            return "{}, {}, {}".format(
                self.name, self.place, self.municipality.name
            )
        return "{}, {}".format(
            self.name, self.municipality.name
        )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f"{self.full_address}"# [{self.name_type.name}]"


class Photo(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    image = ImageField(upload_to=PathAndRename('locations/'))
    title = models.CharField(max_length=100)
    taken_date = models.DateField('Taken', blank=True, null=True)
    credit = models.CharField(max_length=50, blank=True, null=True)
    source = models.URLField(max_length=200, blank=True, null=True)
    license = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # # Properties
    # @property
    # def caption(self):
    #     return '%s%s [%s%s%s]' % (
    #         self.title,
    #         ' (%s)' % (self.year) if self.year else '',
    #         self.credit,
    #         ' - %s' % (urlparse(self.source).hostname.replace('www.', '')) if self.source else '',
    #         ' - %s' % (self.license) if self.license else ''
    #     )

    def __str__(self):
        return self.title
    
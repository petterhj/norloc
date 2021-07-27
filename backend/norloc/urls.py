from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path as url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_nested import routers

from locations.views import (
    LocationViewSet,
    PhotoViewSet,
    NameTypeViewSet,
    CountiesViewSet,
)
from productions.views import (
    ProductionViewSet,
    SceneLocationViewSet,
    SceneResearchViewSet,
)
from people.views import CrewViewSet


schema_view = get_schema_view(
   openapi.Info(
      title="Norske opptakssteder API",
      default_version='v1',
      description="API for Norske opptakssteder",
      contact=openapi.Contact(email="post@petterhj.net"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    # Productions
    path('productions/', ProductionViewSet.as_view(
        {'get': 'list', 'post': 'create'}
    ), name='production-list'),
    path('productions/<str:type>', ProductionViewSet.as_view(
        {'get': 'list'}
    ), name='production-list'),
    path('productions/<str:type>/<str:slug>/', ProductionViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
    }), name='production-detail'),

    path('productions/<str:type>/<str:slug>/crew/', CrewViewSet.as_view({
        'get': 'list',
    }), name='production-crew-list'),
    path('productions/<str:type>/<str:slug>/locations/', SceneLocationViewSet.as_view({
        'get': 'list',
    }), name='production-locations-list'),
    path('productions/<str:type>/<str:slug>/locations/unidentified/', SceneResearchViewSet.as_view({
        'get': 'list',
    }), name='production-research-list'),

    # Locations
    path('locations/', LocationViewSet.as_view(
        {'get': 'list', 'post': 'create'}
    ), name='location-list'),

    path('locations/types/', NameTypeViewSet.as_view(
        {'get': 'list', 'post': 'create'}
    ), name='location-type'),
    # path('locations/types/<str:type>/', LocationViewSet.as_view(
    #     {'get': 'list'}
    # ), name='location-list'), # /locations?type=skole

    path('locations/counties/', CountiesViewSet.as_view(
        {'get': 'list'}
    ), name='location-counties-list'),
    path('locations/<str:county>/', LocationViewSet.as_view(
        {'get': 'list'}#, 'post': 'create'}
    ), name='location-county-list'),
    path('locations/<str:county>/<str:municipality>/', LocationViewSet.as_view(
        {'get': 'list'}#, 'post': 'create'}
    ), name='location-municipality-list'),
    
    path('locations/<str:county>/<str:municipality>/<str:slug>/', LocationViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
    }), name='location-detail'),
    path('locations/<str:county>/<str:municipality>/<str:slug>/photos/', PhotoViewSet.as_view({
        'get': 'list',
    }), name='location-photo-list'),

    path('admin/', admin.site.urls),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

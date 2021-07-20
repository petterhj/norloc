from rest_framework import viewsets
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response

from people.models import Person, Job
from people.serializers import (
    JobSerializer,
)


class CrewViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer

    def get_queryset(self):
        return Job.objects.filter(
            production__slug=self.kwargs['slug']
        )  

from rest_framework import serializers

from people.models import Person, Job


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        # fields = '__all__'
        exclude = ('id',)


class JobSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    # person_name = serializers.ReadOnlyField(source='person.name')

    class Meta:
        model = Job
        # fields = ('person',)
        exclude = ('id', 'production',)

    def to_representation(self, obj):
        '''Move fields from profile to user representation.'''
        representation = super().to_representation(obj)
        person_representation = representation.pop('person')
        for key in person_representation:
            representation[key] = person_representation[key]
        return representation

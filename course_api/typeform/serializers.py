from attr import field
from coreapi import Field
from course_api.typeform.models import Form, FormField
from rest_framework import serializers

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ('id', 'title', 'description', 'is_public')

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ('id', 'label', 'kind', 'options', 'value')

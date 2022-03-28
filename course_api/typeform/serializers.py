from attr import field
from coreapi import Field
from course_api.typeform.models import Form, FormField, Submission
from rest_framework import serializers


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ('id', 'title', 'description', 'is_public', 'created_by', 'created_date', 'modified_date')
        extra_kwargs = {'created_by': {'read_only': True}}


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ('id', 'label', 'kind', 'options', 'value', 'meta')


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'form', 'created_date')

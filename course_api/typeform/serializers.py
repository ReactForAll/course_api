from attr import field
from coreapi import Field
from course_api.typeform.models import Answer, Form, FormField, Submission
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


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('form_field', 'value')


class SubmissionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    form = FormSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ('answers', 'id', 'form', 'created_date')
        read_only_fields = ('id', 'created_date')

    def create(self, validated_data):
        # Create Answer Objects
        answers = validated_data.pop('answers')
        submission = super().create(validated_data)
        for answer in answers:
            Answer.objects.create(submission=submission, **answer)
        return submission

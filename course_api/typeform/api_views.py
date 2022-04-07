from re import X
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.serializers import Serializer, CharField, IntegerField
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from course_api.typeform.models import Answer, Form, FormField, Submission
from course_api.typeform.serializers import AnswerSerializer, FieldSerializer, FormSerializer, SubmissionSerializer
from drf_yasg.utils import swagger_auto_schema
from yaml import serialize


# API View returns a JSON with constant value "[value: "Success"]"
class TestView(GenericViewSet):
    # Dummy Serializer
    class DummyFormSerializer(Serializer):
        id = IntegerField()
        title = CharField()

    @swagger_auto_schema(
        responses={200: DummyFormSerializer(many=True)},
    )
    def mock_test(self, request):
        return Response([
            {
                "id": 1,
                "title": "Form 1",
            },
            {
                "id": 2,
                "title": "Form 2",
            },
            {
                "id": 3,
                "title": "Form 3",
            }
        ])


class FormViewSet(ModelViewSet):
    serializer_class = FormSerializer
    queryset = Form.objects.all()

    def get_queryset(self, *args, **kwargs):
        updateMethods = ['patch', 'update', 'partial_update', 'delete']
        if(self.request.user.is_anonymous and self.action not in updateMethods):
            return self.queryset.filter(is_public=True)
        if(self.request.user.is_anonymous):
            raise PermissionError("You must be authenticated to use this API.")
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class FieldViewSet(ModelViewSet):
    serializer_class = FieldSerializer

    def get_queryset(self):
        if(self.request.user.is_anonymous):
            raise PermissionError("You must be authenticated to use this API.")
        return FormField.objects.filter(form=self.kwargs['form_pk'])

    def perform_create(self, serializer):
        # Add Authorization
        serializer.save(form_id=self.kwargs['form_pk'])


class SubmissionViewSet(RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if(self.request.user.is_anonymous):
            raise PermissionError("You must be authenticated to use this API.")
        return Submission.objects.filter(form=self.kwargs['form_pk'], form__created_by=self.request.user)

    def get_permissions(self):
        if(self.action == 'create'):
            self.permission_classes = []
        return super().get_permissions()

    def perform_create(self, serializer):
        # Add Authorization
        serializer.save(form_id=self.kwargs['form_pk'])


class AnswerViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def get_queryset(self, *args, **kwargs):
        updateMethods = ['patch', 'update', 'partial_update']
        if(self.request.user.is_anonymous and self.action not in updateMethods):
            return self.queryset.filter(submission__form__is_public=True)
        if(self.request.user.is_anonymous):
            raise PermissionError("You must be authenticated to use this API.")
        return self.queryset.filter(submission__form__created_by=self.request.user)

    def perform_create(self, serializer):
        # Add Authorization
        serializer.save(submission_id=self.kwargs['submission_pk'])

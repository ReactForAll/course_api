from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.serializers import Serializer, CharField, IntegerField
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from course_api.typeform.models import Form, FormField
from course_api.typeform.serializers import FieldSerializer, FormSerializer
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


class FormViewSet(LoginRequiredMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet, CreateModelMixin):
    serializer_class = FormSerializer
    authentication_classes = []
    authorization_classes = []
    queryset = Form.objects.all()

    def get_queryset(self, *args, **kwargs):
        updateMethods = ['patch', 'update', 'partial_update']
        if(self.request.user.is_anonymous and self.action not in updateMethods):
            return self.queryset.filter(is_public=True)
        if(self.request.user.is_anonymous):
            raise PermissionError("You must be authenticated to use this API.")
        if(self.action in updateMethods):
            return self.queryset.filter(created_by=self.request.user)
        return self.queryset.all()


class FieldViewSet(ModelViewSet):
    serializer_class = FieldSerializer

    def get_queryset(self):
        if(self.request.user.is_anonymous):
            raise PermissionError("You must be authenticated to use this API.")
        return FormField.objects.filter(form=self.kwargs['form_pk'])

    def perform_create(self, serializer):
        # Add Authorization
        serializer.save(form_id=self.kwargs['form_pk'])

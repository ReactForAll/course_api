
from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter
from course_api.typeform.api_views import FieldViewSet, FormViewSet, TestView

from rest_framework_nested import routers
from course_api.users.api.views import DecoratedTokenObtainPairView, DecoratedTokenRefreshView, UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"

router.register(r'forms', FormViewSet)


forms_router = routers.NestedSimpleRouter(router, r'forms', lookup='form')
forms_router.register(r'fields', FieldViewSet, basename='form-fields')

urlpatterns = [
    # GET /api/test -> TestView.as_view()
    path('mock_test/', TestView.as_view(actions={'get': 'mock_test'}), name='mock_test'),
    path(r'', include(router.urls)),
    path(r'', include(forms_router.urls)),
    path('token/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh'),
]

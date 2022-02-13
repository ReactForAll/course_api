from django.contrib import admin
from course_api.typeform.models import Form, FormField

# Register your models here.
admin.site.register(Form)
admin.site.register(FormField)

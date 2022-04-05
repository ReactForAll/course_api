from django.contrib import admin
from course_api.typeform.models import Answer, Form, FormField, Submission

# Register your models here.
admin.site.register(Form)
admin.site.register(FormField)
admin.site.register(Submission)
admin.site.register(Answer)

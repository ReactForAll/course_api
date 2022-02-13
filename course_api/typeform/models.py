import enum
from django.db import models
from course_api.utils.models.base import BaseManager, BaseModel
from course_api.utils.models.jsonfield import JSONField
from course_api.users.models import User

class FormField(BaseModel):
    class FormFieldKind(enum.Enum):
        TEXT = "text"
        DROPDOWN = "dropdown"
        RADIO = "radio"

    kind = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in FormFieldKind])
    label = models.CharField(max_length=100)    
    options = JSONField(null=True, blank=True, verbose_name="Dropdown Options")
    value = models.CharField(max_length=100, null=True, blank=True)
    form = models.ForeignKey("Form", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Form Field"
        verbose_name_plural = "Form Fields"
    def __str__(self):
        return f"{self.label} ({self.kind})"

class Form(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_public = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_forms")
    # Add the fields of the Form. One field can only be in one Form.

    def __str__(self):
        return self.title

class Submission(BaseModel):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = BaseManager()

    def __str__(self):
        return f"{self.form.name} - {self.form_field.label} ({self.form_field.kind})"

class Answer(BaseModel):
    form_field = models.ForeignKey(FormField, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.submission.form.name} - {self.form_field.label} ({self.form_field.kind})"

    

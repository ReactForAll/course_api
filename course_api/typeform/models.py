import enum
from django.db import models
from course_api.utils.models.base import BaseManager, BaseModel
from django.db.models import JSONField
from course_api.users.models import User


class FormField(BaseModel):
    class FormFieldKind(enum.Enum):
        TEXT = "text"
        DROPDOWN = "dropdown"
        RADIO = "radio"
        GENERIC = "generic"

    kind = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in FormFieldKind])
    label = models.CharField(max_length=100)
    options = JSONField(null=True, blank=True, verbose_name="Dropdown Options")
    value = models.CharField(max_length=100, null=True, blank=True)
    form = models.ForeignKey("Form", on_delete=models.CASCADE)
    # Meta Field used to store additional data
    meta = JSONField(null=True, blank=True, verbose_name="Meta", help_text="Additional data for the field")

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

    @property
    def answers(self):
        return Answer.objects.filter(submission=self)
    objects = BaseManager()

    def __str__(self):
        return f"{self.form.title} - {self.created_date}"


class Answer(BaseModel):
    form_field = models.ForeignKey(FormField, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.submission.form.name} - {self.form_field.label} ({self.form_field.kind})"

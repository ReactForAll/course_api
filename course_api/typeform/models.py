import enum
from django.db import models
from course_api.utils.models.base import BaseManager, BaseModel
from course_api.utils.models.jsonfield import JSONField
from course_api.users.models import User
# Create your models here.

# JS Types: 
# 
# export type textFieldTypes = "text" | "email" | "date";

# export type TextField = {
#   kind: "text";
#   id: number;
#   label: string;
#   fieldType: textFieldTypes;
#   value: string;
# };

# export type DropdownField = {
#   kind: "dropdown";
#   id: number;
#   label: string;
#   options: string[];
#   value: string;
# };
# export type RadioField = {
#   kind: "radio";
#   id: number;
#   label: string;
#   options: string[];
#   value: string;
# };

# export type FormField = TextField | DropdownField | RadioField;
# export type FormFieldKind = FormField["kind"];

class FormField(BaseModel):
    class FormFieldKind(enum.Enum):
        TEXT = "text"
        DROPDOWN = "dropdown"
        RADIO = "radio"

    kind = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in FormFieldKind])
    id = models.IntegerField()
    label = models.CharField(max_length=100)    
    options = JSONField(null=True, blank=True, verbose_name="Dropdown Options")
    value = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.label} ({self.kind})"

class Form(BaseModel):
    name = models.CharField(max_length=100)
    fields = models.ManyToManyField(FormField, related_name="forms")

    def __str__(self):
        return self.name

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

    

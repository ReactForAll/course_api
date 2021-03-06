# Generated by Django 3.2.12 on 2022-02-13 20:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('typeform', '0004_form_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='formfield',
            options={'verbose_name': 'Form Field', 'verbose_name_plural': 'Form Fields'},
        ),
        migrations.AddField(
            model_name='form',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_forms', to='users.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='form',
            name='expires_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

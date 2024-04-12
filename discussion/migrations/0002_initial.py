# Generated by Django 5.0.4 on 2024-04-11 13:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('discussion', '0001_initial'),
        ('home', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturerdiscussion',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.course'),
        ),
        migrations.AddField(
            model_name='lecturerdiscussion',
            name='send_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='studentdiscussion',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.course'),
        ),
        migrations.AddField(
            model_name='studentdiscussion',
            name='send_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.student'),
        ),
    ]
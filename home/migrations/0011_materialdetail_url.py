# Generated by Django 5.0.4 on 2024-04-14 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_remove_material_file_materialdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialdetail',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]

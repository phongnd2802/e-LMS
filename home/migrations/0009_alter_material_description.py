# Generated by Django 5.0.4 on 2024-04-13 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_material_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='description',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
    ]

# Generated by Django 5.0.4 on 2024-04-14 07:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_material_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='file',
        ),
        migrations.CreateModel(
            name='MaterialDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('file', models.FileField(blank=True, null=True, upload_to='materials/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.material')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]

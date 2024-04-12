# Generated by Django 5.0.4 on 2024-04-11 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LecturerDiscussion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=2000)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-sent_at',),
            },
        ),
        migrations.CreateModel(
            name='StudentDiscussion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=2000)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-sent_at',),
            },
        ),
    ]
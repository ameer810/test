# Generated by Django 3.0.7 on 2020-12-20 18:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import job.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('location', django_countries.fields.CountryField(max_length=2)),
                ('job_type', models.CharField(choices=[('Full Time', 'Full Time'), ('Part Time', 'Part Time')], max_length=15)),
                ('description', models.TextField(max_length=1000)),
                ('emails', models.EmailField(blank=True, max_length=254, null=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('Vacancy', models.IntegerField(default=1)),
                ('salary', models.IntegerField(default=0)),
                ('experience', models.IntegerField(default=1)),
                ('apply_count', models.IntegerField(blank=True, default=0, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=job.models.image_upload)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('applied', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='job_wner', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.Category')),
                ('favourite', models.ManyToManyField(blank=True, related_name='favourite', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='job.Job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('website', models.URLField()),
                ('cv', models.FileField(upload_to='apply/')),
                ('cover_letter', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('applied', models.BooleanField(blank=True, default=False, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apply_job', to='job.Job')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

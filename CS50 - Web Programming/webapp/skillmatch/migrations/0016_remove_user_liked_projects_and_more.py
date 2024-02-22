# Generated by Django 4.1.3 on 2023-04-07 14:52

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skillmatch', '0015_user_liked_projects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='liked_projects',
        ),
        migrations.RemoveField(
            model_name='user',
            name='onprogress_projects',
        ),
        migrations.RemoveField(
            model_name='user',
            name='previous_projects',
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('created_projects', models.ManyToManyField(related_name='creator', to='skillmatch.project')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('skillmatch.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ProjectRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_rating', to='skillmatch.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skillmatch.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('liked_projects', models.ManyToManyField(related_name='user_liked', to='skillmatch.project')),
                ('onprogress_projects', models.ManyToManyField(related_name='user_onprogress', to='skillmatch.project')),
                ('previous_projects', models.ManyToManyField(related_name='user_previous', to='skillmatch.project')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('skillmatch.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
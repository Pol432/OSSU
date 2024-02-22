# Generated by Django 4.1.3 on 2023-04-05 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skillmatch', '0014_project_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='liked_projects',
            field=models.ManyToManyField(related_name='user_liked', to='skillmatch.project'),
        ),
    ]

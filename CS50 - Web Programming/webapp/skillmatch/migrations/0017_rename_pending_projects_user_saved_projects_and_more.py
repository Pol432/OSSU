# Generated by Django 4.1.3 on 2023-04-07 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skillmatch', '0016_remove_user_liked_projects_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='pending_projects',
            new_name='saved_projects',
        ),
        migrations.RemoveField(
            model_name='student',
            name='liked_projects',
        ),
        migrations.AddField(
            model_name='user',
            name='liked_projects',
            field=models.ManyToManyField(related_name='user_liked', to='skillmatch.project'),
        ),
    ]

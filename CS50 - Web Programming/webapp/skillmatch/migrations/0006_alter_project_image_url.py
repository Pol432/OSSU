# Generated by Django 4.1.3 on 2023-03-14 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skillmatch', '0005_alter_project_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image_url',
            field=models.URLField(default=None, max_length=500, null=True),
        ),
    ]
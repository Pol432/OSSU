# Generated by Django 4.1.3 on 2023-03-18 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skillmatch', '0012_rename_ability_ability_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ability',
            old_name='name',
            new_name='ability',
        ),
        migrations.RenameField(
            model_name='career',
            old_name='name',
            new_name='career',
        ),
        migrations.AlterField(
            model_name='project',
            name='abilities',
            field=models.ManyToManyField(blank=True, related_name='abilities', to='skillmatch.ability'),
        ),
        migrations.AlterField(
            model_name='project',
            name='careers',
            field=models.ManyToManyField(blank=True, related_name='careers', to='skillmatch.career'),
        ),
    ]

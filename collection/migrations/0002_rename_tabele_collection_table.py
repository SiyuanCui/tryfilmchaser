# Generated by Django 3.2.5 on 2023-03-17 01:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collection',
            old_name='tabele',
            new_name='table',
        ),
    ]
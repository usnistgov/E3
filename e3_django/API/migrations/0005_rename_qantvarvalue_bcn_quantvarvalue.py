# Generated by Django 3.2 on 2021-04-29 23:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_bcn'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bcn',
            old_name='qantVarValue',
            new_name='quantVarValue',
        ),
    ]

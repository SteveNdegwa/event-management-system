# Generated by Django 5.0.2 on 2024-02-13 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_genericbasemodel_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basemodel',
            old_name='created_at',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='basemodel',
            old_name='updated_at',
            new_name='date_modified',
        ),
    ]
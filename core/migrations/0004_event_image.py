# Generated by Django 5.0.2 on 2024-02-26 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_attendee_user_id_attendee_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
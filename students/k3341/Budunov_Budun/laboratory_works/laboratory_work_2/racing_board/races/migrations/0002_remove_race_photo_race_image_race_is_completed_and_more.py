# Generated by Django 5.1.3 on 2024-11-24 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('races', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='race',
            name='photo',
        ),
        migrations.AddField(
            model_name='race',
            name='image',
            field=models.ImageField(default='race_photos/default_race.jpg', upload_to='race_photos/'),
        ),
        migrations.AddField(
            model_name='race',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='racer',
            name='avatar',
            field=models.ImageField(default='avatars/default_avatar.jpg', upload_to='avatars/'),
        ),
    ]

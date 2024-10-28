# Generated by Django 4.2 on 2024-10-28 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_platform', '0003_remove_post_link_url_remove_post_media_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='posts', through='social_platform.PostTag', to='social_platform.tag'),
        ),
    ]

# Generated by Django 4.2 on 2024-10-23 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wardrobe_manager', '0005_item_is_in_love'),
    ]

    operations = [
        migrations.AddField(
            model_name='outfit',
            name='outfit_image',
            field=models.ImageField(blank=True, null=True, upload_to='wardrobe_outfits/'),
        ),
    ]

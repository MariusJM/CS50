# Generated by Django 5.0.1 on 2024-01-25 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_comments_listing'),
    ]

    operations = [
        migrations.DeleteModel(
            name='bid',
        ),
        migrations.DeleteModel(
            name='comments',
        ),
        migrations.DeleteModel(
            name='listing',
        ),
    ]

# Generated by Django 5.0.1 on 2024-01-29 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_bid_bid_bid_bidder_alter_listing_starting_bid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'verbose_name': 'Comment'},
        ),
    ]
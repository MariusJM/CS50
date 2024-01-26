# Generated by Django 5.0.1 on 2024-01-26 19:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_listing_isactive_alter_category_category_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]

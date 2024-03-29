# Generated by Django 5.0.1 on 2024-01-26 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_comments_comment_alter_listing_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

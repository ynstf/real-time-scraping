# Generated by Django 4.0 on 2024-02-10 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraperapp', '0002_niceonesaaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]

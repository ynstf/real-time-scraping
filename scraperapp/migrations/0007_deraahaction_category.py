# Generated by Django 4.0 on 2024-02-09 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraperapp', '0006_deraahaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='deraahaction',
            name='Category',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

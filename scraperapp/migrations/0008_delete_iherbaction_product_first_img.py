# Generated by Django 4.0 on 2024-02-15 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraperapp', '0007_cvaleyaction'),
    ]

    operations = [
        migrations.DeleteModel(
            name='IherbAction',
        ),
        migrations.AddField(
            model_name='product',
            name='first_img',
            field=models.URLField(blank=True, null=True),
        ),
    ]
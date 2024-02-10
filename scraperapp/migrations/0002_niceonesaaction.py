# Generated by Django 4.0 on 2024-02-10 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraperapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NiceonesaAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=400)),
                ('products_number', models.IntegerField()),
                ('repetition_interval', models.IntegerField()),
                ('Category', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(default='Not Started', max_length=20)),
            ],
        ),
    ]

# Generated by Django 3.2.12 on 2023-03-11 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='menu_item_description',
            field=models.CharField(default='', max_length=1000),
        ),
    ]

# Generated by Django 2.2.15 on 2021-03-26 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20210326_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='body',
            field=models.TextField(),
        ),
    ]
# Generated by Django 3.2.12 on 2022-04-08 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0002_auto_20220408_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerfrancebleu',
            name='ville',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
    ]

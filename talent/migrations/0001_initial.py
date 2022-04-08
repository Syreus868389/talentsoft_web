# Generated by Django 3.2.12 on 2022-04-08 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('cat', models.CharField(max_length=300)),
                ('color', models.CharField(max_length=300)),
                ('france_bleu', models.CharField(max_length=300)),
                ('creation_date', models.DateTimeField()),
                ('postes', models.CharField(max_length=300)),
                ('mob', models.CharField(max_length=300)),
                ('direction', models.CharField(max_length=300)),
            ],
        ),
    ]

# Generated by Django 3.1.7 on 2021-05-23 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_number', models.IntegerField()),
                ('station_description', models.CharField(max_length=200)),
            ],
        ),
    ]

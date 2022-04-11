# Generated by Django 2.2.5 on 2022-04-07 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='chain_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='place',
            name='search_name',
            field=models.CharField(default='', max_length=255, verbose_name='Название для поиска'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='place',
            name='sum_rating',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='place',
            name='address',
            field=models.CharField(max_length=1024, verbose_name='Адрес'),
        ),
    ]

# Generated by Django 4.0.1 on 2022-01-24 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdNotifyManager', '0015_goods_external_id_goods_goods_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='description',
            field=models.CharField(max_length=1200),
        ),
    ]
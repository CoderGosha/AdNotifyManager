# Generated by Django 4.0 on 2022-01-22 13:02

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('AdNotifyManager', '0010_alter_querylink_data_create_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='querylink',
            name='data_create',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 22, 16, 1, 59, 803605)),
        ),
        migrations.AlterField(
            model_name='querylink',
            name='data_expired',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 1, 22, 16, 1, 59, 803605), null=True),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='data_create',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 22, 16, 1, 59, 804603)),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='data_expired',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 1, 22, 16, 1, 59, 804603), null=True),
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('data_create', models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0))),
                ('name', models.CharField(max_length=50)),
                ('cost', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('locate', models.CharField(blank=True, max_length=50, null=True)),
                ('success', models.BooleanField(blank=True, null=True)),
                ('query_link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='AdNotifyManager.querylink')),
            ],
        ),
    ]

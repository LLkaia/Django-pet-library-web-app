# Generated by Django 4.2.6 on 2023-10-07 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_plated_end_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 4.1 on 2023-10-08 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_book_count_book_description_book_name_alter_book_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='date_of_release',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]

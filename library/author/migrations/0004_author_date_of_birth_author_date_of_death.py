# Generated by Django 4.1 on 2023-10-08 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0003_alter_author_books'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='date_of_birth',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='date_of_death',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]

# Generated by Django 4.1 on 2023-10-08 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_book_date_of_issue'),
        ('author', '0004_author_date_of_birth_author_date_of_death'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='books',
            field=models.ManyToManyField(blank=True, related_name='authors_set', to='book.book'),
        ),
    ]

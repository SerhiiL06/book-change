# Generated by Django 4.2.7 on 2023-12-01 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_relations', '0003_alter_bookrelations_book_alter_bookrelations_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookrelations',
            options={'verbose_name_plural': 'Book relations'},
        ),
    ]
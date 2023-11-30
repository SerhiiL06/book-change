# Generated by Django 4.2.7 on 2023-11-10 14:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_alter_bookinpdf_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='books.author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='books', to='books.genre'),
        ),
    ]
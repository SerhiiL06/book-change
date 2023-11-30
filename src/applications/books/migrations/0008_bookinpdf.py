# Generated by Django 4.2.7 on 2023-11-03 09:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_book_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookInPDF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(upload_to='book_in_pdf/')),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='in_pdf', to='books.book')),
            ],
        ),
    ]
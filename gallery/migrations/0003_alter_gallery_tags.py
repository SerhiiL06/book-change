# Generated by Django 4.2.7 on 2023-11-25 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_alter_gallery_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='gallery.imagetag'),
        ),
    ]

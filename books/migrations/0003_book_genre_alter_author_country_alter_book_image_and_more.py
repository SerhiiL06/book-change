# Generated by Django 4.2.6 on 2023-10-22 13:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0002_book_created_at_book_last_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='books.genre'),
        ),
        migrations.AlterField(
            model_name='author',
            name='country',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='book_img/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'JPEG'])]),
        ),
        migrations.AlterField(
            model_name='book',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_books', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-06 18:16

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_user_last_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_activity',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.CreateModel(
            name='UserEmailNewsLetter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sending_out_offers', models.BooleanField(default=False)),
                ('news_mailer', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='news_letter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

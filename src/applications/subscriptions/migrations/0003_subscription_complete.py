# Generated by Django 4.2.7 on 2023-11-29 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_alter_subscription_plan_alter_subscription_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]

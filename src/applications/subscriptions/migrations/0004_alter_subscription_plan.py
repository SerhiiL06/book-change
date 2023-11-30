# Generated by Django 4.2.7 on 2023-11-29 13:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_subscription_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.billingplan'),
        ),
    ]
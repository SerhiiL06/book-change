# Generated by Django 4.2.6 on 2023-11-02 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_requests', '0002_bookrequest_comment_alter_bookrequest_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(default={})),
            ],
        ),
    ]
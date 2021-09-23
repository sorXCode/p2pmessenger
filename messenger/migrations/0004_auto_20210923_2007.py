# Generated by Django 3.2.7 on 2021-09-23 20:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0003_alter_messagehistory_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messageentry',
            name='id',
        ),
        migrations.AddField(
            model_name='messageentry',
            name='message_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
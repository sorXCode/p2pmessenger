# Generated by Django 3.2.7 on 2021-09-23 19:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('messenger', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='messagehistory',
            name='user_a',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_a', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='messagehistory',
            name='user_b',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_b', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='messageentry',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='messageentry',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
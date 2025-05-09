# Generated by Django 4.2.7 on 2025-04-20 23:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('brokers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bdm',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_bdms', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bdm',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bdm_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='branch',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_branches', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='broker',
            name='bdms',
            field=models.ManyToManyField(related_name='assigned_brokers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='broker',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_brokers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='broker',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='broker_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]

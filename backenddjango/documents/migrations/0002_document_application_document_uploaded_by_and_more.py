# Generated by Django 4.2.7 on 2025-04-20 23:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applications', '0002_application_bd_application_branch_application_broker_and_more'),
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='application',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='applications.application'),
        ),
        migrations.AddField(
            model_name='document',
            name='uploaded_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uploaded_documents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fee',
            name='application',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fees', to='applications.application'),
        ),
        migrations.AddField(
            model_name='fee',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_fees', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ledger',
            name='application',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ledger_entries', to='applications.application'),
        ),
        migrations.AddField(
            model_name='ledger',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_ledger_entries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ledger',
            name='fee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ledger_entries', to='documents.fee'),
        ),
        migrations.AddField(
            model_name='ledger',
            name='repayment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ledger_entries', to='documents.repayment'),
        ),
        migrations.AddField(
            model_name='note',
            name='application',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='applications.application'),
        ),
        migrations.AddField(
            model_name='note',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_notes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='repayment',
            name='application',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repayments', to='applications.application'),
        ),
        migrations.AddField(
            model_name='repayment',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_repayments', to=settings.AUTH_USER_MODEL),
        ),
    ]

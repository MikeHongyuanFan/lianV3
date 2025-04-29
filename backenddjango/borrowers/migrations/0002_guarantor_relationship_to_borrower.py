from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('borrowers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guarantor',
            name='relationship_to_borrower',
            field=models.CharField(blank=True, choices=[('spouse', 'Spouse'), ('parent', 'Parent'), ('child', 'Child'), ('sibling', 'Sibling'), ('business_partner', 'Business Partner'), ('friend', 'Friend'), ('other', 'Other')], max_length=20, null=True),
        ),
    ]

# Generated by Django 4.2 on 2023-04-05 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0002_alter_regionalinternetregistry_name_policyproposal'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='policyproposal',
            unique_together={('rir', 'identifier')},
        ),
    ]

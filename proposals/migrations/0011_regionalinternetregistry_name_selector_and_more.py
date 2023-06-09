# Generated by Django 4.2 on 2023-04-07 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0010_regionalinternetregistry_identifier_selector'),
    ]

    operations = [
        migrations.AddField(
            model_name='regionalinternetregistry',
            name='name_selector',
            field=models.CharField(blank=True, help_text='CSS selector that selects the name of one proposal', max_length=100, verbose_name='Name selector'),
        ),
        migrations.AddField(
            model_name='regionalinternetregistry',
            name='state_selector',
            field=models.CharField(blank=True, help_text='CSS selector that selects the state of one proposal', max_length=100, verbose_name='State selector'),
        ),
        migrations.AddField(
            model_name='regionalinternetregistry',
            name='url_selector',
            field=models.CharField(blank=True, help_text='CSS selector that selects the URL of one proposal', max_length=100, verbose_name='URL selector'),
        ),
        migrations.AlterField(
            model_name='regionalinternetregistry',
            name='identifier_selector',
            field=models.CharField(blank=True, help_text='CSS selector that selects the identifier of one proposal', max_length=100, verbose_name='Identifier selector'),
        ),
    ]

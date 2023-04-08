# Generated by Django 4.2 on 2023-04-07 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0012_regionalinternetregistry_url_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regionalinternetregistry',
            name='url_template',
            field=models.CharField(blank=True, help_text='Template for converting a proposal into a URL', max_length=100, verbose_name='URL template'),
        ),
    ]

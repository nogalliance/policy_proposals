# Generated by Django 4.2 on 2023-04-07 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0011_regionalinternetregistry_name_selector_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='regionalinternetregistry',
            name='url_template',
            field=models.CharField(blank=True, help_text='Template for converting the identifier into a URL', max_length=100, verbose_name='URL template'),
        ),
    ]
# Generated by Django 4.2 on 2023-04-07 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0005_alter_regionalinternetregistry_html_container'),
    ]

    operations = [
        migrations.AddField(
            model_name='regionalinternetregistry',
            name='slug',
            field=models.SlugField(default='', verbose_name='Slug'),
            preserve_default=False,
        ),
    ]

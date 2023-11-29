# Generated by Django 4.2 on 2023-11-29 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0018_regionalinternetregistry_date_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='StateOverrideFromURL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selector', models.CharField(help_text='CSS selector', max_length=100, verbose_name='Selector')),
                ('priority', models.PositiveSmallIntegerField(default=100, help_text='Higher number = higher priority', verbose_name='Priority')),
                ('contains', models.CharField(help_text='If selected element contains this text', max_length=50, verbose_name='Contains')),
                ('state', models.CharField(help_text='Then override the state with this', max_length=25, verbose_name='State')),
                ('rir', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='proposals.regionalinternetregistry', verbose_name='RIR')),
            ],
        ),
    ]
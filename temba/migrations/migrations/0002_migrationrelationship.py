# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-26 19:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('migrations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MigrationRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(choices=[('contact', 'Contact'), ('contact_group', 'Contact Groups'), ('flow', 'Flows'), ('flow_start', 'Flow Starts'), ('flow_run', 'Flow Runs'), ('campaign', 'Campaigns'), ('msg', 'Messages'), ('msg_label', 'Message Labels'), ('msg_broadcast', 'Message Broadcast')], help_text='The module reference like flow_run, contact, flow, contacts_group...', max_length=100)),
                ('source_value', models.CharField(help_text='The original value from other host', max_length=100)),
                ('destination_value', models.CharField(help_text='The value related on our host', max_length=100)),
                ('migration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='migrations.Migration', verbose_name='Migration')),
            ],
        ),
    ]

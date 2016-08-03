# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0014_auto_20160404_1908'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Title', max_length=60)),
                ('image', models.ImageField(upload_to='images/slides/', blank=True)),
                ('sequence_number', models.IntegerField(default=0, help_text='Sequence number of slide in slide show')),
            ],
            options={
                'ordering': ['sequence_number', 'pk'],
            },
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('name', models.CharField(max_length=60, verbose_name='name')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AddField(
            model_name='slide',
            name='slider',
            field=models.ForeignKey(related_name='slides', to='plugins.Slider'),
        ),
    ]

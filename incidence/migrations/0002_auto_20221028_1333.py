# Generated by Django 3.2.9 on 2022-10-28 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0001_initial'),
        ('incidence', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncidenceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='incidence',
            name='title',
        ),
        migrations.AddField(
            model_name='incidence',
            name='embarque',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='forms.embarque'),
        ),
        migrations.AddField(
            model_name='incidence',
            name='origen',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='incidence',
            name='incidence_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='incidence.incidencetype'),
        ),
    ]

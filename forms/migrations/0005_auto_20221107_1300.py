# Generated by Django 3.2.9 on 2022-11-07 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0004_auto_20221107_0612'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactoClave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=150)),
            ],
        ),
        migrations.AlterField(
            model_name='embarque',
            name='autorizado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='forms.contactoclave'),
        ),
    ]

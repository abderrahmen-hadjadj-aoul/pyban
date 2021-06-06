# Generated by Django 3.1.2 on 2021-06-06 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_auto_20210606_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='board',
        ),
        migrations.AddField(
            model_name='ticket',
            name='column',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tickets.column'),
            preserve_default=False,
        ),
    ]

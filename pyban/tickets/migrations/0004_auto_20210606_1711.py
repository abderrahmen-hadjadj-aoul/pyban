# Generated by Django 3.1.2 on 2021-06-06 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_column'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='tickets.board'),
        ),
    ]

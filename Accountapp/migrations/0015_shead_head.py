# Generated by Django 4.2.6 on 2023-12-22 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accountapp', '0014_alter_accountingentry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='shead',
            name='head',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Accountapp.head'),
            preserve_default=False,
        ),
    ]
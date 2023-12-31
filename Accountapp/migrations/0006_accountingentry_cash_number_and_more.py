# Generated by Django 4.2.6 on 2023-12-14 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accountapp', '0005_alter_accountingentry_charge_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountingentry',
            name='cash_number',
            field=models.CharField(blank=True, default=0, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='accountingentry',
            name='cheque_number',
            field=models.CharField(blank=True, default=0, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='accountingentry',
            name='instrument',
            field=models.CharField(blank=True, choices=[('cash', 'Cash'), ('cheque', 'Cheque'), ('online', 'Online Transfer')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='accountingentry',
            name='online_number',
            field=models.CharField(blank=True, default=0, max_length=20, null=True),
        ),
    ]

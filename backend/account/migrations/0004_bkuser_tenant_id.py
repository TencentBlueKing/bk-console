# Generated by Django 4.2.16 on 2025-01-10 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_bkuser_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='bkuser',
            name='tenant_id',
            field=models.CharField(blank=True, help_text='用户所属的租户 ID', max_length=32, null=True, verbose_name='租户 ID'),
        ),
    ]
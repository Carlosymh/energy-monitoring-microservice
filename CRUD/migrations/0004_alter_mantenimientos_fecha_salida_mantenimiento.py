# Generated by Django 5.0 on 2023-12-09 05:21

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRUD', '0003_alter_mantenimientos_fecha_salida_mantenimiento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mantenimientos',
            name='fecha_salida_mantenimiento',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]

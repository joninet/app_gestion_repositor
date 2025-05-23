# Generated by Django 5.1.7 on 2025-04-27 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0007_producto_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='devolucion',
            name='motivo',
            field=models.TextField(blank=True, help_text='Motivo de la devolución', null=True),
        ),
        migrations.AddField(
            model_name='devolucion',
            name='volver_al_stock',
            field=models.BooleanField(default=True, help_text='Indica si el producto devuelto debe volver al stock'),
        ),
    ]

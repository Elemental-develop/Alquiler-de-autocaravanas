# Generated by Django 4.1 on 2023-12-04 10:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cesta', '0018_alter_pedido_secreto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='secreto',
            field=models.CharField(default=uuid.UUID('bf8e9f0e-ee4a-4084-9f81-4ba0d22761b7'), max_length=255),
        ),
    ]

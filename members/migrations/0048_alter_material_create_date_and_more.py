# Generated by Django 4.2 on 2023-06-16 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0047_material_create_date_material_updated_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='create_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='material',
            name='updated_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]

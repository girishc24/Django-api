# Generated by Django 4.2 on 2023-06-12 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0041_remove_material_create_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialpurchase',
            name='create_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='materialpurchase',
            name='updated_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='materialpurchaseitem',
            name='create_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='materialpurchaseitem',
            name='updated_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]

# Generated by Django 4.2 on 2023-06-12 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0040_alter_materialpurchase_project_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='create_date',
        ),
        migrations.RemoveField(
            model_name='material',
            name='updated_date',
        ),
        migrations.AddField(
            model_name='materialpurchase',
            name='create_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='materialpurchase',
            name='updated_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='materialpurchaseitem',
            name='create_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='materialpurchaseitem',
            name='updated_date',
            field=models.DateField(auto_now=True),
        ),
    ]

# Generated by Django 4.2 on 2023-05-23 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='delete_status',
            field=models.CharField(default=0, max_length=2),
        ),
    ]
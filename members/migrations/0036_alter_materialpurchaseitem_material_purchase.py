# Generated by Django 4.2 on 2023-06-12 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0035_materialpurchase_materialpurchaseitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialpurchaseitem',
            name='material_purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='members.materialpurchase'),
        ),
    ]

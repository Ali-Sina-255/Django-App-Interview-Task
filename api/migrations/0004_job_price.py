# Generated by Django 5.1 on 2024-08-28 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_command"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="price",
            field=models.DecimalField(decimal_places=2, default=200.0, max_digits=10),
            preserve_default=False,
        ),
    ]

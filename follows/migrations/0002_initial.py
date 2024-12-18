# Generated by Django 5.1.2 on 2024-10-20 01:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("follows", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="follow",
            name="follower",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="follower",
                to="users.customuser",
            ),
        ),
        migrations.AddField(
            model_name="follow",
            name="following",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="following",
                to="users.customuser",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="follow",
            unique_together={("follower", "following")},
        ),
    ]

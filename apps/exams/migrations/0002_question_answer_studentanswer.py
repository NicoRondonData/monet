# Generated by Django 4.1.7 on 2023-03-07 15:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("exams", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=255)),
                (
                    "exam",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        to="exams.exam",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Answer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=255)),
                ("is_correct", models.BooleanField(default=False)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answers",
                        to="exams.question",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StudentAnswer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "answer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="exams.answer"
                    ),
                ),
                (
                    "exam",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="exams.exam"
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="exams.question"
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("student", "question")},
            },
        ),
    ]

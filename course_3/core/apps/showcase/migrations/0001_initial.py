# Generated by Django 5.1.2 on 2024-11-02 16:58
import django.core.validators
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Breed",
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
                    "name",
                    models.CharField(max_length=50, verbose_name="Наименование породы"),
                ),
                (
                    "size",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Супер маленькая"),
                            (2, "Маленькая"),
                            (3, "Средняя"),
                            (4, "Большая"),
                        ],
                        verbose_name="Размер",
                    ),
                ),
                (
                    "friendliness",
                    models.PositiveSmallIntegerField(
                        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                        verbose_name="Доброта",
                    ),
                ),
                (
                    "trainability",
                    models.PositiveSmallIntegerField(
                        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                        verbose_name="Удобство тренировки",
                    ),
                ),
                (
                    "shedding_amount",
                    models.PositiveSmallIntegerField(
                        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                        verbose_name="Линяние",
                    ),
                ),
                (
                    "exercise_needs",
                    models.PositiveSmallIntegerField(
                        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                        verbose_name="Энергичность",
                    ),
                ),
            ],
            options={
                "verbose_name": "Порода собаки",
                "verbose_name_plural": "Породы собак",
            },
        ),
        migrations.CreateModel(
            name="Dog",
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
                ("name", models.CharField(max_length=50, verbose_name="Имя")),
                (
                    "color",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Черная"),
                            (2, "Белая"),
                            (3, "Рыжая"),
                            (4, "Многоцветная"),
                        ],
                        verbose_name="Цвет",
                    ),
                ),
                (
                    "age",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(24),
                            django.core.validators.MinValueValidator(1),
                        ],
                        verbose_name="Возраст",
                    ),
                ),
                (
                    "gender",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "М"), (2, "Ж")], verbose_name="Пол"
                    ),
                ),
                (
                    "favorite_food",
                    models.CharField(max_length=50, verbose_name="Любимая еда"),
                ),
                (
                    "favorite_toy",
                    models.CharField(max_length=50, verbose_name="Любимая игрушка"),
                ),
                (
                    "breed",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dogs",
                        to="showcase.breed",
                        verbose_name="Порода",
                    ),
                ),
            ],
            options={
                "verbose_name": "Собака",
                "verbose_name_plural": "Собаки",
            },
        ),
    ]

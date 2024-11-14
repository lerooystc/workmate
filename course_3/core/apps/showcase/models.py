from apps.showcase.choices import BREED_SIZE_CHOICES
from apps.showcase.choices import DOG_COLOR_CHOICES
from apps.showcase.choices import GENDER_CHOICES
from apps.showcase.choices import ONE_TO_FIVE_CHOICES
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models


class Breed(models.Model):
    """Породы собак"""

    name = models.CharField(verbose_name="Наименование породы", max_length=50)
    size = models.PositiveSmallIntegerField(
        verbose_name="Размер", choices=BREED_SIZE_CHOICES
    )
    friendliness = models.PositiveSmallIntegerField(
        verbose_name="Доброта", choices=ONE_TO_FIVE_CHOICES
    )
    trainability = models.PositiveSmallIntegerField(
        verbose_name="Удобство тренировки", choices=ONE_TO_FIVE_CHOICES
    )
    shedding_amount = models.PositiveSmallIntegerField(
        verbose_name="Линяние", choices=ONE_TO_FIVE_CHOICES
    )
    exercise_needs = models.PositiveSmallIntegerField(
        verbose_name="Энергичность", choices=ONE_TO_FIVE_CHOICES
    )

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "Порода собаки"
        verbose_name_plural = "Породы собак"


class Dog(models.Model):
    """Собаки"""

    name = models.CharField(verbose_name="Имя", max_length=50)
    color = models.PositiveSmallIntegerField(
        verbose_name="Цвет", choices=DOG_COLOR_CHOICES
    )
    age = models.PositiveSmallIntegerField(
        verbose_name="Возраст",
        validators=[MaxValueValidator(24), MinValueValidator(1)],
    )
    gender = models.PositiveSmallIntegerField(
        verbose_name="Пол", choices=GENDER_CHOICES
    )
    breed = models.ForeignKey(
        Breed, on_delete=models.CASCADE, verbose_name="Порода", related_name="dogs"
    )
    favorite_food = models.CharField(verbose_name="Любимая еда", max_length=50)
    favorite_toy = models.CharField(verbose_name="Любимая игрушка", max_length=50)

    def __str__(self) -> str:
        return f"{self.name}, {self.age} лет"

    class Meta:
        verbose_name = "Собака"
        verbose_name_plural = "Собаки"

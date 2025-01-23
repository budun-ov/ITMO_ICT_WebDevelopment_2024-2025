from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class User(AbstractUser):
    passport_number = models.CharField(max_length=20, unique=True, verbose_name="Номер паспорта")
    address = models.CharField(max_length=255, verbose_name="Домашний адрес")
    nationality = models.CharField(max_length=50, verbose_name="Национальность")

    def __str__(self):
        return f"{self.username} - {self.passport_number}"

# Модель для таблицы "Автовладелец"
class Owner(models.Model):
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    birth_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата рождения")

    class Meta:
        verbose_name = "Автовладелец"
        verbose_name_plural = "Автовладельцы"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

# Модель для таблицы "Автомобиль"
class Car(models.Model):
    license_plate = models.CharField(max_length=15, unique=True, verbose_name="Гос. номер")
    brand = models.CharField(max_length=20, verbose_name="Марка")
    model = models.CharField(max_length=20, verbose_name="Модель")
    color = models.CharField(max_length=30, null=True, blank=True, verbose_name="Цвет")

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"

# Модель для таблицы "Владение"
class Ownership(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="ownerships"
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        verbose_name="Автомобиль",
        related_name="ownerships"
    )
    start_date = models.DateTimeField(verbose_name="Дата начала")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата окончания")

    class Meta:
        verbose_name = "Владение"
        verbose_name_plural = "Владения"

    def __str__(self):
        return f"{self.owner} - {self.car}"

# Модель для таблицы "Водительское_удостоверение"
class DriverLicense(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="driver_license"
    )
    license_number = models.CharField(max_length=10, unique=True, verbose_name="Номер удостоверения")
    license_type = models.CharField(max_length=10, verbose_name="Тип")
    issue_date = models.DateTimeField(verbose_name="Дата выдачи")

    class Meta:
        verbose_name = "Водительское удостоверение"
        verbose_name_plural = "Водительские удостоверения"

    def __str__(self):
        return f"{self.license_number} ({self.owner})"

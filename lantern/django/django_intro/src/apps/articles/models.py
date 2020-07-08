from django.conf import settings
from django.db import models


# Create your models here.

class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=85)
    country = models.ForeignKey('Country', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'City'


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=56)

    class Meta:
        managed = False
        db_table = 'Country'


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthday = models.DateField(blank=True, null=True)
    position = models.CharField(max_length=15)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Employee'


class Food(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    ingredients = models.TextField(blank=True, null=True)
    vegan = models.BooleanField(blank=True, null=True)
    spicy = models.BooleanField(blank=True, null=True)
    season = models.ForeignKey('Season', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Food'


class Menu(models.Model):
    season = models.ForeignKey('Season', models.DO_NOTHING, blank=True, null=True)
    food = models.ForeignKey('Food', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Menu'


class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(unique=True, max_length=50)
    country_id = models.ForeignKey('Country', models.DO_NOTHING, blank=True, null=True)
    city_id = models.ForeignKey('City', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Restaurant'


class Season(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'Season'

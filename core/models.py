from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Condition(models.Model):
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.state

class Location(models.Model):
    city = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return f"{self.city} - {self.address}"

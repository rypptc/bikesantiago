from django.db import models
from django.contrib.postgres.fields import ArrayField

class Station(models.Model):

    PAYMENT_CHOICES = (
        ('none', 'None'),
        ('transitcard', 'Transit Card'),
        ('creditcard', 'Credit Card'),
        ('phone', 'Phone'),
    )

    station_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    post_code = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    free_bikes = models.IntegerField()
    has_ebikes = models.BooleanField()
    normal_bikes = models.IntegerField()
    slots = models.IntegerField()
    empty_slots = models.IntegerField()
    payment = ArrayField(models.CharField(max_length=20, choices=PAYMENT_CHOICES), default=list)
    payment_terminal = models.BooleanField()
    renting = models.BooleanField()
    returning = models.BooleanField()
    last_updated = models.DateTimeField()
    uid = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.name} ({self.station_id})"

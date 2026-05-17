from django.db import models
from django.contrib.auth.models import User # Ini untuk link dengan fungsi Login/RBAC

class Concert(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    available_tickets = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    # Foreign key ni syarat wajib untuk database yang betul. Dia link tiket dengan user dan konsert.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.concert.name}"
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Patient(models.Model):
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    
    user = models.OneToOneField(User, related_name = "patient", on_delete=models.PROTECT)
    gender = models.CharField(max_length = 1, choices=GENDER_CHOICES)

    def __str__(self):
        return (self.user.first_name + " " + self.user.last_name)

    def has_active_dx(self):
        if self.dx_requests.filter(active=True):
            return True
        return False

    def actual_weight(self):
        try:
            return self.dx_requests.all().order_by('date').reverse()[0].weight
        except Exception as e:
            return None

    def actual_height(self):
        try:
            return self.dx_requests.all().order_by('date').reverse()[0].height
        except Exception as e:
            return None

class DxRequest(models.Model):

    patient = models.ForeignKey(Patient, related_name = "dx_requests", on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True) 
    weight = models.FloatField(validators=[MinValueValidator(3), MaxValueValidator(200)])#kg
    height = models.IntegerField(validators=[MinValueValidator(20), MaxValueValidator(250)])#cm
    active = models.BooleanField(default=True)


class Diagnostic(models.Model):
    patient = models.OneToOneField(DxRequest, related_name = "diagnostics", on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)
    recomendations = models.TextField()

# Create your models here.

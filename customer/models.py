from statistics import mode
from django.db import models

# Customer model or table
class Customer(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    region = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

    

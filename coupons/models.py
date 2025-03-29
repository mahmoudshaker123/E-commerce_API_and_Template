from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Coupon(models.Model):
    code = models.CharField(max_length=8, unique=True)
    valid_from = models.DateTimeField() 
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)] , help_text="Discount percentage (1-100)"
    )
    active = models.BooleanField()

    def __str__(self):
        return self.code
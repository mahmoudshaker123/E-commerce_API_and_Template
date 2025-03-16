from django.db import models
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


    def __str__(self):
        return self.name
    

class Product(models.Model):
    class Status(models.TextChoices):
        AVAILABLE ='AV', 'available'
        NOT_AVAILABLE ='DR' ,'draft'

    name = models.CharField(max_length=250)
    slug= models.SlugField(unique=True)
    image = models.ImageField(upload_to='products/images')
    description = models.TextField(max_length=1500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id','slug']),
            models.Index(fields=['name']),
            models.Index(fields=['price']),
            models.Index(fields=['-created_at']),
        ]



from django.db import models

class Product(models.Model):
    full_name = models.CharField(max_length=255, null=False, blank=False)
    product_code = models.CharField(max_length=255, null=False, blank=False)
    main_price = models.FloatField()
    red_price = models.FloatField()
    color = models.CharField(max_length=100, null=True, blank=True)
    memory = models.CharField(max_length=50, null=True, blank=True)
    producer = models.CharField(max_length=100, null=True, blank=True)
    screen_diagonal = models.CharField(max_length=50, null=True, blank=True)
    display_resolution = models.CharField(max_length=50, null=True, blank=True)
    image = models.TextField()
    review_count = models.IntegerField(default=0)
    characteristics = models.JSONField(default=dict)


    def _str__(self) -> str:
        return f"{self.full_name} (code: {self.product_code})"

from django.db import models


class MAGICIANS(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)


class Magician_hire_cost(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=18, decimal_places=2)


class Total_price(models.Model):
    id = models.AutoField(primary_key=True)
    subtotal = models.DecimalField(max_digits=18, decimal_places=2)
    hire_cost = models.ForeignKey(
        Magician_hire_cost, on_delete=models.CASCADE, null=True)
    magician = models.ManyToManyField(MAGICIANS)
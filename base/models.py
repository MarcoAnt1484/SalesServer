from django.db import models

# Create your models here.

# class Room(models.Model):
# 	# host = 
# 	# topic = 

# 	name = id
# 	# descritpionn = models.TextField(null=True, blank=True)

# 	ProductID = models.IntegerField(null=False, blank=False)
# 	SaleTime = models.DateTimeField(auto_now_add=True)
# 	Amount = models.IntegerField(null=False, blank=False)

# 	def __str__(self):
# 		return "Name"


class Sales(models.Model):
	ProductID = models.IntegerField(null=False, blank=False)
	SaleDate = models.DateTimeField(null=False, blank=False)
	Amount = models.IntegerField(null=False, blank=False)

	def __str__(self):
		return str(self.SaleDate)

class Inventory(models.Model):
	Name = models.CharField(max_length=200, null=False, blank=False)
	Description = models.TextField(null=True, blank=True)
	ProductID = models.IntegerField(null=False, blank=False)
	Amount = models.IntegerField(null=False, blank=False)
	Price = models.IntegerField(null=False, blank=False)

	def __str__(self):
		return self.ProductID
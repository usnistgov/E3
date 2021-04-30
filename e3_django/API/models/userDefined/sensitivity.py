from django.db import models

class Sensitivity(models.Model):
	"""
	Purpose: Initializes a Sensitivity object
	"""
	globalVarBool = models.BooleanField(null= True)
	altID 		  = models.IntegerField(null=True, unique=True)
	bcnID 		  = models.CharField(null=True, max_length=30, default='')
	varName  	  = models.CharField(null=True, max_length=30, default='')
	diffType 	  = models.CharField(null=True, max_length=30, default='')
	diffVal 	  = models.DecimalField(null=True, max_digits=7, decimal_places=2)
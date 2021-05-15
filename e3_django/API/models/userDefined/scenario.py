from django.db import models

class Scenario(models.Model):
	"""
	Purpose: Initializes a Scenario object. Unknown
	"""
	objectVariables = models.JSONField(null=True)
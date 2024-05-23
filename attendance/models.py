from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True, null=False)
    lastname = models.CharField(max_length=255, null=False)
    firstname = models.CharField(max_length=255, null=False)
    middleinitial = models.CharField(max_length=255, null=True)
    ranks = models.CharField(max_length=50, null=False)
    assignment_level = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    password = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.employee_id

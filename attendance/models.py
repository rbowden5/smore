from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

import datetime
now = timezone.now()

# Create your models here.
class Child(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    attendance_status = models.SmallIntegerField(default=0)
    # adult = models.ManyToManyField(Adult, related_name="children")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Adult(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    adult_phone_number = models.CharField(max_length=12, default=00000000000)
    children = models.ManyToManyField(Child, related_name="adults")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Staff(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Attendance_History(models.Model):
    child = models.ForeignKey(Child, on_delete=models.PROTECT, related_name="child")
    adult = models.ForeignKey(Adult, on_delete=models.PROTECT, related_name="adult")
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, related_name="staff")
    status = models.SmallIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.child}: {self.status}"

class Group(models.Model):
    name = models.CharField(max_length=64)
    camper = models.ForeignKey(Child, on_delete=models.PROTECT, related_name="group")
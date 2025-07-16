from django.db import models
from django.contrib.auth.models import AbstractUser

### Department Table---------------------------------------------------------------------------------------------------------

class Department(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name
    
## Employee Table --------------------------------------------------------------------------------------------------------------

class Employee(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)
    join_date =models.DateField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    reporting_manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    

 



## Leave Table=---------------------------------------------------------------------------------------------------------------

class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Approve', 'Approve'),
        ('Rejected','Rejected')
    ], default='Pending')

    def __str__(self):
        return f"{self.employee.name} - {self.status}"

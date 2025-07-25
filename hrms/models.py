from django.db import models
from django.contrib.auth.models import AbstractUser

# Department Table-----------------------------------------


class Department(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


# Employee Table ------------------------------------------
class Employee(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)
    join_date = models.DateField(null=True, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True)
    reporting_manager = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)
    
    is_admin = models.BooleanField(default=False)


# Managers Table ------------------------------------------
class Manager(models.Model):
    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name="manager_profile")

    def __str__(self):
        return f"Manager: {self.employee.get_full_name()}"


# Leave Table=---------------------------------------------
class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Approve', 'Approve'),
        ('Rejected', 'Rejected')
    ], default='Pending')

    def __str__(self):
        return f"{self.employee.name} - {self.status}"


# Employee-Reimbursement Table----------------------------------
class ReimbursementClaim(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    claim_type = models.CharField(max_length=100)
    submitted_at = models.DateField()
    approve_at = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=[
        ('Pending', 'Pending'), 
        ('Approve', 'Approve'), 
        ('Rejected', 'Rejected')
    ], default='Pending')


class ReimbursementFile(models.Model):
    claim = models.ForeignKey(ReimbursementClaim, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='reimbursements')
    uploaded_at = models.DateTimeField(auto_now_add=True)


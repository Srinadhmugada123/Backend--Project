from django.contrib import admin
from .models import Department, Employee, Leave, ReimbursementFile, ReimbursementClaim


admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Leave)
admin.site.register(ReimbursementClaim)
admin.site.register(ReimbursementFile)

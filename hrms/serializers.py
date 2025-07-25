from rest_framework import serializers
from .models import Department, Employee, Leave, Manager, ReimbursementClaim, ReimbursementFile
from django.contrib.auth.hashers import make_password
# from django.contrib.auth import get_user_model
# User = get_user_model()

# --------------------------Department Seriliazer--------------------


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


# -------------------------------Employee Serializer-------------------------
class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_department_name(self, obj):
        return obj.department.name if obj.department else None

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(
                validated_data['password'])
        return super().create(validated_data)


# --------------------------------------Leave Serializer -----------------
class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'


# ------------------------Manager Serializer ----------------
class ManagerSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()

    class Meta:
        model = Manager
        fields = ['id', 'employee', 'employee_name', 'department_name']

    def get_employee_name(self, obj):
        return obj.employee.get_full_name()

    def get_department_name(self, obj):
        return obj.employee.department.name if obj.employee.department else None


# --------------------Employee Reimbursement --------------------------
class ReimbursementFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReimbursementFile
        fields = ['id', 'file', 'uploaded_at']


class ReimbursementClaimSerializer(serializers.ModelSerializer):
    files = ReimbursementFileSerializer(many=True, read_only=True)

    class Meta:
        model = ReimbursementClaim
        fields = ['id', 'employee', 'claim_type', 'amount', 'status', 'remarks', 'submitted_at', 'approve_at', 'files']
from rest_framework import serializers
from .models import Department, Employee, Leave
from django.contrib.auth.hashers import make_password
# from django.contrib.auth import get_user_model
# User = get_user_model()

#--------------------------Department Seriliazer--------------------
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id','name']


#-------------------------------Employee Serializer-------------------------
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
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
#--------------------------------------Leave Serializer ------------------------------
class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'







from rest_framework import serializers
from .models import Department, Employee, Leave
from django.contrib.auth.hashers import make_password
# from django.contrib.auth import get_user_model
# User = get_user_model()

#--------------------------Department Seriliazer--------------------
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


#-------------------------------Employee Serializer-------------------------
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password']) 
        return super().create(validated_data)
#--------------------------------------Leave Serializer ------------------------------
class LeaveSerializer(serializers.ModelSerializer):
    employee = serializers.StringRelatedField()
    class Meta:
        model = Leave
        fields = '__all__'







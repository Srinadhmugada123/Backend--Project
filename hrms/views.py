from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Department, Employee, Leave
from .serializers import *

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from django.utils.timezone import now
#-----------------------------------------Department Views ------------------------------------------------------------------------------------------------

class DepartmentAPIView(APIView):
    
    def get(self,request):
        data = Department.objects.all()
        serializer = DepartmentSerializer(data, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class DepartmentDetailAPIView(APIView):
    
    def get_object(self, pk):
        return Department.objects.get(pk=pk)
        
    def get(self, request, pk):
        serializer = DepartmentSerializer(self.get_object(pk))
        return Response(serializer.data)
    
    def put(self, request, pk):
        instance = self.get_object(pk)
        serializer = DepartmentSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=204)


#-----------------------------------------------------------------------------------Employee Views ---------------------------------------------------
class EmployeeAPIView(APIView):
    
    def get(self, request):
        data = Employee.objects.all()
        # print(data.first().email)
        serializer = EmployeeSerializer(data, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class EmployeeDetailAPIView(APIView):
   
    def get_object(self,pk):
        return Employee.objects.get(pk=pk)
    
    def get(self, request, pk):
        serializer = EmployeeSerializer(self.get_object(pk))
        return Response(serializer.data)
    
    def put(self,request,pk):
        emp = Employee.objects.get(pk=pk)
        serializer = EmployeeSerializer(emp,data=request.data,partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request,pk):
        self.get_object(pk).delete()
        return Response(status=204)
    
#----------------------------------------------------------------------Leave views ------------------------------------------------------------


class LeaveAPIVIew(APIView):
    
    def get(self,request):
        data = Leave.objects.all()
        serializer = LeaveSerializer(data, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = LeaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=401)
    

class LeaveDetailAPIVIew(APIView):
    
    def get_object(self, pk):
        return Leave.objects.get(pk=pk)
    
    def get(self, request, pk):
        serializer = LeaveSerializer(self.get_object(pk))
        return Response(serializer.data)
    
    def put(self,request,pk):
        leave = Leave.objects.get(pk-pk)
        serializer = LeaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request,pk):
        self.get_object(pk).delete()
        return Response(status=204)
    


#----------------------------------------------------------------Team Member -----------------------------------------------------

class TeamMembersUnderManager(APIView):
    def get(self, request, manager_id):
        team_members = Employee.objects.filter(reporting_manager_id = manager_id)
        serializer = EmployeeSerializer(team_members, many=True)
        return Response(serializer.data)
    

#--------------------------------------Leave pending/ approve or reject  by manager  --------------------------------------

class PendingLeavesForManager(APIView):
    def get(self, request, manager_id):
        leaves = Leave.objects.filter(
            employee__reporting_manager__id=manager_id,
            status="Pending"
        )
        serializer = LeaveSerializer(leaves, many=True)
        return Response(serializer.data)


class ManagerLeaveStatusUpdate(APIView):
    def put(self, request, leave_id):
        manager = request.user 
        leave = get_object_or_404(Leave, id=leave_id)

        print("Manager ID (Logged in):", manager.id)
        print("Leave Applied By:", leave.employee.id)
        print("Employee's Reporting Manager ID:", leave.employee.reporting_manager.id if leave.employee.reporting_manager else None)
        
        if leave.employee.reporting_manager != manager:
            return Response({"error":"You are not authorized to approve/reject this leave"}, status=403)
        
        new_status = request.data.get("status")

        if new_status not in["Approve","Rejected"]:
            return Response({"error":"Invalid status. choose 'Approve' od 'Rejected'"},status=400)
        
        leave.status = new_status
        leave.save()
        return Response({"message": f"Leave {new_status.lower()}d successfully"}, status=200)









class ApproveLeave(APIView):
    def put(self, request, leave_id):
        leave = get_object_or_404(Leave, id=leave_id)
        leave.status = "Approve"
        leave.save()
        return Response({"message": "Leave approved"})

class RejectLeave(APIView):
    def put(self, request, leave_id):
        leave = get_object_or_404(Leave, id=leave_id)
        leave.status = "Rejected"
        leave.save()
        return Response({"message": "Leave rejected"})





# ----------------------------Emplooyee Resgister & Login ------------------------------------------------------

class EmployeeRegisterView(APIView):
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=201)
        else:
            print("DEBUG ERRORS:", serializer.errors) 
            return Response(serializer.errors, status=400)




class EmployeeLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password required"}, status=400)

        try:
            emp = Employee.objects.get(email=email)
        except Employee.DoesNotExist:
            return Response({"error": "Email not found"}, status=400)

        if not check_password(password, emp.password):
            return Response({"error": "Invalid password"}, status=400)
        
        emp.last_login=now()
        emp.save()
        token, _ = Token.objects.get_or_create(user=emp)
        return Response({
            "token": token.key,
            "username": emp.username,
            "email": emp.email
        }, status=200)  
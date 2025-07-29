from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Department, Employee, Leave, Manager, ReimbursementClaim, ReimbursementFile
from .serializers import (EmployeeSerializer,
                          DepartmentSerializer,
                          LeaveSerializer,
                          ManagerSerializer,
                          ReimbursementClaimSerializer,
                          )
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from django.utils.timezone import now


# -----------------Admin----------------------
class AdminAPIVIew(APIView):
    def get(self, request):
        admins = Employee.objects.filter(is_admin=True)
        if not admins.exists():
            return Response(
                {"message": "No Admins found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = EmployeeSerializer(admins, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK
        )


# -----------------Department Views -----------
class DepartmentAPIView(APIView):
    def get(self, request):
        data = Department.objects.all()
        if not data.exists():
            return Response(
                {"message": "No Department found."},
                status=status.HTTP_200_OK
            )
        serializer = DepartmentSerializer(data, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK
                        )

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(
            {"error":
             "Department Creation failed.please check the deatils"},
            status=status.HTTP_400_BAD_REQUEST
        )


class DepartmentDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return None

    # def get(self, request, pk):
    #     department = self.get_object(pk)
    #     if not department:
    #         return Response(
    #             {"message":
    #              f"Department with ID {pk} not found"},
    #             status=status.HTTP_404_NOT_FOUND
    #         )
    #     serializer = DepartmentSerializer(self.get_object(pk))
    #     return Response(serializer.data,
    #                     status=status.HTTP_200_OK
    #                     )

    def get(self, request, pk):
        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response(
                {"message": f"Department with ID {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = DepartmentSerializer(department)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        department = self.get_object(pk)
        if not department:
            return Response(
                {"error": f"Department with ID {pk} not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        print("PUT request data:", request.data)
        print("Target department:", department)
        serializer = DepartmentSerializer(
            instance=department,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            {"error":
             "please fill the correct department details"},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        department = self.get_object(pk)
        if department is None:
            return Response(
                {
                    "error": f"Department with ID {pk} not founf"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        department.delete()
        return Response(
            {
                "success": "Department deleted successfull"
            },
            status=status.HTTP_204_NO_CONTENT
        )


# ---------------------Employe views---------------
class EmployeeAPIView(APIView):
    def get(self, request):
        data = Employee.objects.all()
        # print(data.first().email)
        if not data.exists():
            return Response(
                {"Message": "No Employee found"},
                status=status.HTTP_200_OK
            )
        serializer = EmployeeSerializer(data, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK
                        )

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(
            {"error":
             "employee creation failed. please check the details"},
            status=status.HTTP_400_BAD_REQUEST
        )


class EmployeeDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return None

    def get(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response(
                {"message": f"Employee with ID {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        emp = Employee.objects.get(pk=pk)
        serializer = EmployeeSerializer(
            instance=emp,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK
                            )
        return Response(
            {"error":
             "update failed. please fill the correct employee details"},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        employee = self.get_object(pk)
        if employee is None:
            return Response(
                {"error": f"Employee with ID {pk} not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                "Successfully employee Deleted"
            },
            status=status.HTTP_204_NO_CONTENT
        )


# -----------------------------Leave views --------------------
class LeaveAPIVIew(APIView):
    def get(self, request):
        data = Leave.objects.all()
        if not data.exists():
            return Response(
                {"message": "No Leaves found."},
                status=status.HTTP_200_OK
            )
        serializer = LeaveSerializer(data, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK
                        )

    def post(self, request):
        serializer = LeaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": "employee applied leave",
                 "data": serializer.data
                 }, status=status.HTTP_200_OK
            )
        return Response(
            {"error": "Leave request creation failed."},
            status=status.HTTP_400_BAD_REQUEST
        )


class LeaveDetailAPIVIew(APIView):
    def get_object(self, pk):
        try:
            return Leave.objects.get(pk=pk)
        except Leave.DoesNotExist:
            return None

    # def get(self, request, pk):
    #     leave = self.get_object(pk)
    #     if not leave:
    #         return Response(
    #             {"message": f"leave with ID {pk} not found."},
    #             status=status.HTTP_404_NOT_FOUND
    #         )
    #     serializer = LeaveSerializer(self.get_object(pk))
    #     return Response(serializer.data,
    #                     status=status.HTTP_200_OK
    #                     )

    def get(self, request, pk):
        try:
            leave = Leave.objects.get(pk=pk)
        except Leave.DoesNotExist:
            return Response(
                {"message": f"leave with ID {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LeaveSerializer(leave)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        leave = Leave.objects.get(pk=pk)
        serializer = LeaveSerializer(
            instance=leave,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            {"error":
             "Update failed. Please check the provided leave details."},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        leave = self.get_object(pk)
        if leave is None:
            return Response(
                {"error": f"Leave with ID {pk} not found"},
                status=status.HTTP_400_BAD_REQUEST)
        leave.delete()
        return Response(
            {"Success": "Leave Deleted Sucessfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# ----------------TeamMembers --------------------------
class TeamMembersUnderManager(APIView):
    def get(self, request, manager_id):
        team_members = Employee.objects.filter(
            reporting_manager_id=manager_id
        )
        if not team_members.exists():
            return Response(
                {
                    "message": "No Team_members found"
                }, status=status.HTTP_200_OK
            )
        serializer = EmployeeSerializer(team_members, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK
                        )


# ------------Managers ---------------------
class ManagerAPIView(APIView):
    def get(self, request):
        managers = Manager.objects.all()
        if not managers.exists():
            return Response(
                {"message": "No Managers found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ManagerSerializer(managers, many=True)
        return Response(
            {"message": "Managers fetched successfully", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = ManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Manager created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "error": "Update failed. Please correct the error below",
                "details": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


# ---------------Leave views -------------
class PendingLeavesForManager(APIView):
    def get(self, request, manager_id):
        leaves = Leave.objects.filter(
            employee__reporting_manager__id=manager_id,
            status="Pending"
        )

        if not leaves.exists():
            return Response(
                {"message": "No pending leaves"},
                status=status.HTTP_200_OK
            )

        serializer = LeaveSerializer(leaves, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManagerLeaveStatusUpdate(APIView):
    def put(self, request, leave_id):
        manager = request.user
        leave = get_object_or_404(Leave, id=leave_id)
        if leave.employee.reporting_manager != manager:
            return Response(
                {
                    "error": "Not authorized to approve/reject this leave"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        new_status = request.data.get("status")
        if new_status not in ["Approve", "Rejected"]:
            return Response(
                {
                    "error": "Invalid status. choose 'Approve' od 'Rejected'"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        leave.status = new_status
        leave.save()
        return Response(
            {
                "message": f"Leave {new_status.lower()} "
            },
            status=status.HTTP_200_OK
        )


# ----------------------------Emplooyee Resgister & Login -----
class EmployeeRegisterView(APIView):
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "Message": "Registration successfull"
            }, status=status.HTTP_201_CREATED)
        else:
            print("DEBUG ERRORS:", serializer.errors)
            return Response(
                {
                    "error": "Registration failed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class EmployeeLoginView(APIView):
    def post(self, request):
        email_or_username = request.data.get("email") or request.data.get("username")
        password = request.data.get("password")

        if not email_or_username or not password:
            return Response(
                {
                    "error": "Email/username and password required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if '@' in email_or_username:
                emp = Employee.objects.get(email=email_or_username)
            else:
                emp = Employee.objects.get(username=email_or_username)
        except Employee.DoesNotExist:
            return Response(
                {
                    "error": "Email not found"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not check_password(password, emp.password):
            return Response(
                {
                    "error": "Invalid password"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        emp.last_login = now()
        emp.save()
        token, _ = Token.objects.get_or_create(user=emp)
        return Response({
            "token": token.key,
            "username": emp.username,
            "email": emp.email,
            "Message": "Login successfull"
        }, status=status.HTTP_200_OK)


# ---------------Reimbursement views -------------
from rest_framework.parsers import MultiPartParser, FormParser
class ReimbursementClaimAPIView(APIView):
    def get(self, request):
        try:
            data = ReimbursementClaim.objects.all()
            if not data.exists():
                return Response({
                    "status": False,
                    "message": "No Reimbursement Found",
                    "data": []
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = ReimbursementClaimSerializer(data, many=True)
            return Response({
                "status": True,
                "message": "Employee Reimbursements",
                "data": serializer.data
            }, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "status": False,
                    "message": "An error occurred",
                    "errors": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    def post(self, request):
        try:
            serializer = ReimbursementClaimSerializer(data=request.data)
            if serializer.is_valid():
                claim = serializer.save()
                files = request.FILES.getlist('files')
                for file in files:
                    ReimbursementFile.objects.create(claim=claim, file=file)

                return Response(
                    {
                        "status": True,
                        "message": "Reimbursement Created Successfully",
                        "data": ReimbursementClaimSerializer(claim).data
                    }, status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    "status": False,
                    "message": "Reimbursement creation failed",
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {
                    "status": False,
                    "message": "An error occurred",
                    "error": str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReimbursementDeatilAPIView(APIView):
    def get(self, request, pk=None):
        try:
            if pk:
                data = get_object_or_404(ReimbursementClaim, pk=pk)
                serializer = ReimbursementClaimSerializer(data)
                return Response(
                    {
                        "status": True,
                        "message": "Reimbursement retrived successfull",
                        "data": serializer.data
                    }, status=status.HTTP_200_OK
                )
            else:
                data = ReimbursementClaim.objects.all()
                serializer = ReimbursementClaimSerializer(data, many=True)
                return Response(
                    {
                        "status": True,
                        "message": "Reimbursement retrived succcessfull",
                        "data": serializer.data
                    }, status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {
                    "status": False,
                    "message": "An error occurred",
                    "errors": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request, pk):
        try:
            reimbursement = get_object_or_404(ReimbursementClaim, pk=pk)
            serializer = ReimbursementClaimSerializer(reimbursement, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                if request.FILES.getlist('files'):
                    for uploaded_file in request.FILES.getlist('files'):
                        ReimbursementFile.objects.create(
                            claim=reimbursement,
                            file=uploaded_file
                        )
                return Response(
                    {
                        "status": True,
                        "message": "Reimnursement Update successfully",
                        "data": serializer.data
                    }, status=status.HTTP_200_OK
                )
            return Response(
                {
                    "status": False,
                    "message": "Reimbursement update failed",
                    "errors": serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    "status": False,
                    "message": "An error occurred",
                    "errors": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class AdminReimbursementUpdateStatusAPIView(APIView):
    def put(self, request, pk):
        try:
            if not request.user.is_authenticated or not request.user.is_admin:
                return Response(
                    {
                        "status": False,
                        "message": "You are not authorized to perform this action"
                    }, status=status.HTTP_403_FORBIDDEN
                )
            
            claim = get_object_or_404(ReimbursementClaim, pk=pk)
            
            new_status = request.data.get("status")
            remarks = request.data.get("remarks", "")

            if new_status not in ["Approve", "Rejected"]:
                return Response(
                    {
                        "status": False,
                        "message": "Invalid status: choose 'Approve' or 'Rejected'. "
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            
            claim.status = new_status
            claim.remarks = remarks
            claim.approve_at = now()
            claim.save()

            serializer = ReimbursementClaimSerializer(claim)
            return Response(
                {
                    "status": True,
                    "message": f"Reimbursement {new_status.lower()} successfully. ",
                    "data": serializer.data
                }, status=status.HTTP_200_OK
            )
        
        except Exception as e:
            return Response(
                {
                    "status": False,
                    "message": "An error Occured",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
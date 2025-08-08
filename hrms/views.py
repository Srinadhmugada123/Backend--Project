from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Department, Employee, Leave, Manager, ReimbursementClaim
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
        """
        GET /admins/

        Retrieve a list of all admin users.

        Returns:
            Response: A JSON response with the status, message, and data of the admin users.
        """

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
        """
        GET /departments/

        Retrieve a list of all departments.

        Returns:
            Response: A JSON response containing a list of department data if any exist,
            or a message indicating no departments are found.
        """
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
        """
        POST /departments/

        Create a new department.

        Parameters:
            request (Request): The request object containing department data.

        Returns:
            Response: A JSON response with the department data if creation is
            successful, or an error message if it fails.
        """
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
        """
        Retrieve a department by its primary key.

        Args:
            pk (int): The primary key of the department to retrieve.

        Returns:
            Department: The department object if found, otherwise None.
        """

        
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
        """
        GET /departments/{id}/

        Retrieve a department by its ID.

        Parameters:
            request (Request): The request sent to the API.
            pk (int): The primary key of the department to retrieve.

        Returns:
            Response: A JSON response containing the department data if found,
            or a 404 error if the department does not exist.
        """
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
        """
        PUT /departments/{id}/

        Update a department with the given ID.

        Parameters:
            pk (int): The ID of the department to update.
            data (dict): The updated department data.

        Returns:
            Response: A JSON response containing the updated department data
            if the update is successful, or an error message if the update
            fails.
        """
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
        """
        DELETE /departments/{id}/

        Delete a department with the given ID.

        Parameters:
            pk (int): The ID of the department to delete.

        Returns:
            Response: A JSON response indicating whether the delete was successful or not.
        """
        
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
        """
        GET /employees/

        Retrieve a list of all employees.

        Returns:
            Response: A JSON response containing a list of employee data if any exist,
            or a message indicating no employees are found.
        """

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
        """
        POST /employees/

        Create a new employee.

        Parameters:
            request (Request): The request object containing employee data.

        Returns:
            Response: A JSON response with the employee data if creation is
            successful, or an error message if it fails.
        """

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
        """
        Retrieve an employee by their primary key.

        Args:
            pk (int): The primary key of the employee to retrieve.

        Returns:
            Employee: The employee object if found, otherwise None.
        """

        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        GET /employees/{id}/
        
        Retrieve a single employee by ID.
        
        Parameters:
            pk (int): The ID of the employee to retrieve.
        
        Returns:
            Response: A JSON response containing the employee data if found,
            or a 404 error if the employee does not exist.
        """
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
        """
        PUT /employees/{id}/
        
        Update an employee with the given ID.
        
        Parameters:
            pk (int): The ID of the employee to update.
            data (dict): The updated employee data.
        
        Returns:
            Response: A JSON response with the updated employee data if the update
            is successful, or an error message if the update fails.
        """
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
        """
        DELETE /employees/{id}/
        
        Delete an employee with the given ID.
        
        Parameters:
            pk (int): The ID of the employee to delete.
        
        Returns:
            Response: A JSON response indicating whether the delete was successful or not.
        """
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
        """
        GET /leaves/
        
        Retrieve all leave requests.
        
        Returns:
            Response: A JSON response containing all leave requests if found,
            or a message indicating no leave requests are found.
        """
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
        """
        POST /leaves/
        
        Apply a new leave request.
        
        Parameters:
            employee (int): ID of the employee applying for the leave
            start_date (datetime): The date and time the leave starts
            end_date (datetime): The date and time the leave ends
            reason (str): The reason for the leave
            leave_type (str): The type of leave (optional)
        
        Returns:
            Response: A JSON response with the status, message, and the created leave request.
        """
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
        """
        Retrieve a leave request by its primary key.

        Args:
            pk (int): The primary key of the leave request to retrieve.

        Returns:
            Leave: The leave request object if found, otherwise None.
        """

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
        """
        Get a single leave request by its primary key.

        Args:
            request (Request): The request sent to the API.
            pk (int): The primary key of the leave request to retrieve.

        Returns:
            Response: A JSON response containing the leave request data if the
            request is successful, or an error message if the leave request does
            not exist.
        """
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
        """
        Update the details of a leave request.

        Args:
            request (Request): The request sent to the API containing updated leave data.
            pk (int): The primary key of the leave request to update.

        Returns:
            Response: A JSON response containing the updated leave data if the update
            is successful, or an error message if the update fails.
        """

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
        """
        Delete a leave request.

        Args:
            request (Request): The request sent to the API.
            pk (int): The primary key of the leave request to delete.

        Returns:
            Response: A response indicating whether the delete was successful or not.
        """

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
        """
        Retrieve all team members under a specific manager.

        Args:
            request: The HTTP request object.
            manager_id (int): The ID of the manager whose team members are to be retrieved.

        Returns:
            Response: A JSON response containing a list of team members if found,
                    or a message indicating no team members are found.
        """

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
        """
        GET /managers/

        Returns a list of all managers.

        Returns:
            Response: A JSON response with the status, message, and data of the managers.
        """
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
        """
        POST /managers/

        Create a new manager.

        Parameters:
            name (str): The name of the manager
            employee (int): The ID of the employee who is the manager

        Returns:
            Response: A JSON response with the status, message, and data of the manager.
        """
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
        """
        Get all pending leaves of the employees under the given manager_id
        :param request: The request object
        :param manager_id: The id of the manager
        :return: A list of pending leaves of the employees under the given manager
        """
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
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK
        )


class ManagerLeaveStatusUpdate(APIView):
    def put(self, request, leave_id):
        """
        Update the status of a leave request.

        Args:
            leave_id (int): The id of the leave request to update.
            status (str): The new status of the leave request. Must be one of "Approve" or "Rejected".

        Returns:
            Response: A JSON response with the status of the update operation.

        Raises:
            HTTPError: If the user is not authorized to update the leave request.
            ValueError: If the new status is not one of "Approve" or "Rejected".
        """
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
        """
        POST /register/
        
        Register a new employee.
        
        Parameters:
            username (str): The username of the new employee.
            email (str): The email of the new employee.
            password (str): The password of the new employee.
        
        Returns:
            Response: A JSON response with the status, message, and the authentication token.
        """
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
        """
        Employee login API.

        Parameters:
        email (str): Employee email
        password (str): Employee password

        Returns:
        Response: A JSON response with a token key and the employee's username and email.

        Raises:
        HTTPError: If the email/username or password is invalid or incorrect.
        """
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
        
        """
        GET /api/reimbursementclaims/
        Returns a list of all reimbursements made by employees
        """
        
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
        
        """
        POST /reimbursement-claims/

        Create a new reimbursement claim.

        Parameters:
            amount (int): The amount of the reimbursement claim
            claim_type (str): The type of the reimbursement claim
            submitted_at (datetime): The date and time the reimbursement claim was submitted
            approve_at (datetime): The date and time the reimbursement claim was approved
            remarks (str): Optional remarks about the reimbursement claim
            employee (int): The ID of the employee who submitted the reimbursement claim

        Returns:
            Response: A JSON response with the status, message, and data of the reimbursement claim.
        """

        try:
            serializer = ReimbursementClaimSerializer(data=request.data)
            if serializer.is_valid():
                claim = serializer.save()
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
        
        """
        GET /reimbursement-claims/
        GET /reimbursement-claims/{id}/

        Returns a list of all reimbursement claims if no ID is provided or
        a single reimbursement claim if an ID is provided.

        Parameters:
            pk (int): ID of the reimbursement claim to retreive

        Returns:
            Response: JSON response with the status, message, and data.
        """
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
        """
        Update a reimbursement claim.

        Args:
            request (Request): The request sent to the API.
            pk (int): The primary key of the reimbursement claim to update.

        Returns:
            Response: A response indicating whether the update was successful or not.
            If successful, the response will contain the updated reimbursement claim.
        """
        try:
            reimbursement = get_object_or_404(ReimbursementClaim, pk=pk)
            serializer = ReimbursementClaimSerializer(reimbursement, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
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
        """
        Update the status of a reimbursement claim.

        Args:
            pk (int): The ID of the reimbursement claim to update.
            status (str): The new status of the reimbursement claim. Must be one of "Approve" or "Rejected".
            remarks (str): Optional remarks to add to the reimbursement claim.

        Returns:
            Response: A JSON response with the status of the update operation.

        Raises:
            HTTPError: If the user is not authenticated or authorized to update the reimbursement claim.
            ValueError: If the new status is not one of "Approve" or "Rejected".
        """
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

    def delete(self, request, pk):
        """
        Delete a reimbursement claim.

        Args:
            request (Request): The request sent to the API.
            pk (int): The primary key of the reimbursement claim to delete.

        Returns:
            Response: A response indicating whether the delete was successful or not.
        """

        try:
            reimbursement = get_object_or_404(ReimbursementClaim, pk=pk)
            reimbursement.delete()
            return Response(
                {
                    "status": True,
                    "message": "Reimbursement deleted successfully"
                }, status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {
                    "status": False,
                    "message": "An error occured",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
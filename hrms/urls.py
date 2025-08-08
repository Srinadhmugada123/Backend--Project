from django.urls import path
from .views import (
    DepartmentAPIView,
    DepartmentDetailAPIView,
    EmployeeAPIView,
    EmployeeDetailAPIView,
    LeaveAPIVIew,
    LeaveDetailAPIVIew,
    TeamMembersUnderManager,
    ManagerAPIView,
    PendingLeavesForManager,
    EmployeeRegisterView,
    EmployeeLoginView,
    ManagerLeaveStatusUpdate,
    ReimbursementClaimAPIView,
    ReimbursementDeatilAPIView,
    AdminReimbursementUpdateStatusAPIView,
)
from django.views.generic import TemplateView


urlpatterns = [
    # ----------Department urls-----------------
    path(
        'api/departments/',
        DepartmentAPIView.as_view(),
        name='departmentlist'),
    path(
        'api/departments/<int:pk>/',
        DepartmentDetailAPIView.as_view(),
        name='departmentdetails'),

    # -------------------Employee Urls-------------------------
    path('api/employees/', EmployeeAPIView.as_view(), name='employeelist'),
    path(
        'api/employees/<int:pk>/',
        EmployeeDetailAPIView.as_view(),
        name='employeedetails'),

    # --------------------Leave Urls ---------------------------
    path('api/leaves/', LeaveAPIVIew.as_view(), name='leaveslist'),
    path(
        'api/leaves/<int:pk>/',
        LeaveDetailAPIVIew.as_view(),
        name='leavedetail'),

    # ------------------------Team members ---------------------
    path('api/team_members/managers/<int:manager_id>/',
         TeamMembersUnderManager.as_view(), name='team_members'),
    path('api/managers/', ManagerAPIView.as_view(), name='managers'),


    # --------------------Leave status ----------------------------------
    path('api/managers/pending_leaves/<int:manager_id>/',
         PendingLeavesForManager.as_view(), name='pending_leaves'),
    # path(
    #     'api/leaves/<int:leave_id>/approve/',
    #     ApproveLeave.as_view(),
    #     name='approve-reject-leave'),
    # path(
    #     'api/leaves/<int:pk>/rejected/',
    #     RejectLeave.as_view(),
    #     name='rejected-leaves'),

    path(
        'api/leaves/<int:leave_id>/status_update/',
        ManagerLeaveStatusUpdate.as_view(),
        name='leave-status-update'),



    # ---------------------------Login View-----------------
    path(
        'api/register/',
        EmployeeRegisterView.as_view(),
        name='employee-register'),
    path('api/login/',
         EmployeeLoginView.as_view(),
         name='employee-login'),


    # --------------------Reimbursement urls -----------------
    path(
        'api/reimbursementclaims/',
          ReimbursementClaimAPIView.as_view(), 
          name='reimbursementclaims'),
    path('api/reimbursementclaims/<int:pk>/', 
         ReimbursementDeatilAPIView.as_view(), 
         name='reimbursementdetails'),
    

    path('api/admin/reimbursement/<int:pk>/status/',
     AdminReimbursementUpdateStatusAPIView.as_view(),
     name='admin-reimbursement-status-update'),
    
    path(
        'api/admin/reimbursement/<int:pk>/delete/', 
        AdminReimbursementUpdateStatusAPIView.as_view(), name='delete_claim'),



    # ---------------------------Frontend view ----------------------

    path(
        'login/',
        TemplateView.as_view(
            template_name="login.html"),
        name='login'),
    path(
        'register/',
        TemplateView.as_view(
            template_name="register.html"),
        name='register'),


    path(
        'admin-dashboard/',
        TemplateView.as_view(
            template_name="admin_dashboard.html")),
    path(
        'admin-dashboard/departments/',
        TemplateView.as_view(
            template_name='departments.html')),
    path(
        'admin-dashboard/employees/',
        TemplateView.as_view(
            template_name='employees.html')),
    path(
        'admin-dashboard/leaves/',
        TemplateView.as_view(
            template_name='leaves.html')),

    path(
        'admin-dashboard/departments/<int:dept_id>/employees/',
        TemplateView.as_view(template_name='department_employees.html')
    ),
    path(
        'admin-dashboard/employees/<int:emp_id>/details/',
        TemplateView.as_view(template_name='employee_details.html')
    ),



]

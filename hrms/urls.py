from django.urls import path
from .views import (
    DepartmentAPIView,
    DepartmentDetailAPIView,
    EmployeeAPIView, 
    EmployeeDetailAPIView, 
    LeaveAPIVIew, 
    LeaveDetailAPIVIew, 
    TeamMembersUnderManager,
    PendingLeavesForManager,
    ApproveLeave,
    RejectLeave,
    EmployeeRegisterView,
    EmployeeLoginView,
    
) 
from django.views.generic import TemplateView


urlpatterns=[
    #----------Department urls-----------------
    path('departments/',DepartmentAPIView.as_view(), name='departmentlist'),
    path('departments/<int:pk>/',DepartmentDetailAPIView.as_view(), name='departmentdetails'),

    #-------------------Employee Urls-------------------------
    path('employees/',EmployeeAPIView.as_view(), name='employeelist'),
    path('employees/<int:pk>/',EmployeeDetailAPIView.as_view(), name='employeedetails'),

    #--------------------Leave Urls ---------------------------
    path('leaves/',LeaveAPIVIew.as_view(), name='leaveslist'),
    path('leaves/<int:pk>/',LeaveDetailAPIVIew.as_view(), name='leavedetail'),

    #------------------------Team members ---------------------
    path('team_members/managers/<int:manager_id>/',TeamMembersUnderManager.as_view(),name='team_members'),


    #--------------------Leave status ----------------------------------
    path('managers/pending_leaves/<int:manager_id>/',PendingLeavesForManager.as_view(), name='pending_leaves'),
    path('leaves/<int:leave_id>/approve/',ApproveLeave.as_view(), name='approve-reject-leave'),
    path('leaves/<int:pk>/rejected/',RejectLeave.as_view(), name='rejected-leaves'),


    #---------------------------Login View-----------------
    path('register/',EmployeeRegisterView.as_view(),name='employee-register'),
    path('login/',EmployeeLoginView.as_view(), name='employee-login'),


    #---------------------------Frontend view ----------------------

    path('admin/login/', TemplateView.as_view(template_name='login.html')),

    path('admin-dashboard/',TemplateView.as_view(template_name="admin_dashboard.html")),
    path('admin-dashboard/departments/', TemplateView.as_view(template_name='departments.html')),
    path('admin-dashboard/employees/', TemplateView.as_view(template_name='employees.html')),
    path('admin-dashboard/leaves/', TemplateView.as_view(template_name='leaves.html')),

    path('admin-dashboard/departments/<int:dept_id>/employees/', TemplateView.as_view(template_name='department_employees.html')),
    path('admin-dashboard/employees/<int:emp_id>/details/', TemplateView.as_view(template_name='employee_details.html')),
    

    
]
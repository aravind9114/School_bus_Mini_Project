from django.urls import path
from .views import (
    StudentListView, select_role, custom_login, admin_dashboard, driver_dashboard,
    parent_dashboard, custom_logout, add_user, delete_user, add_student, delete_student ,mark_attendance, admin_view_attendance,
    update_location, get_location,submit_feedback, view_feedback, manage_feedback, respond_feedback
)


urlpatterns = [
    path('students/', StudentListView.as_view(), name='student-list'),
    path('', select_role, name="select_role"),
    path('login/<str:role>/', custom_login, name="custom_login"),
    path('admin_dashboard/', admin_dashboard, name="admin_dashboard"),
    path('add_user/', add_user, name='add_user'),  
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('add_student/', add_student, name='add_student'),
    path('delete_student/<int:student_id>/', delete_student, name='delete_student'),
    path('driver_dashboard/', driver_dashboard, name="driver_dashboard"),
    path("submit-feedback/", submit_feedback, name="submit_feedback"),
    path("view-feedback/", view_feedback, name="view_feedback"),
    path("manage-feedback/", manage_feedback, name="manage_feedback"),
    path("respond-feedback/<int:feedback_id>/", respond_feedback, name="respond_feedback"),
    path('mark_attendance/', mark_attendance, name='mark_attendance'),
    path('admin_view_attendance/', admin_view_attendance, name='admin_view_attendance'),
    path('parent_dashboard/', parent_dashboard, name="parent_dashboard"),
    path('logout/', custom_logout, name="logout"),
    path("update-location/", update_location, name="update_location"),
    path("get-location/<str:bus_number>/", get_location, name="get_location"),
]

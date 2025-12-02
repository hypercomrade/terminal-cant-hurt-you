from django.urls import path
from .views import (
    SignUpView,
    SignInView,
    logout_view,
    TeacherDashBoardView,
    StudenDashBoardView,
    PersonalDashBoardView,
    delete_classroom,
    remove_student,
    SettingsView
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("logout/", logout_view, name="logout"),
    path("teacher/", TeacherDashBoardView.as_view(), name="teacher_dashboard"),
    path("student/", StudenDashBoardView.as_view(), name="student_dashboard"),
    path("personal/", PersonalDashBoardView.as_view(), name="personal_dashboard"),
    path("teacher/delete_classroom/<int:classroom_id>/", delete_classroom, name="delete_classroom"),
    path("teacher/remove_student/<int:classroom_id>/<int:student_id>/", remove_student, name="remove_student"),
    path("settings/", SettingsView.as_view(), name="settings"),
]
    
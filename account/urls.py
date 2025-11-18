from django.urls import path
from .views import SignUpView, SignInView, TeacherDashBoardView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("logout/", LogoutView.as_view(next_page="signin"), name="logout"),
    path("teacher/", TeacherDashBoardView.as_view(), name= 'teacher_dashboard'),
]

from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect, get_object_or_404, render
from .forms import SignUpForm, SignInForm, ProfileUpdateForm, CustomPasswordChangeForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import (
    Teacher,
    Student,
    Classroom,
    Personal,
    PowerShellChecklist,
    BashChecklist,
)


class SignUpView(FormView):
    template_name = "accounts/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        if user.role == "teacher":
            return redirect("teacher_dashboard")
        elif user.role == "student":
            return redirect("student_dashboard")
        elif user.role == "personal":
            return redirect("personal_dashboard")
        return redirect(self.get_success_url())


class SignInView(FormView):
    template_name = "accounts/signin.html"
    form_class = SignInForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(self.request, username=username, password=password)

        if user is None:
            form.add_error(None, "Invalid username or password")
            return self.form_invalid(form)

        login(self.request, user)

        if user.role == "teacher":
            return redirect("teacher_dashboard")
        elif user.role == "student":
            return redirect("student_dashboard")
        elif user.role == "personal":
            return redirect("personal_dashboard")
        return redirect(self.get_success_url())


def logout_view(request):
    logout(request)
    return redirect("signin")


@method_decorator(login_required, name="dispatch")
class TeacherDashBoardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/TeacherDash.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = Teacher.objects.get(user=self.request.user)
        context["teacher"] = teacher
        context["classrooms"] = Classroom.objects.filter(teacher=teacher)

        # attach per-user checklists if they exist
        context["powershell_checklist"] = getattr(
            self.request.user, "powershell_checklist", None
        )
        context["bash_checklist"] = getattr(self.request.user, "bash_checklist", None)
        return context


class StudenDashBoardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/StudentDash.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = Student.objects.get(user=self.request.user)
        context["student"] = student
        context["classrooms"] = student.classroom.all()

        context["powershell_checklist"] = getattr(
            self.request.user, "powershell_checklist", None
        )
        context["bash_checklist"] = getattr(self.request.user, "bash_checklist", None)
        return context


class PersonalDashBoardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/PersonalDash.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user

        context["powershell_checklist"] = getattr(
            self.request.user, "powershell_checklist", None
        )
        context["bash_checklist"] = getattr(self.request.user, "bash_checklist", None)
        return context


@login_required
@require_POST
def delete_classroom(request, classroom_id):
    user = request.user
    teacher = getattr(user, "teacher_profile", None)
    if not teacher:
        return redirect("home")

    classroom = Classroom.objects.filter(id=classroom_id, teacher=teacher).first()
    if classroom:
        classroom.delete()

    return redirect("teacher_dashboard")


@login_required
@require_POST
def remove_student(request, classroom_id, student_id):
    user = request.user
    teacher = getattr(user, "teacher_profile", None)
    if not teacher:
        return redirect("home")

    classroom = Classroom.objects.filter(id=classroom_id, teacher=teacher).first()
    if not classroom:
        return redirect("teacher_dashboard")

    student = Student.objects.filter(id=student_id).first()
    if student:
        classroom.students.remove(student)

    return redirect("teacher_dashboard")


@method_decorator(login_required, name="dispatch")
class SettingsView(LoginRequiredMixin, View):
    template_name = "accounts/AccountSetting.html"

    def get(self, request, *args, **kwargs):
        profile_form = ProfileUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)
        context = {
            "profile_form": profile_form,
            "password_form": password_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        action = request.POST.get("action")

        # update name/email
        if action == "update_profile":
            profile_form = ProfileUpdateForm(request.POST, instance=user)
            password_form = CustomPasswordChangeForm(user=user)
            if profile_form.is_valid():
                profile_form.save()

        # change password
        elif action == "change_password":
            profile_form = ProfileUpdateForm(instance=user)
            password_form = CustomPasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                # keep user logged in after password change
                update_session_auth_hash(request, user)

        # delete account
        elif action == "delete_account":
            user.delete()
            return redirect("home")

        # NEW: reset PS + Bash checklists for this user
        elif action == "reset_checklists":
            # reset any existing PowerShell checklist
            PowerShellChecklist.objects.filter(user=user).update(
                list_files=False,
                system_info=False,
                move_location=False,
                read_write=False,
                manipulate_files=False,
                navigate=False,
            )
            # reset any existing Bash checklist
            BashChecklist.objects.filter(user=user).update(
                list_files=False,
                system_info=False,
                move_location=False,
                read_write=False,
                manipulate_files=False,
                navigate=False,
            )

            # reload forms normally
            profile_form = ProfileUpdateForm(instance=user)
            password_form = CustomPasswordChangeForm(user=user)

        else:
            # fallback – just reload with current data
            profile_form = ProfileUpdateForm(instance=user)
            password_form = CustomPasswordChangeForm(user=user)

        context = {
            "profile_form": profile_form,
            "password_form": password_form,
        }
        return render(request, self.template_name, context)

from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .forms import SignUpForm, SignInForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Teacher, Student, Classroom, Personal


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
            return redirect("personal_dahsboard")
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
            return redirect("personal_dahsboard")
        return redirect(self.get_success_url())

def logout_view(request):
    logout(request)
    return redirect('signin')

@method_decorator(login_required, name="dispatch")
class TeacherDashBoardView(TemplateView):
    template_name = "accounts/TeacherDash.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "teacher":
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        teacher = getattr(user, "teacher_profile", None)
        classrooms = teacher.classrooms.all() if teacher else []
        ctx["teacher"] = teacher
        ctx["classrooms"] = classrooms
        return ctx

    def post(self, request, *args, **kwargs):

        teacher = request.user.teacher_profile
        name = request.POST.get("classroom_name")

        if name:
            Classroom.objects.create(name=name, teacher=teacher)

        return redirect("teacher_dashboard")


@method_decorator(login_required, name="dispatch")
class StudenDashBoardView(TemplateView):
    template_name = "accounts/StudentDash.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "student":
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        student = getattr(user, "student_profile", None)
        classes = student.classroom.select_related("teacher__user")
        ctx["student"] = student
        ctx["classes"] = classes
        ctx.setdefault("error", None)
        ctx.setdefault("success", None)
        return ctx

    def post(self, request, *args, **kwargs):
        student = request.user.student_profile
        code = request.POST.get("classroom_code", "").strip().upper()

        ctx = self.get_context_data()

        if not code:
            ctx["error"] = "Please enter a classroom code."
            return self.render_to_response(ctx)

        try:
            classroom = Classroom.objects.get(code=code)
        except Classroom.DoesNotExist:
            ctx["error"] = "No Classroom found with that code."
            return self.render_to_response(ctx)

        student.classroom.add(classroom)
        ctx["success"] = f"You joined {classroom.name}!"
        ctx["classes"] = student.classroom.select_related("teacher__user")
        return self.render_to_response(ctx)


class PersonalDashBoardView(TemplateView):
    template_name = "accounts/PersonalDash.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "personal":
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["user"] = self.request.user
        return ctx

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Teacher, Student, Personal, Classroom


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    fieldsets = UserAdmin.fieldsets + (("Role", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Role", {"fields": ("role",)}),)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):  # <-- fixed ModelAdmina -> ModelAdmin
    list_display = ("user",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # use the actual method name below
    list_display = ("user", "get_classrooms")

    def get_classrooms(self, obj):
        # Student has a ManyToManyField named "classrooms"
        return ", ".join(c.name for c in obj.classrooms.all())

    get_classrooms.short_description = "Classes"


@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ("user",)


class StudentInline(admin.TabularInline):  # <-- better name
    # ManyToManyField -> use the "through" model
    model = Student.classroom.through
    extra = 0


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "teacher")
    readonly_fields = ("code",)
    inlines = [StudentInline]

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,
    Teacher,
    Student,
    Personal,
    Classroom,
    PowerShellChecklist,
    BashChecklist,   # <-- add this
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    fieldsets = UserAdmin.fieldsets + (("Role", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Role", {"fields": ("role",)}),)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("user",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "get_classrooms")

    def get_classrooms(self, obj):
        return ", ".join(c.name for c in obj.classroom.all())

    get_classrooms.short_description = "Classes"


@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ("user",)


class StudentInline(admin.TabularInline):
    model = Student.classroom.through
    extra = 0


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "teacher")
    readonly_fields = ("code",)
    inlines = [StudentInline]


@admin.register(PowerShellChecklist)
class PowerShellChecklistAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "list_files",
        "system_info",
        "move_location",
        "read_write",
        "manipulate_files",
        "navigate",
    )
    list_filter = (
        "list_files",
        "system_info",
        "move_location",
        "read_write",
        "manipulate_files",
        "navigate",
    )


@admin.register(BashChecklist)
class BashChecklistAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "list_files",
        "system_info",
        "move_location",
        "read_write",
        "manipulate_files",
        "navigate",
    )
    list_filter = (
        "list_files",
        "system_info",
        "move_location",
        "read_write",
        "manipulate_files",
        "navigate",
    )

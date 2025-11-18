from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Teacher, Student, Personal, Classroom

class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.RadioSelect,
        label= "Account type"
    )
    classroom_code = forms.CharField(
        max_length=12,
        required=False,
        help_text="Required if you are a student."
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
            'role',
            'classroom_code',
        ]
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        classroom_code = cleaned_data.get('classroom_code')

        if role == 'student':
            if not classroom_code:
                self.add_error('classroom_code', "Classroom code is required for students.")
            else:
                try:
                    Classroom.objects.get(code=classroom_code)
                except Classroom.DoesNotExist:
                    self.add_error('classroom_code', "No classroom found with that code.")
        return cleaned_data
    
    def save(self, commit=True):
        user =super().save(commit=False)
        role = self.cleaned_data['role']
        user.role = role

        if commit:
            user.save()

            if role == 'teacher':
                Teacher.objects.create(user=user)
            elif role ==  'student':
                classroom = Classroom.objects.get(code=self.cleaned_data['classroom_code'])
                Student.objects.create(user=user, classroom=classroom)
            elif role == 'personal':
                Personal.objects.create(user=user)
        return user
    
class SignInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
        

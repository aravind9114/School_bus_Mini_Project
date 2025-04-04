from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Student

# ✅ Form for Adding Drivers & Parents
class UserForm(UserCreationForm):
    role = forms.ChoiceField(choices=[('driver', 'Driver'), ('parent', 'Parent')])
    bus_number = forms.CharField(required=False, help_text="Only for drivers")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role', 'bus_number']

    def clean_bus_number(self):
        bus_number = self.cleaned_data.get('bus_number')
        role = self.cleaned_data.get('role')
        if role == 'driver' and not bus_number:
            raise forms.ValidationError("Bus number is required for drivers.")
        return bus_number


        
        
from django import forms
from .models import Student, User

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'parent', 'driver', 'bus_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Show only parents in the parent dropdown
        self.fields['parent'].queryset = User.objects.filter(role='parent')

        # Show only drivers in the driver dropdown
        self.fields['driver'].queryset = User.objects.filter(role='driver')

        # Allow bus_number to be editable, but we will update it dynamically in the frontend
        self.fields['bus_number'].required = False

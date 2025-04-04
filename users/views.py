from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
import json

# Import models
from .models import User, Student, Attendance, DriverAttendance

# Import forms
from .forms import UserForm, StudentForm


# Custom Login View
def custom_login(request, role):
    form = AuthenticationForm(request, data=request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        if user and user.role == role:
            login(request, user)

            # Mark attendance for drivers
            if role == 'driver':
                DriverAttendance.objects.create(driver=user, login_time=now())

            return redirect(f'{role}_dashboard')
    
    return render(request, 'users/login.html', {'role': role, 'form': form})

# --------------------------------------------
# ✅ Admin Views
# --------------------------------------------

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')

    users = User.objects.exclude(is_superuser=True)
    students = Student.objects.all()
    parents = User.objects.filter(role='parent')
    drivers = User.objects.filter(role='driver')
    attendance_records = Attendance.objects.all().order_by('-date')
    feedbacks = Feedback.objects.all().order_by('-id')  # Fetch feedback data

    return render(request, 'users/admin_dashboard.html', {
        'users': users,
        'students': students,
        'parents': parents,
        'drivers': drivers,
        'attendance_records': attendance_records,
        'feedbacks': feedbacks  # Pass feedbacks to template
    })



@login_required
def add_user(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('admin_dashboard')
    else:
        form = UserForm()

    return render(request, 'users/add_user.html', {'form': form})


@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return redirect('home')

    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('admin_dashboard')


# --------------------------------------------
# ✅ Student Views
# --------------------------------------------

@login_required
def add_student(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)

            if student.driver:
                student.bus_number = student.driver.bus_number

            student.save()
            return redirect('admin_dashboard')
    else:
        form = StudentForm()

    parents = User.objects.filter(role='parent')
    drivers = User.objects.filter(role='driver')

    return render(request, 'users/add_student.html', {
        'form': form,
        'parents': parents,
        'drivers': drivers
    })


@login_required
def delete_student(request, student_id):
    if not request.user.is_superuser:
        return redirect('home')

    student = Student.objects.get(id=student_id)
    student.delete()
    return redirect('admin_dashboard')


class StudentListView(ListView):
    model = Student
    template_name = 'users/student_list.html'


# ✅ Student List View
class StudentListView(ListView):
    model = Student
    template_name = 'users/student_list.html'

# ✅ Role Selection Page
def select_role(request):
    if request.method == "POST":
        selected_role = request.POST.get("role")
        if selected_role:
            return redirect(f'/login/{selected_role}/')  # Redirect to role-specific login page
    return render(request, "users/select_role.html")

def custom_login(request, role):
    form = AuthenticationForm(request, data=request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            if user and user.role == role:
                login(request, user)

                # ✅ If driver logs in, mark attendance
                if role == 'driver':
                    DriverAttendance.objects.create(driver=user, login_time=now())

                return redirect(f'{role}_dashboard')
    
    return render(request, 'users/login.html', {'role': role, 'form': form})
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import User, Student
from .forms import UserForm, StudentForm

User = get_user_model()

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')

    users = User.objects.exclude(is_superuser=True)  
    students = Student.objects.all()
    parents = User.objects.filter(role='parent')
    drivers = User.objects.filter(role='driver')
    attendance_records = Attendance.objects.all().order_by('-date')  # Fetch attendance

    return render(request, 'users/admin_dashboard.html', {
        'users': users,
        'students': students,
        'parents': parents,
        'drivers': drivers,
        'attendance_records': attendance_records  # Pass attendance data
    })


# ✅ Add Driver or Parent
@login_required
def add_user(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Hash password
            user.save()
            return redirect('admin_dashboard')
    else:
        form = UserForm()

    return render(request, 'users/add_user.html', {'form': form})

# ✅ Add Student
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student, User
from .forms import StudentForm

@login_required
def add_student(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)

            # If a driver is selected, assign the bus number from the driver
            if student.driver:
                student.bus_number = student.driver.bus_number

            student.save()
            return redirect('admin_dashboard')
    else:
        form = StudentForm()

    parents = User.objects.filter(role='parent')
    drivers = User.objects.filter(role='driver')

    return render(request, 'users/add_student.html', {
        'form': form,
        'parents': parents,
        'drivers': drivers
    })



# ✅ Delete User
@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return redirect('home')

    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('admin_dashboard')

# ✅ Delete Student
@login_required
def delete_student(request, student_id):
    if not request.user.is_superuser:
        return redirect('home')

    student = Student.objects.get(id=student_id)
    student.delete()
    return redirect('admin_dashboard')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student, Attendance, User

# ✅ Driver Dashboard - Show Assigned Students
@login_required
def driver_dashboard(request):
    if request.user.role != 'driver':
        return redirect('home')

    students = Student.objects.filter(driver=request.user)  # Only students assigned to the driver
    return render(request, 'users/driver_dashboard.html', {'students': students})

from django.utils.timezone import now

@login_required
def mark_attendance(request):
    if request.user.role != 'driver':
        return redirect('home')

    # Show only students assigned to this driver's bus
    students = Student.objects.filter(driver=request.user)

    if request.method == "POST":
        for student in students:
            status = request.POST.get(f"attendance_{student.id}")
            if status:
                Attendance.objects.create(
                    student=student,
                    driver=request.user,
                    status=status,
                    date=now().date()  # Save attendance date
                )
        return redirect('driver_dashboard')

    return render(request, 'users/mark_attendance.html', {'students': students})


# ✅ Admin View Attendance
@login_required
def admin_view_attendance(request):
    if not request.user.is_superuser:
        return redirect('home')

    attendance_records = Attendance.objects.all().order_by('-date')
    return render(request, 'users/admin_dashboard.html', {'attendance_records': attendance_records})




@login_required
def parent_dashboard(request):
    students = Student.objects.filter(parent=request.user)  # ✅ Get all children
    buses = Student.objects.exclude(bus_number=None).values_list('bus_number', flat=True).distinct()

    # ✅ Get all attendance records for the parent's children
    attendance_records = Attendance.objects.filter(student__in=students, date=now().date())

    return render(request, "users/parent_dashboard.html", {
        "students": students,
        "buses": buses,
        "attendance_records": attendance_records,  # ✅ Pass all records
    })

# ✅ Custom Logout: Updates Working Hours
def custom_logout(request):
    if request.user.is_authenticated and request.user.role == "driver":
        attendance = DriverAttendance.objects.filter(driver=request.user, date=now().date()).last()
        if attendance and not attendance.logout_time:
            attendance.logout_time = now()
            attendance.calculate_hours()

    logout(request)
    return redirect('select_role')

# ✅ Update Driver's Location (Every 5 Min)
@csrf_exempt
@login_required
def update_location(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            request.user.latitude = data.get("latitude")
            request.user.longitude = data.get("longitude")
            request.user.save()
            return JsonResponse({"message": "Location updated successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)

import requests
import requests
from django.http import JsonResponse
from django.utils.timezone import now

def get_location(request, bus_number):
    try:
        driver = User.objects.filter(role="driver", bus_number=bus_number).first()

        if not driver or not driver.latitude or not driver.longitude:
            return JsonResponse({
                "bus_number": bus_number,
                "latitude": None,
                "longitude": None,
                "location_name": "Last location not available"
            })

        # Reverse Geocoding using OpenStreetMap (Nominatim)
        geocode_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={driver.latitude}&lon={driver.longitude}"
        response = requests.get(geocode_url)
        location_name = "Unknown Location"

        if response.status_code == 200:
            data = response.json()
            location_name = data.get("display_name", "Unknown Location")

        return JsonResponse({
            "bus_number": bus_number,
            "latitude": driver.latitude,
            "longitude": driver.longitude,
            "location_name": location_name,
            "last_updated": driver.last_login.strftime("%Y-%m-%d %H:%M:%S")  # Show last recorded timestamp
        })
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)






from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Feedback
from django.contrib import messages

# ✅ Parent: Submit Feedback
@login_required
def submit_feedback(request):
    if request.method == "POST":
        message = request.POST.get("message")
        if message:
            Feedback.objects.create(parent=request.user, message=message)
            messages.success(request, "Feedback submitted successfully!")
            return redirect("parent_dashboard")
    return redirect("parent_dashboard")

# ✅ Parent: View Feedback History
@login_required
def view_feedback(request):
    feedbacks = Feedback.objects.filter(parent=request.user).order_by('-created_at')
    return render(request, "users/view_feedback.html", {"feedbacks": feedbacks})

# ✅ Admin: View and Respond to Feedback
@login_required
def manage_feedback(request):
    if not request.user.is_superuser:
        return redirect("home")

    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, "users/manage_feedback.html", {"feedbacks": feedbacks})

# ✅ Admin: Respond to Feedback
@login_required
def respond_feedback(request, feedback_id):
    if not request.user.is_superuser:
        return redirect("home")

    feedback = get_object_or_404(Feedback, id=feedback_id)

    if request.method == "POST":
        response = request.POST.get("response")
        if response:
            feedback.response = response
            feedback.status = "closed"
            feedback.save()
            messages.success(request, "Response sent successfully!")
            return redirect("admin_dashboard")

    return render(request, "users/respond_feedback.html", {"feedback": feedback})

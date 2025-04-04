
## School Bus Tracking System

A comprehensive, real-time bus tracking and attendance management system designed for schools, offering role-based access for admins, drivers, and parents.

---

### Key Features

**Role-Based Access**  
- **Admin**: Manage users and students, view attendance records, and respond to feedback  
- **Driver**: Mark attendance, update bus location  
- **Parent**: Track child’s bus, check attendance, submit feedback  

**Core Functionalities**  
- Live GPS Tracking accessible through browsers, no app required  
- Automated Attendance where drivers mark students as Present or Absent  
- Feedback System enabling two-way communication between parents and admin  
- Driver Shift Tracking with automatic calculation of working hours  

---

### Technologies Used

- **Backend**: Django 5.1.7  
- **Database**: SQLite for development, PostgreSQL for production  
- **APIs**: Django REST Framework for mobile app integration (future)  
- **Geolocation**: OpenStreetMap Nominatim for reverse geocoding  
- **Frontend**: HTML, Bootstrap, JavaScript (with AJAX for live updates)  

---

### Installation Guide

1. Clone the repository:  
   `git clone https://github.com/yourusername/school-bus-tracking.git`  
   Navigate to the project folder: `cd school-bus-tracking`

2. Set up a virtual environment:  
   `python -m venv venv`  
   Activate the virtual environment:  
   - Linux/Mac: `source venv/bin/activate`  
   - Windows: `venv\Scripts\activate`  

3. Install dependencies:  
   `pip install -r requirements.txt`

4. Run database migrations:  
   `python manage.py migrate`

5. Create a superuser:  
   `python manage.py createsuperuser`

6. Start the development server:  
   `python manage.py runserver`  
   Access the app locally at: `http://127.0.0.1:8000`  

---

### Database Models

**User Model**  
```python
class User(AbstractUser):
    role = models.CharField(choices=[('admin', 'Admin'), ('driver', 'Driver'), ('parent', 'Parent')])
    bus_number = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
```

**Student Model**  
```python
class Student(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(User, limit_choices_to={'role': 'parent'})
    driver = models.ForeignKey(User, limit_choices_to={'role': 'driver'}, null=True)
    bus_number = models.CharField(max_length=10, blank=True)
```

**Attendance & Feedback Models**  
```python
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent')])

class Feedback(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')], default='open')
```

---

### Views and Workflow

**Authentication Flow**  
Role Selection → Login → Redirect to Dashboard  
Drivers are auto-tracked for attendance on login/logout  

**Admin Workflow**  
- Add/remove users and students  
- View reports for attendance, feedback, and driver attendance 

**Driver Workflow**  
- Update bus location through browser GPS or API  
- Mark attendance for assigned students  

**Parent Workflow**  
- Track child’s bus via live map (using OpenStreetMap)  
- Check attendance and submit feedback  

---

### APIs

**Endpoints**  
- `/update-location/`: Updates driver’s GPS coordinates (POST method)  
- `/get-location/<bus_number>/`: Fetches bus location and address (GET method)  

**Example Response**  
```json
{
    "bus_number": "BUS-101",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "location_name": "Bangalore, Karnataka, India"
}
```

---

### Future Improvements

- SMS Alerts notifying parents when the bus is nearby  
- Live Maps using Google Maps for improved interface and features  
- Mobile App for drivers and parents, built with Flutter or React Native  


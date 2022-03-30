from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Rooms(models.Model):
    room_number = models.CharField(max_length=10)
    hall_containing_room = models.ForeignKey('Hall', on_delete=models.CASCADE)
    room_is_occupied = models.BooleanField(default=False)
    room_capacity = models.IntegerField()
    room_resident1 = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='room_resident1')
    room_resident2 = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='room_resident2')
    room_resident3 = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='room_resident3')
    room_resident4 = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='room_resident4')

    def __str__(self):
        return self.room_number

class Hall(models.Model):
    hall_name = models.CharField(max_length=100)
    hall_warden = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name='hall_warden')

    def __str__(self):
        return self.hall_name

class Staff(models.Model):
    staff_name = models.CharField(max_length=100)
    staff_position = models.CharField(max_length=100)
    staff_dob = models.DateField()
    staff_email = models.EmailField()
    staff_phone = models.CharField(max_length=15)
    staff_address = models.CharField(max_length=200)
    staff_city = models.CharField(max_length=100)
    staff_state = models.CharField(max_length=100)
    staff_zipcode = models.CharField(max_length=10)

    def __str__(self):
        return self.staff_name

class Complaint(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    complaint_description = models.CharField(max_length=500)
    complaint_date = models.DateField()
    complaint_by = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='complaint_by')
    complaint_status = models.IntegerField(default=0)
    complaint_resolved_by = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name='complaint_resolved_by')
    complaint_resolved_date = models.DateField()
    action_taken_report = models.CharField(max_length=500)
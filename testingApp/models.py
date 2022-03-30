from django.db import models
from django.contrib.auth.models import User
import os
import uuid


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    ROLES = [
        ('student', 'Student'),
        ('warden', 'Warden'),
        ('hall_clerk', 'Hall Clerk'),
        ('hmc_chairman', 'HMC Chairman'),
        ('administrator', 'Administrator'),
        ('mess_manager', 'Mess Manager')
    ]
    role = models.CharField(
        max_length=30,
        choices=ROLES,
        default='student'
    )


class Hall(models.Model):
    hall_name = models.CharField(max_length=100)
    warden = models.OneToOneField(User, null=True,
                                  on_delete=models.SET_NULL)  # can delete wardens without affecting Halls


class Student(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, null=True, on_delete=models.SET_NULL)
    mess_fees = models.DecimalField(max_digits=10, decimal_places=2)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    surcharges = models.DecimalField(max_digits=10, decimal_places=2)


def get_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('complaints', filename)


def get_atr_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('action_taken_reports', filename)


class Complaint(models.Model):
    date_filed = models.DateField(auto_now_add=True)
    COMP_TYPES = [
        ('mess', 'Mess related issues'),
        ('electrical', 'Electrical issues'),
        ('cleaning', 'Cleaning'),
        ('other', 'Other')
    ]
    complaint_type = models.CharField(max_length=20, choices=COMP_TYPES, default='other')
    complainant = models.ForeignKey(User,
                                    on_delete=models.CASCADE)  # if student is deleted, complaint is also deleted
    description = models.TextField(null=False, blank=False)
    image_upload = models.ImageField(null=True, blank=True, upload_to=get_image_upload_path)
    action_taken_report = models.FileField(null=True, blank=True, upload_to=get_atr_upload_path)

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, ComplaintForm, ATRUploadForm
from .models import Complaint, Student, Hall, User


# Create your views here.
def register(request):
    if request.method == 'POST':
        # given the POST data, is_valid detects any errors
        # If there are errors, the condition fails, and the registration
        # form is displayed again with the errors marked.
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Registration successful for {username}')
            return redirect('registration-page')
    else:
        form = RegistrationForm()
    return render(request, 'users/registration.html', {'form': form})


@login_required
def dashboard(request):
    current_user = request.user
    return render(request, f'users/dashboard_{current_user.profile.role}.html', {})


@login_required
def file_complaint(request):
    if request.user.profile.role != 'student':
        return redirect('access-denied')
    elif request.method == 'POST':
        print(request.FILES)
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.complainant = request.user
            complaint.save()
            messages.success(request, f'Complaint successfully filed!')
            return redirect('file-complaint')
    else:
        form = ComplaintForm()
    return render(request, 'file-complaint.html', {'form': form})


@login_required
def view_complaints(request):
    if request.method == 'GET':
        if request.user.profile.role == 'student':
            complaints = Complaint.objects.filter(complainant=request.user)
            return render(request, 'view-complaints.html',
                          {'complaints': complaints, 'role': request.user.profile.role})
        elif request.user.profile.role == 'warden':
            studentsInThisHall = User.objects.filter(student__hall=request.user.hall)
            relevantComplaints = Complaint.objects.filter(complainant__in=studentsInThisHall)

            atr_form = ATRUploadForm()
            return render(request, 'view-complaints.html',
                          {'complaints': relevantComplaints, 'role': request.user.profile.role, 'atr_form': atr_form})
        elif request.user.profile.role == 'hall-clerk':
            pass
        else:
            return redirect('access-denied')


@login_required
def file_atr(request):
    if request.method == 'POST' and request.user.profile.role == 'warden':
        form = ATRUploadForm(request.POST, request.FILES)
        if form.is_valid():
            current_complaint = Complaint.objects.get(pk=request.POST['complaint_id'])
            current_complaint.action_taken_report = form.cleaned_data['action_taken_report']
            current_complaint.save(update_fields=['action_taken_report'])
            messages.success(request, 'Report filed successfully!')
            return redirect('view-complaints')
        else:
            messages.error(request, 'Something went wrong. Try again later.')
            return redirect('view-complaints')

    else:
        return redirect('access-denied')


@login_required
def hall_fees(request):
    if request.method == 'POST':
        if request.user == 'student':
            request.user.student
    elif request.method == 'GET':
        rent_owed = request.user.student.rent_amount
        surcharges = request.user.student.surcharges
        return render(request, 'fees-dues/hall-fees.html', {'rent_owed': rent_owed, 'surcharges_owed': surcharges,
                                                            'total_money_owed': rent_owed + surcharges})


def under_construction(request):
    return render(request, 'under_construction.html')


def access_denied(request):
    return render(request, 'users/access_denied.html')
